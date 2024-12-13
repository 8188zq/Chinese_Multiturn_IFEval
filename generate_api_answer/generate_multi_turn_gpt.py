import json
import re
from tqdm import tqdm
from utils_gpt import generate_message, get_content

path = ".\Chinese_Multiturn_IFEval\data\multi_turn.jsonl"
output_path = ".\Chinese_Multiturn_IFEval\data\multi_turn_response.jsonl"
def save_cache(item, output_path):
    with open(output_path, "a", encoding='utf-8') as g:
        g.write(json.dumps(item, ensure_ascii=False) + "\n")
        g.flush()

with open(path, "r", encoding='utf-8') as f:
    data = [json.loads(line) for line in f]
    for item in tqdm(data[0:25]):
        prompt_list = item["prompt"]
        conversation_history = []
        response_list = []
        for user_input in prompt_list:
            response, conversation_history = get_content(user_input, conversation_history)
            response_list.append(response)
        temp = {"prompt": prompt_list, "conversation_history": conversation_history, "response": response_list}
        save_cache(temp, output_path)
