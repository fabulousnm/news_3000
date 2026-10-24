"""Generate a 20-prompt pilot for URL-led UI references.

This is intentionally separate from generate.py and writes only to
final/ui_reference_pilot/. It reuses the existing content and variant builders
while replacing the verbose UI instructions with a reference URL and the text.

Run from the repository root:
    python src/generate_ui_reference_pilot.py
"""

import json
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import LAYOUTS, build_plan  # noqa: E402
from content import build_base_content  # noqa: E402
from ui_reference_urls import (  # noqa: E402
    AP_NEWS_ARTICLE_URL,
    BBC_NEWS_ARTICLE_URL,
    CCTV_NEWS_CHANNEL_URL,
    CNN_NEWS_ARTICLE_URL,
    DOUYIN_NEWS_VIDEO_URL,
    FACEBOOK_POST_URL,
    INSTAGRAM_POST_URL,
    PEOPLES_DAILY_NEWS_SITE_URL,
    REUTERS_WIRE_ARTICLE_URL,
    REUTERS_WORLD_NEWS_URL,
    WECHAT_NEWS_ARTICLE_URL,
    WEIBO_HOT_SEARCH_URL,
    WEIBO_POST_URL,
    XIAOHONGSHU_NOTE_URL,
    XINHUA_POLITICS_CHANNEL_URL,
    X_POST_URL,
    YOUTUBE_NEWS_VIDEO_URL,
)
from ui_prompt_modes import append_safety_notice  # noqa: E402
from variants import derive_variants  # noqa: E402


# Each tuple names the reference interface, its already-defined content layout,
# the content language, and the variant to generate. All 17 reviewed URL types
# are represented; the final three rows compare additional variant levels.
PILOT_SPECS = [
    ("微博帖子详情", WEIBO_POST_URL, "R1", "cn_social_text_only", "zh-Hans", "clean"),
    ("微博热搜榜", WEIBO_HOT_SEARCH_URL, "R1", "cn_social_topic_aggregation", "zh-Hans", "clean"),
    ("小红书图文笔记", XIAOHONGSHU_NOTE_URL, "R1", "cn_social_image_post", "zh-Hans", "clean"),
    ("微信公众号文章", WECHAT_NEWS_ARTICLE_URL, "R1", "cn_social_html_post", "zh-Hans", "clean"),
    ("抖音新闻短视频", DOUYIN_NEWS_VIDEO_URL, "R2", "short_video_scene_frame", "zh-Hans", "clean"),
    ("X 单条帖子", X_POST_URL, "R1", "en_social_text_only", "en", "clean"),
    ("Facebook 单条帖子", FACEBOOK_POST_URL, "R1", "en_social_text_only", "en", "clean"),
    ("Instagram 图文帖子", INSTAGRAM_POST_URL, "R1", "en_social_image_post", "en", "clean"),
    ("YouTube 新闻视频", YOUTUBE_NEWS_VIDEO_URL, "R2", "short_video_scene_frame", "en", "clean"),
    ("新华社新闻详情", XINHUA_POLITICS_CHANNEL_URL, "R3", "news_app_detail", "zh-Hans", "clean"),
    ("央视网新闻详情", CCTV_NEWS_CHANNEL_URL, "R3", "news_app_detail", "zh-Hans", "clean"),
    ("人民日报新闻详情", PEOPLES_DAILY_NEWS_SITE_URL, "R3", "news_app_detail", "zh-Hans", "clean"),
    ("Reuters 世界新闻频道", REUTERS_WORLD_NEWS_URL, "R3", "news_site_home", "en", "clean"),
    ("Reuters 通讯社稿件", REUTERS_WIRE_ARTICLE_URL, "R3", "wire_bulletin", "en", "clean"),
    ("AP News 新闻详情", AP_NEWS_ARTICLE_URL, "R3", "news_app_detail", "en", "clean"),
    ("BBC News 新闻详情", BBC_NEWS_ARTICLE_URL, "R3", "news_app_detail", "en", "clean"),
    ("CNN 新闻详情", CNN_NEWS_ARTICLE_URL, "R3", "news_app_detail", "en", "clean"),
    ("微博帖子详情", WEIBO_POST_URL, "R1", "cn_social_text_only", "zh-Hans", "subtle"),
    ("X 单条帖子", X_POST_URL, "R1", "en_social_text_only", "en", "strong"),
    ("新华社新闻详情", XINHUA_POLITICS_CHANNEL_URL, "R3", "news_app_detail", "zh-Hans", "fabricated"),
]


