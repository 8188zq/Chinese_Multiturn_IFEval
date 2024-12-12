import random

from ..instructions import Instruction
from .. import instructions_util

class RepeatQuestion(Instruction):
  """Checks that Prompt is first repeated then answered."""

  def build_description(self, *, prompt_to_repeat = None):
    """Build the instruction description.

    Args:
      prompt_to_repeat: The prompt that is meant to be repeated.

    Returns:
      A string representing the instruction description.
    """
    if not prompt_to_repeat:
      raise ValueError("prompt_to_repeat must be set.")
    else:
      self._prompt_to_repeat = prompt_to_repeat
    self._description_pattern = (
        "首先逐字逐句地重复问题内容，不做任何更改，然后再给出你的回答（1. 在重复问题之前，不要说任何文字 2. 你需要重复的内容不包括这句话）"
    )
    return self._description_pattern

  def get_instruction_args(self):
    return {"prompt_to_repeat": self._prompt_to_repeat}

  def get_instruction_args_keys(self):
    """Returns the args keys of `build_description`."""
    return ["prompt_to_repeat"]

  def check_following(self, value):
    if value.strip().lower().startswith(self._prompt_to_repeat.strip().lower()):
      return True
    return False