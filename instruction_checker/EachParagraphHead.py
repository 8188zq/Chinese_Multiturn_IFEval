import random
import re

from ..instructions import Instruction
from .. import instructions_util


class EachParagraphHead(Instruction):
  """Checks the paragraphs."""

  def build_description(self, *, special_word):
    """
    """
    
    self.special_word = special_word
    self._description_pattern = ("你的回答的每一段落第一行要以{special_word}作为开头。你的段落之间需要用markdown分隔符隔开,即***")

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
    
    paragraphs = re.split(r"\s?\*\*\*\s?", value)
    
    for paragraph in paragraphs:
      if not paragraph.split("\n")[0].startswith(self.special_word):
        return False
    
    return True