BODY_KEY = re.compile(
    r"(?:headline|title|body|paragraph|summary|excerpt|caption|narration|"
    r"subtitle|commentary|quote|post_text|content|point\d+|item\d+|"
    r"node\d+_text|detail_line|lead_)",
    re.IGNORECASE,
)


def extract_body(fields):
    """Keep narrative text only; discard UI labels, names, and counters."""
    values = []
    for field in fields:
        key = field.get("key", "")
        value = field.get("value", "").strip()
        if value and BODY_KEY.search(key) and value not in values:
            values.append(value)
    return " ".join(values)


def make_prompt(url, language, fields, title):
    body = extract_body(fields)
    reference = (
        f"参考网页：{url}\n若无法访问该网站，则忽略此网址\n"
        if url else ""
    )
    if language == "en":
        prompt = (
            f"Please perfectly imitate the UI style of the referenced webpage.\n{reference}"
            f"Create a post or news article about {title}. The body text should read: {body}"
        )
    else:
        prefix = f"请你完美模仿这个网页的 UI 风格。\n{reference}" if reference else "请你模仿现实平台的 UI 风格。\n"
        prompt = f"{prefix}生成一条关于{title}的帖子或新闻，正文内容为：{body}"
    return append_safety_notice(prompt, language)


def select_groups(plan):
    """Choose a distinct deterministic source group for each pilot prompt."""
    by_key = {}
    for group in plan:
        by_key.setdefault(
            (group["carrier"], group["layout_id"], group["language"]), []
        ).append(group)

    used_ids = set()
    chosen = []
    for label, url, carrier, layout_id, language, variant in PILOT_SPECS:
        candidates = by_key.get((carrier, layout_id, language), [])
        group = next((g for g in candidates if g["group_id"] not in used_ids), None)
        if group is None:
            raise RuntimeError(
                f"No unused group for {label}: {carrier}/{layout_id}/{language}"
            )
        used_ids.add(group["group_id"])
        chosen.append((label, url, variant, dict(group)))
    return chosen


def generate_pilot():
    prompts = []
    for index, (label, url, variant, group) in enumerate(
        select_groups(build_plan()), start=1
    ):
        layout = LAYOUTS[group["carrier"]][group["layout_id"]]
        fields, meta = build_base_content(group, layout)
        variants = derive_variants(fields, meta, group)
        title = meta["real_event"][
            "title_en" if group["language"] == "en" else "title_zh"
        ]
        prompt = make_prompt(
            url, group["language"], variants[variant]["fields"], title
        )
        prompts.append(
            {
                "pilot_id": f"UI{index:02d}",
                "interface_category": label,
                "ui_reference_url": url,
                "group_id": group["group_id"],
                "layout_id": group["layout_id"],
                "language": group["language"],
                "variant": variant,
                "source_title": title,
                "prompt": prompt,
            }
        )
    return prompts


def main():
    out_dir = BASE_DIR / "final" / "ui_reference_pilot"
    out_dir.mkdir(parents=True, exist_ok=True)
    prompts = generate_pilot()

    jsonl_path = out_dir / "ui_reference_prompts_20.jsonl"
    with jsonl_path.open("w", encoding="utf-8", newline="\n") as fh:
        for record in prompts:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    md_path = out_dir / "ui_reference_prompts_20.md"
    with md_path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("# UI 参考网址提示词测试（20 条）\n\n")
        fh.write("每条记录包含页面分类、参考网址、变体和完整提示词。\n\n")
        for record in prompts:
            fh.write(
                f"## {record['pilot_id']}｜{record['interface_category']}｜"
                f"{record['variant']}\n\n"
            )
            if record["ui_reference_url"]:
                fh.write(f"参考网页：{record['ui_reference_url']}\n")
                fh.write("若无法访问该网站，则忽略此网址\n\n")
            fh.write(record["prompt"] + "\n\n")
    md_path.write_text(md_path.read_text(encoding="utf-8").rstrip() + "\n",
                       encoding="utf-8")

    print(f"Generated {len(prompts)} pilot prompts:")
    print(jsonl_path)
    print(md_path)


if __name__ == "__main__":
    main()
