import pandas as pd

from swiftora.backend.utils import filter_comps


def test_filter_comps_returns_relevant_rows():
    data = {
        "source": ["seed"] * 4,
        "url": ["#"] * 4,
        "price": [500, 700, 450, 100],
        "currency": ["USD"] * 4,
        "title": [
            "Apple iPhone 12 128GB Blue",
            "Samsung Galaxy S21 256GB",
            "Apple iPhone 11 64GB",
            "Nike Air Force 1 Sneakers",
        ],
        "image": [None] * 4,
        "condition": ["good"] * 4,
        "shipping": [None] * 4,
    }
    df = pd.DataFrame(data)
    results = filter_comps(df, brand="Apple", model="IPHONE 12")
    # The first result should be the iPhone 12 listing
    assert results[0]["title"].lower().startswith("apple iphone 12")
    # Should return at most 4 results here
    assert len(results) == 4