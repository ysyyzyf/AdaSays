# 1. AdaSays
A very simple ChatBot based on ChatGPT
# 2. required python pkgs
## 2.1. tiktoken
for caculating message's tokens will be used, refer to https://github.com/openai/tiktoken
# 3. command
## 3.1. for help
```shell
> python3.11 ada -h
usage: ada [-h] --character CHARACTER [--mode MODE] [--key KEY] --ip IP

options:
  -h, --help            show this help message and exit
  --character CHARACTER, -c CHARACTER
                        choose the character
  --mode MODE, -m MODE  choose the mode: 'onetime' for don't remember chat
  --key KEY, -k KEY     set the file path which stored the ChatGPT's api-key
  --ip IP, -i IP        when you set proxy for Terminal, and you want to makesure if you
                        are submittng request with that IP
```
### 3.1.1. characters
characters/ada.json show the template, you can set the `system prompt` there, which can told ChatGPT who should it be.
### 3.1.2. mode
with mode of "onetime", every time, your chat is new, with no chat history sent (but the `system prompt` is sent every time)
### 3.1.3 key
touch a file to store the ChatGPT's api-key, and specify its path with this
### 3.1.4 ip
if you are using proxy to access, you may need to check if you do using the `proxy-ip` to submit requests, use this to specify it, like `-i "111.123.11.22"`, every time you start this script, it will check if the proxy is activated at the beginning.