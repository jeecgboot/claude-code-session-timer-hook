# Session Timer

Claude Code 每轮对话结束自动显示耗时：

```
⏱ 本轮耗时 4.72s · 累计 1m18s
```

## 安装（让 Claude Code 自动完成）

把以下**这段话完整复制**粘贴给 Claude Code，它会自动把脚本放到 `~/.claude/hooks/` 并合并 `~/.claude/settings.json`：

```
请帮我安装 session_timer。步骤：

1. 把当前目录下的 session_timer.py 复制到 ~/.claude/hooks/session_timer.py（目录不存在就创建）。
2. 合并以下 hooks 到 ~/.claude/settings.json 的 hooks 字段(保留我现有的其他配置，不要覆盖)：
   - SessionStart → command: python "$HOME/.claude/hooks/session_timer.py" session_start 2>/dev/null || true
   - UserPromptSubmit → command: python "$HOME/.claude/hooks/session_timer.py" start 2>/dev/null || true
   - Stop → command: python "$HOME/.claude/hooks/session_timer.py" stop 2>/dev/null || true
   - SessionEnd → command: python "$HOME/.claude/hooks/session_timer.py" end 2>/dev/null || true
   每个 hook 的 type 都是 "command"。
3. 校验 settings.json 是合法 JSON，然后告诉我敲 /hooks 激活。
```

> 前置要求：本机已有 Python 3（命令 `python` 可执行）。macOS / Linux / Windows(git bash) 都支持。

## 使用

- **自动显示耗时**：装完后什么都不用做，每轮 Claude 回复末尾自动出现
- **清空累计**：对 Claude 说「清空累计耗时」，或终端跑 `python ~/.claude/hooks/session_timer.py reset --all`

## 卸载

```
帮我卸载 session_timer：删除 ~/.claude/hooks/session_timer.py 和 ~/.claude/session_timing/ 目录，并从 ~/.claude/settings.json 移除这 4 个 hook（SessionStart / UserPromptSubmit / Stop / SessionEnd 中只保留我其他项目的命令）。
```
