import random
import re

from ..instructions import Instruction
from .. import instructions_util


class MarkdownBold(Instruction):
  """Checks the paragraphs."""

  def build_description(self, *, num_bold):
    """
    """
    
    self.num_bold = num_bold
    self._description_pattern = ("在你的回答中至少需要对{num_bold}处进行markdown格式下的加粗（**）")

    return self._description_pattern.format(num_bold=self.num_bold)

  def get_instruction_args(self):
    """Returns the keyward args of `build_description`."""
    return {"num_bold": self.num_bold}

  def get_instruction_args_keys(self):
    """Returns the args keys of `build_description`."""
    return ["num_bold"]

  def check_following(self, value):
    """
    """
    
    bolds = re.findall(r"\*\*[^\n\*]*\*\*", value)

    return len(bolds) >= self.num_bold