#!/usr/bin/env python3
"""
龙虾新闻 - 端到端演示脚本
模拟 Agent 接收新闻稿后的完整工作流，可在课堂上直接运行展示。

用法:
  python3 demo.py                    # 使用内置测试新闻稿
  python3 demo.py tests/sample-news.txt  # 使用自定义新闻稿文件
"""

import json
import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "agent", "tools"))
from tools import handle_tool_call, sanitize_news_text, read_news_data

# 内置测试新闻稿
DEFAULT_NEWS = """
Anthropic 发布 Claude 4 系列模型：Agent 能力大幅跃迁

Anthropic 官方博客 · 2026年6月17日

旧金山时间 6 月 16 日，Anthropic 正式发布 Claude 4 系列模型，包括 Claude Opus 4、Claude Sonnet 4 和 Claude Haiku 4 三款。

新一代模型在 Agent 任务中表现尤为突出。在 SWE-bench Verified 基准测试中，Claude Opus 4 的解题率达到 72.5%，刷新了行业纪录。模型能够在复杂软件工程任务中自主规划、执行多步骤操作，并从错误中恢复。

Claude 4 系列还引入了「扩展思考」能力，允许模型在回答前进行深度推理，特别适合数学证明、代码调试和复杂分析等场景。

Anthropic CEO Dario Amodei 表示：「Claude 4 代表了我们在安全性和能力之间取得的最佳平衡。我们相信强大的 AI 和负责任的 AI 可以兼得。」

Claude 4 系列模型已通过 Anthropic API 和 Amazon Bedrock 面向全球开发者开放。
""".strip()


def print_step(step_num, title, detail=""):
    """美化输出步骤信息"""
    print(f"\n{'─' * 60}")
    print(f"  Step {step_num} │ {title}")
    if detail:
        print(f"         │ {detail}")
    print(f"{'─' * 60}")
    time.sleep(0.5)


def simulate_llm_parse(text):
    """
    模拟大模型结构化解析。
    实际使用中这一步由 DeepSeek V4 完成，这里用规则提取做演示。
    """
    lines = text.strip().split("\n")

    title = lines[0].strip() if lines else "未知标题"

    author = "未知来源"
    date = "2026-06-17"
    for line in lines[1:5]:
        if "·" in line:
            parts = line.split("·")
            author = parts[0].strip()
            date_str = parts[1].strip() if len(parts) > 1 else ""
            if "2026" in date_str:
                date = date_str.replace("年", "-").replace("月", "-").replace("日", "").strip()
                parts_d = date.split("-")
                if len(parts_d) == 3:
                    date = f"{parts_d[0]}-{parts_d[1].zfill(2)}-{parts_d[2].zfill(2)}"
            break

    content_lines = []
    for line in lines[2:]:
        if line.strip() and "·" not in line:
            content_lines.append(line.strip())
    content = "\n\n".join(content_lines)

    first_para = content_lines[0] if content_lines else title
    summary = first_para[:100]

    return {
        "title": title,
        "author": author,
        "date": date,
        "summary": summary,
        "content": content,
        "category": "AI 前沿",
        "tags": ["AI", "大模型", "Agent"]
    }


def main():
    # 读取新闻稿
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
        print(f"📄 读取新闻稿: {file_path}")
    else:
        raw_text = DEFAULT_NEWS
        print("📄 使用内置测试新闻稿")

    print(f"\n{'═' * 60}")
    print(f"  🦞 龙虾新闻 - 自动化发布演示")
    print(f"{'═' * 60}")

    # Step 1: 输入展示
    print_step(1, "接收新闻稿原文")
    print(f"\n{raw_text[:200]}...")
    print(f"\n  📏 总长度: {len(raw_text)} 字符")

    # Step 2: 文本清洗
    print_step(2, "安全清洗", "过滤 Prompt 注入和恶意内容")
    sanitized = sanitize_news_text(raw_text)
    if sanitized != raw_text:
        print("  ⚠️  检测到并过滤了潜在危险内容")
    else:
        print("  ✅ 文本安全，无需过滤")

    # Step 3: 结构化解析
    print_step(3, "结构化解析", "大模型提取新闻要素（演示使用规则引擎模拟）")
    parsed = simulate_llm_parse(sanitized)
    time.sleep(0.3)

    print(f"""
  📰 标题: {parsed['title']}
  ✍️  作者: {parsed['author']}
  📅 日期: {parsed['date']}
  📝 摘要: {parsed['summary'][:60]}...
  📂 分类: {parsed['category']}
  🏷️  标签: {', '.join(parsed['tags'])}
  📄 正文: {len(parsed['content'])} 字符
""")

    # Step 4: 写入数据
    print_step(4, "写入新闻数据", "调用 add_news 工具")
    result = handle_tool_call("add_news", parsed)
    time.sleep(0.3)

    if result["success"]:
        print(f"  ✅ 成功写入!")
        print(f"     News ID: {result['news_id']}")
        print(f"     当前总数: {result['total_count']} 条")
    else:
        print(f"  ❌ 写入失败: {result['error']}")
        return

    # Step 5: Git 提交
    print_step(5, "Git 提交推送", "调用 git_publish 工具")
    commit_msg = f"publish: {parsed['title']}"
    git_result = handle_tool_call("git_publish", {"commit_message": commit_msg})
    time.sleep(0.3)

    if git_result["success"]:
        print(f"  ✅ Git 提交成功!")
        print(f"     Commit: {git_result['commit_hash']}")
        print(f"     推送: {'✅ 已推送' if git_result.get('pushed') else '⚠️ 未推送（无远端）'}")
        print(f"     变更文件: {git_result['changed_files']}")
    else:
        print(f"  ⚠️  Git: {git_result.get('error', git_result.get('warning'))}")

    # 最终报告
    print(f"\n{'═' * 60}")
    print(f"  🎉 发布完成!")
    print(f"{'═' * 60}")
    print(f"""
  验证方式:
  1. 打开 website/index.html 查看新闻是否显示
  2. 运行 git log --oneline -3 查看提交记录
  3. 运行 git diff HEAD~1 --stat 确认只修改了 news.json
""")

    # 显示 git log
    import subprocess
    result = subprocess.run(
        ["git", "log", "--oneline", "-5"],
        cwd=os.path.dirname(__file__) or ".",
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print("  最近提交记录:")
        for line in result.stdout.strip().split("\n"):
            print(f"    {line}")


if __name__ == "__main__":
    main()
