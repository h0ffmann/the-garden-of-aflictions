import os
import re
import asyncio
import aiofiles
from typing import Dict, List, Optional
from pathlib import Path
from .text_processor import TextProcessor

class ObsidianGenerator:
    def __init__(self, text_processor: TextProcessor):
        import logging
        self.logger = logging.getLogger(__name__)
        self.text_processor = text_processor
        self.logger.info("ObsidianGenerator initialized")

    async def generate_vault(self, analysis_results: Dict, output_dir: str) -> None:
        """Generate complete Obsidian vault from analysis results"""
        tasks = []
        for lang in analysis_results.get("langs", ["en"]):
            lang_dir = Path(output_dir) / lang
            tasks.append(self._generate_lang_vault(lang, analysis_results, lang_dir))
        
        await asyncio.gather(*tasks)

    async def _generate_lang_vault(self, lang: str, results: Dict, output_dir: Path) -> None:
        """Generate vault files for a specific language"""
        os.makedirs(output_dir, exist_ok=True)
        
        tasks = [
            self._generate_index_note(lang, results, output_dir),
            self._generate_metrics_note(lang, results, output_dir),
            self._generate_diagrams_note(lang, results, output_dir),
            self._generate_concepts_note(lang, results, output_dir),
            self._generate_multicorr_note(lang, results, output_dir),
            self._generate_entity_notes(lang, results, output_dir)
        ]
        
        await asyncio.gather(*tasks)

    async def _generate_index_note(self, lang: str, results: Dict, output_dir: Path) -> None:
        """Generate index note for the vault"""
        source_file = results.get('source_file', 'unknown_source')
        content = f"# Analysis of {source_file}\n\n"
        content += "## Key Entities\n"
        for entity in results.get('entities', []):
            content += f"- [[{entity}]]\n"
        
        file_path = output_dir / "00 Index.md"
        async with aiofiles.open(file_path, 'w') as f:
            await f.write(content)

    async def _generate_metrics_note(self, lang: str, results: Dict, output_dir: Path) -> None:
        """Generate metrics note"""
        if 'metrics' not in results:
            return
            
        content = "# Text Metrics\n\n"
        for metric, value in results['metrics'].items():
            content += f"- **{metric}**: {value}\n"
        
        file_path = output_dir / "Metrics.md"
        async with aiofiles.open(file_path, 'w') as f:
            await f.write(content)

    async def _generate_diagrams_note(self, lang: str, results: Dict, output_dir: Path) -> None:
        """Generate diagrams note"""
        if 'diagrams' not in results:
            return
            
        content = "# Diagrams\n\n"
        for name, diagram in results['diagrams'].items():
            content += f"## {name}\n```mermaid\n{diagram}\n```\n\n"
        
        file_path = output_dir / "Diagrams.md"
        async with aiofiles.open(file_path, 'w') as f:
            await f.write(content)

    async def _generate_concepts_note(self, lang: str, results: Dict, output_dir: Path) -> None:
        """Generate concepts note"""
        if 'key_concepts' not in results:
            return
            
        content = "# Key Concepts\n\n"
        for concept, desc in results['key_concepts'].items():
            content += f"## {concept}\n{desc}\n\n"
        
        file_path = output_dir / "Concepts.md"
        async with aiofiles.open(file_path, 'w') as f:
            await f.write(content)

    async def _generate_multicorr_note(self, lang: str, results: Dict, output_dir: Path) -> None:
        """Generate multi-correlation note"""
        if 'correlations' not in results or 'multi' not in results['correlations']:
            return
            
        content = "# Multi-Entity Correlations\n\n"
        for theme, entities in results['correlations']['multi'].items():
            content += f"## {theme}\n"
            content += "Related entities: " + ", ".join(f"[[{e}]]" for e in entities) + "\n\n"
        
        file_path = output_dir / "Multi-Correlations.md"
        async with aiofiles.open(file_path, 'w') as f:
            await f.write(content)

    async def _generate_entity_notes(self, lang: str, results: Dict, output_dir: Path) -> None:
        """Generate individual entity notes"""
        if 'entities' not in results:
            return
            
        tasks = []
        for entity in results['entities']:
            file_path = output_dir / f"{entity}.md"
            content = f"# {entity}\n\n## Mentions\n- Found in analysis of [[{results['source_file']}]]\n"
            async def write_note(file_path, content):
                async with aiofiles.open(file_path, 'w') as f:
                    await f.write(content)
            tasks.append(write_note(file_path, content))
        
        await asyncio.gather(*tasks)
