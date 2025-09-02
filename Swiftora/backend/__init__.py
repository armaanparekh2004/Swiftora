"""Swiftora backend package.

This package contains the FastAPI application and supporting modules.
"""

from .main import app  # re-export the FastAPI app at package level

__all__ = ["app"]