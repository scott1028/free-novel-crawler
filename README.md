## Prerequisite

```
sudo apt-get install libxslt-dev python3-dev
```

## Usage

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

- Load local file named ends with `*.txt` and skip file named starts with `done-*`.

```
./txtUtils.py
```

## Plan

- Refactor previous implementation with class base.
- Refactor `lib/*`

## Troubleshooting

- pip._vendor.urllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool(host='files.pythonhosted.org', port=443): Read timed out.

```
export PIP_DEFAULT_TIMEOUT=100
```

