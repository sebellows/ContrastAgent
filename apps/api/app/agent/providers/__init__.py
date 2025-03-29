from typing import NewType

from .app_config import AppConfig
from .app_state import AppState
from .filesystem_provider import FilesystemProvider

FS = NewType('FS', FilesystemProvider)
IAppConfig = NewType('IAppConfig', AppConfig)
IAppState = NewType('IAppState', AppState)

__all__ = (
    'AppConfig',
    'IAppConfig',
    'AppState',
    'IAppState',
    'FilesystemProvider',
    'FS',
)