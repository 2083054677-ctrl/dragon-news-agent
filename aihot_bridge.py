#!/usr/bin/env python3
"""
aihot_bridge.py — 从 AI HOT API 拉取真实 AI 新闻，灌入龙虾新闻网站 news.json

用法:
  python3 aihot_bridge.py                    # 拉最近 7 天精选，覆盖 news.json
  python3 aihot_bridge.py --mode selected     # 同上
  python3 aihot_bridge.py --days 3            # 最近 3 天
  python3 aihot_bridge.py --daily             # 拉最新日报
  python3 aihot_bridge.py --publish           # 拉完自动 git commit + push
"""

import json
import os
import sys
import hashlib
import argparse
import subprocess
from datetime import datetime, timedelta, timezone, date
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

API_BASE = "https://aihot.virxact.com"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 aihot-skill/0.2.0"
DATA_DIR = os.path.join(os.path.dirname(__file__), "website", "data")
NEWS_JSON_PATH = os.path.join(DATA_DIR, "news.json")
DAILY_JSON_PATH = os.path.join(DATA_DIR, "daily.json")

# AI HOT category → 龙虾新闻 category
CATEGORY_MAP = {
    "ai-models":  "AI 前沿",
    "ai-products": "产品发布",
    "industry":   "行业观察",
    "paper":      "研究论文",
    "tip":        "AI 前沿",
    None:         "行业观察",
}

def api_get(path):
    """Call AI HOT public API."""
    url = f"{API_BASE}{path}"
    req = Request(url, headers={"User-Agent": UA})
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"  ⚠️ HTTP {e.code}: {body[:200]}")
        return None
    except URLError as e:
        print(f"  ⚠️ 网络错误: {e}")
        return None

def fetch_items(mode="selected", days=7, take=100):
    """Fetch AI news items from the items API."""
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    path = f"/api/public/items?mode={mode}&since={since}&take={take}"
    print(f"📡 拉取 AI HOT items: mode={mode}, 最近 {days} 天, take={take}...")
    result = api_get(path)
    if not result:
        return []
    items = result.get("items", [])
    print(f"  ✅ 获取到 {len(items)} 条新闻")
    return items

def fetch_daily(date_str=None):
    """Fetch a specific daily report."""
    if date_str:
        path = f"/api/public/daily/{date_str}"
    else:
        path = "/api/public/daily"
    print(f"📡 拉取 AI HOT 日报: {path}")
    result = api_get(path)
    if not result:
        return []
    items = []
    for section in result.get("sections", []):
        label = section.get("label", "")
        # Map section label → category
        label_to_cat = {
            "模型发布/更新": "AI 前沿",
            "产品发布/更新": "产品发布",
            "行业动态": "行业观察",
            "论文研究": "研究论文",
            "技巧与观点": "AI 前沿",
        }
        cat = label_to_cat.get(label, "行业观察")
        for item in section.get("items", []):
            items.append({
                "title": item.get("title", ""),
                "author": item.get("sourceName", ""),
                "date": result.get("date", date_str or ""),
                "summary": (item.get("summary") or item.get("title", ""))[:100],
                "content": item.get("summary", ""),
                "source_url": item.get("sourceUrl", ""),
                "category": cat,
                "tags": _extract_tags(item.get("title", ""), cat),
                "published_at": item.get("publishedAt", ""),
            })
    # Flashes
    for flash in result.get("flashes", []):
        items.append({
            "title": flash.get("title", ""),
            "author": flash.get("sourceName", ""),
            "date": result.get("date", date_str or ""),
            "summary": flash.get("title", "")[:100],
            "content": flash.get("title", ""),
            "source_url": flash.get("sourceUrl", ""),
            "category": "行业观察",
            "tags": ["快讯"],
            "published_at": flash.get("publishedAt", ""),
        })
    print(f"  ✅ 日报 {result.get('date', '?')}: {len(items)} 条")
    return items

