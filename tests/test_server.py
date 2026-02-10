#!/usr/bin/env python3
from contextlib import AbstractAsyncContextManager
from unittest.mock import AsyncMock

import pytest
from mcp import ClientSession
from pytest_mock import MockerFixture

from mathematica_mcp.logger import logger
from mathematica_mcp.server import _run_wolframscript

# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_run_wolframscript_success(mocker: MockerFixture) -> None:
    """
    Test _run_wolframscript() with successful command execution.
    """
    # Mock the subprocess to return successful output
    mock_process = AsyncMock()
    mock_process.returncode = 0
    mock_process.communicate = AsyncMock(return_value=(b"WolframScript 1.13.0 for Mac OS X ARM (64-bit)", b""))

    mock_create_subprocess = mocker.patch(
        "mathematica_mcp.server.asyncio.create_subprocess_exec",
        return_value=mock_process,
    )

    result = await _run_wolframscript(["-version"])

    assert result == "WolframScript 1.13.0 for Mac OS X ARM (64-bit)"
    mock_create_subprocess.assert_called_once()
    call_args = mock_create_subprocess.call_args
    assert call_args[0][0] == "wolframscript"
    assert call_args[0][1] == "-version"


@pytest.mark.asyncio
async def test_run_wolframscript_file_not_found(mocker: MockerFixture) -> None:
    """
    Test _run_wolframscript() when wolframscript command is not found.
    """
    # Mock the subprocess to raise FileNotFoundError
    mocker.patch(
        "mathematica_mcp.server.asyncio.create_subprocess_exec",
        side_effect=FileNotFoundError("wolframscript: command not found"),
    )

    with pytest.raises(RuntimeError) as exc_info:
        await _run_wolframscript(["-version"])

    assert "wolframscript' command not found" in str(exc_info.value)
    assert "Wolfram Engine installation" in str(exc_info.value)


@pytest.mark.asyncio
async def test_run_wolframscript_command_failure(mocker: MockerFixture) -> None:
    """
    Test _run_wolframscript() when the command fails with non-zero exit code.
    """
    # Mock the subprocess to return a failed process
    mock_process = AsyncMock()
    mock_process.returncode = 1
    mock_process.communicate = AsyncMock(return_value=(b"", b"Error: Invalid syntax"))

    mocker.patch(
        "mathematica_mcp.server.asyncio.create_subprocess_exec",
        return_value=mock_process,
    )

    with pytest.raises(RuntimeError) as exc_info:
        await _run_wolframscript(["-file", "nonexistent.wl"])

    assert "'wolframscript' command failed" in str(exc_info.value)
    assert "Error: Invalid syntax" in str(exc_info.value)


@pytest.mark.asyncio
async def test_run_wolframscript_command_failure_no_stderr(mocker: MockerFixture) -> None:
    """
    Test _run_wolframscript() when the command fails but stderr is empty.
    """
    # Mock the subprocess to return a failed process with empty stderr
    mock_process = AsyncMock()
    mock_process.returncode = 1
    mock_process.communicate = AsyncMock(return_value=(b"", b""))

    mocker.patch(
        "mathematica_mcp.server.asyncio.create_subprocess_exec",
        return_value=mock_process,
    )

    with pytest.raises(RuntimeError) as exc_info:
        await _run_wolframscript(["--invalid-flag"])

    assert "'wolframscript' command failed" in str(exc_info.value)
    assert "Unknown error" in str(exc_info.value)


# ---------------------------------------------------------------------------
# Integration tests (require local WolframScript installation)
# ---------------------------------------------------------------------------


@pytest.mark.wolframscript
@pytest.mark.asyncio
async def test_tool_catalog(mcp_session: AbstractAsyncContextManager[ClientSession]) -> None:
    """Verify the MCP server exposes the expected set of tools."""
    async with mcp_session as session:
        result = await session.list_tools()
        tool_names = {tool.name for tool in result.tools}
        logger.debug(f"Available tools on wolframscript server: {sorted(tool_names)}")
        assert tool_names == {"evaluate", "version_wolframscript", "version_wolframengine", "licensetype"}


@pytest.mark.wolframscript
@pytest.mark.asyncio
async def test_evaluate(mcp_session: AbstractAsyncContextManager[ClientSession]) -> None:
    """Test the 'evaluate' tool by computing a symbolic integral."""
    async with mcp_session as session:
        result = await session.call_tool("evaluate", {"script": "Integrate[x*Sin[x], x]"})
        text = getattr(result.content[0], "text", str(result.content[0]))
        logger.debug(f"Script output: {text}")
        assert len(text) > 0


@pytest.mark.wolframscript
@pytest.mark.asyncio
async def test_version_wolframscript(mcp_session: AbstractAsyncContextManager[ClientSession]) -> None:
    """Test the 'version_wolframscript' tool."""
    async with mcp_session as session:
        result = await session.call_tool("version_wolframscript", {})
        text = getattr(result.content[0], "text", str(result.content[0]))
        logger.debug(f"WolframScript version: {text}")
        assert len(text) > 0
        assert any(char.isdigit() for char in text), "Version should contain digits"


@pytest.mark.wolframscript
@pytest.mark.asyncio
async def test_version_wolframengine(mcp_session: AbstractAsyncContextManager[ClientSession]) -> None:
    """Test the 'version_wolframengine' tool."""
    async with mcp_session as session:
        result = await session.call_tool("version_wolframengine", {})
        text = getattr(result.content[0], "text", str(result.content[0]))
        logger.debug(f"Wolfram Engine version: {text}")
        assert len(text) > 0
        assert any(char.isdigit() for char in text), "Version should contain digits"


@pytest.mark.wolframscript
@pytest.mark.asyncio
async def test_licensetype(mcp_session: AbstractAsyncContextManager[ClientSession]) -> None:
    """Test the 'licensetype' tool."""
    async with mcp_session as session:
        result = await session.call_tool("licensetype", {})
        text = getattr(result.content[0], "text", str(result.content[0]))
        logger.debug(f"Wolfram Engine license type: {text}")
        assert len(text) > 0
