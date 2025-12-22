"""
Generating reports on plagiarism detection and text improvement.
"""


class Reporter:
    """
    Generates reports for plagiarism detection and text improvement.
    """

    def generate_plagiarism_report(self, plag_report: dict) -> str:  # Method 'generate_plagiarism_report' may be 'static'
        """
        Args:
            plag_report (dict): Result from PlagiarismRevealer.

        Returns:
            str: Formatted text report.
        """
        score = plag_report['similarity'] * 100
        report = [
            '--- Plagiarism Report ---',
            f'Overall Similarity: {score:.2f}%',
            f'Cosine Metric: {plag_report["cosine_similarity"]:.2f}',
            f'Jaccard Metric: {plag_report["jaccard_similarity"]:.2f}',
            f'Matching key concepts: {", ".join(plag_report["common_lemmas"][:10])}...',
        ]
        return '\n'.join(report)

    def generate_rewrite_report(self, rewritten: str, old_sim: float, new_sim: float) -> str:  # Method 'generate_rewrite_report' may be 'static'
        """
        Args:
            rewritten (str): Text after improvement.
            old_sim (float): Initial similarity score.
            new_sim (float): Similarity score after rewrite.

        Returns:
            str: Comparison report.
        """
        return (
            '--- Improvement Report ---\n'
            f'Original similarity: {old_sim * 100:.1f}%\n'
            f'New similarity: {new_sim * 100:.1f}%\n'
            f'Improvement: {(old_sim - new_sim) * 100:.1f}%\n\n'
            f'Suggested text:\n{rewritten}'
        )
