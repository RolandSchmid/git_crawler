import json
import os

from Config import Config
from repo.Repository import Repository


class JsonTools:

    @staticmethod
    def save_repository(repository):
        return json.dumps(repository.__dict__)

    @staticmethod
    def save_repositories(repositories):
        with open(Config.get_dir_out() + 'repos.json', 'w', encoding='utf-8') as outfile:
            outfile.write(json.dumps(repositories, indent=2))

    @staticmethod
    def read_repositories():
        repos = []
        for file in os.listdir(Config.get_dir_repos()):
            filename = os.path.join(Config.get_dir_repos(), file)
            if filename.endswith('.json'):
                with open(filename) as infile:
                    data = ''.join(infile.readlines())
                r = Repository(None, None, None)
                r.__dict__ = json.loads(data)
                repos.append(r)
        return repos
