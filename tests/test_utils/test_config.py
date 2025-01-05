"""Tests for the config utility module."""

import pytest

from src.utils.config import Config


pytest.__version__


class TestConfig:
    """Test Config class."""

    def test_get__success(self):
        """Test that a value can be successfully retrieved from config.toml."""
        name = "logging.level"
        expected_value = "INFO"

        actual_value = Config.get(name)

        assert actual_value == expected_value

    def test_name_to_list__success(self):
        """Test that a config name is successfully converted to a list of words."""
        name = "one.two.three"
        expected_value = ["one", "two", "three"]

        actual_value = Config._Config__name_to_list(name)

        assert actual_value == expected_value

    def test_load_config__success(self):
        """Test that the config file can be opened, parsed and returned successfully."""
        config = Config._Config__load_config()

        assert config is not None
