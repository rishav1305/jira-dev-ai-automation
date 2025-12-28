# Changelog: JDAA-4 MCP Server Fixes

## Date
2025-12-28

## Changes
- Fixed `src/mcp_server.py` to correctly handle `transport="sse"` configuration.
- Disabled `DNS rebinding protection` when binding to non-local hosts (e.g., `0.0.0.0`) to allow remote access.
- Verified fix using `curl` with mismatched Host header.
- Verified regression tests with `tests/test_mcp_server.py`.

## Impact
- The MCP server can now be accessed remotely or via `0.0.0.0` without 403 Forbidden / 421 Misdirected Request errors.
