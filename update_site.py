#!/usr/bin/env python3
"""
AI新闻播报网站更新脚本
每次生成播报后，自动追加到网站数据文件
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

SITE_DIR = Path("/root/.openclaw/workspace/ai-news-site")
DATA_FILE = SITE_DIR / "news-data.json"

def load_existing_data():
    """加载现有数据"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def add_news_item(title, summary, score=0, source="AI精选", keywords="", url="", news_type="AI早报"):
    """
    添加一条新闻到网站数据
    
    Args:
        title: 新闻标题（中文）
        summary: 新闻摘要（中文）
        score: 质量评分
        source: 来源
        keywords: 关键词
        url: 原文链接
        news_type: 播报类型
    """
    data = load_existing_data()
    
    now = datetime.now()
    
    item = {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "type": news_type,
        "title": title,
        "summary": summary,
        "score": score,
        "source": source,
        "keywords": keywords,
        "url": url
    }
    
    data.append(item)
    
    # 保留最近30天的数据
    cutoff = now.replace(hour=0, minute=0, second=0, microsecond=0)
    # 简单保留最近100条
    if len(data) > 100:
        data = data[-100:]
    
    # 保存
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已添加新闻: {title}", file=sys.stderr)
    return True

def batch_add_news(news_list):
    """
    批量添加新闻
    news_list: list of dict with keys: title, summary, score, source, keywords, url
    """
    data = load_existing_data()
    now = datetime.now()
    
    for news in news_list:
        item = {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M"),
            "type": news.get("type", "AI早报"),
            "title": news["title"],
            "summary": news["summary"],
            "score": news.get("score", 0),
            "source": news.get("source", "AI精选"),
            "keywords": news.get("keywords", ""),
            "url": news.get("url", "")
        }
        data.append(item)
    
    # 保留最近100条
    if len(data) > 100:
        data = data[-100:]
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已批量添加 {len(news_list)} 条新闻", file=sys.stderr)
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="更新AI新闻播报网站数据")
    parser.add_argument("--title", help="新闻标题")
    parser.add_argument("--summary", help="新闻摘要")
    parser.add_argument("--score", type=int, default=0, help="质量评分")
    parser.add_argument("--source", default="AI精选", help="来源")
    parser.add_argument("--keywords", default="", help="关键词")
    parser.add_argument("--url", default="", help="原文链接")
    parser.add_argument("--type", default="AI早报", help="播报类型")
    
    args = parser.parse_args()
    
    if args.title and args.summary:
        add_news_item(
            title=args.title,
            summary=args.summary,
            score=args.score,
            source=args.source,
            keywords=args.keywords,
            url=args.url,
            news_type=args.type
        )
    else:
        print("用法: python3 update_site.py --title '标题' --summary '摘要' [--score 5]", file=sys.stderr)
        sys.exit(1)
