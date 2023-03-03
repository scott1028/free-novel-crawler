## Prerequisite

```
sudo apt-get install libxslt-dev python3-dev
```

## Usage

```
./miaoshuwuDownloader.py
  ... or
./8wenkuDownloader.py  
```

- Load local file named ends with `*.txt` and skip file named starts with `done-*`.

```
./txtUtils.py
```

## Troubleshooting

- pip._vendor.urllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool(host='files.pythonhosted.org', port=443): Read timed out.

```
export PIP_DEFAULT_TIMEOUT=100
```

## Lint & format & git hook

```
$ pre-commit install
```
