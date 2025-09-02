"""Utility functions for Swiftora's backend.

This module contains helper routines used throughout the API:

* Image and filename heuristics to extract category/brand/model and other
  simple properties.
* Loading and filtering of comparison data from CSV fixtures.
* Copy generation from detected attributes and pricing information.

The heuristics implemented here are intentionally deterministic and
lightweight so that Demo Mode can run entirely offline.  They are not
intended to be accurate but rather to demonstrate the shape of a
production pipeline that might leverage more sophisticated models.
"""

from __future__ import annotations

import hashlib
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from PIL import Image
from rapidfuzz import fuzz


# A small mapping from common filename keywords to categories and brands
CATEGORY_KEYWORDS = {
    "phone": "smartphone",
    "iphone": "smartphone",
    "galaxy": "smartphone",
    "bag": "bag",
    "shoe": "shoes",
    "sneaker": "shoes",
    "airpods": "headphones",
    "headphone": "headphones",
    "camera": "camera",
    "keyboard": "keyboard",
    "laptop": "laptop",
}

BRAND_KEYWORDS = {
    "iphone": "Apple",
    "galaxy": "Samsung",
    "pixel": "Google",
    "nike": "Nike",
    "adidas": "Adidas",
    "sony": "Sony",
    "canon": "Canon",
    "nikon": "Nikon",
    "dell": "Dell",
    "lenovo": "Lenovo",
    "macbook": "Apple",
    "ipad": "Apple",
}


def detect_attributes(filename: str, image: Image.Image) -> Dict[str, object]:
    """Derive a pseudo‑set of product attributes from a filename and image.

    Args:
        filename: Name of the uploaded file (without path).
        image: PIL Image object opened from the uploaded bytes.

    Returns:
        A dictionary conforming to the `detected` schema in `UserJob`.
    """
    name = filename.lower()
    detected: Dict[str, object] = {
        "category": None,
        "brand": None,
        "model": None,
        "color": None,
        "size": None,
        "condition": None,
        "notable_features": [],
        "defects": [],
    }

    # Determine category and brand from keywords in filename
    for kw, category in CATEGORY_KEYWORDS.items():
        if kw in name:
            detected["category"] = category
            break

    for kw, brand in BRAND_KEYWORDS.items():
        if kw in name:
            detected["brand"] = brand
            # Use the remainder of the filename as model when possible
            parts = name.replace(kw, "").replace("_", " ").replace("-", " ").split()
            if parts:
                # Take the first non‑empty token as model
                detected["model"] = parts[0].upper()
            break

    # Compute dominant colour as the channel with the highest average value
    np_img = np.array(image.resize((50, 50)))  # downsample for speed
    avg = np.mean(np_img.reshape(-1, 3), axis=0)
    channels = {"red": avg[0], "green": avg[1], "blue": avg[2]}
    detected["color"] = max(channels, key=channels.get)

    # Size bucket by image dimensions
    w, h = image.size
    diag = (w ** 2 + h ** 2) ** 0.5
    if diag >= 2000:
        detected["size"] = "large"
    elif diag >= 1200:
        detected["size"] = "medium"
    else:
        detected["size"] = "small"

    # Deterministic condition based on filename hash
    conditions = ["new", "like new", "good", "fair", "poor"]
    hsh = int(hashlib.sha256(name.encode()).hexdigest(), 16)
    detected["condition"] = conditions[hsh % len(conditions)]

    # Notable features heuristics
    features: List[str] = []
    if detected.get("color"):
        features.append(f"Beautiful {detected['color']} finish")
    if detected.get("size"):
        features.append(f"{detected['size'].capitalize()} form factor")
    if detected.get("condition"):
        features.append(f"Condition: {detected['condition']}")
    detected["notable_features"] = features

    # Defects left empty for demo
    detected["defects"] = []

    return detected


def load_comps_csv(path: str) -> pd.DataFrame:
    """Load the comparison seed CSV into a pandas DataFrame.

    The CSV is expected to have the columns: source, url, price, currency,
    title, image, condition, shipping.
    """
    df = pd.read_csv(path)
    # Ensure price is numeric
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df.dropna(subset=["price"], inplace=True)
    return df


def filter_comps(df: pd.DataFrame, brand: Optional[str], model: Optional[str]) -> List[Dict[str, object]]:
    """Filter the comps DataFrame based on a brand and model.

    A fuzzy string matching approach is used to score the relevance of
    each row.  Items with the highest scores are returned first.

    Args:
        df: Loaded comps DataFrame
        brand: Brand string from detection
        model: Model string from detection

    Returns:
        A list of dicts (converted rows) sorted by descending relevance.
    """
    if brand is None and model is None:
        # No filter available – just return a sample of the data
        sample = df.sample(min(len(df), 10), random_state=42)
        return sample.to_dict(orient="records")

    def score_row(row: pd.Series) -> float:
        title = str(row["title"]).lower()
        score = 0.0
        if brand:
            score += fuzz.partial_ratio(brand.lower(), title)
        if model:
            score += fuzz.partial_ratio(model.lower(), title)
        return score

    df = df.copy()
    df["_score"] = df.apply(score_row, axis=1)
    df_sorted = df.sort_values(by="_score", ascending=False)
    return df_sorted.head(12).drop(columns=["_score"]).to_dict(orient="records")


def build_copy(brand: Optional[str], model: Optional[str], detected: Dict[str, object], price_band: Dict[str, float]) -> Dict[str, object]:
    """Construct a deterministic title and bullet points based on detections.

    Args:
        brand: Brand name or None
        model: Model name or None
        detected: Detected attributes dictionary
        price_band: Dictionary with keys low, mid, high, confidence

    Returns:
        A dictionary with `title` and `bullets` fields.
    """
    # Title: "Brand Model – Feature (Condition)"
    brand_part = brand or "Item"
    model_part = model or ""
    feature_part = detected.get("notable_features", ["Great item"])[0]
    condition_part = detected.get("condition", "good").title()
    title = f"{brand_part} {model_part} – {feature_part} ({condition_part})"

    # Bullets: summarise detected properties and price range
    bullets: List[str] = []
    if detected.get("color"):
        bullets.append(f"Color: {detected['color'].title()}")
    if detected.get("size"):
        bullets.append(f"Size: {detected['size']}")
    if detected.get("condition"):
        bullets.append(f"Condition: {condition_part}")
    bullets.append(
        f"Price range: ${price_band['low']:.2f}–${price_band['high']:.2f} (est. ${price_band['mid']:.2f})"
    )
    bullets.append("Ships quickly, carefully packaged")

    return {
        "title": title.strip(),
        "bullets": bullets[:5],
    }


def assemble_user_job(user_id: str, image_url: str, notes: Optional[str], detected: Dict[str, object], comps: List[Dict[str, object]], price_band: Dict[str, float], copy: Dict[str, object]) -> Dict[str, object]:
    """Assemble the final UserJob structure.

    A unique identifier is generated for each job.  The createdAt field is
    set to the current UTC time in ISO 8601 format.
    """
    job_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat() + "Z"

    return {
        "id": job_id,
        "userId": user_id,
        "imageUrl": image_url,
        "notes": notes,
        "detected": detected,
        "comps": comps,
        "suggestedPrice": price_band,
        "copy": copy,
        "createdAt": created_at,
    }