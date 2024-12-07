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

"""Binary of evaluating instruction following. See README.md."""

import argparse
import collections
import dataclasses
import json
import logging
import os
import sys
from typing import Dict, Optional, Sequence, Union

from chinese_multiturn_ifeval import instructions_registry


@dataclasses.dataclass
class InputExample:
    key: int
    instruction_id_list: list[str]
    prompt: str
    kwargs: list[Dict[str, Optional[Union[str, int]]]]


@dataclasses.dataclass
class OutputExample:
    instruction_id_list: list[str]
    prompt: str
    response: str
    follow_all_instructions: bool
    follow_instruction_list: list[bool]


def read_prompt_list(input_jsonl_filename):
    """Read inputs from jsonl."""
    inputs = []
    with open(input_jsonl_filename, "r", encoding="utf-8") as f:
        for l in f:
            example = json.loads(l)
            inputs.append(
                InputExample(
                    key=example["key"],
                    instruction_id_list=example["instruction_id_list"],
                    prompt=example["prompt"],
                    kwargs=example["kwargs"],
                )
            )
    return inputs


def write_outputs(output_jsonl_filename, outputs):
    """Writes outputs to jsonl."""
    assert outputs
    with open(output_jsonl_filename, "w", encoding="utf-8") as f:
        for o in outputs:
            output_dict = {
                attr_name: getattr(o, attr_name)
                for attr_name in o.__dataclass_fields__
            }
            f.write(json.dumps(output_dict, ensure_ascii=False))
            f.write("\n")


def test_instruction_following_strict(inp, prompt_to_response):
    """Tests response to see if instructions are followed."""
    response = prompt_to_response.get(inp.prompt, "").strip()
    instruction_list = inp.instruction_id_list
    is_following_list = []

    for index, instruction_id in enumerate(instruction_list):
        instruction_cls = instructions_registry.INSTRUCTION_DICT.get(instruction_id)
        if not instruction_cls:
            logging.warning(f"Instruction ID {instruction_id} not found in registry.")
            is_following_list.append(False)
            continue

        instruction = instruction_cls(instruction_id)
        instruction.build_description(**inp.kwargs[index])
        args = instruction.get_instruction_args()
        if args and "prompt" in args:
            instruction.build_description(prompt=inp.prompt)

        if response and instruction.check_following(response):
            is_following_list.append(True)
        else:
            is_following_list.append(False)

    return OutputExample(
        instruction_id_list=inp.instruction_id_list,
        prompt=inp.prompt,
        response=response,
        follow_all_instructions=all(is_following_list),
        follow_instruction_list=is_following_list,
    )


def test_instruction_following_loose(inp, prompt_to_response):
    """Tests response for an upper bound for following instructions."""
    response = prompt_to_response.get(inp.prompt, "").strip()
    r = response.split("\n")
    response_remove_first = "\n".join(r[1:]).strip()
    response_remove_last = "\n".join(r[:-1]).strip()
    response_remove_both = "\n".join(r[1:-1]).strip()
    revised_response = response.replace("*", "")
    revised_response_remove_first = response_remove_first.replace("*", "")
    revised_response_remove_last = response_remove_last.replace("*", "")
    revised_response_remove_both = response_remove_both.replace("*", "")
    all_responses = [
        response,
        revised_response,
        response_remove_first,
        response_remove_last,
        response_remove_both,
        revised_response_remove_first,
        revised_response_remove_last,
        revised_response_remove_both,
    ]
    instruction_list = inp.instruction_id_list
    is_following_list = []

    for index, instruction_id in enumerate(instruction_list):
        instruction_cls = instructions_registry.INSTRUCTION_DICT.get(instruction_id)
        if not instruction_cls:
            logging.warning(f"Instruction ID {instruction_id} not found in registry.")
            is_following_list.append(False)
            continue

        instruction = instruction_cls(instruction_id)
        instruction.build_description(**inp.kwargs[index])
        args = instruction.get_instruction_args()
        if args and "prompt" in args:
            instruction.build_description(prompt=inp.prompt)

        is_following = False
        for r in all_responses:
            if r and instruction.check_following(r):
                is_following = True
                break

        is_following_list.append(is_following)

    return OutputExample(
        instruction_id_list=inp.instruction_id_list,
        prompt=inp.prompt,
        response=response,
        follow_all_instructions=all(is_following_list),
        follow_instruction_list=is_following_list,
    )


