# Session Timer

> Claude Code 每轮 + 累计耗时自动反馈

每轮对话结束自动显示本轮耗时与累计耗时：

```
⏱ 本轮耗时 4.72s · 累计 1m18s
```

项目地址：<https://github.com/jeecgboot/claude-code-session-timer-hook>

## 安装（一段话丢给 Claude Code）

把下面这段话**完整复制**粘贴给 Claude Code，它会自己下载脚本、合并配置：

```
请帮我从 https://github.com/jeecgboot/claude-code-session-timer-hook 安装 session_timer。步骤：

1. 下载 session_timer.py 到 ~/.claude/hooks/(目录不存在就创建)。下载地址：
   https://raw.githubusercontent.com/jeecgboot/claude-code-session-timer-hook/main/session_timer.py
2. 合并以下 4 个 hook 到 ~/.claude/settings.json 的 hooks 字段(保留我现有配置，不要覆盖)：
   - SessionStart     → python "$HOME/.claude/hooks/session_timer.py" session_start 2>/dev/null || true
   - UserPromptSubmit → python "$HOME/.claude/hooks/session_timer.py" start         2>/dev/null || true
   - Stop             → python "$HOME/.claude/hooks/session_timer.py" stop          2>/dev/null || true
   - SessionEnd       → python "$HOME/.claude/hooks/session_timer.py" end           2>/dev/null || true
   每个 hook 的 type 都是 "command"。
3. 校验 settings.json 是合法 JSON，然后提示我敲 /hooks 激活。
```

装完敲一次 `/hooks` 重载配置，下一轮对话就能看到秒表。

> 前置要求：本机已有 Python 3（命令 `python` 可执行）。macOS / Linux / Windows(git bash) 都支持。

## 使用

- **自动显示耗时**：装完什么都不用做，每轮 Claude 回复末尾自动出现
- **清空累计**：对 Claude 说「清空累计耗时」，或终端跑 `python ~/.claude/hooks/session_timer.py reset --all`

## 卸载

```
帮我卸载 session_timer：删除 ~/.claude/hooks/session_timer.py 和 ~/.claude/session_timing/ 目录，并从 ~/.claude/settings.json 移除这 4 个 hook（SessionStart / UserPromptSubmit / Stop / SessionEnd 中只保留我其他项目的命令）。
```
