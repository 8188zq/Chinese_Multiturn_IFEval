import collections
import json
import random
import re
import string
from typing import Dict, Optional, Sequence, Union

import logging

from ..instructions import Instruction
from .. import instructions_util

_NUM_KEYWORDS = 2

class KeywordChecker(Instruction):
  """Check the exisitence of certain keywords."""

  def build_description(self, *, keywords = None
                        ):
    """Build the instruction description.

    Args:
      keywords: A sequence of strings representing the keywords that are
        expected in the response.

    Returns:
      A string representing the instruction description.
    """

    if not keywords:
      self._keywords = instructions_util.generate_keywords(
          num_keywords=_NUM_KEYWORDS)
    else:
      self._keywords = keywords
    self._keywords = sorted(self._keywords)

    self._description_pattern = ("在你的回答里要使用“{keywords}”这两个词语。")

    return self._description_pattern.format(keywords=self._keywords)

  def get_instruction_args(self):
    """Returns the keyward args of `build_description`."""
    return {"keywords": self._keywords}

  def get_instruction_args_keys(self):
    """Returns the args keys of `build_description`."""
    return ["keywords"]

  def check_following(self, value):
    """Check if the response contain the expected keywords."""
    for keyword in self._keywords:
      if not re.search(keyword, value, flags=re.IGNORECASE):
        return False
    return True
