"""
Checks Text Improver functionality.
"""

import pytest
from src.plagiarism_detector import TextImprover


class TestTextImprover:
    """
    Tests for the TextImprover class.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        """
        SetUp for TextImprover class.
        """
        self.synonyms = {"делать": ["выполнять"], "хороший": ["прекрасный"]}
        self.improver = TextImprover(self.synonyms)

    def test_rewrite_ideal(self):
        """
        Ideal rewrite scenario.
        """
        text = "Делать хороший проект."
        rewritten = self.improver.rewrite_text(text)

        assert "выполнять" in rewritten.lower()
        assert "прекрасный" in rewritten.lower()

    def test_rewrite_no_synonyms_available(self):
        """
        Check behavior when no synonyms are in the dictionary.
        """
        text = "Неизвестное слово."
        assert self.improver.rewrite_text(text).strip(".") == "Неизвестное слово"
