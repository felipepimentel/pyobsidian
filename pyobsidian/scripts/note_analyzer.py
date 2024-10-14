# pyobsidian/note_analysis.py

import logging
import os
import re
from collections import defaultdict
from typing import Dict, List

import click

from .config import ObsidianConfig
from .utils.file_operations import get_all_files, get_file_content

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class NoteAnalyzer:
    def __init__(self, config: ObsidianConfig):
        self.config = config
        self.vault_path = config.vault_path
        self.small_note_threshold = config.small_note_threshold
        self.empty_note_threshold = config.empty_note_threshold

    def analyze_notes(self) -> Dict[str, Any]:
        """
        Perform a comprehensive analysis of notes.

        :return: A dictionary containing results of various analyses
        """
        results = {
            "small_notes": [],
            "empty_notes": [],
            "broken_links": defaultdict(list),
            "completely_empty_notes": [],
        }

        for file_path in get_all_files(self.vault_path):
            content = get_file_content(file_path)
            self._check_note_size(file_path, content, results)
            self._check_links(file_path, content, results)
            self._check_empty_content(file_path, content, results)

        return results

    def _check_note_size(self, file_path: str, content: str, results: Dict[str, List]):
        if len(content) < self.empty_note_threshold:
            results["empty_notes"].append(file_path)
        elif len(content) < self.small_note_threshold:
            results["small_notes"].append(file_path)

    def _check_links(
        self, file_path: str, content: str, results: Dict[str, Dict[str, List]]
    ):
        if not file_path.endswith(".md"):
            return

        link_pattern = re.compile(r"\[\[([^\]]+)\]\]")
        md_files = {
            os.path.splitext(os.path.basename(f))[0]
            for f in get_all_files(self.vault_path)
        }

        for match in link_pattern.findall(content):
            link_name = match.split("|")[0]
            if link_name not in md_files:
                results["broken_links"][file_path].append(link_name)

    def _check_empty_content(
        self, file_path: str, content: str, results: Dict[str, List]
    ):
        content_without_frontmatter = re.sub(
            r"^---\n.*?\n---\n", "", content, flags=re.DOTALL
        ).strip()
        if not content_without_frontmatter:
            results["completely_empty_notes"].append(file_path)


@click.group()
@click.pass_context
def cli(ctx):
    """Analyze Obsidian notes for various issues."""
    ctx.obj = NoteAnalyzer(ObsidianConfig())


@cli.command()
@click.pass_obj
def analyze(analyzer: NoteAnalyzer):
    """Perform a comprehensive analysis of notes."""
    try:
        results = analyzer.analyze_notes()

        click.echo("Analysis Results:")
        click.echo(f"Small Notes: {len(results['small_notes'])}")
        click.echo(f"Empty Notes: {len(results['empty_notes'])}")
        click.echo(f"Completely Empty Notes: {len(results['completely_empty_notes'])}")

        total_broken_links = sum(
            len(links) for links in results["broken_links"].values()
        )
        click.echo(
            f"Broken Links: {total_broken_links} in {len(results['broken_links'])} files"
        )

        # Detailed reporting can be added here if needed

        logger.info("Note analysis completed successfully")
    except Exception as e:
        click.echo(f"An error occurred during analysis: {str(e)}")
        logger.exception("Error in analyze command")


if __name__ == "__main__":
    cli()
