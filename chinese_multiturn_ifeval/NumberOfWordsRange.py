import random
import re

from ..instructions import Instruction
from .. import instructions_util

_NUM_WORDS_LOWER_LIMIT = 20
_NUM_WORDS_UPPER_LIMIT = 450
_COMPARISON_RELATION = ("超过", "少于")
class NumberOfWordsRange(Instruction):
  """Checks the number of words."""

  def build_description(self, *, lower_limit_num_words = None,
                        upper_limit_num_words = None):
    """Build the instruction description.

    Args:
      lower_limit_num_words: An integer specifying the number of words contained in the
        response.
      upper_limit_num_words: An integer specifying the number of words contained in the
        response.

    Returns:
      A string representing the instruction description.
    """

    self._lower_limit_num_words = lower_limit_num_words
    self._upper_limit_num_words = upper_limit_num_words
    if self._lower_limit_num_words is None or self._lower_limit_num_words < 0:
      self._lower_limit_num_words = _NUM_WORDS_LOWER_LIMIT
    
    if self._upper_limit_num_words is None or self._upper_limit_num_words < 0:
      self._upper_limit_num_words = _NUM_WORDS_UPPER_LIMIT


    self._description_pattern = (
        "你的回答必须在{lower_limit_num_words}字到{upper_limit_num_words}字的范围内。")

    return self._description_pattern.format(
        lower_limit_num_words=self._lower_limit_num_words,
        upper_limit_num_words=self._upper_limit_num_words)

  def get_instruction_args(self):
    """Returns the keyward args of `build_description`."""
    return {"lower_limit_num_words": self._lower_limit_num_words,
            "upper_limit_num_words": self._upper_limit_num_words}

  def get_instruction_args_keys(self):
    """Returns the args keys of `build_description`."""
    return ["lower_limit_num_words", "upper_limit_num_words"]

  def check_following(self, value):
    """Checks if the response contains the expected number of words."""
    num_words = instructions_util.count_words(value)

    if num_words <= self._upper_limit_num_words and num_words >= self._lower_limit_num_words:
      return True
    else:
      return False