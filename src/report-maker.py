"""
Generating reports on plagiarism detection and text improvement.
"""


class Reporter:
    """
    Generates reports for plagiarism detection and text improvement.
    """

    def generate_plagiarism_report(self, plag_report: dict):
        """
        Generates a string report for plagiarism detection results.

        Args:
            plag_report (dict): The result from plagiarism detection.

        Returns:
            str: The generated plagiarism report string.
        """
        pass

    def generate_rewrite_report(self, original_text: str, rewritten_text: str, original_similarity: float, final_similarity: float):
        """
        Generates a string report for text rewriting results.

        Args:
            original_text (str): The original text before rewriting.
            rewritten_text (str): The text after rewriting.
            original_similarity (float): The similarity score before rewriting.
            final_similarity (float): The similarity score after rewriting.

        Returns:
            str: The generated report string.
        """
        pass
