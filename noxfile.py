#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["nox"]
# ///
"""Automation using nox."""

from __future__ import annotations

import nox

nox.needs_version = "2024.10.9"
nox.options.default_venv_backend = "uv|virtualenv"


@nox.session(python=["3.9", "3.10", "3.11", "3.12"])
def tests(session: nox.Session) -> None:
    """Run the unit and regular tests."""
    session.install(".[test]")
    session.run("pytest", *session.posargs)


if __name__ == "__main__":
    nox.main()
