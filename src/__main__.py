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


def loadCollection(url):
    # Load repositories from collection
    repo_urls = pipeline.search_collections([url])
    # Save repositories
    with open(Config.get_dir_out() + "repos_" + url.replace('/', '_') + '.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json.dumps(repo_urls, indent=2))
    return repo_urls


def loadRepository(url, file_ending_whitelist):
    # Load single repository
    repos = pipeline.clone_repositories([url], file_ending_whitelist)


def loadRepositoriesFile(filename, file_ending_whitelist):
    # Git repositories
    with open(Config.get_dir_data() + 'repos.json', 'r', encoding='utf-8') as infile:
        repo_urls = json.loads(''.join(infile.readlines()))
    repos = pipeline.clone_repositories(repo_urls, file_ending_whitelist)


file_ending_white = {'json', 'md', 'js'}

# loadCollection('collections/front-end-javascript-frameworks')
# loadRepository('leonardomso/33-js-concepts', file_ending_white)
# loadRepositoriesFile('repos.json', file_ending_white)
