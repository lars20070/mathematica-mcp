# Mathematica MCP Server

<!-- mcp-name: io.github.lars20070/mathematica-mcp -->

[![Build](https://github.com/lars20070/mathematica-mcp/actions/workflows/build.yaml/badge.svg)](https://github.com/lars20070/mathematica-mcp/actions/workflows/build.yaml)
[![Python Version](https://img.shields.io/badge/dynamic/toml?url=https://raw.githubusercontent.com/lars20070/mathematica-mcp/master/pyproject.toml&query=project.requires-python&label=python)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/lars20070/mathematica-mcp)](https://github.com/lars20070/mathematica-mcp/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/mathematica-mcp.svg)](https://badge.fury.io/py/mathematica-mcp)

MCP server that wraps Mathematica's `wolframscript` command-line interface. It provides tools to evaluate Wolfram Language code and retrieve information about the Wolfram Engine installation.

| Tool | Description |
|------|-------------|
| `evaluate` | Evaluates a Wolfram Language script |
| `version_wolframscript` | Returns version of `wolframscript` |
| `version_wolframengine` | Returns version of Wolfram Engine |
| `licensetype` | Returns license type of Wolfram Engine |

## Background

* *Wolfram Language*: symbolic programming language e.g. `Integrate[x*Sin[x], x]`
* *Wolfram Engine*: kernel for running Wolfram Language code
* *WolframScript*: command-line interface to Wolfram Engine
* *Mathematica*: notebook interface to Wolfram Engine

Both Wolfram Engine and WolframScript are [freely available](https://www.wolfram.com/engine/) for personal use.

## Installation

1. Please ensure WolframScript is locally installed and activated:

```bash
wolframscript -version
wolframscript -activate
wolframscript -code "Integrate[x*Sin[x], x]"
```

2. Install the [uv package manager](https://docs.astral.sh/uv/getting-started/installation/).

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Edit the Claude Desktop config file and add the `mathematica-mcp` server.<br>`~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mathematica-mcp": {
    "command": "uvx",
    "args": [
      "mathematica-mcp"
    ]
  }
}
```