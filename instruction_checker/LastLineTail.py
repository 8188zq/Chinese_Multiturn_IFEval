import random
import re

from ..instructions import Instruction
from .. import instructions_util


class LastLineTail(Instruction):
  """Checks the paragraphs."""

  def build_description(self, *, special_word):
    """
    """
    
    self.special_word = special_word
    self._description_pattern = ("你的回答的最后一行要以{special_word}作为结尾。")

    return self._description_pattern.format(special_word=self.special_word)

  def get_instruction_args(self):
    """Returns the keyward args of `build_description`."""
    return {"special_word": self.special_word}

  def get_instruction_args_keys(self):
    """Returns the args keys of `build_description`."""
    return ["special_word"]

  def check_following(self, value):
    """
    """
    
    paragraphs = value.split("\n")

    return paragraphs[-1].endswith(self.special_word)