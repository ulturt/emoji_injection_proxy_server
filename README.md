# Emoji injection proxy-server (test task)

## Dependencies
The main dependency is [proxy.py](https://github.com/abhinavsingh/proxy.py).

To install dependencies and virtual environment use [poetry](https://python-poetry.org/):
```bash
poetry install
poetry shell
```

## Usage

You can define an emoji list using a file with emoji on each line ([emoji codes](https://www.webfx.com/tools/emoji-cheat-sheet/)). Example:
```
:alien:
:older_man:
...
```
Use env variable EMOJI_LIST_FILE to define the absolute path to your file:
```bash
export EMOJI_LIST_FILE=/path/to/file
```
If you don't define an emoji list, then the default emoji list will be used.

To start proxy-server execute:
```bash
proxy --hostname 0.0.0.0 --plugins emoji_injection_proxy.plugin.EmojiInjectionPlugin
```
> If the plugin isn't loaded, use [this instruction](https://github.com/abhinavsingh/proxy.py#unable-to-load-plugins) to fix it.

Verify the emoji injection proxy-server using curl:
```bash
curl -v -x localhost:8899 http://httpbin.org/html
```
