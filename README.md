# Session Timer

**English** · [简体中文](./README.zh-CN.md)

> A stopwatch for Claude Code — per-turn + cumulative elapsed time, auto-reported

At the end of every Claude turn you'll see the time spent on this round **and** the running total:

```
⏱ Turn 4.72s · Total 1m18s
```

Project: <https://github.com/jeecgboot/claude-code-session-timer-hook>

## Global Install (paste this paragraph into Claude Code)

Installs into `~/.claude/` so the timer is enabled **globally for every project** — no per-project setup.

**Copy the block below verbatim** and send it to Claude Code — it will download the script and merge the config for you:

```
Please install session_timer from https://github.com/jeecgboot/claude-code-session-timer-hook **globally** (under ~/.claude/, NOT into the current project's .claude/). Steps:

1. Download session_timer.py to ~/.claude/hooks/ (create the directory if it doesn't exist). URL:
   https://raw.githubusercontent.com/jeecgboot/claude-code-session-timer-hook/main/session_timer.py
2. Merge the following 4 hooks into the `hooks` field of the **global** ~/.claude/settings.json (keep my existing config — do not overwrite):
   - SessionStart     → python "$HOME/.claude/hooks/session_timer.py" session_start 2>/dev/null || true
   - UserPromptSubmit → python "$HOME/.claude/hooks/session_timer.py" start         2>/dev/null || true
   - Stop             → python "$HOME/.claude/hooks/session_timer.py" stop          2>/dev/null || true
   - SessionEnd       → python "$HOME/.claude/hooks/session_timer.py" end           2>/dev/null || true
   Each hook's type is "command".
3. Validate that settings.json is valid JSON, then tell me to run /hooks to activate.
```

Once installed, run `/hooks` to reload the config — the stopwatch will show up on the next turn.

> Requirement: Python 3 on PATH (the `python` command must work). macOS / Linux / Windows (git bash) all supported.

## Usage

- **Automatic display** — nothing else to do; each Claude reply ends with the timer line.
- **Reset the cumulative total** — tell Claude "reset cumulative time", or run `python ~/.claude/hooks/session_timer.py reset --all` in your terminal.

## Uninstall

```
Please uninstall session_timer: delete ~/.claude/hooks/session_timer.py and the ~/.claude/session_timing/ directory, and remove these 4 hooks from ~/.claude/settings.json (SessionStart / UserPromptSubmit / Stop / SessionEnd — keep entries from my other projects).
```
