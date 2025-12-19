"""
Checks Text Processor functionality.
"""

import pytest
from src.plagiarism_detector import TextProcessor


class TestTextProcessor:
    """Tests for the TextProcessor class."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """
        SetUp for TextProcessor class.
        """
        self.processor = TextProcessor(stop_words=["и", "в", "на"])

    def test_preprocess_ideal(self):
        """
        Ideal preprocess scenario.
        """
        text = "Студенты делают проекты!"
        result = self.processor.preprocess(text)

        assert isinstance(result, list)
        assert "студент" in result
        assert "делать" in result
        assert "!" not in result

    def test_preprocess_empty_input(self):
        """
        Check the processor handling empty strings.
        """
        assert self.processor.preprocess("") == []
        assert self.processor.preprocess(None) == []

    def test_preprocess_only_punctuation(self):
        """
        Check input with no words.
        """
        assert self.processor.preprocess("!!! ??? ,,,") == []
