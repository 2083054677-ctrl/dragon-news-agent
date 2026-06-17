#!/usr/bin/env python3
"""
龙虾新闻 Agent 工具集
提供文件读写和 Git 自动化能力，供 OpenClaw Agent 通过 Tool Calling 调用。
"""

import json
import subprocess
import os
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional

# 项目根目录（website 所在位置）
PROJECT_ROOT = Path(__file__).parent.parent / "website"
NEWS_DATA_FILE = PROJECT_ROOT / "data" / "news.json"


# ═══════════════════════════════════════════════════════════════
# 工具 1: 读取当前新闻数据
# ═══════════════════════════════════════════════════════════════

def read_news_data() -> dict:
    """
    读取当前新闻 JSON 数据文件。
    返回: {"success": bool, "data": list | None, "error": str | None}
    """
    try:
        if not NEWS_DATA_FILE.exists():
            return {"success": True, "data": [], "count": 0}

        with open(NEWS_DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return {"success": True, "data": data, "count": len(data)}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


# ═══════════════════════════════════════════════════════════════
# 工具 2: 添加新闻条目
# ═══════════════════════════════════════════════════════════════

def add_news_item(
    title: str,
    author: str,
    date: str,
    summary: str,
    content: str,
    category: str,
    tags: list[str]
) -> dict:
    """
    向新闻数据文件中添加一条新闻。
    严格约束：只操作 data/news.json，不修改任何其他文件。

    参数:
        title: 新闻标题
        author: 作者/来源
        date: 发布日期 (YYYY-MM-DD)
        summary: 新闻摘要（一句话）
        content: 新闻正文
        category: 分类
        tags: 标签列表

    返回: {"success": bool, "news_id": str | None, "error": str | None}
    """
    try:
        # 输入验证
        if not title or not title.strip():
            return {"success": False, "error": "标题不能为空"}
        if not date or not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
            return {"success": False, "error": "日期格式必须为 YYYY-MM-DD"}
        if not content or not content.strip():
            return {"success": False, "error": "正文内容不能为空"}

        # 生成唯一 ID
        date_part = date.replace("-", "")
        hash_part = hashlib.md5(title.encode()).hexdigest()[:4]
        news_id = f"news-{date_part}-{hash_part}"

        # 读取现有数据
        if NEWS_DATA_FILE.exists():
            with open(NEWS_DATA_FILE, "r", encoding="utf-8") as f:
                news_list = json.load(f)
        else:
            news_list = []

        # 检查重复
        for item in news_list:
            if item.get("title") == title.strip():
                return {"success": False, "error": f"标题重复，已存在相同新闻: {title}"}

        # 构造新闻对象
        new_item = {
            "id": news_id,
            "title": title.strip(),
            "author": author.strip(),
            "date": date,
            "summary": summary.strip(),
            "content": content.strip(),
            "category": category.strip(),
            "tags": [t.strip() for t in tags if t.strip()]
        }

        # 插入到列表头部（最新的在前）
        news_list.insert(0, new_item)

        # 写入文件
        with open(NEWS_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(news_list, f, ensure_ascii=False, indent=2)

        return {"success": True, "news_id": news_id, "total_count": len(news_list)}

    except Exception as e:
        return {"success": False, "error": str(e)}


# ═══════════════════════════════════════════════════════════════
# 工具 3: Git 自动提交并推送
# ═══════════════════════════════════════════════════════════════

def git_commit_and_push(commit_message: str) -> dict:
    """
    将 news.json 的变更提交到 Git 并推送到远端。
    严格约束：只 add data/news.json 文件，不会 add 其他文件。

    参数:
        commit_message: 提交信息

    返回: {"success": bool, "commit_hash": str | None, "error": str | None}
    """
    try:
        cwd = str(PROJECT_ROOT)

        # 检查是否是 git 仓库
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=cwd, capture_output=True, text=True
        )
        if result.returncode != 0:
            return {"success": False, "error": "当前目录不是 Git 仓库"}

        # 只 add 新闻数据文件（核心安全约束）
        result = subprocess.run(
            ["git", "add", "data/news.json"],
            cwd=cwd, capture_output=True, text=True
        )
        if result.returncode != 0:
            return {"success": False, "error": f"git add 失败: {result.stderr}"}

        # 检查是否有变更
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=cwd, capture_output=True, text=True
        )
        if not result.stdout.strip():
            return {"success": False, "error": "没有检测到文件变更，无需提交"}

        changed_files = result.stdout.strip().split("\n")

        # 提交
        result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=cwd, capture_output=True, text=True
        )
        if result.returncode != 0:
            return {"success": False, "error": f"git commit 失败: {result.stderr}"}

        # 获取 commit hash
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=cwd, capture_output=True, text=True
        )
        commit_hash = result.stdout.strip()[:8]

        # 推送
        result = subprocess.run(
            ["git", "push"],
            cwd=cwd, capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return {
                "success": True,
                "commit_hash": commit_hash,
                "pushed": False,
                "warning": f"提交成功但推送失败: {result.stderr}",
                "changed_files": changed_files
            }

        return {
            "success": True,
            "commit_hash": commit_hash,
            "pushed": True,
            "changed_files": changed_files
        }

    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Git 推送超时（30秒），请检查网络连接"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ═══════════════════════════════════════════════════════════════
# 工具 4: 查看 Git 状态
# ═══════════════════════════════════════════════════════════════

def git_status() -> dict:
    """
    查看当前仓库的 Git 状态。
    返回: {"success": bool, "status": str, "branch": str}
    """
    try:
        cwd = str(PROJECT_ROOT)

        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=cwd, capture_output=True, text=True
        )
        status = result.stdout.strip() if result.stdout.strip() else "工作区干净，无变更"

        result_branch = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=cwd, capture_output=True, text=True
        )
        branch = result_branch.stdout.strip()

        return {"success": True, "status": status, "branch": branch}

    except Exception as e:
        return {"success": False, "error": str(e)}


