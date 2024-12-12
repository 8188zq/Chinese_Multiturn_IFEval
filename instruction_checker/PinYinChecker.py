import random
import re
from pypinyin import pinyin, lazy_pinyin, Style
from ..instructions import Instruction
from .. import instructions_util

class PinyinChecker(Instruction):
    """Check that the second response is the pinyin transcription of the first response."""

    def build_description(self):
        """Build the instruction description."""
        self._description_pattern = (
            "你的回答有且只能有两部分，后者是前者的拼音标注，用9个*分隔，即*********，拼音不需要标注音调，"
            "使用拉丁字母来表示，和输入法保持一致，如“ü”可以用“v”替代。"
        )
        return self._description_pattern

    def get_instruction_args(self):
        """Returns the keyword args of `build_description`."""
        return None

    def get_instruction_args_keys(self):
        """Returns the args keys of `build_description`."""
        return []

    def check_following(self, value):
        """Checks if the second response is the pinyin transcription of the first response.

        Args:
            value: A string representing the response.

        Returns:
            True if the second response matches the pinyin transcription of the first response, False otherwise.
        """
        valid_responses = list()
        responses = value.split("*********")
        
        if len(responses) != 2:
            return False

        first_sentence = responses[0].strip()
        second_sentence = responses[1].strip()

        if not first_sentence or not second_sentence:
            return False

        # Function to convert a Chinese sentence to pinyin without tone and with 'v' for 'ü'
        def convert_to_pinyin(chinese_sentence):
            pinyin_list = lazy_pinyin(chinese_sentence)  # Get pinyin without tone
            # Join the pinyin into a single string, replacing 'ü' with 'v'
            pinyin_string = ''.join([word.replace('ü', 'v') for word in pinyin_list])
            return pinyin_string

        # Remove non-pinyin characters (e.g., punctuation, spaces, newlines) using regex
        def clean_text(text):
            # Keep only Latin letters (a-z, A-Z) and 'v' for 'ü'
            return re.sub(r'[^a-zA-Zv]', '', text.replace(' ', '').replace('\n', ''))

        # Get the pinyin of the first sentence (no tone, 'ü' -> 'v')
        expected_pinyin = convert_to_pinyin(first_sentence)

        # Clean both the expected pinyin and the second sentence by removing non-pinyin characters
        expected_pinyin = clean_text(expected_pinyin)
        second_sentence = clean_text(second_sentence)
        return expected_pinyin == second_sentence
