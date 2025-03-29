# standard
from pathlib import Path
from typing import TYPE_CHECKING, Any

# packages
from injector import inject

# local
from app.core.utils.collection.path import to_dirpath
from app.core.utils.filesystem import get_file_data, resolve_file_data, write_to_file


if TYPE_CHECKING:
    from . import IAppConfig, IAppState
    # from core.models.app_config import AppConfigABC as AppConfig
    # from core.models.app_state import AppStateABC as AppState


class FilesystemProvider:
    _config: IAppConfig
    _state: IAppState

    @inject
    def __init__(self, config: IAppConfig, state: IAppState):
        self._config = config
        self._state = state

    @property
    def config(self):
        return self._config

    @property
    def state(self):
        return self._state

    @property
    def outdir(self):
        return self.config.get('fs.outdir')

    @property
    def filenames(self):
        return self.config.get('fs.filenames')
    
    def exists(self, filepath: str) -> bool:
        return Path(filepath).is_file()

    def get_file_path(
        self,
        vendor: str,
        product_line_name: str,
        content_type: str = '',
        outdir: str | None = None
    ) -> str:
        if not outdir:
            outdir = self.outdir
        locale = '_'.join(self.state.locale.split('-'))
        lang_code = self.state.language
        prefix = vendor 
        suffix = self.filenames.get(content_type, content_type)
        paths = [outdir]
        if suffix:
            suffix = suffix.format(language_code=lang_code, locale=locale)
        filename = '-'.join([prefix, product_line_name, suffix]).lower()
        paths.append(filename)
        return to_dirpath(paths)

    def read(self, filepath: str, throw_on_error = True, default: Any = None) -> Any:
        try:
            if self.exists(filepath):
                return get_file_data(filepath)
            if throw_on_error:
                raise FileNotFoundError(f'File at filepath "{filepath}" does not exist.')
        except FileNotFoundError as fexc:
            print(fexc)
        except Exception as exc:
            print(f'FilesystemProvider Error: Cannot read file path: "{filepath}" - {type(exc)} {exc}')
        return default

    def write(self, filepath: str, data: Any):
        try:
            write_to_file(filepath, data)
        except FileExistsError as ferr:
            print(f'FilesystemProvider Error: You do not have permission to access this file: {ferr}')
        except NotADirectoryError as derr:
            print(f'FilesystemProvider Error: You do not have permission to access this file: {derr}')
        except OSError as e:
            print(f'FilesystemProvider Error: A system-related error occurred: {e}')
        except Exception as exc:
            print(f'FilesystemProvider Error: Encounted an exception: {exc}')

    def resolve(self, filepath: str, **kwargs):
        try:
            return resolve_file_data(filepath, **kwargs)
        except Exception as exc:
            print(f'FilesystemProvider Error: Cannot resolve file path: "{filepath}" - {type(exc)} {exc}')
