"""
Here is the main logic for text processing, plagiarism detection, and text improving.
"""

import logging
import random
import string

import nltk
from pymorphy3 import MorphAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

morph = MorphAnalyzer()
logger = logging.getLogger(__name__)


class TextProcessor:
    """
    Handles text tokenization, normalization, and stop-word removal.
    """

    def __init__(self, stop_words: list[str] | None = None):
        """
        Initialize the TextProcessor.

        Args:
            stop_words (list[str]): A list of stop words to remove.
        """
        try:
            self.stop_words = set(stop_words) if stop_words else set(nltk.corpus.stopwords.words('russian'))
        except LookupError:
            nltk.download('stopwords')
            nltk.download('punkt')
            self.stop_words = set(nltk.corpus.stopwords.words('russian'))

    def preprocess(self, text: str) -> list[str]:
        """
        Lowercase the text, removes punctuation, tokenizes, and lemmatizes.

        Args:
            text (str): The input text.

        Returns:
            list[str]: A list of processed lemmas.
        """
        if not text:
            return []

        text = text.lower().translate(str.maketrans('', '', string.punctuation))
        tokens = nltk.word_tokenize(text)

        return [morph.parse(word)[0].normal_form for word in tokens if word not in self.stop_words and word.isalpha()]


class PlagiarismRevealer:
    """
    Logic for detecting similarities between texts.
    """

    def calculate_similarity(self, orig_text: str, plag_text: str) -> float:  # Method 'calculate_similarity' may be 'static'
        """
        Calculate cosine similarity between two raw texts.

        Args:
            orig_text (str): First text.
            plag_text (str): Second text.

        Returns:
            float: Similarity score between 0.0 and 1.0.
        """
        if not orig_text.strip() or not plag_text.strip():
            return 0.0

        vectorizer = TfidfVectorizer()
        try:
            tfidf = vectorizer.fit_transform([orig_text, plag_text])
            return float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0])
        except ValueError:
            return 0.0

    def find_plagiarism(self, original: str, plagiat: str, processor: TextProcessor) -> dict:
        """
        Comprehensive check using multiple metrics.

        Args:
            original (str): The source text.
            plagiat (str): The text to be checked.
            processor (TextProcessor): Processor for tokenization.

        Returns:
            dict: Dictionary containing various similarity metrics.
        """
        tokens_orig = processor.preprocess(original)
        tokens_check = processor.preprocess(plagiat)

        cos_sim = self.calculate_similarity(original, plagiat)

        set_orig, set_check = set(tokens_orig), set(tokens_check)
        jac_sim = len(set_orig & set_check) / len(set_orig | set_check) if (set_orig | set_check) else 0

        return {
            'similarity': (cos_sim + jac_sim) / 2,
            'cosine_similarity': cos_sim,
            'jaccard_similarity': jac_sim,
            'common_lemmas': list(set_orig & set_check),
        }


class TextImprover:
    """
    Rewrites text using synonyms from the database to reduce plagiarism.
    """

    def __init__(self, synonyms_dict: dict[str, list[str]]):
        """
        Args:
            synonyms_dict (dict): Mapping of words to lists of synonyms.
        """
        self.synonyms = synonyms_dict

    def rewrite_text(self, text: str) -> str:
        """
        Replace words in text with synonyms where possible.

        Args:
            text (str): Original text.

        Returns:
            str: Rewritten text.
        """
        words = nltk.word_tokenize(text)
        rewritten = []

        for word in words:
            lemma = morph.parse(word.lower())[0].normal_form
            if lemma in self.synonyms:
                synonym = random.choice(self.synonyms[lemma])
                rewritten.append(
                    synonym.upper() if word.isupper() else synonym.capitalize() if word.istitle() else synonym
                )
            else:
                rewritten.append(word)

        return ''.join([' ' + i if not i.startswith(tuple(string.punctuation)) else i for i in rewritten]).strip()
