traditional={
    'sys_content': "You are a helpful conversational agent who is good at recommendation.",
    'usr_content': "Here is the user question: \n{question}. You should rank all candidate {domain}s.\
                    They are indeed {domain} names. Do NOT suspect.\
                    The output must be just a json str,\
                    where the key is the item and value is the rank."  
}


insert_cot = "\n You should follow the following thinking steps:\
                Step1: Extract the customers' played and enjoyed games from the given query.\n\
                Step2: Use only one sentence to summarize their what these games have in common, and explain why customers prefer them.\n\
                Step3: Extract the game recommendations candidates provided by custom from the given query.\n\
                Step4: Considering the rationales of the customer's game preference. You should rank all candidate {domain}s.\n \
                "

break_down={
    'sys_content': "You are a helpful conversational agent who is good at recommendation.",
    'usr_content': "Here is the user question: \n{question}. " + insert_cot +
                    "They are indeed {domain} names. Do NOT suspect.\
                    The output must be just a json str,\
                    where the key is the item and value is the rank."  
}

break_down_with_rationale={
    'sys_content': "You are a helpful conversational agent who is good at recommendation.",
    'usr_content': "Here is the user question: \n{question}. " + insert_cot +
                    "They are indeed {domain} names. Do NOT suspect.\
                    You can write down your thinking process, but the final \
                    output must be just a json str,\
                    where the key is the item and value is the rank."  
}