# Session Timer

Claude Code 每轮对话结束自动显示耗时：

```
⏱ 本轮耗时 4.72s · 累计 1m18s
```

项目地址：<https://github.com/jeecgboot/claude-code-session-timer-hook>

## 获取

下载方式三选一：

### 方式 1：git clone

```bash
git clone https://github.com/jeecgboot/claude-code-session-timer-hook.git
cd claude-code-session-timer-hook
```

然后执行下方【安装】中的指令（Claude 会从当前目录读取 `session_timer.py`）。

### 方式 2：curl 单文件

```bash
mkdir -p ~/.claude/hooks
curl -fsSL https://raw.githubusercontent.com/jeecgboot/claude-code-session-timer-hook/main/session_timer.py \
    -o ~/.claude/hooks/session_timer.py
```

文件已就位，跳过【安装】的第 1 步，让 Claude 只合并 hook 配置即可。

### 方式 3（最懒）：直接让 Claude Code 从 GitHub 装

连 git、curl 都不用敲。把下面这段话**完整复制**粘贴给 Claude Code：

```
请帮我从 https://github.com/jeecgboot/claude-code-session-timer-hook 安装 session_timer。步骤：

1. 用 WebFetch 读取仓库 README.md 了解完整安装说明。
2. 下载 session_timer.py 到 ~/.claude/hooks/(目录不存在就创建)。下载地址：
   https://raw.githubusercontent.com/jeecgboot/claude-code-session-timer-hook/main/session_timer.py
3. 按 README 中的 hooks 配置合并到我的 ~/.claude/settings.json（保留现有配置，不要整段覆盖）。
4. 校验 settings.json 是合法 JSON，然后提示我敲 /hooks 激活。
```

## 安装（让 Claude Code 自动完成）

如果你用方式 1 本地 clone 后 `cd` 进目录，把下面**这段话完整复制**粘贴给 Claude Code，它会自动把脚本放到 `~/.claude/hooks/` 并合并 `~/.claude/settings.json`：

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