def _extract_tags(title, category):
    """Generate tags from title keywords and category."""
    tags = []
    keywords = {
        "OpenAI": ["OpenAI"], "GPT": ["GPT"], "Claude": ["Claude", "Anthropic"],
        "Google": ["Google"], "Gemini": ["Gemini"], "Meta": ["Meta"],
        "Llama": ["Llama", "Meta"], "DeepSeek": ["DeepSeek"],
        "开源": ["开源"], "融资": ["融资"], "政策": ["政策"],
        "Agent": ["Agent"], "机器人": ["机器人"], "人形": ["机器人"],
        "模型": ["大模型"], "发布": ["发布"], "论文": ["论文"],
        "芯片": ["芯片"], "GPU": ["GPU"], "NVIDIA": ["NVIDIA"],
        "视频": ["视频生成"], "语音": ["语音AI"],
        "欧盟": ["AI监管"], "美国": ["AI政策"],
    }
    for kw, tgs in keywords.items():
        if kw.lower() in title.lower():
            tags.extend(tgs)
    # Deduplicate and limit
    seen = set()
    result = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            result.append(t)
    return result[:5] if result else [category[:4]]

def api_item_to_news(item):
    """Convert an items API result to dragon-news format."""
    title = item.get("title", "")
    source = item.get("source", "")
    published = item.get("publishedAt", "")
    date_str = published[:10] if published else date.today().isoformat()
    summary = (item.get("summary") or title)[:120]
    content = item.get("summary") or title
    url = item.get("url", "")
    cat_raw = item.get("category")
    cat = CATEGORY_MAP.get(cat_raw, "行业观察")
    tags = _extract_tags(title, cat)

    # Generate stable ID
    id_hash = hashlib.md5(f"{title}-{source}".encode()).hexdigest()[:8]
    news_id = f"news-{date_str.replace('-', '')}-{id_hash}"

    return {
        "id": news_id,
        "title": title,
        "author": source,
        "date": date_str,
        "summary": summary,
        "content": f"{content}\n\n原文链接: {url}" if url else content,
        "category": cat,
        "tags": tags,
    }

def daily_item_to_news(item):
    """Convert a daily report item to dragon-news format."""
    title = item.get("title", "")
    source = item.get("author", "")
    date_str = item.get("date", date.today().isoformat())
    summary = item.get("summary", "")[:120]
    content = item.get("content", "")
    url = item.get("source_url", "")
    cat = item.get("category", "行业观察")
    tags = item.get("tags", [cat[:4]])

    id_hash = hashlib.md5(f"{title}-{source}".encode()).hexdigest()[:8]
    news_id = f"news-{date_str.replace('-', '')}-{id_hash}"

    return {
        "id": news_id,
        "title": title,
        "author": source,
        "date": date_str,
        "summary": summary,
        "content": f"{content}\n\n原文链接: {url}" if url and content else (content or f"{title}\n{url}"),
        "category": cat,
        "tags": tags,
    }

def load_existing():
    """Load current news.json."""
    if os.path.exists(NEWS_JSON_PATH):
        with open(NEWS_JSON_PATH) as f:
            return json.load(f)
    return []

def save_news(news_list):
    """Save news.json."""
    os.makedirs(os.path.dirname(NEWS_JSON_PATH), exist_ok=True)
    with open(NEWS_JSON_PATH, "w") as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)
    print(f"💾 已写入 {len(news_list)} 条新闻 → {NEWS_JSON_PATH}")

