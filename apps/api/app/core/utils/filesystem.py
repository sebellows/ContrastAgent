import json
import os
from collections.abc import Callable
from typing import Any

from ..exceptions.job_exceptions import ExceptionInRunner
from .collection import is_async

def write_to_file(path: str, data: Any = None):
    """
    Ensures that all directories in a nested path exist.
    If the final part of the path is a file, it checks for its existence but does not create it.

    Args:
        path (str): The full nested path to check and create if necessary.

    Example:

    nested_path = "/home/user/folder/sub/folder/file.txt"
    ensure_nested_path_exists(nested_path)
    """
    # Split the path into head (directory) and tail (file or directory)
    # Example:
    # os.path.split('/home/user/folder/sub/folder/file.txt')
    # => '/home/user/folder/sub/folder', 'file.txt'
    head, tail = os.path.split(path)

    if '.' not in tail:
        # If there is no file extension, '.txt' is appended as a backup
        tail += '.txt'

    # Ensure the directory part exists
    if not os.path.exists(head):
        os.makedirs(head)

    full_path = os.path.join(head, tail)
    with open(full_path, 'w', encoding = 'utf-8') as file:
        json.dump(data, file)

FILE_NOT_FOUND_ERROR_MESSAGE = 'File at path "{file_path}" does not exist.'

def get_file_data(file_path, ignore_error=False):
    if os.path.exists(file_path):
        with open(file_path) as file:
            return json.loads(file.read())
    else:
        if not ignore_error:
            print(FILE_NOT_FOUND_ERROR_MESSAGE.format(file_path=file_path))
        raise FileNotFoundError(FILE_NOT_FOUND_ERROR_MESSAGE.format(file_path=file_path))


async def exec_callback(cb, *args):
    try:
        if is_async(cb):
            print('exec_callback async')
            results = await cb(*args) if len(args) else await cb()
        else:
            results = cb(*args) if len(args) else cb()
        return results
    except TypeError as e:
        raise TypeError(f'Callback must be callable or async callable. {e}')
    except Exception as e:
        raise e


async def resolve_file_data(
    file_path,
    resolver: Callable | None = None,
    before_write = None,
    after_write = None,
    override = False,
    ignore_error = True
):
    try:
        data = get_file_data(file_path, ignore_error=ignore_error)

        if override or data is None:
            data = await exec_callback(resolver)

            if data is None:
                raise ExceptionInRunner()

            if before_write:
                await exec_callback(before_write, data)

            write_to_file(file_path, data)

            if after_write:
                await exec_callback(after_write, data)

        return data
    except Exception as e:
        print(f'Error resolving file at file path "{file_path}" - {e}')
        raise e
