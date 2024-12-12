import json
import re
from tqdm import tqdm
from utils_gpt import generate_message, get_content

path = "E:\研三\cmif-eval-code\Chinese_Multiturn_IFEval\data\single_turn.jsonl"
output_path = "E:\研三\cmif-eval-code\Chinese_Multiturn_IFEval\data\single_turn_response.jsonl"
def save_cache(item, output_path):
    with open(output_path, "a", encoding='utf-8') as g:
        g.write(json.dumps(item, ensure_ascii=False) + "\n")
        g.flush()

with open(path, "r", encoding='utf-8') as f:
    data = [json.loads(line) for line in f]
    for item in tqdm(data):
        user_input = item["prompt"]
        conversation_history = []
        response, conversation_history = get_content(user_input, conversation_history)
        temp = {"prompt": user_input, "conversation_history": conversation_history, "response": response}
        save_cache(temp, output_path)
