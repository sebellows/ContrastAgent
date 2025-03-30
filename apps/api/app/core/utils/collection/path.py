# standard
import re

from .set import default_customizer
from .variadic import variadic


# Matches on path strings like "[<int>]". This is used to
# test whether a path string part is a list index.
INDEX_KEY_RE = re.compile(r"^\[-?\d+\]$")


def parse_key(key: int | str) -> int | str:
    if isinstance(key, int):
        return key
    return int(key[1:-1]) if INDEX_KEY_RE.match(key) else key


def parse_keys(keys: list[str], sep=".") -> list[str]:
    def _parse(key: str):
        if sep in key:
            return [parse_key(k) for k in key.split(sep)]
        return parse_key(key)

    results = [_parse(key) for key in keys]
    return variadic(*results)


def to_path(*paths, sep=".", customizer=default_customizer):
    return sep.join([customizer(path) for path in variadic(paths)])


def to_paths(*args, sep=".") -> list[str]:
    keys = [arg for arg in variadic(*args) if arg is not None]
    return parse_keys(keys, sep=sep)


def unslash(path: str) -> str:
    return (
        path[1:]
        if path.startswith("/")
        else path[:-1]
        if path.endswith("/") and not path.endswith("//")
        else path
    )


def to_dirpath(*paths: list[str]) -> str:
    if len(paths) == 0:
        return ""
    return to_path(*paths, sep="/", customizer=unslash)


def to_url(*paths: list[str]) -> str:
    path = to_path(*paths, sep="/", customizer=unslash)
    return path if path.startswith("http") else f"https://{path}"


def isurl(value: str) -> bool:
    return isinstance(value, str) and value.startswith("http")


def sanitize_path(path: str) -> str:
    return path.strip("/").replace("/", "_")
