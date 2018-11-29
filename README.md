# git_crawler

## Dependencies

* tqdm
* GitPython
* beautifulsoup4
* requests
* fake-useragent
* configparser

## Git Config

To be able to parse git repositories with file names longer than 260 characters on Windows, the following setting has to be applied:

```git config --system core.longpaths true```
