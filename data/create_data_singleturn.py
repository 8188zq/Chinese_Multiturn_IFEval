import json
import random
import re
random.seed(42)
path = ".\Chinese_Multiturn_IFEval\data\data_v1.1_release.jsonl"
questions = []
with open(path,"r", encoding='utf-8') as f:
    data = [json.loads(line) for line in f]
    for item in data:
        if item["category"] in ["综合问答","角色扮演","文本写作","中文理解","基本任务","专业能力"]:
            questions.append(item)

output_path = ".\Chinese_Multiturn_IFEval\data\single_turn.jsonl"
new_data = []

_KEYWORD = "keywords:"

_LANGUAGE = "language:"

_LENGTH = "length_constraints:"

_COMBINATION = "combination:"

_SYMBOLS = "symbols:"

_CHINESE = "chinese:"
from .. import instructions_registry
# from ..instruction_checker import ResponseLanguageChecker
from ..instruction_checker import KeywordChecker,KeywordFrequencyChecker,ForbiddenWords
from ..instruction_checker import ParagraphChecker,NumberOfWords,NumberOfWordsRange,NumOfithParagraph,NumOfithParagraphRange
from ..instruction_checker import RepeatQuestion,TwoResponse
from ..instruction_checker import BooknameChecker,EachParagraphHead,EachParagraphTail,FirstLineHead,JsonChecker,LastLineTail,MarkdownBold,NumberOfLists,NumOfDeclarative,NumOfExclamatory,NumOfInterrogative
from ..instruction_checker import TwoPartWithTone,PinYinChecker,ParallelismChecker,NoPunctuationChecker
INSTRUCTION_List = [
    _KEYWORD + "existence",
    _KEYWORD + "frequency",
    _KEYWORD + "forbidden_words",
    # _LANGUAGE + "response_language",
    _LENGTH + "number_paragraphs",
    _LENGTH + "number_words",
    _LENGTH + "number_words_range",
    _LENGTH + "number_of_ith_paragraph",
    _LENGTH + "number_of_ith_paragraph_range",
    _COMBINATION + "repeat_question_first",
    _COMBINATION + "two_response",
    _SYMBOLS + "bookname",
    _SYMBOLS + "each_paragragh_head",
    _SYMBOLS + "each_paragragh_tail",
    _SYMBOLS + "first_line_head",
    _SYMBOLS + "last_line_tail",
    _SYMBOLS + "json",
    _SYMBOLS + "markdown_bold",
    _SYMBOLS + "number_of_list",
    _SYMBOLS + "number_of_declarative",
    _SYMBOLS + "number_of_exlamatory",
    _SYMBOLS + "number_of_interrogative",
    _CHINESE + "two_part_with_tone",
    _CHINESE + "pinyin_checker",
    _CHINESE + "parallelism_checker",
    _CHINESE + "no_punctuation_checker",
]

def filter_punctuation(word_list):
    pattern = re.compile(r'^[\u4e00-\u9fa5]+$')  # 只匹配中文字符
    return [word for word in word_list if pattern.match(word)] # 只保留中文字符

