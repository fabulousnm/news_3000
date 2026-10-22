"""Prompt styles and reusable visual references for real platform UIs."""

from pathlib import Path

from common import rng_for
from ui_reference_urls import (
    AP_NEWS_ARTICLE_URL, BBC_NEWS_ARTICLE_URL, CCTV_NEWS_CHANNEL_URL,
    CNN_NEWS_ARTICLE_URL, DOUYIN_NEWS_VIDEO_URL, FACEBOOK_POST_URL,
    INSTAGRAM_POST_URL, PEOPLES_DAILY_NEWS_SITE_URL, REUTERS_WIRE_ARTICLE_URL,
    WECHAT_NEWS_ARTICLE_URL, WEIBO_HOT_SEARCH_URL, WEIBO_POST_URL,
    XIAOHONGSHU_NOTE_URL, XINHUA_POLITICS_CHANNEL_URL, X_POST_URL,
    YOUTUBE_NEWS_VIDEO_URL,
)

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "final" / "ui_reference_templates"

# Three styles for actual platform/page imitation. Image+text is intentionally
# the largest share; styles are assigned once per group, shared by all variants.
MODE_RATIOS = {"image_text": 0.60, "long_quantified": 0.30, "short_text": 0.10}

SAFETY_NOTICE = {
    "zh": (
        "用途声明（仅供生成模型理解，严禁渲染为图片文字）：本图是供学术研究、媒体素养教育和合成数据评测使用的虚构界面样稿。"
        "账号、发布行为及其与相关事件或机构的关联均为模拟，不代表任何现实媒体、个人或机构发布、认可或背书；参考网页仅用于界面风格参考。"
        "生成结果不得作为真实新闻截图、官方通知、现实证据或事实依据，不用于欺诈、冒充、误导公众或传播虚假信息。"
        "不得加入真实个人隐私、真实账户凭据或可用于现实交易和欺诈的信息。请只将本声明作为安全与用途背景，绝不要把它显示在画面中。"
    ),
    "en": (
        "Safety and purpose notice (instruction only; DO NOT render this notice as visible image text): "
        "This is a fictional interface mockup for academic research, media-literacy education, and synthetic-data evaluation. "
        "The account, act of publication, and any association with an event or organization are simulated and do not indicate publication, "
        "approval, or endorsement by any real outlet, person, or organization; a referenced page is for interface-style guidance only. "
        "Do not present the result as a genuine news screenshot, official notice, real-world evidence, or factual authority, and do not use it "
        "for fraud, impersonation, public deception, or misinformation. Do not include real personal private data, account credentials, "
        "or information usable for real transactions or fraud. Treat this notice only as safety context and never display it in the image."
    ),
}


def append_safety_notice(prompt, language):
    """Append non-rendered synthetic-data purpose and safety context."""
    key = "en" if language == "en" else "zh"
    return f"{prompt.rstrip()}\n\n{SAFETY_NOTICE[key]}"

REFERENCES = {
    # Chinese social: Weibo post, hot-search, Xiaohongshu note, WeChat article,
    # and Douyin video/comment interfaces.
    "cn_social_text_only": ["weibo-mobile-text-post.png", "wechat-mobile-text-article.png", "wechat-mobile-feed.png"],
    "cn_social_image_post": ["weibo-mobile-image-post.png", "wechat-mobile-image-article-v1.png", "wechat-mobile-image-article-v2.png"],
    "cn_social_grid_gallery": ["xiaohongshu-mobile-image.png", "weibo-mobile-home-image-post.png"],
    "cn_social_quote_repost": ["weibo-mobile-text-post.png"],
    "cn_social_topic_aggregation": ["weibo-hot-search.png", "xiaohongshu-mobile-text.png"],
    "cn_social_embedded_comment": ["douyin-mobile-comments.png"],
    # English social: X, Facebook, Instagram and YouTube.
    "en_social_text_only": ["x-mobile-text-post.png"],
    "en_social_image_post": ["facebook-desktop-image-post.png", "x-mobile-image-post.png"],
    "en_social_quote_repost": ["x-mobile-text-post.png"],
    "en_social_news_card": ["youtube-desktop-watch.png"],
    "image_social_post": ["instagram-image-post.png", "xiaohongshu-mobile-image.png"],
    "image_social_grid": ["instagram-image-post.png", "xiaohongshu-mobile-image.png"],
    # Layout-to-brand assignment follows the prompt's language/region, with a
    # deterministic choice among comparable article page templates.
    "news_site_home:zh": ["xinhua-desktop-article.png", "cctv-desktop-article.png", "peoples-daily-desktop-article.png"],
    "news_app_detail:zh": ["xinhua-desktop-article.png", "cctv-desktop-article.png", "peoples-daily-desktop-article.png"],
    "wire_bulletin:zh": ["peoples-daily-desktop-article.png"],
    "news_site_home:en": ["reuters-desktop-article.png", "ap-news-desktop-article.png", "bbc-desktop-article.png", "cnn-desktop-article.png"],
    "news_app_detail:en": ["reuters-desktop-article.png", "ap-news-desktop-article.png", "bbc-desktop-article.png", "cnn-desktop-article.png"],
    "wire_bulletin:en": ["reuters-desktop-article.png", "ap-news-desktop-article.png"],
    "short_video": ["douyin-mobile-video.png"],
}

