import pickle
from llama_index.llms import OpenAI
from llama_index import download_loader, GPTVectorStoreIndex, ServiceContext, KeywordTableIndex, StorageContext, load_index_from_storage
from llama_hub.github_repo import GithubClient, GithubRepositoryReader
import os
import markdown
import html2text
import mdv
import yaml
def load_file(filename):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
        return config
    
def parse_and_load(config):
    all_docs = []
    for repo_config in config['repos']:
        owner = repo_config['owner']
        repo = repo_config['repo']
        branch = repo_config['branch']
        filters = {
            "directories": (
                repo_config['filters']['directories']['value'],
                getattr(GithubRepositoryReader.FilterType, repo_config['filters']['directories']['type'])
            ),
            "file_extensions": (
                repo_config['filters']['file_extensions']['value'],
                getattr(GithubRepositoryReader.FilterType, repo_config['filters']['file_extensions']['type'])
            )
        }
        docs = load_repos2(branch, owner, repo, filters)
        all_docs.extend(docs)

    return all_docs

def load_repos2(branch,owner="istio", repo="istio.io", filters=None):
    docs = load_docs_if_exist(owner,repo)
    if docs is None:
        print(f"repo not cached, loading docs for {repo} from github")
        download_loader("GithubRepositoryReader")
        github_client = GithubClient(os.getenv("GITHUB_TOKEN"))
        
        # Default filters if none are provided
        if filters is None:
            filters = {
                "directories": (["content/en/docs"], GithubRepositoryReader.FilterType.INCLUDE),
                "file_extensions": ([".md"], GithubRepositoryReader.FilterType.INCLUDE)
            }
    
        loader = GithubRepositoryReader(
            github_client,
            owner=owner,
            repo=repo,
            filter_directories=filters["directories"],
            filter_file_extensions=filters["file_extensions"],
            verbose=False,
            concurrent_requests=10,
        )

        docs = loader.load_data(branch=branch)
        #Save docs to file
        with open(f"./storage/{owner}_{repo}_docs", 'wb') as file:
            pickle.dump(docs, file)
            print(f"saving docs for {repo} to file")

    return docs

def load_docs_if_exist(owner,repo):
    docs = None
    if os.path.exists(f"./storage/{owner}_{repo}_docs"):
        with open(f"./storage/{owner}_{repo}_docs", 'rb') as file:
            docs = pickle.load(file)
            print(f"loaded docs for {repo} from cache")
    return docs


def create_index(docs,model):
    print("checking for stored index")
    if os.path.exists("./storage/index"):
        print("using stored index")
        storage_context = StorageContext.from_defaults(persist_dir=f'./storage/index')
        index = load_index_from_storage(storage_context=storage_context)
        return index
    storage_context = StorageContext.from_defaults()
    llm = OpenAI(temperature=0.1, model=model)
    service_context = ServiceContext.from_defaults(llm=llm)
    index = GPTVectorStoreIndex.from_documents(docs,storage_context=storage_context,service_context=service_context)
    print("created new index")
    storage_context.persist(persist_dir=f'./storage/index')
    return index

def display_markdown(md_content):
    print(mdv.main(md_content, theme=970))

