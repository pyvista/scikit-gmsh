"""scikit-gmsh setuptools packaging."""
from __future__ import annotations

from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="scikit-gmsh",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
