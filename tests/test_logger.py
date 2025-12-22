#!/usr/bin/env python3

from mathematica_mcp.logger import logger


def test_loguru() -> None:
    """
    Test the Loguru logging functionality
    """
    logger.info("Testing Loguru logging functionality")

    # Check the Loguru output at ./mathematica_mcp.log
