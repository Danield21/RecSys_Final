import argparse
import json
import math
import os
import random
import re
import sys
import threading
import time
from datetime import datetime
from typing import *

import numpy as np
import openai
from rapidfuzz import fuzz
from tqdm import tqdm

from rapidfuzz import fuzz
from datetime import datetime
import sys
from config import traditional, break_down, break_down_with_rationale

prompt_style='break_down_with_rationale'
retry_cnt = 6
if prompt_style == 'traditonal':
    prompt_content = traditional
elif prompt_style == 'break_down':
    prompt_content = break_down
elif prompt_style == 'break_down_with_rationale':
    prompt_content = break_down_with_rationale

save_path = f"code/gpt4o_{prompt_style}.jsonl"

def read_jsonl(fpath: str) -> List[Dict]:
    res = []
    with open(fpath, 'r') as f:
        for line in f:
            data = json.loads(line)
            res.append(data)
    return res

def write_jsonl(ans_file, obj):
    ans_file.write(json.dumps(obj, ensure_ascii=False) + '\n')
    

seed=2024
random.seed(seed)
domain = 'game'
domain_map = {'item': domain, 'Item': domain.capitalize(), 'ITEM': domain.upper()}
data = "data/steam/steam_oneturn_ranking_data_100.jsonl"
eval_data = read_jsonl(data)[2:]


openai.api_base = ""
openai.api_key = ''

with open(save_path, 'a') as fw:
    for instance in eval_data:
        question = instance['question']
        # prompt = "You are a helpful conversational agent who is good at recommendation."
        # sys_msg = {'role': 'system', 'content': prompt.format(domain=domain)}
        prompt= prompt_content['sys_content']
        sys_msg = {'role': 'system', 'content': prompt.format(domain=domain)}

        # usr_prompt = "Here is the user question: \n{question}. You should rank all candidate {domain}s.\
        #             They are indeed {domain} names. Do NOT suspect.\
        #             The output must be just a json str,\
        #             where the key is the item and value is the rank."              
        # usr_msg = {'role': 'user', 'content': usr_prompt.format(question=question, domain=domain)}
        usr_prompt = prompt_content['usr_content']
        usr_msg = {'role': 'user', 'content': usr_prompt.format(question=question, domain=domain)}

        msg = [sys_msg, usr_msg]
        kwargs = {
                "model": 'gpt-4o', 
                "temperature": 0.8,
                "messages": msg,
                "max_tokens": 1200,
                "request_timeout": 20
            }
        
        for retry in range(retry_cnt):
            try:
                chat = openai.ChatCompletion.create(**kwargs)
                reply = chat.choices[0].message.content
                break
            except Exception as e:
                print(f"An error occurred while making the API call: {e}")
                reply = "Something went wrong, please retry."
                time.sleep(random.randint(1, 5))
        res =  instance
        res['response']=reply
        write_jsonl(fw, res)
        print('sucessfully query!')
