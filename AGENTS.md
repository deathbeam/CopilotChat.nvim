# AGENTS.md

## Overview

Neovim plugin (pure Lua) providing GitHub Copilot Chat integration. Requires Neovim 0.10.0+, curl 8.0.0+, plenary.nvim.

## Commands

```bash
# Run tests (headless Neovim + plenary test harness)
make test

# Format check (what CI runs)
stylua --check .
```

`make test` runs `nvim --headless --clean -u ./scripts/test.lua`, which clones plenary.nvim into `.dependencies/` on first run, then executes all `tests/*_spec.lua` files via plenary's busted-style harness.

## Project layout

```
plugin/CopilotChat.lua    — Neovim plugin entry: commands, highlights, autocmds
lua/CopilotChat/
  init.lua                — Main module: setup(), ask(), open/close/toggle, save/load
  client.lua              — Copilot API client (auth, streaming, tool calls)
  config.lua              — Default configuration schema
  config/                 — Sub-configs: functions, mappings, prompts, providers
  constants.lua           — Shared constants (roles, etc.)
  completion.lua          — Completion source
  functions.lua           — Built-in functions/tools exposed to the LLM
  prompts.lua             — Built-in prompt definitions
  resources.lua           — Resource handling
  select.lua              — Selection strategies (visual, buffer, diagnostics, git diff)
  tiktoken.lua            — Token counting via native tiktoken lib
  health.lua              — :checkhealth integration
  notify.lua              — Notification utilities
  instructions/           — System prompt templates injected into LLM conversations (not agent guidance)
  ui/                     — Chat window, overlay, spinner
  utils.lua               — General utilities
  utils/                  — Utility modules: class, curl, diff, files, orderedmap, stringbuffer
queries/                  — Treesitter queries for copilot-chat filetype
tests/                    — Plenary busted-style specs (*_spec.lua)
scripts/
  test.lua                — Test runner bootstrap (sets up plenary)
  minimal.lua             — Minimal reproduction config
doc/CopilotChat.txt       — Auto-generated vimdoc (do NOT edit; generated from README by panvimdoc in CI)
```

## Style and formatting

- **Lua formatter:** StyLua — 2-space indent, 120 column width, single quotes preferred, Unix line endings. Config in `.stylua.toml`.
- **Pre-commit hooks:** Prettier (markdown/json/yaml) + StyLua (Lua). CI will fail if StyLua check fails.
- **No linter** (no luacheck/selene configured).
- Type annotations use EmmyLua/LuaCATS `---@class`, `---@param`, `---@return` style.

## Testing

- Framework: plenary.nvim busted-style (`describe`, `it`, `before_each`, `after_each`, `assert`).
- Test files live in `tests/` and must be named `*_spec.lua`.
- CI runs tests against Neovim nightly with LuaJIT 2.1 and LuaRocks 3.12.2.
- Tests are unit-level (class, diff, utils, orderedmap, stringbuffer, functions, init). No integration tests requiring Copilot auth.

## CI and releases

- CI (`ci.yml`): lint (StyLua) + test (plenary) on all PRs; vimdoc generation on main only.
- Releases via release-please (`simple` type). Version tracked in `version.txt`.
- `doc/CopilotChat.txt` is auto-committed by CI — do not edit manually.
- `CHANGELOG.md` is managed by release-please — do not edit manually.

## Key gotchas

- The module is loaded as `require('CopilotChat')` (capital C's) — this matches the `lua/CopilotChat/` directory name. Case matters.
- `init.lua` uses lazy self-initialization via `__index` metamethod — accessing any field triggers `setup()` if not already called.
- `.dependencies/` is gitignored and auto-populated by the test runner (plenary clone).
- `build/` is gitignored and holds downloaded tiktoken native libraries.
