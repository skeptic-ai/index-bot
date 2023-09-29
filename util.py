import pickle
from llama_index.llms import OpenAI
from llama_index import download_loader, GPTVectorStoreIndex, ServiceContext, KeywordTableIndex

from llama_hub.github_repo import GithubClient, GithubRepositoryReader
import os

import yaml

def parse_and_load(yaml_file_path):
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)

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


