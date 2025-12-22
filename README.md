# Mathematica MCP Server

[![Build](https://github.com/lars20070/mathematica-mcp/actions/workflows/build.yaml/badge.svg)](https://github.com/lars20070/mathematica-mcp/actions/workflows/build.yaml)
[![Python Version](https://img.shields.io/badge/dynamic/toml?url=https://raw.githubusercontent.com/lars20070/mathematica-mcp/master/pyproject.toml&query=project.requires-python&label=python)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/lars20070/mathematica-mcp)](https://github.com/lars20070/mathematica-mcp/blob/master/LICENSE)

* *Wolfram Language*: symbolic programming language e.g. `Integrate[x*Sin[x], x]`
* *Wolfram Engine*: kernel for running Wolfram Language code
* *WolframScript*: command-line interface to Wolfram Engine
* *Mathematica*: notebook interface to Wolfram Engine
* Both Wolfram Engine and WolframScript are [freely available](https://www.wolfram.com/engine/) for personal use.

Please ensure you have WolframScript installed and activated.
```bash
wolframscript -version
wolframscript -activate
wolframscript -code "Integrate[x*Sin[x], x]"
```