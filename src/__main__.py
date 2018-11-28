import json
import logging

from Config import Config
from concurrency.Pipeline import Pipeline
from concurrency.workers.WorkerFile import WorkerFile
from spiders.GitHubSpider import GitHubSpider
from tools.Logger import init_main

# Logging
logger = init_main()
logger.setLevel(logging.DEBUG)

# Pipeline
pipeline = Pipeline(GitHubSpider, Config.get_n_git_threads(), Config.get_n_file_threads(), WorkerFile)


def pull_collection(url):
    # Load repositories from collection
    repo_urls = pipeline.search_collections([url])
    # Save repositories
    with open(Config.get_dir_out() + "repos_" + url.replace('/', '_') + '.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json.dumps(repo_urls, indent=2))
    return repo_urls


def pull_repository(url, file_ending_whitelist):
    # Load single repository
    return pipeline.clone_repositories([url], file_ending_whitelist)


def pull_repositories(filename, file_ending_whitelist):
    # Git repositories
    with open(Config.get_dir_data() + filename, 'r', encoding='utf-8') as infile:
        repo_urls = json.loads(''.join(infile.readlines()))
    return pipeline.clone_repositories(repo_urls, file_ending_whitelist)


file_ending_white = {'json', 'md', 'js'}

# pull_collection('collections/front-end-javascript-frameworks')
# pull_repository('leonardomso/33-js-concepts', file_ending_white)
# pull_repositories('repos.json', file_ending_white)
