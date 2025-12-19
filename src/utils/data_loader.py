import json
import logging
from pathlib import Path

from database.db_utils import add_synonym_pair

logger = logging.getLogger(__name__)


class SynonymLoader:
    """
    Advanced service for migrating synonym data.
    """

    @staticmethod
    def load_from_json(file_path: str | Path) -> None:
        """
        Read a JSON file and saves synonym pairs to the database.
        Use a safe approach to prevent database bloat.

        Args:
            file_path (str | Path): Path to the JSON file.
        """
        path = Path(file_path)
        if not path.exists():
            logger.warning(f'File {path} not found. Skipping initial data load.')
            return

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data: dict[str, list[str]] = json.load(f)

            added_count = 0
            for word, synonyms in data.items():
                for syn in synonyms:
                    add_synonym_pair(word.strip().lower(), syn.strip().lower())
                    added_count += 1

            if added_count > 0:
                logger.info(f'Database enriched with {added_count} synonym pairs.')
        except Exception as e:
            logger.error(f'Error during data migration: {e}')
