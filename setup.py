"""pvgmsh setuptools packaging."""

from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="pvgmsh",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
