import json
import random
import re
random.seed(42)
path = "E:\研三\cmif-eval-code\Chinese_Multiturn_IFEval\data\data_v1.1_release.jsonl"
questions = []
with open(path,"r") as f:
    data = [json.loads(line) for line in f]
    for item in data:
        if item["category"] in ["综合问答","角色扮演","文本写作","中文理解","基本任务","专业能力"]:
            questions.append(item)