import random
import re
from pypinyin import pinyin, lazy_pinyin, Style
from ..instructions import Instruction
from .. import instructions_util

class TwoPartWithTone(Instruction):
    """Check that there are exactly two parts, with the first ending in an oblique tone and the second in a level tone."""

    def build_description(self):
        """Build the instruction description."""
        self._description_pattern = (
            "你的回答有且只能有两部分，用9个*分隔，即*********，前一部分的结尾字必须是仄声，后一部分的结尾字必须是平声,不允许以轻声结尾。"
        )
        return self._description_pattern

    def get_instruction_args(self):
        """Returns the keyword args of `build_description`."""
        return None

    def get_instruction_args_keys(self):
        """Returns the args keys of `build_description`."""
        return []

    def check_following(self, value):
        """Checks if the response has two sentences, with the first ending in an oblique tone and the second in a level tone.

        Args:
            value: A string representing the response.

        Returns:
            True if two sentences are detected and they meet the tone criteria, false otherwise.
        """
        responses = value.split("*********")
        
        if len(responses) != 2:
            return False

        first_sentence = responses[0].strip()
        second_sentence = responses[1].strip()

        if not first_sentence or not second_sentence:
            return False
        
        def remove_punctuation_and_get_last_char(sentence):
            # Remove all punctuation using a regular expression (Chinese and English punctuation)
            sentence = re.sub(r'[^\w\u4e00-\u9fa5]', '', sentence)
            return sentence[-1] if sentence else None

        # Define a function to get the tone of the last character of a sentence
        def get_last_tone(sentence):
            # Get the pinyin with tone for the last character of the sentence
            # last_char = sentence[-1]
            last_char = remove_punctuation_and_get_last_char(sentence)
            pinyin_tone = pinyin(last_char, style=Style.TONE3)  # Style.TONE3 gives the pinyin with tone number
            if pinyin_tone:
                return pinyin_tone[0][0][-1]  # Return the tone number (1-4)
            return None

        # Check if the tone of the last character of the first sentence is oblique (3 or 4)
        def is_oblique_tone(tone):
            return tone in ['3', '4', 3, 4]  # 仄声: 三声、四声

        # Check if the tone of the last character of the second sentence is level (1 or 2)
        def is_level_tone(tone):
            return tone in ['1', '2', 1, 2]  # 平声: 一声、二声

        # Get the tones for the last characters of the two sentences
        first_tone = get_last_tone(first_sentence)
        second_tone = get_last_tone(second_sentence)

        # Check if tones are valid and match the expected pattern
        if first_tone is None or second_tone is None:
            return False

        if not is_oblique_tone(first_tone):  # First sentence should end in oblique tone
            return False
        if not is_level_tone(second_tone):  # Second sentence should end in level tone
            return False

        return True