# ═══════════════════════════════════════════════════════════════
# 工具 5: 新闻文本清洗（防注入）
# ═══════════════════════════════════════════════════════════════

def sanitize_news_text(text: str) -> str:
    """
    清洗新闻文本，移除可能的 Prompt 注入内容和危险字符。

    防御策略:
    - 移除常见的 prompt injection 模式
    - 移除 HTML/JS 标签
    - 移除控制字符
    """
    if not text:
        return ""

    # 移除 prompt injection 常见模式
    injection_patterns = [
        r"(?i)ignore\s+(previous|above|all)\s+(instructions?|prompts?|rules?)",
        r"(?i)you\s+are\s+now\s+",
        r"(?i)forget\s+(everything|all|previous)",
        r"(?i)new\s+instructions?:",
        r"(?i)system\s*prompt:",
        r"(?i)act\s+as\s+",
        r"(?i)pretend\s+(you|to)\s+",
        r"(?i)\[INST\]",
        r"(?i)<\|system\|>",
        r"(?i)<\|user\|>",
        r"(?i)<\|assistant\|>",
        r"(?i)```\s*system",
    ]

    for pattern in injection_patterns:
        text = re.sub(pattern, "[已过滤]", text)

    # 移除 HTML 标签
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)

    # 移除控制字符（保留换行和制表符）
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    return text.strip()


# ═══════════════════════════════════════════════════════════════
# MCP 工具服务入口（供 OpenClaw 调用）
# ═══════════════════════════════════════════════════════════════

TOOLS_MANIFEST = {
    "name": "dragon-news-tools",
    "version": "1.0.0",
    "description": "龙虾新闻自动化发布工具集",
    "tools": [
        {
            "name": "read_news",
            "description": "读取当前所有已发布的新闻列表",
            "parameters": {}
        },
        {
            "name": "add_news",
            "description": "添加一条新闻到网站。只修改 data/news.json，不触碰其他文件。",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "新闻标题"},
                    "author": {"type": "string", "description": "作者/来源"},
                    "date": {"type": "string", "description": "日期 YYYY-MM-DD"},
                    "summary": {"type": "string", "description": "一句话摘要"},
                    "content": {"type": "string", "description": "新闻正文"},
                    "category": {"type": "string", "description": "分类"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "标签"}
                },
                "required": ["title", "author", "date", "summary", "content", "category", "tags"]
            }
        },
        {
            "name": "git_publish",
            "description": "将新闻变更提交到 Git 并推送，只会 add data/news.json",
            "parameters": {
                "type": "object",
                "properties": {
                    "commit_message": {"type": "string", "description": "Git 提交信息"}
                },
                "required": ["commit_message"]
            }
        },
        {
            "name": "git_status",
            "description": "查看仓库当前 Git 状态",
            "parameters": {}
        }
    ]
}


def handle_tool_call(tool_name: str, arguments: dict) -> dict:
    """统一的工具调用分发器"""
    if tool_name == "read_news":
        return read_news_data()

    elif tool_name == "add_news":
        # 对文本字段进行清洗
        sanitized_args = {
            "title": sanitize_news_text(arguments.get("title", "")),
            "author": sanitize_news_text(arguments.get("author", "")),
            "date": arguments.get("date", ""),
            "summary": sanitize_news_text(arguments.get("summary", "")),
            "content": sanitize_news_text(arguments.get("content", "")),
            "category": sanitize_news_text(arguments.get("category", "")),
            "tags": [sanitize_news_text(t) for t in arguments.get("tags", [])]
        }
        return add_news_item(**sanitized_args)

    elif tool_name == "git_publish":
        msg = arguments.get("commit_message", "")
        if not msg:
            return {"success": False, "error": "提交信息不能为空"}
        return git_commit_and_push(sanitize_news_text(msg))

    elif tool_name == "git_status":
        return git_status()

    else:
        return {"success": False, "error": f"未知工具: {tool_name}"}


# ═══════════════════════════════════════════════════════════════
# 命令行入口（测试用）
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法:")
        print("  python tools.py read_news")
        print("  python tools.py add_news '{...json...}'")
        print("  python tools.py git_publish '提交信息'")
        print("  python tools.py git_status")
        print("  python tools.py manifest")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "manifest":
        print(json.dumps(TOOLS_MANIFEST, ensure_ascii=False, indent=2))
    elif cmd == "read_news":
        result = handle_tool_call("read_news", {})
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif cmd == "add_news":
        args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
        result = handle_tool_call("add_news", args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif cmd == "git_publish":
        msg = sys.argv[2] if len(sys.argv) > 2 else ""
        result = handle_tool_call("git_publish", {"commit_message": msg})
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif cmd == "git_status":
        result = handle_tool_call("git_status", {})
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"未知命令: {cmd}")
