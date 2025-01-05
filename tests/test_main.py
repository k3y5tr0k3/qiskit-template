"""Tests code from the src.main module."""

import pytest

from src.main import setup_test


pytest.__version__


def test_setup_test__success():
    """A placeholder test that tests the project configuration test function."""
    result = setup_test()

    assert result is not None
