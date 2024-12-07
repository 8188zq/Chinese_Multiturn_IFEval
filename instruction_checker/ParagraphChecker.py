import random
import re

from chinese_multiturn_ifeval.instructions import Instruction

_NUM_PARAGRAPHS = 3

class ParagraphChecker(Instruction):
  """Checks the paragraphs."""

  def build_description(self, *, num_paragraphs = None):
    """Build the instruction description.

    Args:
      num_paragraphs: An integer specifying the number of paragraphs.

    Returns:
      A string representing the instruction description.
    """
    self._num_paragraphs = num_paragraphs
    if self._num_paragraphs is None or self._num_paragraphs < 0:
      self._num_paragraphs = random.randint(1, _NUM_PARAGRAPHS)

    self._description_pattern = (
        "你的回答中有且只能包含{num_paragraphs}段。你的段落之间需要用markdown分隔符隔开,即***。"
        )

    return self._description_pattern.format(num_paragraphs=self._num_paragraphs)

  def get_instruction_args(self):
    """Returns the keyward args of `build_description`."""
    return {"num_paragraphs": self._num_paragraphs}

  def get_instruction_args_keys(self):
    """Returns the args keys of `build_description`."""
    return ["num_paragraphs"]

  def check_following(self, value):
    """Checks the response contains required number of paragraphs.

    Args:
      value: A string representing the response. The response may contain
        paragraphs that are separated by the markdown divider: `***`.

    Returns:
      True if the actual number of paragraphs is the same as required;
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

    return num_paragraphs == self._num_paragraphs