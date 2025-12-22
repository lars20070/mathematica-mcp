#!/usr/bin/env python3

from loguru import logger

__all__ = ["logger"]

# Configure Loguru
logger.remove(0)  # Remove default console logger
logger.add(
    __name__.split(".")[0] + ".log",
    rotation="500 MB",
    level="DEBUG",
)
