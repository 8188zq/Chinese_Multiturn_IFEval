import json
import random
import re

from ..instructions import Instruction
from .. import instructions_util


class JsonChecker(Instruction):
  """Checks the paragraphs."""

  def build_description(self, **kwargs):
    """
    """
    
    self._description_pattern = ("你的回答必须按照json的格式进行包装，不能包含其他任何内容。")

    return self._description_pattern

  def get_instruction_args(self):
    """Returns the keyward args of `build_description`."""
    return {}

  def get_instruction_args_keys(self):
    """Returns the args keys of `build_description`."""
    return []

  def check_following(self, value):
    value = re.sub(r"```.*\n|\n```", "", value).strip()    
    try:
      json.loads(value)
    except Exception:
      return False
    
    return True