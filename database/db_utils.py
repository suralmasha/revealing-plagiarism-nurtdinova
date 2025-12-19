import logging

from .connection import get_connection

logger = logging.getLogger(__name__)

SYNONYMS_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS synonyms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL,
    synonym TEXT NOT NULL,
    UNIQUE(word, synonym)
);
"""

PLAGIARISM_CHECK_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS plagiarism_checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_text TEXT NOT NULL,
    checked_text TEXT NOT NULL,
    similarity REAL NOT NULL CHECK(similarity >= 0.0 AND similarity <= 1.0),
    rewritten_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def create_database():
    """
    Create database tables if not exist.
    """
    conn = get_connection()
    cursor = conn.cursor()

    logger.info('Initializing database...')
    cursor.executescript(SYNONYMS_TABLE_SCHEMA)
    cursor.executescript(PLAGIARISM_CHECK_TABLE_SCHEMA)

    conn.commit()
    conn.close()
    logger.info('Database initialized successfully.')


def add_synonym_pair(word: str, synonym: str):
    """
    Add a word-synonym pair to the synonyms table.

    Args:
        word: The original word.
        synonym: The synonym for the word.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT OR IGNORE INTO synonyms (word, synonym) VALUES (?, ?)',
        (word, synonym)
    )
    conn.commit()
    conn.close()
    logger.info(f"Added synonym pair: '{word}' -> '{synonym}'")


def add_plagiarism_check(original_text: str, checked_text: str, similarity: float, rewritten_text: str = None):
    """
    Add a plagiarism check record to the plagiarism_checks table.

    Args:
        original_text: The original text.
        checked_text: The text that was checked.
        similarity: The calculated similarity score.
        rewritten_text: The rewritten version of the checked text.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO plagiarism_checks (original_text, checked_text, similarity, rewritten_text) VALUES (?, ?, ?, ?)',
        (original_text, checked_text, similarity, rewritten_text)
    )
    conn.commit()
    conn.close()
    logger.info(f'Added plagiarism check record for original text id: {cursor.lastrowid}')


def get_synonyms_for_word(word: str) -> list[str]:
    """
    Get a list of synonyms for a given word from the synonyms table.

    Args:
        word: The word to find synonyms for.

    Returns:
        A list of synonyms for the word.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT synonym FROM synonyms WHERE word = ?', (word,))
    rows = cursor.fetchall()
    synonyms = [row[0] for row in rows]
    conn.close()
    return synonyms


def load_synonyms_dict_from_db() -> dict[str, list[str]]:
    """
    Load all synonyms from the table into a dictionary.

    Returns:
        A dictionary mapping words to their synonyms.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT word, synonym FROM synonyms')
    rows = cursor.fetchall()
    synonyms_dict = {}
    for row in rows:
        word, synonym = row[0], row[1]
        if word not in synonyms_dict:
            synonyms_dict[word] = []
        synonyms_dict[word].append(synonym)
    conn.close()
    return synonyms_dict
