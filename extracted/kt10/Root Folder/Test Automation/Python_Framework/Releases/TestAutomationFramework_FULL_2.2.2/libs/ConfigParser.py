"""
This library manage parsing of configurations from txt file to dictionaries

Changelog

[1.7.0] - 2024-03-15
- code review

[1.6.0] - 2024-01-23

- Update only for tag

[1.5.0] - 2023-11-15
- Update only for tag

1.0 2022-01-31
"""

__version__ = '2.2.2'
__author__ = 'Intelligentia SRL & Juan Pablo Perruzza'


class ConfigParser:
    _configs = {}


    def __init__(self, config_file_path: str) -> None:
        """
        SW spec :	NA\n
        parameter : self  class instance\n
        parameter : config_file_path: path to config's file to parse[String]\n
        return values: none\n
        description :Initialize the parser\n
        remarks: none\n
		"""
        with open(config_file_path, 'r') as f:
            for line in f:
                current = line.strip()

                if current:
                    if current[0] == "@":
                        current_index = current[1:]
                        self._configs[current_index] = {}
                    else:
                        key, value = current.split(":")
                        if value[0] == "\"":
                            self._configs[current_index][key] = value.strip("\"")
                        else:
                            self._configs[current_index][key] = int(value)


    def get_configuration(self, configuration: str) -> dict:
        """
		SW spec :	NA\n
        parameter : self  class instance\n
        parameter : configuration: path to config's file to parse[String]\n
        return values: required configuration\n
        description :Get specific configuration\n
        remarks: none\n
		"""

        if self._configs.get(configuration) is not None:
            return self._configs[configuration]
        else:
            raise Exception("Configuration's name not found")
