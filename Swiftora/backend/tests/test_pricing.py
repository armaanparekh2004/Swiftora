import pytest

from swiftora.backend.pricing import calculate_price_band


def test_calculate_price_band_typical_case():
    prices = [10, 12, 14, 15, 100]
    band = calculate_price_band(prices)
    # Outlier 100 should be trimmed away by Tukey's fences
    assert band["low"] == pytest.approx(10.0)
    assert band["mid"] == pytest.approx(13.0)
    assert band["high"] == pytest.approx(15.0)
    # Confidence should be between 0 and 1
    assert 0.0 <= band["confidence"] <= 1.0


def test_calculate_price_band_single_value():
    prices = [50]
    band = calculate_price_band(prices)
    assert band["low"] == 50
    assert band["mid"] == 50
    assert band["high"] == 50
    assert band["confidence"] == 0.2


def test_calculate_price_band_no_values():
    band = calculate_price_band([])
    assert band["low"] == 0
    assert band["mid"] == 0
    assert band["high"] == 0
    assert band["confidence"] == 0