def fetch_and_save_daily(date_str=None):
    """Fetch daily report and save as structured daily.json."""
    if date_str:
        result = api_get(f"/api/public/daily/{date_str}")
    else:
        result = api_get("/api/public/daily")
    if not result:
        print("  ⚠️ 日报数据获取失败")
        return False

    # Build the daily report in a display-friendly format
    daily = {
        "date": result.get("date", ""),
        "generatedAt": result.get("generatedAt", ""),
        "lead": result.get("lead"),
        "sections": [],
        "flashes": result.get("flashes", []),
    }

    # Map section labels to Chinese and add icons
    section_icons = {
        "模型发布/更新": "🧠",
        "产品发布/更新": "🚀",
        "行业动态": "📊",
        "论文研究": "📄",
        "技巧与观点": "💡",
    }

    for section in result.get("sections", []):
        label = section.get("label", "")
        items = []
        for item in section.get("items", []):
            items.append({
                "title": item.get("title", ""),
                "summary": item.get("summary", ""),
                "sourceUrl": item.get("sourceUrl", ""),
                "sourceName": item.get("sourceName", ""),
                "publishedAt": item.get("publishedAt", ""),
            })
        daily["sections"].append({
            "icon": section_icons.get(label, "📌"),
            "label": label,
            "items": items,
        })

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DAILY_JSON_PATH, "w") as f:
        json.dump(daily, f, ensure_ascii=False, indent=2)
    total = sum(len(s["items"]) for s in daily["sections"]) + len(daily["flashes"])
    print(f"📋 日报已保存: {daily['date']}, {len(daily['sections'])} 个版块, {total} 条")
    return True

def git_publish(commit_msg="publish: AI HOT 自动同步新闻"):
    """Commit and push news.json and daily.json."""
    project_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        subprocess.run(["git", "-C", project_dir, "add", "website/data/news.json", "website/data/daily.json"], check=True)
        subprocess.run(["git", "-C", project_dir, "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "-C", project_dir, "push"], check=True)
        print(f"🚀 已提交并推送: {commit_msg}")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git 操作失败: {e}")

def main():
    parser = argparse.ArgumentParser(description="AI HOT → 龙虾新闻 桥接器")
    parser.add_argument("--mode", default="selected", choices=["selected", "all"],
                        help="拉取模式 (默认: selected)")
    parser.add_argument("--days", type=int, default=7,
                        help="拉取最近 N 天 (默认: 7)")
    parser.add_argument("--take", type=int, default=100,
                        help="最多取 N 条 (默认: 100)")
    parser.add_argument("--daily", action="store_true",
                        help="拉取日报而非 items")
    parser.add_argument("--daily-date", type=str,
                        help="拉取指定日期日报 (YYYY-MM-DD)")
    parser.add_argument("--publish", action="store_true",
                        help="拉取后自动 git commit + push")
    parser.add_argument("--replace", action="store_true",
                        help="完全替换 news.json (默认: 保留旧条目，去重合并)")
    parser.add_argument("--save-daily", action="store_true",
                        help="同时拉取并保存日报到 daily.json")
    args = parser.parse_args()

    # Fetch daily report if requested
    if args.save_daily:
        fetch_and_save_daily(args.daily_date)

    # Fetch items
    if args.daily or args.daily_date:
        raw_items = fetch_daily(args.daily_date)
        new_news = [daily_item_to_news(i) for i in raw_items]
    else:
        raw_items = fetch_items(mode=args.mode, days=args.days, take=args.take)
        new_news = [api_item_to_news(i) for i in raw_items]

    if not new_news:
        print("❌ 未获取到任何新闻")
        return

    # Merge with existing
    if args.replace:
        final = new_news
        print(f"🔄 替换模式: {len(new_news)} 条新新闻")
    else:
        existing = load_existing()
        existing_ids = {n["id"] for n in existing}
        added = 0
        for n in new_news:
            if n["id"] not in existing_ids:
                existing.insert(0, n)
                existing_ids.add(n["id"])
                added += 1
        final = existing
        print(f"🔄 合并模式: 已有 {len(existing) - added} 条 + 新增 {added} 条 → 共 {len(final)} 条")

    # Stats
    cats = {}
    for n in final:
        cats[n["category"]] = cats.get(n["category"], 0) + 1
    print("📊 分类统计:")
    for cat, cnt in sorted(cats.items()):
        print(f"    {cat}: {cnt}")

    save_news(final)

    if args.publish:
        today = date.today().isoformat()
        git_publish(f"publish: AI HOT 同步 {len(new_news)} 条新闻 ({today})")


if __name__ == "__main__":
    main()
