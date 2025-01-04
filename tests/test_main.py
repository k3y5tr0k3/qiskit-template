import pytest

from src.main import setup_test


def test_setup_test():
    result = setup_test() 

    assert result is not None
