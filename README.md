## Prerequisite

```
sudo apt-get install libxslt-dev python3-dev
```

## Usage

- Use Python3
- To remove `done-` prefix.(-maxdepth 1: no search sub-directory)
- File Name with space become wrap.
- Ref: http://askubuntu.com/questions/343727/filenames-with-spaces-breaking-for-loop-find-command
- Ref: http://stackoverflow.com/questions/8759285/alternatives-to-xargs-l

```
find . -maxdepth 1 -name "done-*" | while read i; do mv "$i" "`echo "\"$i\"" | sed \"s/done-//g\"`"; done
```

- Fetch without proxy

```
./miaoshuwuDownloader.py
```

- Fetch with proxy
```
PROXY=true ./miaoshuwuDownloader.py
```

- Switch HTML Parser Mode using `TXTMODE`

```
TXTMODE=6 ./txtUtils.py
```

## Troubleshooting

- pip._vendor.urllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool(host='files.pythonhosted.org', port=443): Read timed out.

```
export PIP_DEFAULT_TIMEOUT=100
```
