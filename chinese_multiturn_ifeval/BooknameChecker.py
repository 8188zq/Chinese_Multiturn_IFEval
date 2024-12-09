import random
import re

from ..instructions import Instruction
from .. import instructions_util


class BooknameChecker(Instruction):
  """Checks the paragraphs."""

  def build_description(self, **kwargs):
    """
    """

    self._description_pattern = ("你的回答需要包含一个题目，用书名号(《》)括起来。")

    return self._description_pattern

  def get_instruction_args(self):
    """Returns the keyward args of `build_description`."""
    return {}

  def get_instruction_args_keys(self):
    """Returns the args keys of `build_description`."""
    return []

  def check_following(self, value):
    """Checks the response contains required number of paragraphs.

    Args:
      value: A string representing the response. The response may contain
        paragraphs that are separated by the markdown divider: `***`.

    Returns:
      True if the actual number of ith paragraphs is the same as required;
      otherwise, False.
    """
    if value.count("《") != 1 or value.count("》") != 1:
      return False
    return value.index("《") < value.index("》")