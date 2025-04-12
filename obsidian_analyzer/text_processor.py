import os
import re
import asyncio
import wikipedia
from itertools import combinations
from .config import settings
from .llm_provider import LLMProvider
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
import sys
import re
from dotenv import load_dotenv
from .prompt_loader import load_prompt

def sanitize_filename(filename: str) -> str:
    """Sanitize a string to be safe for use as a filename."""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "", filename)
    # Replace spaces with underscores
    filename = filename.replace(" ", "_")
    # Remove leading/trailing whitespace
    filename = filename.strip()
    # Truncate long filenames
    if len(filename) > 255:
        filename = filename[:255]
    return filename

try:
    from langchain_openai import ChatOpenAI as AsyncChatModel
except ImportError as e:
    print(f"ERROR: {e}. Please install langchain-openai>=0.1.3")
    sys.exit(1)

# --- Setup ---
load_dotenv()

class TextProcessor:

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
            raise ValueError("DEEPSEEK_API_KEY environment variable missing")

        from .deepseek_client import DeepseekClient
        return DeepseekClient(
            api_key=api_key,
            base_url=os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1"),
            model=os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat"),
            temperature=0.2,
            timeout=120
        )

    def split_text(self, text: str) -> List[Document]:
        """Split text into chunks using the configured splitter"""
        return self.text_splitter.create_documents([text])

    async def identify_entities_async(self, chunks: List[Document]) -> List[str]:
        """Identify entities in text chunks"""
        # Mock implementation for testing
        return ["Nietzsche", "Kant"]

    def __init__(self, llm_provider: LLMProvider = None):
        import logging
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing TextProcessor")
        self._setup_nltk()
        self.llm = llm_provider or self._init_llm()
        self._api_semaphore = asyncio.Semaphore(settings.max_concurrent_tasks)
        self._response_cache = {}
        self.logger.info("TextProcessor initialized successfully")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.text_chunk_size,
            chunk_overlap=settings.text_chunk_overlap
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

        # Run all analysis tasks with concurrency control
        analysis_tasks = []
        for lang in langs:
            if not options.get("skip_metrics", False):
                analysis_tasks.append(self._analyze_metrics(lang, chunks, results))
            if not options.get("skip_concepts", False):
                analysis_tasks.append(self._analyze_concepts(lang, chunks, results))
            if not options.get("skip_pairs", False):
                analysis_tasks.append(self._analyze_entity_pairs(lang, results))
            if not options.get("skip_multi", False):
                analysis_tasks.append(self._analyze_multi_correlations(lang, results))
            if not options.get("skip_diagrams", False):
                analysis_tasks.append(self._generate_diagrams(lang, results))

        if analysis_tasks:
            await asyncio.gather(*analysis_tasks)

        return results

    async def _cached_llm_call(self, prompt_name: str, variables: Dict[str, str]) -> str:
        """Make LLM calls with caching"""
        cache_key = (prompt_name, frozenset(variables.items()))
        if cache_key in self._response_cache:
            return self._response_cache[cache_key]

        prompt = load_prompt(prompt_name, variables)
        if not prompt:
            raise ValueError(f"Prompt {prompt_name} not found")

        async with self._api_semaphore:
            response = await self.llm.ainvoke(prompt)
            self._response_cache[cache_key] = response
            return response

    async def _analyze_metrics(self, lang: str, chunks: List[Document], results: Dict) -> None:
        """Analyze text metrics like tone, aggressiveness etc."""
        prompt_vars = {
            "text": "\n\n".join([c.page_content for c in chunks]),
            "lang": lang
        }
        response = await self._cached_llm_call(f"analyze_tone_{lang}", prompt_vars)
        results["metrics"][lang] = response

    async def _analyze_concepts(self, lang: str, chunks: List[Document], results: Dict) -> None:
        """Identify and map key concepts"""
        # First pass - identify concepts
        prompt_vars = {
            "text": "\n\n".join([c.page_content for c in chunks]),
            "lang": lang,
            "entities": ", ".join(results["entities"])
        }
        response = await self._cached_llm_call(f"concepts_map_{lang}", prompt_vars)
        results["key_concepts"][lang] = response

    async def _analyze_entity_pairs(self, lang: str, results: Dict) -> None:
        """Analyze correlations between entity pairs"""
        entities = results["entities"]
        if len(entities) < 2:
            return

        pairs = list(combinations(entities, 2))
        for pair in pairs[:settings.max_entity_pairs]:
            prompt_vars = {
                "entity1": pair[0],
                "entity2": pair[1],
                "lang": lang
            }
            response = await self._cached_llm_call(f"correlate_entities_{lang}", prompt_vars)
            results["correlations"]["pairs"][f"{pair[0]}-{pair[1]}"] = response

    async def _analyze_multi_correlations(self, lang: str, results: Dict) -> None:
        """Analyze multi-entity correlations"""
        if len(results["entities"]) < 3:
            return

        prompt_vars = {
            "entities": ", ".join(results["entities"]),
            "lang": lang
        }
        response = await self._cached_llm_call(f"multi_correlation_map_{lang}", prompt_vars)
        results["correlations"]["multi"][lang] = response

    async def _generate_diagrams(self, lang: str, results: Dict) -> None:
        """Generate Mermaid diagrams from correlations"""
        if not results["correlations"]["pairs"]:
            return

        diagram = "graph TD\n"
        for pair, desc in results["correlations"]["pairs"].items():
            a, b = pair.split("-")
            diagram += f'    {a} -->|"{desc[:30]}..."| {b}\n'
        results["diagrams"][lang] = diagram

    # [Rest of TextProcessor implementation would go here...]
