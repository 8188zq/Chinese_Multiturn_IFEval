import collections
import json
import random
import re
import string
from typing import Dict, Optional, Sequence, Union

import logging

from ..instructions import Instruction
from .. import instructions_util

_KEYWORD_FREQUENCY = 3

class KeywordFrequencyChecker(Instruction):
  """Check the keyword frequency."""

  def build_description(self, *, keyword = None,
                        frequency = None):
    """Build the instruction description.

    Args:
      keyword: A string representing a keyword that is expected in the response.
      frequency: An integer specifying the number of times `keyword` is expected
        to appear in the response.

    Returns:
      A string representing the instruction description.
    """
    if not keyword:
      self._keyword = instructions_util.generate_keywords(num_keywords=1)[0]
    else:
      self._keyword = keyword.strip()

    self._frequency = frequency
    if self._frequency is None or self._frequency < 0:
      self._frequency = random.randint(1, _KEYWORD_FREQUENCY)

    self._description_pattern = (
        "在你的回答里需要恰好使用“{keyword}”这个词语{frequency}次。")

    return self._description_pattern.format(
        keyword=self._keyword,
        frequency=self._frequency)

  def get_instruction_args(self):
    """Returns the keyward args of `build_description`."""
    return {"keyword": self._keyword,
            "frequency": self._frequency}

  def get_instruction_args_keys(self):
    """Returns the args keys of `build_description`."""
    return ["keyword", "frequency"]

  def check_following(self, value):
    """Checks if the response contain the keyword with required frequency."""
    actual_occurrences = len(re.findall(
        self._keyword, value, flags=re.IGNORECASE))

    return actual_occurrences == self._frequency 