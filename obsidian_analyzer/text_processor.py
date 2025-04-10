import os
import re
import asyncio
import wikipedia
import nltk
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
from typing import Dict, List, Tuple, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
try: 
    from langchain_openai import ChatOpenAI as AsyncChatModel
except ImportError: 
    print("ERROR: langchain-openai required")
    sys.exit(1)
from .prompt_loader import load_prompt
from dotenv import load_dotenv
import sys

# --- Setup ---
load_dotenv()

class TextProcessor:
    def __init__(self):
        self._setup_nltk()
        self.llm = self._init_llm()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000, 
            chunk_overlap=300
        )

    def _setup_nltk(self):
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)

    def _init_llm(self):
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("API Key missing")

        return AsyncChatModel(
            model=os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat"),
            api_key=api_key,
            base_url=os.getenv("DEEPSEEK_API_BASE"),
            temperature=0.2,
            request_timeout=120
        )

    async def analyze_text(self, file_path: str, langs: List[str], options: Dict) -> Dict:
        """Main analysis pipeline"""
        from .file_handler import read_file
        content = read_file(file_path)
        if not content:
            return {"error": "Failed to read file"}

        chunks = self.split_text(content)
        results = {
            "source_file": file_path,
            "entities": [],
            "correlations": {"pairs": {}, "multi": {}},
            "key_concepts": {},
            "metrics": {},
            "diagrams": {}
        }

        # Entity identification
        results["entities"] = await self.identify_entities_async(chunks)

        # Parallel analysis tasks
        analysis_tasks = []
        for lang in langs:
            analysis_tasks.extend(self._create_lang_tasks(lang, chunks, results, options))

        # Run all analysis tasks
        if analysis_tasks:
            await asyncio.gather(*analysis_tasks)

        return results

    # [Rest of TextProcessor implementation would go here...]
