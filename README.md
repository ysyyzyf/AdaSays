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
  --ip IP, -i IP        when you set proxy for Terminal, and you want to makesure if you                       are submittng request with that IP
```
## 3.2. characters
characters/ada.json show the template, you can set the system type prompt there