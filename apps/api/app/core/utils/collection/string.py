import re
from typing import Any

from .assertions import is_str

pattern = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')


def slugify(s: str) -> str:
  s = s.lower().strip()
  s = re.sub(r'[^\w\s-]', '', s)
  s = re.sub(r'[\s_-]+', '-', s)
  s = re.sub(r'^-+|-+$', '', s)
  return s


def snake_case(value: str) -> str:
    return pattern.sub(r'_\1', value.replace('-', '_')).lower()


def kebab_case(value: str) -> str:
    return pattern.sub(r'-\1', value.replace('_', '-')).lower()


def capitalize(value: str) -> str:
    def format_word(word: str):
        return word.upper() if len(word) == 1 else (word[0].upper() + word[1:].lower())
    words = value.split(' ')
    return ' '.join([format_word(word) for word in words])


def str_requires_formatting(text: str) -> str:
    return isinstance(text, str) and re.search(r"\{\w+\}", text) or '%' in text


def get_formatting_variables(text: str) -> str:
    """
    Returns a list of all formatting variables in a string.
    
    Args:
    -----
        text: The string to iterate over.

    Returns:
    --------
        List of formatting variables.

    Examples:
    ---------
    >>>string1 = "This is a string with {one} and {two} variables."
    >>>string2 = "Another string with just {one} variable."
    >>>string3 = "String with no %s variables."

    >>>print(get_formatting_variables(string1))
    ["one", "two"]
    >>>print(get_formatting_variables(string2))
    ["one"]
    >>>print(get_formatting_variables(string3))
    ["s"]
    """
    if isinstance(text, str):
        items = list(re.findall(r'(%\w|{[^}]*})', text))
        if len(items):
            return [item[1:] if item.startswith('%') else item[1:-1] for item in items]
    return []


def count_formatting_variables(text: str) -> str:
    """
    Counts the number of formatting variables in a string.
    
    Searches for all instances of the formatting variable patterns (like "{}", "{word}", and "%s") in the
    string and returns the number of matches.

    Args:
    -----
        text: The string to check.

    Returns:
    --------
        The number of formatting variables in the string.

    Examples:
    ---------
    >>>string1 = "This is a string with {one} and {two} variables."
    >>>string2 = "Another string with just {one} variable."
    >>>string3 = "String with no %s variables."

    >>>print(f"string1 has {count_formatting_variables(string1)} formatting variables.")
    "string1 has 2 formatting variables."
    >>>print(f"string2 has {count_formatting_variables(string2)} formatting variables.")
    "string2 has 1 formatting variables."
    >>>print(f"string3 has {count_formatting_variables(string3)} formatting variables.")
    "string3 has 1 formatting variables."
    """
    if isinstance(text, str):
        return len(re.findall(r'(%\w|{[^}]*})', text))
    return 0


def has_formatting_variables(text: str, *args, strict=True) -> bool:
    if not isinstance(text, str):
        return False
    hasvars = str_requires_formatting(text)
    if hasvars and len(args):
        results = [re.search(r"\{" + re.escape(arg) + r"\}", text) is not None for arg in args]
        return all(results) if strict else any(results)
    return hasvars


def is_blank(text: Any) -> bool:
    return bool(re.match(r"^(\s+)?$", text)) if is_str(text) else False
