import random
import re

from ..instructions import Instruction
from .. import instructions_util

_NUM_WORDS_LOWER_LIMIT = 20
_NUM_WORDS_UPPER_LIMIT = 450
_COMPARISON_RELATION = ("超过", "少于")
_NUM_PARAGRAPHS = 3

class NumOfithParagraph(Instruction):
  """Checks the paragraphs."""

  def build_description(self, *, num_words = None,relation = None, ith = None):
    """Build the instruction description.

    Args:
      num_words: An integer specifying the number of words contained in the
        ith paragraph.
      relation: A string in (`超过`, `少于`), defining the relational
        operator for comparison.
        Two relational comparisons are supported for now:
        if 不能'超过', the actual number of words < num_words;
        if 不能'少于', the actual number of words >= num_words.
      ith : An integer specifying which paragraph to test

    Returns:
      A string representing the instruction description.
    """
    self._num_words = num_words
    if self._num_words is None or self._num_words < 0:
      self._num_words = random.randint(
          _NUM_WORDS_LOWER_LIMIT, _NUM_WORDS_UPPER_LIMIT
      )
    self._ith = ith
    if self._ith is None or self._ith < 0:
      self._ith = random.randint(1, _NUM_PARAGRAPHS)

    if relation is None:
      self._comparison_relation = random.choice(_COMPARISON_RELATION)
    elif relation not in _COMPARISON_RELATION:
      raise ValueError("The supported relation for comparison must be in "
                       f"{_COMPARISON_RELATION}, but {relation} is given.")
    else:
      self._comparison_relation = relation

    self._description_pattern = (
        "你的回答中的第{ith}段不能{relation}{num_words}字。你的段落之间需要用markdown分隔符隔开,即***。")

    return self._description_pattern.format(
        ith=self._ith,
        relation=self._comparison_relation,
        num_words=self._num_words)

  def get_instruction_args(self):
    """Returns the keyward args of `build_description`."""
    return {"num_words": self._num_words,
            "relation": self._comparison_relation,
            "ith": self._ith,
            }

  def get_instruction_args_keys(self):
    """Returns the args keys of `build_description`."""
    return ["num_words", "relation", "ith"]

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

    if self._comparison_relation == _COMPARISON_RELATION[0]:
      return num_words < self._num_words
    elif self._comparison_relation == _COMPARISON_RELATION[1]:
      return num_words >= self._num_words