def read_prompt_to_response_dict(input_jsonl_filename):
    """Creates dictionary matching prompt and response."""
    return_dict = {}
    with open(input_jsonl_filename, "r", encoding="utf-8") as f:
        for l in f:
            example = json.loads(l)
            return_dict[example["prompt"]] = example["response"]
    return return_dict


def print_report(outputs):
    """Prints a report on accuracy scores."""

    prompt_total = 0
    prompt_correct = 0
    instruction_total = 0
    instruction_correct = 0

    tier0_total = collections.defaultdict(int)
    tier0_correct = collections.defaultdict(int)

    tier1_total = collections.defaultdict(int)
    tier1_correct = collections.defaultdict(int)

    for example in outputs:
        follow_instruction_list = example.follow_instruction_list
        instruction_id_list = example.instruction_id_list

        prompt_total += 1
        if all(follow_instruction_list):
            prompt_correct += 1

        instruction_total += len(instruction_id_list)
        instruction_correct += sum(follow_instruction_list)

        for instruction_id, followed_or_not in zip(
            instruction_id_list, follow_instruction_list
        ):
            instruction_id_base = instruction_id.split(":")[0]
            tier0_total[instruction_id_base] += 1
            if followed_or_not:
                tier0_correct[instruction_id_base] += 1

        for instruction_id, followed_or_not in zip(
            instruction_id_list, follow_instruction_list
        ):
            tier1_total[instruction_id] += 1
            if followed_or_not:
                tier1_correct[instruction_id] += 1

    if prompt_total > 0:
        prompt_accuracy = prompt_correct / prompt_total
    else:
        prompt_accuracy = 0.0
    if instruction_total > 0:
        instruction_accuracy = instruction_correct / instruction_total
    else:
        instruction_accuracy = 0.0

    print(f"prompt-level accuracy: {prompt_accuracy:.6f}")
    print(f"instruction-level accuracy: {instruction_accuracy:.6f}")
    print()

    for instruction_id in sorted(tier0_total.keys()):
        if tier0_total[instruction_id] > 0:
            accuracy = tier0_correct[instruction_id] / tier0_total[instruction_id]
        else:
            accuracy = 0.0
        print(f"{instruction_id} tier0 accuracy: {accuracy:.6f}")
    print()

    for instruction_id in sorted(tier1_total.keys()):
        if tier1_total[instruction_id] > 0:
            accuracy = tier1_correct[instruction_id] / tier1_total[instruction_id]
        else:
            accuracy = 0.0
        print(f"{instruction_id} tier1 accuracy: {accuracy:.6f}")


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate instruction following based on input data and responses."
    )
    parser.add_argument(
        "--input_data",
        type=str,
        required=True,
        help="Path to input data (jsonl format).",
    )
    parser.add_argument(
        "--input_response_data",
        type=str,
        required=False,
        default=None,
        help="Path to input response data (jsonl format).",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        required=True,
        help="Output directory for inference and eval results.",
    )
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Validate output directory
    if not os.path.exists(args.output_dir):
        try:
            os.makedirs(args.output_dir)
            logging.info(f"Created output directory: {args.output_dir}")
        except Exception as e:
            logging.error(f"Failed to create output directory: {e}")
            sys.exit(1)

    # Read input data
    logging.info(f"Reading input data from {args.input_data}...")
    inputs = read_prompt_list(args.input_data)

    # Read response data if provided
    if args.input_response_data:
        logging.info(f"Reading response data from {args.input_response_data}...")
        prompt_to_response = read_prompt_to_response_dict(args.input_response_data)
    else:
        logging.error("Input response data is required.")
        sys.exit(1)

    # Define evaluation functions and corresponding output filenames
    eval_functions = [
        (test_instruction_following_strict, "eval_results_strict"),
        (test_instruction_following_loose, "eval_results_loose"),
    ]

    # Perform evaluations
    for func, output_file_name in eval_functions:
        logging.info(f"Generating {output_file_name}...")
        outputs = []
        for inp in inputs:
            output = func(inp, prompt_to_response)
            outputs.append(output)

        if outputs:
            follow_all_instructions = [o.follow_all_instructions for o in outputs]
            accuracy = sum(follow_all_instructions) / len(outputs)
            logging.info("Accuracy: %.6f", accuracy)
        else:
            logging.warning("No outputs to evaluate.")

        output_file_path = os.path.join(args.output_dir, f"{output_file_name}.jsonl")
        write_outputs(output_file_path, outputs)
        logging.info(f"Generated: {output_file_path}")

        # Print instruction following accuracy report
        print("=" * 64)
        print(f"{output_file_name} Accuracy Scores:")
        print_report(outputs)


if __name__ == "__main__":
    main()
