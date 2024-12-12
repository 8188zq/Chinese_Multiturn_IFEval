import random
import re

from ..instructions import Instruction
from .. import instructions_util

class TwoResponse(Instruction):
  """Check that two responses were given."""

  def build_description(self):
    """Build the instruction description."""
    self._description_pattern = (
        "给出两个不同的回答，两个回答间用9个星形符号，即*********，进行分隔。"
    )
    return self._description_pattern

  def get_instruction_args(self):
    """Returns the keyward args of `build_description`."""
    return None

  def get_instruction_args_keys(self):
    """Returns the args keys of `build_description`."""
    return []

  def check_following(self, value):
    """Checks if the response has two different answers.

    Args:
      value: A string representing the response.

    Returns:
      True if two responses are detected and false otherwise.
    """
    valid_responses = list()
    responses = value.split("*********")
    for index, response in enumerate(responses):
      if not response.strip():
        if index != 0 and index != len(responses) - 1:
          return False
      else:
        valid_responses.append(response)
    return (
        len(valid_responses) == 2
        and valid_responses[0].strip() != valid_responses[1].strip()
    )