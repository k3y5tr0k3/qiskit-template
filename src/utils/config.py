"""Module that handles toml configuration."""

import tomllib
import pathlib


class Config:
    """Class that handles the retrieval of application configuration."""

    @staticmethod
    def __name_to_list(name):
        """Takes a string of words separated by periods, and returns a list of those words."""
        if not isinstance(name, str):
            raise TypeError("Input must be a string.")

        if not name:
            raise ValueError("Input string cannot be empty.")

        words = name.rstrip(".").split(".")
        if not words:
            raise ValueError(
                "Input string contains no words after removing trailing periods."
            )

        return words

    @staticmethod
    def __load_config():
        """Load the configuration file are return its dictionary representation."""
        config_path = pathlib.Path(__file__).parent / "../../config.toml"

        if config_path.exists():
            try:
                with open(config_path, "rb") as f:
                    return tomllib.load(f)

            except tomllib.TomlDecodeError as e:
                raise tomllib.TomlDecodeError(f"Error decoding config.toml: {e}")

        else:
            raise FileNotFoundError("Error: config.toml not found.")

    @staticmethod
    def get(name):
        """Retrieve and return a value from the configuration file."""
        words = Config.__name_to_list(name)
        config = Config.__load_config()

        try:
            for word in words:
                config = config[word]
        except KeyError:
            raise KeyError("The given name was not found in the config file.")

        if not isinstance(config, dict):
            return config
        else:
            raise ValueError("Incomplete name.")
