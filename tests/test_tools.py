"""Checks for the restricted arithmetic tool."""

import pytest

from app.tools import safe_calculate


def test_calculator_arithmetic():
    """Percentages and grouping evaluate to the expected number."""
    assert safe_calculate("(18 / 100) * 2450") == 441


def test_calculator_power():
    """Exponentiation is allowed for small powers."""
    assert safe_calculate("2 ** 3") == 8


def test_calculator_rejects_code():
    """A function call disguised as math is refused."""
    with pytest.raises((ValueError, TypeError)):
        safe_calculate("__import__('os').system('echo unsafe')")
