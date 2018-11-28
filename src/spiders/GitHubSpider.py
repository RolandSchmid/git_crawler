import traceback

from bs4 import BeautifulSoup

from repo.Repository import Repository
from spiders.AbstractSpider import AbstractSpider
from tools.Logger import init_main

logger = init_main()


class GitHubSpider(AbstractSpider):

    def __init__(self, main_url='https://github.com/'):
        super().__init__(main_url)

    def process_collection(self, url):
        try:
            source = self.reader.get_html(self.main_url + url)
            soup = BeautifulSoup(source, 'html.parser')
            # TODO This has already changed, may change in the future
            anchors = soup.find_all('a', {'data-ga-click': 'Repository, go to repository'}, href=True)
            anchors = [a['href'] for a in anchors]
            # Remove prefix /
            anchors = [a[1:] if a.startswith('/') else a for a in anchors]
            return anchors
        except Exception as e:
            logger.error('Process collection error: %s %s' % (url, str(e)))
        logger.error(traceback.format_exc())
        return set()

    def process_repository(self, suffix):
        url = self.main_url + suffix
        try:
            source = self.reader.get_html(url, retry=True)
            soup = BeautifulSoup(source, 'html.parser')

            commit_tease = soup.find('a', {'class': 'commit-tease-sha'})
            if commit_tease:
                latest_commit = commit_tease['href']
            else:
                latest_commit = soup.find('include-fragment', {'class': 'commit-tease'})['src']
            latest_commit = latest_commit.split('/')[-1]

            topics = soup.find_all('a', {'class': 'topic-tag'})
            topics = [topic.string.replace('\n', '').replace(' ', '') for topic in topics]

            return Repository(suffix, latest_commit, topics)

        except Exception as e:
            logger.error('Process article error: %s %s' % (url, str(e)))
            # logger.error(traceback.format_exc())
        return None
