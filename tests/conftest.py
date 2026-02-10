#!/usr/bin/env python3
import os
from collections.abc import AsyncGenerator
from contextlib import AbstractAsyncContextManager, asynccontextmanager

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


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


@asynccontextmanager
async def _create_mcp_session() -> AsyncGenerator[ClientSession, None]:
    """
    Connect to the MCP server and yield an initialized ClientSession.
    """
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "mathematica-mcp"],
        env=dict(os.environ),
    )
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        yield session


@pytest.fixture
def mcp_session() -> AbstractAsyncContextManager[ClientSession]:
    """
    Provide an async context manager for a connected MCP client session.

    Usage in tests::

        async with mcp_session as session:
            result = await session.call_tool("evaluate", {"script": "1+1"})
    """
    return _create_mcp_session()
