import re
from ..instructions import Instruction
from .. import instructions_util

class NoPunctuationChecker(Instruction):
    """Check if the response contains no punctuation."""

    def build_description(self):
        """Build the instruction description."""
        self._description_pattern = (
            "你的回答需要用文言文的形式给出，即中间不加任何标点符号。"
        )
        return self._description_pattern

    def get_instruction_args(self):
        """Returns the keyword args of `build_description`."""
        return None

    def get_instruction_args_keys(self):
        """Returns the args keys of `build_description`."""
        return []

    def check_following(self, value):
        """Checks if the response contains no punctuation.

        Args:
            value: A string representing the response.

        Returns:
            True if the response contains no punctuation, False otherwise.
        """
        # Remove all punctuation characters (both Chinese and English punctuation)
        cleaned_value = re.sub(r'[^\w\u4e00-\u9fa5]', '', value)
        
        # If the cleaned value is the same length as the original value, there were no punctuation marks
        if len(cleaned_value) == len(value):
            return True
        else:
            return False
