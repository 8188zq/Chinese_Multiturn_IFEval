import os
import time
from openai import OpenAI
os.environ["OPENAI_API_KEY"] = "sk-hONtZOK4B0Zptn3yD608Ce26D6494cC787B323984d954f63"
os.environ["OPENAI_BASE_URL"] = "https://api.yesapikey.com/v1"
client = OpenAI()

import time

def generate_message(user_input, conversation_history):
    """
    根据用户输入和对话历史生成消息格式。

    :param user_input: 当前用户的输入
    :param conversation_history: 之前的对话历史 (列表)
    :return: 更新后的对话历史 (列表)
    """
    conversation_history.append({"role": "user", "content": user_input})
    
    return conversation_history

def get_content(message, conversation_history=None):
    """
    发起多轮对话的 API 调用函数。

    :param message: 当前用户输入的消息
    :param conversation_history: 当前对话历史 (可选，默认为空)
    :return: 从 API 获取的回复内容
    """
    if conversation_history is None:
        conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]
    
    conversation_history = generate_message(message, conversation_history)
    
    while True:
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-2024-08-06",  
                messages=conversation_history
            )
            
            response = completion.choices[0].message.content
            
            if response:
                conversation_history.append({"role": "assistant", "content": response})
                return response, conversation_history  
            else:
                print('error_wait_2s')
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(2)

if __name__ == "__main__":
    conversation_history = []
    user_input = "Hello!"
    response, conversation_history = get_content(user_input, conversation_history)
    print(f"Response: {response}")

    user_input = "How are you?"
    response, conversation_history = get_content(user_input, conversation_history)
    print(f"Response: {response}")

