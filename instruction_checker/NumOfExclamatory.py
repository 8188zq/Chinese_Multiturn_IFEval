import random
import re

from ..instructions import Instruction
from .. import instructions_util

_NUM_WORDS_LOWER_LIMIT = 20
_NUM_WORDS_UPPER_LIMIT = 450
_COMPARISON_RELATION = ("超过", "少于")
_NUM_PARAGRAPHS = 3

class NumOfExlamatory(Instruction):
  """Checks the paragraphs."""

  def build_description(self, *, special_word = ""):
    """Build the instruction description.

    Args:
      punctuation: ？ 后面的标点符号
        
    Returns:
      A string representing the instruction description.
    """
    self.special_word = special_word

    self._description_pattern = (f"你的回答中至少需要包含两句以上的感叹句。每个感叹句的`！`之后需要字符`{special_word}`。")

    return self._description_pattern.format(special_word=self.special_word)

  def get_instruction_args(self):
    """Returns the keyward args of `build_description`."""
    return {"special_word": self.special_word}

  def get_instruction_args_keys(self):
    """Returns the args keys of `build_description`."""
    return ["special_word"]

  def check_following(self, value):
    """Checks the response contains required number of paragraphs.

    Args:
      value: A string representing the response. The response may contain
        paragraphs that are separated by the markdown divider: `***`.

    Returns:
      True if the actual number of ith paragraphs is the same as required;
      otherwise, False.
    """
    n = len(value)

    count = 0
    index = 0
    while index < n:
        if value[index] == "！":
            begin = index + 1
            end = begin + len(self.special_word)
            if value[begin:end] != self.special_word:
                return False
            index += len(self.special_word)+1
            count += 1
        else:
            index += 1

    return count >= 2