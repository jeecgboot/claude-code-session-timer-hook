#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
会话耗时钩子 - 记录每轮对话耗时并通过 systemMessage 反馈给用户。

用法:
  python session_timer.py start     # UserPromptSubmit hook: 记录本轮起始时间
  python session_timer.py stop      # Stop hook: 读取起始时间并计算本轮耗时
  python session_timer.py end       # SessionEnd hook: 累计整个会话总耗时
  python session_timer.py reset     # 清空累计耗时 (stdin 有 session_id 则只清当前会话, 否则清全部)
  python session_timer.py reset --all  # 强制清空所有会话的累计耗时

stdin 接收 Claude Code 传入的 JSON（至少包含 session_id）。
存储文件位于 ~/.claude/session_timing/<session_id>.{turn_start,session_start,total}
"""
import sys
import os
import json
import time
import pathlib


def fmt(seconds: float) -> str:
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    if seconds < 60:
        return f"{seconds:.2f}s"
    mins, secs = divmod(seconds, 60)
    if mins < 60:
        return f"{int(mins)}m{secs:.0f}s"
    hours, mins = divmod(mins, 60)
    return f"{int(hours)}h{int(mins)}m{secs:.0f}s"


def main():
    event = sys.argv[1] if len(sys.argv) > 1 else 'unknown'
    extra_args = sys.argv[2:]

    raw = sys.stdin.read() if not sys.stdin.isatty() else ''
    try:
        data = json.loads(raw) if raw else {}
    except json.JSONDecodeError:
        data = {}

    sid_from_stdin = data.get('session_id')
    sid = sid_from_stdin or 'default'

    timing_dir = pathlib.Path.home() / '.claude' / 'session_timing'
    timing_dir.mkdir(parents=True, exist_ok=True)
    start_file = timing_dir / f'{sid}.turn_start'
    session_start_file = timing_dir / f'{sid}.session_start'
    total_file = timing_dir / f'{sid}.total'

    now = time.time()

    if event == 'session_start':
        session_start_file.write_text(str(now), encoding='utf-8')
        total_file.write_text('0', encoding='utf-8')

    elif event == 'start':
        # UserPromptSubmit: 记录本轮起始时间
        start_file.write_text(str(now), encoding='utf-8')
        if not session_start_file.exists():
            session_start_file.write_text(str(now), encoding='utf-8')
        if not total_file.exists():
            total_file.write_text('0', encoding='utf-8')

    elif event == 'stop':
        # Stop: 计算本轮耗时并反馈
        if not start_file.exists():
            return
        try:
            start = float(start_file.read_text(encoding='utf-8'))
        except (ValueError, OSError):
            return
        elapsed = now - start

        # 累加到总耗时
        try:
            total = float(total_file.read_text(encoding='utf-8')) if total_file.exists() else 0.0
        except (ValueError, OSError):
            total = 0.0
        total += elapsed
        total_file.write_text(str(total), encoding='utf-8')

        # 删除本轮计时文件，避免重复计算
        try:
            start_file.unlink()
        except OSError:
            pass

        msg = f"⏱ 本轮耗时 {fmt(elapsed)} · 累计 {fmt(total)}"
        print(json.dumps({"systemMessage": msg}, ensure_ascii=False))

    elif event == 'end':
        # SessionEnd: 输出整个会话总耗时 + 清理文件
        if session_start_file.exists():
            try:
                session_start = float(session_start_file.read_text(encoding='utf-8'))
                session_elapsed = now - session_start
            except (ValueError, OSError):
                session_elapsed = 0.0
        else:
            session_elapsed = 0.0

        try:
            total = float(total_file.read_text(encoding='utf-8')) if total_file.exists() else 0.0
        except (ValueError, OSError):
            total = 0.0

        msg = f"📊 会话结束 · Claude 响应累计 {fmt(total)} · 会话时长 {fmt(session_elapsed)}"
        print(json.dumps({"systemMessage": msg}, ensure_ascii=False))

        # 清理
        for f in (start_file, session_start_file, total_file):
            try:
                if f.exists():
                    f.unlink()
            except OSError:
                pass

    elif event == 'reset':
        # 清空累计耗时
        # - stdin 有 session_id 且未指定 --all → 只清当前会话
        # - 无 session_id 或指定 --all → 清所有会话
        scope_all = ('--all' in extra_args) or (sid_from_stdin is None)

        if scope_all:
            count = 0
            for f in timing_dir.glob('*.total'):
                try:
                    f.write_text('0', encoding='utf-8')
                    count += 1
                except OSError:
                    pass
            # 同时删除孤立的 turn_start（避免误算一轮超大时长）
            for f in timing_dir.glob('*.turn_start'):
                try:
                    f.unlink()
                except OSError:
                    pass
            msg = f"♻️ 已重置 {count} 个会话的累计耗时"
        else:
            if total_file.exists():
                total_file.write_text('0', encoding='utf-8')
            else:
                total_file.write_text('0', encoding='utf-8')
            # 清理残留的 turn_start，避免把 reset 之前的等待时间算进下一轮
            try:
                if start_file.exists():
                    start_file.unlink()
            except OSError:
                pass
            msg = "♻️ 当前会话累计耗时已重置为 0"

        print(json.dumps({"systemMessage": msg}, ensure_ascii=False))


if __name__ == '__main__':
    main()
