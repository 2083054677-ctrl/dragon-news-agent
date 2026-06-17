#!/usr/bin/env python3
"""
龙虾新闻 - RSS 新闻采集器
从多个 AI 新闻 RSS 源拉取最新资讯，转化为 news.json 格式。

用法:
  python3 fetch_news.py              # 拉取并合并到 news.json
  python3 fetch_news.py --preview    # 仅预览，不写入文件
  python3 fetch_news.py --source hn  # 只从 Hacker News 拉取
"""

import json
import hashlib
import re
import sys
import os
from urllib.request import urlopen, Request
from urllib.error import URLError
from xml.etree import ElementTree as ET
from datetime import datetime, timezone
from html import unescape

# 新闻数据文件路径
NEWS_FILE = os.path.join(os.path.dirname(__file__), "website", "data", "news.json")

# ═══════════════════════════════════════════════════════════════
# RSS 源配置
# ═══════════════════════════════════════════════════════════════

SOURCES = {
    "hn_ai": {
        "name": "Hacker News AI",
        "url": "https://hnrss.org/newest?q=AI&points=30",
        "category": "AI 前沿",
        "lang": "en"
    },
    "hn_llm": {
        "name": "Hacker News LLM",
        "url": "https://hnrss.org/newest?q=LLM&points=20",
        "category": "AI 前沿",
        "lang": "en"
    },
    "jiqizhixin": {
        "name": "机器之心",
        "url": "https://rsshub.app/jiqizhixin",
        "category": "AI 前沿",
        "lang": "zh"
    },
    "infoq_ai": {
        "name": "InfoQ AI",
        "url": "https://rsshub.app/infoq/topic/AI",
        "category": "行业观察",
        "lang": "zh"
    },
    "36kr_ai": {
        "name": "36氪 AI",
        "url": "https://rsshub.app/36kr/information/AI",
        "category": "行业观察",
        "lang": "zh"
    }
}

# ═══════════════════════════════════════════════════════════════
# RSS 解析
# ═══════════════════════════════════════════════════════════════

def fetch_rss(url, timeout=15):
    """拉取 RSS XML 内容"""
    headers = {
        "User-Agent": "DragonNewsBot/1.0 (RSS Reader)",
        "Accept": "application/rss+xml, application/xml, text/xml"
    }
    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except URLError as e:
        print(f"  ⚠️  网络错误: {e.reason}")
        return None
    except Exception as e:
        print(f"  ⚠️  拉取失败: {e}")
        return None


def parse_rss_items(xml_text):
    """解析 RSS XML 为条目列表"""
    items = []
    try:
        root = ET.fromstring(xml_text)
        # 处理 RSS 2.0
        for item in root.findall(".//item"):
            title = item.findtext("title", "").strip()
            link = item.findtext("link", "").strip()
            desc = item.findtext("description", "").strip()
            pub_date = item.findtext("pubDate", "").strip()
            author = item.findtext("author", "").strip() or item.findtext("{http://purl.org/dc/elements/1.1/}creator", "").strip()

            if not title:
                continue

            items.append({
                "title": title,
                "link": link,
                "description": desc,
                "pub_date": pub_date,
                "author": author
            })
    except ET.ParseError as e:
        print(f"  ⚠️  XML 解析错误: {e}")

    return items


