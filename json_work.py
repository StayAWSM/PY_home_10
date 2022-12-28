'''
{
    123: {1: 1+1, 2: 1+2, ... }


    124:{1: 1+1, 2: 1+2, ... }
}
'''
import json
def add_history(chat_id: str, text:str, my_dikt: dict):
    for i in range(1, 5):
        my_dikt[chat_id][str(i)] = my_dikt[chat_id][str(i + 1)]
    my_dikt[chat_id]["5"] = text
    return my_dikt

def write(chat_id: int, text:str, user: str):
    chat_id = str(chat_id)
    flag = True
    with open("my_json.json", 'r') as file:
        my_dikt = json.load(file)
    if chat_id in my_dikt:
        flag = False
        my_dikt = add_history(chat_id, text, my_dikt)
    if flag:
        temo_dikt = {1: "", 2: "", 3: "", 4: "", 5: text, "user": user}
        my_dikt[chat_id] = temo_dikt

    with open("my_json.json", 'w') as file:
        json.dump(my_dikt, file, indent=4)

def read(chat_id: int):
    chat_id = str(chat_id)
    with open("my_json.json", 'r') as file:
        my_dikt = json.load(file)
    res_list = []
    if chat_id in my_dikt:
        for k, v in my_dikt[chat_id].items():
            if v != '':
                res_list.append(v)
        res_list.pop()
        return res_list
