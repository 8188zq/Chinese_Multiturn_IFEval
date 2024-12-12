import random
import re

from ..instructions import Instruction
from .. import instructions_util

_NUM_WORDS_LOWER_LIMIT = 20
_NUM_WORDS_UPPER_LIMIT = 450
_NUM_PARAGRAPHS = 3

class NumOfithParagraphRange(Instruction):
  """Checks the paragraphs."""

  def build_description(self, *, lower_limit_num_words = None,
                        upper_limit_num_words = None, ith = None):
    """Build the instruction description.

    Args:
      lower_limit_num_words: An integer specifying the number of words contained in the
        ith paragragh.
      upper_limit_num_words: An integer specifying the number of words contained in the
        ith paragragh.
      ith : An integer specifying which paragraph to test

    Returns:
      A string representing the instruction description.
    """
    self._lower_limit_num_words = lower_limit_num_words
    self._upper_limit_num_words = upper_limit_num_words
    if self._lower_limit_num_words is None or self._lower_limit_num_words < 0:
      self._lower_limit_num_words = _NUM_WORDS_LOWER_LIMIT
    
    if self._upper_limit_num_words is None or self._upper_limit_num_words < 0:
      self._upper_limit_num_words = _NUM_WORDS_UPPER_LIMIT
    
    self._ith = ith
    if self._ith is None or self._ith < 0:
      self._ith = random.randint(1, _NUM_PARAGRAPHS)

    self._description_pattern = (
        "你的回答中的第{ith}段必须在{lower_limit_num_words}字到{upper_limit_num_words}字的范围内。你的段落之间需要用markdown分隔符隔开,即***。")

    return self._description_pattern.format(
        ith=self._ith,
        lower_limit_num_words=self._lower_limit_num_words,
        upper_limit_num_words=self._upper_limit_num_words)

  def get_instruction_args(self):
    """Returns the keyward args of `build_description`."""
    return {
            "lower_limit_num_words": self._lower_limit_num_words,
            "upper_limit_num_words": self._upper_limit_num_words,
            "ith": self._ith,
            }

  def get_instruction_args_keys(self):
    """Returns the args keys of `build_description`."""
    return ["lower_limit_num_words", "upper_limit_num_words", "ith"]

  def check_following(self, value):
    """Checks the response contains required number of paragraphs.

    Args:
      value: A string representing the response. The response may contain
        paragraphs that are separated by the markdown divider: `***`.

    Returns:
      True if the actual number of ith paragraphs is the same as required;
      otherwise, False.
    """
    paragraphs = re.split(r"\s?\*\*\*\s?", value)
    num_paragraphs = len(paragraphs)

    for index, paragraph in enumerate(paragraphs):
      if not paragraph.strip():
        if index == 0 or index == len(paragraphs) - 1:
          num_paragraphs -= 1
        else:
          return False
    if num_paragraphs < self._ith:
      return False
    paragraphs = [p for p in paragraphs if p.strip()]
    ith_paragraph = paragraphs[self._ith - 1].strip()
    num_words = instructions_util.count_words(ith_paragraph)

    if num_words <= self._upper_limit_num_words and num_words >= self._lower_limit_num_words:
      return True
    else:
      return False