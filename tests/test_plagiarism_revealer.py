"""
Checks Plagiarism Revealer functionality.
"""

import pytest
from src.plagiarism_detector import TextProcessor, PlagiarismRevealer  # from plagiarism_detector import ...

class TestPlagiarismRevealer:
    """
    Tests for the PlagiarismRevealer class.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        """
        SetUp for PlagiarismRevealer class.
        """
        self.revealer = PlagiarismRevealer()
        self.processor = TextProcessor()

    def test_find_plagiarism_return_value(self):
        """
        Check return value.
        """
        res = self.revealer.find_plagiarism("Оригинал", "Плагиат", self.processor)

        assert isinstance(res, dict)
        assert all(key in res for key in ["similarity", "cosine_similarity", "jaccard_similarity", "common_lemmas"])
        assert isinstance(res["similarity"], float)

    def test_identical_texts(self):
        """
        Perfect match scenario (100% similarity).
        """
        text = "Это тестовое предложение для проверки."
        res = self.revealer.find_plagiarism(text, text, self.processor)
        assert res["similarity"] == 1.0

    def test_completely_different_texts(self):
        """
        Scenario with zero or very low similarity.
        """
        txt1 = "Яблоко красное"
        txt2 = "Космос бесконечен"
        res = self.revealer.find_plagiarism(txt1, txt2, self.processor)
        assert res["similarity"] < 0.2
