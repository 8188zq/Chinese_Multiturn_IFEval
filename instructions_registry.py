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

"""Registry of all instructions."""
from Chinese_Multiturn_IFEval import instructions

_KEYWORD = "keywords:"

_LANGUAGE = "language:"

_LENGTH = "length_constraints:"

_COMBINATION = "combination:"

_SYMBOLS = "symbols:"

_CHINESE = "chinese:"

# from Chinese_Multiturn_IFEval.instruction_checker import ResponseLanguageChecker
from Chinese_Multiturn_IFEval.instruction_checker import KeywordChecker,KeywordFrequencyChecker,ForbiddenWords
from Chinese_Multiturn_IFEval.instruction_checker import ParagraphChecker,NumberOfWords,NumberOfWordsRange,NumOfithParagraph,NumOfithParagraphRange
from Chinese_Multiturn_IFEval.instruction_checker import RepeatQuestion,TwoResponse
from Chinese_Multiturn_IFEval.instruction_checker import BooknameChecker,EachParagraphHead,EachParagraphTail,FirstLineHead,JsonChecker,LastLineTail,MarkdownBold,NumberOfLists,NumOfDeclarative,NumOfExclamatory,NumOfInterrogative
from Chinese_Multiturn_IFEval.instruction_checker import TwoPartWithTone,PinYinChecker,ParallelismChecker,NoPunctuationChecker
INSTRUCTION_DICT = {
    _KEYWORD + "existence": KeywordChecker.KeywordChecker,
    _KEYWORD + "frequency": KeywordFrequencyChecker.KeywordFrequencyChecker,
    _KEYWORD + "forbidden_words": ForbiddenWords.ForbiddenWords,
    # _LANGUAGE + "response_language": ResponseLanguageChecker.ResponseLanguageChecker,
    _LENGTH + "number_paragraphs": ParagraphChecker.ParagraphChecker,
    _LENGTH + "number_words": NumberOfWords.NumberOfWords,
    _LENGTH + "number_words_range": NumberOfWordsRange.NumberOfWordsRange,
    _LENGTH + "number_of_ith_paragraph": NumOfithParagraph.NumOfithParagraph,
    _LENGTH + "number_of_ith_paragraph_range": NumOfithParagraphRange.NumOfithParagraphRange,
    
    _COMBINATION + "repeat_question_first": RepeatQuestion.RepeatQuestion,
    _COMBINATION + "two_response": TwoResponse.TwoResponse,

    _SYMBOLS + "bookname": BooknameChecker.BooknameChecker,
    _SYMBOLS + "each_paragragh_head": EachParagraphHead.EachParagraphHead,
    _SYMBOLS + "each_paragragh_tail": EachParagraphTail.EachParagraphTail,
    _SYMBOLS + "first_line_head": FirstLineHead.FirstLineHead,
    _SYMBOLS + "last_line_tail": LastLineTail.LastLineTail,
    _SYMBOLS + "json": JsonChecker.JsonChecker,
    _SYMBOLS + "markdown_bold": MarkdownBold.MarkdownBold,
    _SYMBOLS + "number_of_list": NumberOfLists.NumberOfLists,
    _SYMBOLS + "number_of_declarative": NumOfDeclarative.NumOfDeclarative,
    _SYMBOLS + "number_of_exlamatory": NumOfExclamatory.NumOfExlamatory,
    _SYMBOLS + "number_of_interrogative": NumOfInterrogative.NumOfInterrogative,

    _CHINESE + "two_part_with_tone": TwoPartWithTone.TwoPartWithTone,
    _CHINESE + "pinyin_checker": PinYinChecker.PinyinChecker,
    _CHINESE + "parallelism_checker": ParallelismChecker.ParallelismChecker,
    _CHINESE + "no_punctuation_checker": NoPunctuationChecker.NoPunctuationChecker,

}

INSTRUCTION_CONFLICTS = {
    _KEYWORD + "existence": {_KEYWORD + "existence"},
    _KEYWORD + "frequency": {_KEYWORD + "frequency"},
    _KEYWORD + "forbidden_words": {_KEYWORD + "forbidden_words"},
    _KEYWORD + "letter_frequency": {_KEYWORD + "letter_frequency"},
    _LANGUAGE
    + "response_language": {
        _LANGUAGE + "response_language",
        _KEYWORD + "existence",
        _KEYWORD + "frequency",
        _KEYWORD + "forbidden_words",
    },
    _LENGTH + "number_sentences": {_LENGTH + "number_sentences"},
    _LENGTH + "number_paragraphs": {
        _LENGTH + "number_paragraphs",
        _LENGTH + "nth_paragraph_first_word",
        _LENGTH + "number_sentences",
        _LENGTH + "nth_paragraph_first_word",
    },
    _LENGTH + "number_words": {_LENGTH + "number_words"},
    _LENGTH + "nth_paragraph_first_word": {
        _LENGTH + "nth_paragraph_first_word",
        _LENGTH + "number_paragraphs",
    },

}


def conflict_make(conflicts):
  """Makes sure if A conflicts with B, B will conflict with A.

  Args:
    conflicts: Dictionary of potential conflicts where key is instruction id
      and value is set of instruction ids that it conflicts with.

  Returns:
    Revised version of the dictionary. All instructions conflict with
    themselves. If A conflicts with B, B will conflict with A.
  """
  for key in conflicts:
    for k in conflicts[key]:
      conflicts[k].add(key)
    conflicts[key].add(key)
  return conflicts
