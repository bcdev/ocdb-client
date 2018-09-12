import json
import os
from abc import ABCMeta, abstractmethod
from typing import Any, Dict

Config = Dict[str, Any]


class ConfigStore(metaclass=ABCMeta):
    @abstractmethod
    def read(self) -> Config:
        """
        Read a configuration.
        Returns a JSON-serializable configuration Python dictionary.
        """

    @abstractmethod
    def write(self, config: Config):
        """
        Write a configuration *conf*which is a JSON-serializable configuration Python dictionary.
        """


class MemConfigStore(ConfigStore):
    def __init__(self, **config):
        self._config = config

    def read(self) -> Config:
        return dict(self._config)

    def write(self, config: Config):
        self._config.update(config)


class JsonConfigStore(ConfigStore):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self) -> Config:
        if os.path.isfile(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return {}

    def write(self, config: Config):
        dir_path = os.path.dirname(self.file_path)
        if dir_path and not os.path.isdir(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        with open(self.file_path, 'w') as fp:
            json.dump(config, fp, indent=4)
