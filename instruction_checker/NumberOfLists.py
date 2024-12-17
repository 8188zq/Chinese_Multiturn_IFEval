import random
import re

from ..instructions import Instruction
from .. import instructions_util


class NumberOfLists(Instruction):
  """Checks the paragraphs."""

  def build_description(self, num_lists, **kwargs):
    """
    """

    self._num_lists = num_lists

    self._description_pattern = ("你的回答中必须包含{num_lists}处分点，使用markdown格式下的项目符号进行分点。")

    return self._description_pattern.format(
      num_lists=self._num_lists
    )

  def get_instruction_args(self):
    """Returns the keyward args of `build_description`."""
    return {"num_lists": self._num_lists}

  def get_instruction_args_keys(self):
    """Returns the args keys of `build_description`."""
    return ["num_lists"]

  def check_following(self, value):
    bullet_lists = re.findall(r"^\s*[\*\+\-\d][^\*].*$|^\s*\d+\..*$", value, flags=re.MULTILINE)
    
    return len(bullet_lists) >= self._num_lists