"""Automation using nox."""

from __future__ import annotations

import nox


@nox.session(python=["3.10", "3.11", "3.12"])
def tests(session: nox.Session) -> None:
    """Run the unit and regular tests."""
    session.install(".[test]")
    session.run("pytest", *session.posargs)
