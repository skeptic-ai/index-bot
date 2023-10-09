import pickle
import os
import sys

from util import  create_index, display_markdown, load_file, parse_and_load
from llama_index.llms import OpenAI
from llama_index import  GPTVectorStoreIndex, ServiceContext, KeywordTableIndex, StorageContext, load_index_from_storage
from IPython.display import display, Markdown
storage_context = None
index = None


# check for config filename argument and default to "./config.yaml" if not provided
config_filename = sys.argv[1] if len(sys.argv) > 1 else "./config.yaml"
config = load_file(config_filename)
docs = parse_and_load(config)
index = create_index(docs, config["model"])




# index = KeywordTableIndex.from_documents(docs,service_context=service_context)
print("done creating index")


query_engine = index.as_query_engine()
while True:
    text_input = input("User: ")
    response = query_engine.query(text_input)
    display_markdown(f"Bot: {response}")

# response = query_engine.query("what version of istio is supported with envoy 1.27, reply with a semver only")
# print(response)
# assert str(response) == "1.19.x"
# response = query_engine.query("what versions of istio are supported with kubernetes 1.22, reply with a json array of semver only")
# print(response)