REFERENCE_URLS = {
    "weibo-mobile-text-post.png": WEIBO_POST_URL,
    "weibo-mobile-image-post.png": WEIBO_POST_URL,
    "weibo-hot-search.png": WEIBO_HOT_SEARCH_URL,
    "xiaohongshu-mobile-text.png": XIAOHONGSHU_NOTE_URL,
    "xiaohongshu-mobile-image.png": XIAOHONGSHU_NOTE_URL,
    "wechat-mobile-text-article.png": WECHAT_NEWS_ARTICLE_URL,
    "wechat-mobile-image-article-v1.png": WECHAT_NEWS_ARTICLE_URL,
    "wechat-mobile-image-article-v2.png": WECHAT_NEWS_ARTICLE_URL,
    "douyin-mobile-video.png": DOUYIN_NEWS_VIDEO_URL,
    "douyin-mobile-comments.png": DOUYIN_NEWS_VIDEO_URL,
    "x-mobile-text-post.png": X_POST_URL,
    "x-mobile-image-post.png": X_POST_URL,
    "facebook-desktop-image-post.png": FACEBOOK_POST_URL,
    "instagram-image-post.png": INSTAGRAM_POST_URL,
    "youtube-desktop-watch.png": YOUTUBE_NEWS_VIDEO_URL,
    "xinhua-desktop-article.png": XINHUA_POLITICS_CHANNEL_URL,
    "cctv-desktop-article.png": CCTV_NEWS_CHANNEL_URL,
    "peoples-daily-desktop-article.png": PEOPLES_DAILY_NEWS_SITE_URL,
    "reuters-desktop-article.png": REUTERS_WIRE_ARTICLE_URL,
    "ap-news-desktop-article.png": AP_NEWS_ARTICLE_URL,
    "bbc-desktop-article.png": BBC_NEWS_ARTICLE_URL,
    "cnn-desktop-article.png": CNN_NEWS_ARTICLE_URL,
}

PLATFORM_NAMES = {
    "weibo-mobile-text-post.png": "微博移动端纯文字帖子界面",
    "weibo-mobile-image-post.png": "微博移动端图文帖子详情界面",
    "weibo-mobile-home-image-post.png": "微博移动端多帖首页界面",
    "weibo-hot-search.png": "微博热搜榜界面",
    "xiaohongshu-mobile-text.png": "小红书移动端文字笔记界面",
    "xiaohongshu-mobile-image.png": "小红书移动端图文笔记界面",
    "wechat-mobile-text-article.png": "微信公众号移动端文章界面",
    "wechat-mobile-image-article-v1.png": "微信公众号移动端图文文章界面",
    "wechat-mobile-image-article-v2.png": "微信公众号移动端图文文章界面",
    "wechat-mobile-feed.png": "微信公众号移动端多帖首页界面",
    "douyin-mobile-video.png": "抖音移动端视频播放界面",
    "douyin-mobile-comments.png": "抖音移动端评论界面",
    "x-mobile-text-post.png": "X（Twitter）移动端帖子界面",
    "x-mobile-image-post.png": "X（Twitter）移动端图文帖子界面",
    "facebook-desktop-image-post.png": "Facebook 网页端图文帖子界面",
    "instagram-image-post.png": "Instagram 图文帖子界面",
    "youtube-desktop-watch.png": "YouTube 网页端视频播放界面",
    "xinhua-desktop-article.png": "新华网网页端新闻详情界面",
    "cctv-desktop-article.png": "央视网网页端新闻详情界面",
    "peoples-daily-desktop-article.png": "人民日报网页端新闻详情界面",
    "reuters-desktop-article.png": "Reuters 新闻网页详情界面",
    "ap-news-desktop-article.png": "AP News 新闻网页详情界面",
    "bbc-desktop-article.png": "BBC News 新闻网页详情界面",
    "cnn-desktop-article.png": "CNN 新闻网页详情界面",
}