def clean_html(text):
    """移除 HTML 标签"""
    text = re.sub(r"<[^>]+>", "", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_date(date_str):
    """将 RSS 日期格式转为 YYYY-MM-DD"""
    if not date_str:
        return datetime.now().strftime("%Y-%m-%d")

    # RFC 2822 格式 (RSS 标准)
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(date_str)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        pass

    # ISO 格式
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except Exception:
        pass

    return datetime.now().strftime("%Y-%m-%d")


def generate_id(title, date):
    """生成唯一新闻 ID"""
    hash_part = hashlib.md5(title.encode()).hexdigest()[:6]
    date_part = date.replace("-", "")
    return f"news-{date_part}-{hash_part}"


def auto_categorize(title, description):
    """根据内容自动分类"""
    text = (title + " " + description).lower()

    if any(k in text for k in ["政策", "国务院", "监管", "法规", "regulation", "policy", "government"]):
        return "政策动态"
    if any(k in text for k in ["开源", "github", "open source", "apache", "mit license", "hugging face"]):
        return "开源项目"
    if any(k in text for k in ["论文", "paper", "arxiv", "研究", "icml", "neurips", "iclr"]):
        return "研究论文"
    if any(k in text for k in ["发布", "launch", "release", "推出", "上线", "发售"]):
        return "产品发布"
    if any(k in text for k in ["融资", "收购", "ipo", "估值", "市场", "营收", "funding"]):
        return "行业观察"

    return "AI 前沿"


def extract_tags(title, description, max_tags=4):
    """从标题和描述中提取标签"""
    text = title + " " + description

    # 常见 AI 关键词
    keywords = [
        "OpenAI", "GPT", "Claude", "Anthropic", "Google", "DeepMind",
        "Meta", "LLaMA", "DeepSeek", "Qwen", "通义", "智谱", "百度",
        "大模型", "LLM", "Agent", "多模态", "RAG", "微调",
        "开源", "API", "芯片", "GPU", "NVIDIA", "算力",
        "机器人", "自动驾驶", "医疗", "教育", "金融"
    ]

    found = []
    for kw in keywords:
        if kw.lower() in text.lower() and kw not in found:
            found.append(kw)
        if len(found) >= max_tags:
            break

    if not found:
        found = ["AI"]

    return found


# ═══════════════════════════════════════════════════════════════
# 主逻辑
# ═══════════════════════════════════════════════════════════════

def fetch_from_source(source_key, source_config, max_items=5):
    """从单个源拉取新闻"""
    print(f"\n📡 拉取: {source_config['name']} ({source_config['url'][:50]}...)")

    xml_text = fetch_rss(source_config["url"])
    if not xml_text:
        return []

    items = parse_rss_items(xml_text)
    print(f"   获取到 {len(items)} 条原始条目")

    news_items = []
    for item in items[:max_items]:
        title = clean_html(item["title"])
        desc = clean_html(item["description"])
        date = parse_date(item["pub_date"])
        author = item["author"] or source_config["name"]

        if len(desc) > 300:
            content = desc
            summary = desc[:100] + "..."
        else:
            content = desc
            summary = desc if desc else title

        category = auto_categorize(title, desc) if source_config["category"] == "auto" else source_config.get("category", auto_categorize(title, desc))
        tags = extract_tags(title, desc)

        news_item = {
            "id": generate_id(title, date),
            "title": title,
            "author": author,
            "date": date,
            "summary": summary,
            "content": content,
            "category": category,
            "tags": tags
        }
        news_items.append(news_item)

    print(f"   ✅ 转化 {len(news_items)} 条新闻")
    return news_items


def merge_news(new_items, existing_items):
    """合并新闻，去重"""
    existing_titles = {item["title"] for item in existing_items}
    existing_ids = {item["id"] for item in existing_items}

    added = []
    for item in new_items:
        if item["title"] not in existing_titles and item["id"] not in existing_ids:
            added.append(item)
            existing_titles.add(item["title"])

    merged = added + existing_items
    merged.sort(key=lambda x: x["date"], reverse=True)
    return merged, len(added)


def main():
    preview_only = "--preview" in sys.argv
    source_filter = None

    for i, arg in enumerate(sys.argv):
        if arg == "--source" and i + 1 < len(sys.argv):
            source_filter = sys.argv[i + 1]

    print("🦞 龙虾新闻 - RSS 采集器")
    print("=" * 50)

    # 读取现有数据
    existing = []
    if os.path.exists(NEWS_FILE):
        with open(NEWS_FILE, "r", encoding="utf-8") as f:
            existing = json.load(f)
        print(f"📂 现有新闻: {len(existing)} 条")

    # 拉取新闻
    all_new = []
    sources_to_fetch = SOURCES

    if source_filter:
        if source_filter in SOURCES:
            sources_to_fetch = {source_filter: SOURCES[source_filter]}
        else:
            # 模糊匹配
            matched = {k: v for k, v in SOURCES.items() if source_filter.lower() in k.lower()}
            if matched:
                sources_to_fetch = matched
            else:
                print(f"⚠️  未知源: {source_filter}")
                print(f"   可用: {', '.join(SOURCES.keys())}")
                return

    for key, config in sources_to_fetch.items():
        items = fetch_from_source(key, config)
        all_new.extend(items)

    # 合并去重
    merged, added_count = merge_news(all_new, existing)

    print(f"\n{'=' * 50}")
    print(f"📊 结果: 新增 {added_count} 条，总计 {len(merged)} 条")

    if preview_only:
        print("\n📋 预览模式，不写入文件。新增条目:")
        for item in merged[:added_count]:
            print(f"  • [{item['category']}] {item['title']}")
            print(f"    {item['date']} | {item['author']}")
        return

    if added_count > 0:
        with open(NEWS_FILE, "w", encoding="utf-8") as f:
            json.dump(merged, f, ensure_ascii=False, indent=2)
        print(f"✅ 已写入 {NEWS_FILE}")
    else:
        print("ℹ️  无新增内容，文件未变更")


if __name__ == "__main__":
    main()
