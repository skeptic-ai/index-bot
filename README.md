# index-bot

Simple python script to easily configure and run custom index with a chatgpt chatbot using only a yaml file. Supports github repos only right now. 

## Setup

You will need python 3.10+ and to set GITHUB_TOKEN and a OPENAI_API_KEY in your environment variables to run the python notebook. 

`pip3 install -r requirements.txt` to grab the dependencies. 

## Running

- configure your repo list in the repos.yaml file. 
- `mkdir storage` and then
- `python index-bot 0T90 M 65 9065MM 90M65Y T.py`

## Cache

The repos documents and a GPT index are stored locally in the storage directory to speed startup time of the chatbot. If you want to refresh the index run `rm -rf ./storage/*` and restart the bot. 

## Repo yaml

Specify a yaml list of repos with their owner, the branch, and the file types and directories to include. 

```yaml
  - owner: istio
    repo: istio.io
    branch: master
    filters:
      directories:
        value: ["content/en/docs"]
        type: INCLUDE
      file_extensions:
        value: [".md"]
        type: INCLUDE
```

test