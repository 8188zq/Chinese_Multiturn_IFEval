# coding=utf-8
# Copyright 2024 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

_CONSTRAINED_RESPONSE_OPTIONS = (
    "My answer is yes.", "My answer is no.", "My answer is maybe.")

_STARTER_OPTIONS = ("I would say", "My answer is", "I believe",
                    "In my opinion", "I think", "I reckon", "I feel",
                    "From my perspective", "As I see it", "According to me",
                    "As far as I'm concerned", "To my understanding",
                    "In my view", "My take on it is", "As per my perception")

_ENDING_OPTIONS = ("Any other questions?",
                   "Is there anything else I can help with?")

_SECTION_SPLITER = ("Section", "SECTION")

_POSTSCRIPT_MARKER = ("P.S.", "P.P.S")

class Instruction:
  """An instruction template."""

  def __init__(self, instruction_id):
    self.id = instruction_id

  def build_description(self, **kwargs):
    raise NotImplementedError("`build_description` not implemented.")

  def get_instruction_args(self):
    raise NotImplementedError("`get_instruction_args` not implemented.")

  def get_instruction_args_keys(self):
    raise NotImplementedError("`get_instruction_args_keys` not implemented.")

  def check_following(self, value):
    raise NotImplementedError("`check_following` not implemented.")