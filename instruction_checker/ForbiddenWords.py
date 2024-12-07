import collections
import json
import random
import re
import string
from typing import Dict, Optional, Sequence, Union

import logging

from chinese_multiturn_ifeval.instructions import Instruction
from chinese_multiturn_ifeval import instructions_util

_NUM_KEYWORDS = 2

class ForbiddenWords(Instruction):
  """Checks that specified words are not used in response."""

  def build_description(self, forbidden_words = None
                        ):
    """Build the instruction description.

    Args:
      forbidden_words: A sequences of strings respresenting words that are not
        allowed in the response.

    Returns:
      A string representing the instruction description.
    """

    if not forbidden_words:
      self._forbidden_words = instructions_util.generate_keywords(
          num_keywords=_NUM_KEYWORDS)
    else:
      self._forbidden_words = list(set(forbidden_words))
    self._forbidden_words = sorted(self._forbidden_words)
    self._description_pattern = (
        "在你的回答里禁止出现“{forbidden_words}”这些词。"
    )

    return self._description_pattern.format(
        forbidden_words=self._forbidden_words
    )

  def get_instruction_args(self):
    """Returns the keyward args of `build_description`."""
    return {"forbidden_words": self._forbidden_words}

  def get_instruction_args_keys(self):
    """Returns the args keys of `build_description`."""
    return ["forbidden_words"]

  def check_following(self, value):
    """Check if the response does not contain the expected keywords."""
    for word in self._forbidden_words:
      if re.search(r"\b" + word + r"\b", value, flags=re.IGNORECASE):
        return False
    return True