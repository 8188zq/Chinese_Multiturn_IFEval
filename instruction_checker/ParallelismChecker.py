import re
from ..instructions import Instruction
from .. import instructions_util

class ParallelismChecker(Instruction):
    """Check that the response contains a parallel sentence with each clause having the same number of characters."""

    def build_description(self):
        """Build the instruction description."""
        self._description_pattern = (
            "你的回答需要包含一句排比句，用&&框起来，如&排比句&。排比句中用逗号分隔的每个分句字数要一致。"
        )
        return self._description_pattern

    def get_instruction_args(self):
        """Returns the keyword args of `build_description`."""
        return None

    def get_instruction_args_keys(self):
        """Returns the args keys of `build_description`."""
        return []

    def check_following(self, value):
        """Checks if the response contains a parallel sentence with consistent clause length.

        Args:
            value: A string representing the response.

        Returns:
            True if the response contains a valid parallel sentence with equal clause length, False otherwise.
        """
        # Check if the input contains a sentence enclosed by && (排比句)
        pattern = r"&([^&]+)&"  # Match the content between &&

        match = re.search(pattern, value)
        if not match:
            return False

        # Extract the parallel sentence part
        parallel_sentence = match.group(1).strip()

        # Split the sentence by commas to get each clause
        clauses = [clause.strip() for clause in re.split(r'[，,]', parallel_sentence)]

        # Function to clean the text by removing punctuation and spaces
        def clean_text(text):
            # Remove punctuation and spaces
            return re.sub(r'[^\w\u4e00-\u9fa5]', '', text)

        # Clean all clauses by removing punctuation
        cleaned_clauses = [clean_text(clause) for clause in clauses]

        # Check if all clauses have the same length (in terms of number of characters)
        if len(set(len(clause) for clause in cleaned_clauses)) == 1:  # All lengths must be the same
            return True
        return False
