"""Test custom logging module."""

import pytest

from src.utils.logging import Logging


pytest.__version__


class Test_Logging:
    """Test custom logging class."""

    def test_get_logger():
        """Tests get_logger method. Simply checks that None is not returned."""
        logger = Logging.get_logger()

        assert logger is not None
