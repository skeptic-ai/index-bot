import pickle
import os

from util import  parse_and_load
from llama_index.llms import OpenAI
from llama_index import  GPTVectorStoreIndex, ServiceContext, KeywordTableIndex, StorageContext, load_index_from_storage
from IPython.display import display, Markdown
storage_context = None
index = None
# print("checking for stored index")
# if os.path.exists("./storage/index"):
#     storage_context = StorageContext.from_defaults(persist_dir=f'./storage/index')
#     index = load_index_from_storage(storage_context=storage_context)
#     print("use stored index")

# if index is None:
docs = parse_and_load("repos.yaml")
storage_context = StorageContext.from_defaults()
index = GPTVectorStoreIndex.from_documents(docs,storage_context=storage_context)
print("created new index")
storage_context.persist(persist_dir=f'./storage/index')
# llm = OpenAI(temperature=0.1, model="gpt-4")
# service_context = ServiceContext.from_defaults(llm=llm)
# index = KeywordTableIndex.from_documents(docs,service_context=service_context)
print("done creating index")
chat_engine = index.as_chat_engine()


while True:
    text_input = input("User: ")
    response = chat_engine.chat(text_input)
    display(Markdown(f"Bot: {response}"))

# query_engine = index.as_query_engine()


# response = query_engine.query("what version of istio is supported with envoy 1.27, reply with a semver only")
# print(response)
# assert str(response) == "1.19.x"
# response = query_engine.query("what versions of istio are supported with kubernetes 1.22, reply with a json array of semver only")
# print(response)