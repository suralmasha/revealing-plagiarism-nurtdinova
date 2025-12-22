"""Database module for plagiarism detector."""

from .connection import get_connection
from .db_utils import (
    create_database,
    add_synonym_pair,
    add_plagiarism_check,
    get_synonyms_for_word,
    load_synonyms_dict_from_db,
)

__all__ = [
    "get_connection",
    "create_database",
    "add_synonym_pair",
    "add_plagiarism_check",
    "get_synonyms_for_word",
    "load_synonyms_dict_from_db",
]
