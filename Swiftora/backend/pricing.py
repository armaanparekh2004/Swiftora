"""Pricing utilities for Swiftora.

This module implements a robust estimator for a price band based off a
collection of comparable prices.  The approach uses Tukey's fences to
trim outliers, then calculates the low (10th percentile), mid (median)
and high (90th percentile) of the remaining distribution.  A crude
confidence score is computed based on the relative width of the
interquartile range compared to the median.
"""

from __future__ import annotations

from typing import Iterable, Dict

import numpy as np


def calculate_price_band(prices: Iterable[float]) -> Dict[str, float]:
    """Compute a robust price band from a list of prices.

    Args:
        prices: An iterable of numerical price values.

    Returns:
        A dict with keys `low`, `mid`, `high` and `confidence`.  Values
        are floats.  If fewer than two prices are provided, the low,
        mid and high will all equal the single price and confidence
        will be low (0.2).
    """
    arr = np.array([p for p in prices if p is not None and not np.isnan(p)], dtype=float)
    if arr.size == 0:
        return {"low": 0.0, "mid": 0.0, "high": 0.0, "confidence": 0.0}
    if arr.size == 1:
        price = float(arr[0])
        return {"low": price, "mid": price, "high": price, "confidence": 0.2}

    # Tukey trimming: remove values outside 1.5 IQR
    q1, q3 = np.percentile(arr, [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    trimmed = arr[(arr >= lower_bound) & (arr <= upper_bound)]
    if trimmed.size == 0:
        trimmed = arr  # fallback if everything is trimmed

    low = float(np.percentile(trimmed, 10))
    mid = float(np.median(trimmed))
    high = float(np.percentile(trimmed, 90))

    # Confidence decreases as the spread widens relative to the median
    if mid == 0:
        confidence = 0.0
    else:
        spread = high - low
        confidence = max(0.0, min(1.0, 1 - (spread / max(mid, 1))))

    return {
        "low": round(low, 2),
        "mid": round(mid, 2),
        "high": round(high, 2),
        "confidence": round(confidence, 2),
    }