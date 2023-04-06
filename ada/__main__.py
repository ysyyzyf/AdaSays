import os
import openai
import requests
import string
import argparse
import json
import tiktoken
import re

def parse_key(key_file):
    keys = []
    f = open(key_file, 'r')
    lines = f.readlines()
    for line in lines:
        keys.append(line.strip())
    if len(keys) > 0:
        return keys
    else:
        exit("invalid key")

def loadMsg(msgLoc):
    msgR = open(msgLoc, 'r', encoding='utf-8')
    msg = json.load(msgR)
    if len(msg) > 0:
        #delete prompt, if there is
        del msg[0]
    #print(msg)
    return msg

def parseCharacter(character):
    cLoc = f"./characters/{character}.json"
    cW = open(cLoc, 'r', encoding='utf-8')
    c = json.load(cW)
    print(f"Name: {c['name']}")
    print(f"Introduction: {c['intro']}")
    return c['prompt']

def gateMsg(msgs):
    #print(msgs)
    while num_tokens_from_messages(msgs) > 1500:
        del msgs[1]
    print(f"Tokens of the next request: {num_tokens_from_messages(msgs)}")
    return msgs

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

def initChat(msgRequest):
    Ada="Hello, Ada"
    msgs = []
    msgs.append(Ada)
    for initMsg in msgs:
        msgRequest.append({"role": "user", "content": initMsg})
        completion = openai.ChatCompletion.create(
          model="gpt-3.5-turbo-0301",
          messages = msgRequest
        )
        msg = completion.choices[0].message
        msgRequest.append({"role":"assistant", "content":msg.content})
        msgZh = str(msg.content.encode("utf-8"), 'utf-8') 
        print(msgZh)
    return msgRequest

def chat(mode = "gpt-3.5-turbo-0301", msgLoc = "", prompt = "", ct="onetime"):
    keep_chat = ""
    prefix = ""
    print("[Notice] Input 'exit' to stop chating")
    msgRequest = []
    msgSave = []
    #load prompt to set character
    msgRequest.append({"role": "system", "content": prompt})
    #msgRequest = initChat(msgRequest)
    #load chat history
    msgHistory = loadMsg(msgLoc)
    if ct != "onetime":
        msgRequest = msgRequest + msgHistory
    msgSave = msgRequest + msgHistory
    while keep_chat != "exit":
        keep_chat = input("You: ")
        if keep_chat == "exit":
            msgSaveW = open(msgLoc, 'w')
            json.dump(msgSave, msgSaveW)
            exit("See you later :)")
        #merge new msg in
        if ct == "onetime":
            del msgRequest[1:]
        if re.match(r'np:', keep_chat):
            msgRequest.append({"role": "user", "content": keep_chat})
        else:
            msgRequest.append({"role": "user", "content": prefix+keep_chat})
        msgSave.append({"role": "user", "content": keep_chat})
        #gate msg len
        if ct != "onetime":
            msgRequest = gateMsg(msgRequest)
        for msg in msgRequest:
            print(msg)
        #send request to chatGPT
        completion = openai.ChatCompletion.create(
          model=mode,
          messages = msgRequest
        )
        #parse response from chatGPT
        msg = completion.choices[0].message
        if ct != "onetime":
            msgRequest.append({"role":"assistant", "content":msg.content})
        msgSave.append({"role":"assistant", "content":msg.content})
        msgZh = str(msg.content.encode("utf-8"), 'utf-8') 
        print(msgZh)

def accessGate(exp_ip):
    ip = requests.get("https://ifconfig.me/ip", timeout=300).text.strip()
    print(ip)
    if ip != exp_ip:
        exit(f"Invalid ip: {ip}")
    else:
        print(f"IP check pass: {ip}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--character', '-c', action = 'store', default = "ada", \
            required = True, help = "choose the character")
    parser.add_argument('--mode', '-m', action = 'store', default = "onetime", \
            help = "choose the mode: 'onetime' for don't remember chat")
    parser.add_argument('--key', '-k', action = 'store', default = "m.key", \
            help = "set the file path which stored the ChatGPT's api-key")
    parser.add_argument('--ip', '-i', action = 'store', default = "localhost", \
            required = True, help = "when you set proxy for Terminal, \
                and you want to makesure if you are submittng request with that IP")
    args = parser.parse_args()
    initPrompt = parseCharacter(args.character)
    print("Check if your ip is legal ...")
    accessGate(args.ip)
    print("Welcome to Chat :)")
    keys = parse_key(args.key)
    openai.api_key = keys[0]
    chat(msgLoc=f"./history/{args.character}_chat.json", prompt=initPrompt, ct=args.mode)