def auto_generate_kwargs(instruction_id, ref, question):
    kwargs_list = [] 
    if instruction_id == _KEYWORD + "existence":
        import jieba
        words = jieba.cut(ref)
        word_list = list(words)
        word_list = filter_punctuation(word_list)
        if len(word_list) >= 2:
            keywords = random.sample(word_list, 2)  
        else:
            keywords = word_list  
        kwargs = {"keywords": keywords}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _KEYWORD + "frequency":
        import jieba
        words = jieba.cut(ref)
        word_list = list(words)
        word_list = filter_punctuation(word_list)
        keyword = random.choice(word_list)
        kwargs = {"keyword": keyword, "frequency": random.randint(2,3)}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _KEYWORD + "forbidden_words":
        forbidden_words = random.sample([
    "和", "或", "但是", "而", "所以", "因为", "如果", "既然", "虽然", "即使", "在", "不过", "因此", "然后", "否则", 
    "同时", "除非", "只有", "即", "虽然", "但是", "然后", "而且", "此外", "的", "了", "是", "我", "你", "他", "她", "它", "我们", "你们", "他们", "这", "那", "有", "在", "和", "就", "不", "也", 
    "很", "对", "把", "把", "而", "所以", "但是", "如果", "因为", "虽然", "或", "或者", "与", "为", "被", "被", "在", "到", 
    "上", "下", "里", "前", "后", "中", "对", "与", "着", "从", "给", "向", "但", "即", "且", "如", "则", "也", "更", "只", 
    "都", "及", "及其", "并", "即使", "然而", "就", "也", "所", "能", "至", "此", "未"], 4)
        kwargs = {"forbidden_words": forbidden_words}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _LENGTH + "number_paragraphs":
        kwargs = {"num_paragraphs": random.randint(1,3)}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _LENGTH + "number_words":
        kwargs = {"num_words": random.choice([100,200,300]), "relation": random.choice(["超过","少于"])}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _LENGTH + "number_words_range":
        kwargs = {"lower_limit_num_words": random.choice([100,200,300]), "upper_limit_num_words": random.choice([400,500,600])}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _LENGTH + "number_of_ith_paragraph":
        kwargs = {"num_words": random.choice([100,200,300]), "relation": random.choice(["超过","少于"]),"ith": random.randint(1,3)}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _LENGTH + "number_of_ith_paragraph_range":
        kwargs = {"lower_limit_num_words": random.choice([100,200,300]), "upper_limit_num_words": random.choice([400,500,600]),"ith": random.randint(1,3)}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _COMBINATION + "repeat_question_first":
        prompt_to_repeat = question
        kwargs = {"prompt_to_repeat": prompt_to_repeat}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _COMBINATION + "two_response":
        return [{}]
    if instruction_id == _SYMBOLS + "bookname":
        return [{}]
    if instruction_id == _SYMBOLS + "each_paragragh_head":
        special_word = random.choice(["我认为","我觉得","我想","客观地说","可以说","某种程度上","似乎","某种意义上","一般来说","事实上","实际上","总的来说","值得注意的是"])
        kwargs = {"special_word": special_word}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _SYMBOLS + "each_paragragh_tail":
        special_word = random.choice(["吧","呀", "呢", "啊", "了", "的", "吧", "呢", "嘛", "哦", "哈", "啊", "啦", "对吧", "对不对", "是不是", "对吧", "啥的", "什么的"])
        kwargs = {"special_word": special_word}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _SYMBOLS + "first_line_head":
        special_word = random.choice(["我认为","我觉得","我想","客观地说","可以说","某种程度上","似乎","某种意义上","一般来说","事实上","实际上","总的来说","值得注意的是"])
        kwargs = {"special_word": special_word}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _SYMBOLS + "last_line_tail":
        special_word = random.choice(["吧","呀", "呢", "啊", "了", "的", "吧", "呢", "嘛", "哦", "哈", "啊", "啦", "对吧", "对不对", "是不是", "对吧", "啥的", "什么的"])
        kwargs = {"special_word": special_word}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _SYMBOLS + "json":
        return [{}]
    if instruction_id == _SYMBOLS + "markdown_bold":
        num_bold = random.randint(1,5)
        kwargs = {"num_bold": num_bold}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _SYMBOLS + "number_of_list":
        num_lists = random.randint(1,3)
        kwargs = {"num_lists": num_lists}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _SYMBOLS + "number_of_declarative":
        special_word = random.choice(["对不对？","是不是？","对吧？","难道不是吗？"])
        kwargs = {"special_word": special_word}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _SYMBOLS + "number_of_exlamatory":
        special_word = random.choice(["对不对？","是不是？","对吧？","难道不是吗？"])
        kwargs = {"special_word": special_word}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _SYMBOLS + "number_of_interrogative":
        special_word = random.choice(["对不对？","是不是？","对吧？","难道不是吗？"])
        kwargs = {"special_word": special_word}
        kwargs_list.append(kwargs)
        return kwargs_list
    if instruction_id == _CHINESE + "two_part_with_tone":
        return [{}]
    if instruction_id == _CHINESE + "pinyin_checker":
        return [{}]
    if instruction_id == _CHINESE + "parallelism_checker":
        return [{}]
    if instruction_id == _CHINESE + "no_punctuation_checker":
        return [{}]
    print(f"instruction_id: {instruction_id}  not found!")
    return [{}]

for index, item in enumerate(questions):
    # if index <= 2:
    #     continue
    try:
        instruction_id = INSTRUCTION_List[index]
    except:
        break
    instruction_cls = instructions_registry.INSTRUCTION_DICT.get(instruction_id)
    instruction = instruction_cls(instruction_id)
    kwargs = auto_generate_kwargs(instruction_id, item["reference"], item["question"])
    try:
        if len(kwargs) == 0:
            require = instruction.build_description()
        else:
            require = instruction.build_description(**kwargs[0])
    except:
        print(f"error: {instruction_id}")
        continue
    prompt = item["question"] + "\n" + require
    temp = {
        "key": index,
        "prompt": prompt,
        "instruction_id_list": [instruction_id],
        "kwargs": kwargs,
    }
    new_data.append(temp)
with open(output_path, "w", encoding='utf-8') as g:
    for item in new_data:
        g.write(json.dumps(item,ensure_ascii=False) + "\n")
        g.flush()