"""Main entry point for the Swiftora backend.

This file defines a FastAPI application that exposes three endpoints:

* `GET /healthz` – health check returning a static OK status.
* `GET /comps` – returns comparable listings from local fixtures filtered
  by optional query parameters.
* `POST /analyze` – accepts an image upload and optional notes and
  returns a complete `UserJob` JSON document.  When demo mode is
  disabled (Live Mode) it will return a placeholder response.

At startup the backend loads comparison seed data into memory.  The
behaviour of the API is governed by the `DEMO_MODE` environment
variable loaded via `config.Settings`.
"""

import io
import logging
import os
import uuid
from typing import Optional

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image

from .config import get_settings
from .utils import (
    detect_attributes,
    load_comps_csv,
    filter_comps,
    build_copy,
    assemble_user_job,
)
from .pricing import calculate_price_band


logger = logging.getLogger(__name__)

# Create the FastAPI app
app = FastAPI(title="Swiftora Backend", version="0.0.1")

# Allow requests from the local iOS app during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup_event() -> None:
    """Load fixtures and configure the application state."""
    settings = get_settings()
    comps_path = os.path.join(os.path.dirname(__file__), "fixtures", "comps_seed.csv")
    if not os.path.exists(comps_path):
        logger.warning("Comparison seed data not found at %s", comps_path)
        app.state.comps_df = None
    else:
        app.state.comps_df = load_comps_csv(comps_path)
        logger.info("Loaded %d comparison rows", len(app.state.comps_df))
    app.state.settings = settings


class AnalyzeResponse(BaseModel):
    id: str
    userId: str
    imageUrl: str
    notes: Optional[str]
    detected: dict
    comps: list
    suggestedPrice: dict
    copy: dict
    createdAt: str


@app.get("/healthz")
async def healthz() -> dict:
    """Simple health check endpoint."""
    return {"status": "OK"}


@app.get("/comps")
async def get_comps(q: Optional[str] = None) -> list:
    """Return comparison listings filtered by an optional query.

    The optional `q` parameter allows the caller to provide a free text
    search term which is matched against the titles of the comps.  When
    omitted a random sample of listings is returned.
    """
    if not hasattr(app.state, "comps_df") or app.state.comps_df is None:
        raise HTTPException(status_code=500, detail="Comparison seed data not loaded")
    df = app.state.comps_df
    if q:
        q_lower = q.lower()
        df_filtered = df[df["title"].str.lower().str.contains(q_lower, na=False)]
    else:
        df_filtered = df
    # Return up to 12 items as dictionaries
    return df_filtered.head(12).to_dict(orient="records")


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    file: UploadFile = File(...),
    notes: Optional[str] = Form(None),
    userId: str = Form("demo_user")
) -> dict:
    """Perform offline analysis of an uploaded image and return a UserJob.

    In Demo Mode the file is parsed and simple heuristics are used to
    extract high level attributes.  These values are then used to
    filter comparison data and compute a price band.  Title and
    description copy are generated from templates.  When Live Mode is
    enabled this endpoint should call real machine learning services and
    external APIs instead (not implemented in this demo).
    """
    settings = app.state.settings
    if not settings.demo_mode:
        # Demo mode disabled – stub response
        raise HTTPException(status_code=503, detail="Live mode not implemented in demo")

    # Read the file into memory
    content = await file.read()
    try:
        image = Image.open(io.BytesIO(content)).convert("RGB")
    except Exception as exc:
        logger.error("Failed to open image: %s", exc)
        raise HTTPException(status_code=400, detail="Invalid image file")

    filename = os.path.basename(file.filename or "uploaded")

    # Save the image into a temp directory for reference.  In a real
    # deployment this could be persisted to object storage.  Here we
    # generate a unique filename and store it under /tmp.
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    tmp_dir = os.path.join(os.getcwd(), "tmp_uploads")
    os.makedirs(tmp_dir, exist_ok=True)
    tmp_path = os.path.join(tmp_dir, unique_name)
    with open(tmp_path, "wb") as f:
        f.write(content)
    image_url = tmp_path  # local path used as URL in demo

    # Detect attributes from the filename and image
    detected = detect_attributes(filename, image)

    # Filter comps
    df = app.state.comps_df
    comps_list = filter_comps(df, detected.get("brand"), detected.get("model")) if df is not None else []

    # Compute price band from comps
    prices = [float(item["price"]) for item in comps_list if isinstance(item.get("price"), (int, float))]
    price_band = calculate_price_band(prices)

    # Build templated copy
    copy_dict = build_copy(detected.get("brand"), detected.get("model"), detected, price_band)

    # Assemble final UserJob
    job = assemble_user_job(userId, image_url, notes, detected, comps_list, price_band, copy_dict)
    return job