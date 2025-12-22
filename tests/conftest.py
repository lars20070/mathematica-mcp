#!/usr/bin/env python3
import os

import pytest


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "wolframscript: tests requiring a local WolframScript installation")


@pytest.fixture(autouse=True)
def skip_wolframscript_tests(request: pytest.FixtureRequest) -> None:
    """
    Skip tests marked with 'wolframscript' when running in CI environment.
    Run these tests only locally.
    """
    if request.node.get_closest_marker("wolframscript") and os.getenv("GITHUB_ACTIONS") == "true":
        pytest.skip("Tests requiring WolframScript skipped in CI environment")

