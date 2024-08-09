"""Automation using nox."""

from __future__ import annotations

import nox


@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12"])
def tests(session: nox.Session) -> None:
    """Run the unit and regular tests."""
    session.install(".[test]")
    session.install("-r", "requirements_test.txt", *session.posargs)
    session.run("pytest", *session.posargs)
