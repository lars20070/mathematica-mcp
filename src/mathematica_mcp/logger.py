#!/usr/bin/env python3

from pathlib import Path

from loguru import logger
from platformdirs import user_log_dir

__all__ = ["logger"]

# Use platform-appropriate log directory
log_dir = Path(user_log_dir("mathematica_mcp", ensure_exists=True))
log_path = log_dir / "mathematica_mcp.log"

# Configure Loguru
logger.remove(0)  # Remove default console logger
logger.add(
    log_path,
    rotation="500 MB",
    level="DEBUG",
)