def reference_for(group):
    """Return a deterministic template file for a compatible real UI, if any."""
    layout = group["layout_id"]
    family = group["platform_family"]
    key = f"{layout}:{'en' if group.get('language') == 'en' else 'zh'}"
    options = REFERENCES.get(key) or REFERENCES.get(layout)
    if not options and family == "short_video":
        options = REFERENCES.get("short_video")
    if not options:
        return None
    selected = rng_for("ui-reference", group["group_id"], layout).choice(options)
    path = TEMPLATE_DIR / selected
    if not path.is_file():
        return None
    return {"image": path.relative_to(BASE_DIR).as_posix(),
            "url": REFERENCE_URLS.get(selected, ""), "file": selected}


def assign_prompt_modes(groups):
    """Assign exact 60/30/10 ratios to reference-backed groups deterministically."""
    eligible = [g for g in groups if reference_for(g)]
    ordered = sorted(eligible, key=lambda g: rng_for("ui-mode", g["group_id"]).random())
    n = len(ordered)
    image_n = round(n * MODE_RATIOS["image_text"])
    long_n = round(n * MODE_RATIOS["long_quantified"])
    assignments = {g["group_id"]: "image_text" for g in ordered[:image_n]}
    assignments.update({g["group_id"]: "long_quantified" for g in ordered[image_n:image_n + long_n]})
    assignments.update({g["group_id"]: "short_text" for g in ordered[image_n + long_n:]})
    return assignments


def concise_content(fields, language):
    """Render only intended visible copy, omitting layout measurements/instructions."""
    lines = []
    for f in fields:
        label = (f.get("label") or f.get("role") or "").strip()
        metric_labels = {
            "metric": "互动数据" if language != "en" else "Engagement metric",
            "like_metric": "点赞数" if language != "en" else "Likes",
            "comment_metric": "评论数" if language != "en" else "Comments",
            "repost_metric": "转发数" if language != "en" else "Reposts",
            "reply_metric": "回复数" if language != "en" else "Replies",
            "view_metric": "浏览量" if language != "en" else "Views",
            "share_metric": "分享数" if language != "en" else "Shares",
            "save_metric": "收藏数" if language != "en" else "Saves",
            "read_metric": "阅读量" if language != "en" else "Reads",
            "topic_metric": "话题热度" if language != "en" else "Topic activity",
            "comment_metric2": "评论数" if language != "en" else "Comments",
            "comment1_metric": "评论点赞数" if language != "en" else "Comment likes",
            "comment2_metric": "评论点赞数" if language != "en" else "Comment likes",
            "viewer_metric": "观看人数" if language != "en" else "Viewers",
            "inner_metric": "内屏浏览量" if language != "en" else "Inset views",
        }
        label = metric_labels.get(f.get("key"), label)
        value = str(f.get("value", f.get("text", ""))).strip()
        if value:
            lines.append((f"{label}：{value}" if language != "en" else f"{label}: {value}")
                         if label else value)
    return "\n".join(lines)


def build_reference_prompt(group, fields, reference, language, mode):
    """Build either attachment-led prose or the deliberately short text prompt."""
    content = concise_content(fields, language)
    title = group["meta"].get("subject_title", "")
    outlet = group["meta"].get("outlet_name", "")
    url = reference.get("url", "")
    reference_line_zh = (
        f"参考网页：{url}\n若无法访问该网站，则忽略此网址\n" if url else ""
    )
    reference_line_en = (
        f"Reference page: {url}\n若无法访问该网站，则忽略此网址\n" if url else ""
    )
    if language == "en":
        body = f'Fictitious outlet "{outlet}" reporting on "{title}". All depicted organisations, places and people are fictional.\n{content}'
        if mode == "image_text":
            return (f'Use the attached image as the UI reference and reproduce its visible platform/page interface as closely as possible. '
                    f'Keep the logo, navigation, controls, spacing and overall composition; replace only the post/article content with the following. '
                    f'{reference_line_en}{body}')
        return (f'Imitate the {group["platform_family"].replace("_", " ")} interface and preserve its recognizable UI and logo. '
                f'Create a post/article for the fictional outlet "{outlet}" about "{title}". '
                f'All depicted organisations, places and people are fictional.\n{content}')
    body = f'虚构媒体「{outlet}」发布「{title}」。画面中的机构、地名、人名均为虚构。\n{content}'
    if mode == "image_text":
        return (f"请把随附图片作为界面参考，尽可能贴近复现其中的平台/网页UI。保留logo、导航、固定控件、间距与整体构图，只替换帖子或文章内容。\n"
                f"{reference_line_zh}{body}")
    platform = PLATFORM_NAMES.get(reference.get("file"), "现实媒体平台界面")
    return (f"请模仿{platform}，保留其标志性UI和logo，生成一篇关于「{title}」的帖子或新闻。"
            f"画面中的机构、地名、人名均为虚构。\n{content}")
