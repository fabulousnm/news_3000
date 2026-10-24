"""Template-specific body limits used when writing complete-image prompts.

Visual completion instructions live in ui_prompt_modes.py and are sent to the
image model together with the selected full template reference. These limits
keep copy within the visible space of each template.
"""

from __future__ import annotations

TEMPLATE_SPECS = {
    "weibo-mobile-text-post.png": {
        "slots": [("author", "account_name", "text", 18), ("body", "body_text", "text", 140),
                  ("publish_time", "publish_time", "text", 24), ("metrics", "engagement_metrics", "text", 12)],
        "preserve": [], "body_limit": 140,
    },
    "weibo-mobile-image-post.png": {
        "slots": [("author", "account_name", "text", 18), ("body", "body_text", "text", 120),
                  ("media", "media_asset", "image", 0), ("comments", "comments", "comment", 54),
                  ("metrics", "engagement_metrics", "text", 12)], "preserve": [], "body_limit": 120,
    },
    "weibo-mobile-home-image-post.png": {
        "slots": [("author", "account_name", "text", 18), ("body", "body_text", "text", 90),
                  ("gallery", "media_assets", "image_grid", 0), ("metrics", "engagement_metrics", "text", 12)],
        "preserve": [], "body_limit": 90,
    },
    "weibo-hot-search.png": {
        "slots": [("topic_rows", "topic_items", "ranked_text", 18), ("heat", "topic_metrics", "text", 12),
                  ("featured_media", "media_asset", "image", 0)],
        "preserve": [], "body_limit": 0,
    },
    "xiaohongshu-mobile-text.png": {
        "slots": [("author", "account_name", "text", 18), ("title", "headline", "text", 34),
                  ("body", "body_text", "text", 100), ("hashtags", "hashtags", "text_blue", 30),
                  ("comment_1", "comments", "comment", 56), ("comment_2", "comments", "comment", 56),
                  ("comment_3", "comments", "comment", 56), ("metrics", "engagement_metrics", "text", 12)],
        "preserve": [], "body_limit": 100,
    },
    "xiaohongshu-mobile-image.png": {
        "slots": [("author", "account_name", "text", 18), ("title", "headline", "text", 34),
                  ("body", "body_text", "text", 90), ("media", "media_asset", "image", 0),
                  ("hashtags", "hashtags", "text_blue", 28), ("metrics", "engagement_metrics", "text", 12)],
        "preserve": [], "body_limit": 90,
    },
    "wechat-mobile-text-article.png": {
        "slots": [("headline", "headline", "text", 34), ("byline", "author_source_time", "text", 30),
                  ("body", "body_text", "text", 620), ("metrics", "engagement_metrics", "text", 12)],
        "preserve": [], "body_limit": 620,
    },
    "wechat-mobile-image-article-v1.png": {
        "slots": [("headline", "headline", "text", 34), ("byline", "author_source_time", "text", 30),
                  ("body", "body_text", "text", 440), ("media", "media_asset", "image", 0),
                  ("metrics", "engagement_metrics", "text", 12)], "preserve": [], "body_limit": 440,
    },
    "wechat-mobile-image-article-v2.png": {
        "slots": [("headline", "headline", "text", 34), ("body", "body_text", "text", 240),
                  ("media_left", "media_asset_1", "image", 0), ("media_right", "media_asset_2", "image", 0),
                  ("captions", "captions", "text", 32), ("metrics", "engagement_metrics", "text", 12)],
        "preserve": [], "body_limit": 240,
    },
    "wechat-mobile-feed.png": {
        "slots": [("feed_cards", "feed_items", "card_text", 36), ("cover_images", "media_assets", "image_grid", 0)],
        "preserve": [], "body_limit": 36,
    },
    "douyin-mobile-video.png": {
        "slots": [("caption", "caption_text", "text", 42), ("location", "location", "text", 18),
                  ("audio", "audio_name", "text", 24), ("status", "status_bar", "status", 0),
                  ("metrics", "engagement_metrics", "text", 12), ("video", "media_asset", "image", 0)],
        "preserve": [], "body_limit": 42,
    },
    "douyin-mobile-comments.png": {
        "slots": [("comment_1", "comments", "comment", 52), ("comment_2", "comments", "comment", 52),
                  ("comment_3", "comments", "comment", 52), ("search_phrase", "search_phrase", "text_blue", 24),
                  ("status", "status_bar", "status", 0), ("video", "media_asset", "image", 0)],
        "preserve": [], "body_limit": 0,
    },
    "x-mobile-text-post.png": {
        "slots": [("author", "account_name", "text", 18), ("body", "body_text", "text", 220),
                  ("publish_time", "publish_time", "text", 24), ("metrics", "engagement_metrics", "text", 12)],
        "preserve": [], "body_limit": 220,
    },
    "x-mobile-image-post.png": {
        "slots": [("author", "account_name", "text", 18), ("body", "body_text", "text", 150),
                  ("media", "media_asset", "image", 0), ("metrics", "engagement_metrics", "text", 12)],
        "preserve": [], "body_limit": 150,
    },
    "facebook-desktop-image-post.png": {
        "slots": [("author", "account_name", "text", 28), ("body", "body_text", "text", 150),
                  ("media", "media_asset", "image", 0), ("metrics", "engagement_metrics", "text", 12)],
        "preserve": [], "body_limit": 150,
    },
    "instagram-image-post.png": {
        "slots": [("author", "account_name", "text", 18), ("caption", "caption_text", "text", 120),
                  ("media", "media_asset", "image", 0), ("hashtags", "hashtags", "text_blue", 30),
                  ("status", "status_bar", "status", 0), ("metrics", "engagement_metrics", "text", 12)],
        "preserve": [], "body_limit": 120,
    },
    "youtube-desktop-watch.png": {
        "slots": [("video", "media_asset", "image", 0), ("title", "headline", "text", 80),
                  ("channel", "account_name", "text", 28), ("description", "body_text", "text", 180),
                  ("metrics", "engagement_metrics", "text", 12)], "preserve": [], "body_limit": 180,
    },
    "xinhua-desktop-article.png": {
        "slots": [("headline", "headline", "text", 48), ("byline", "author_source_time", "text", 36),
                  ("body", "body_text", "text", 480), ("media", "media_asset", "image", 0),
                  ("sidebar_media", "sidebar_image", "image", 0),
                  ("sidebar", "sidebar_items", "card_text", 42)], "preserve": [], "body_limit": 480,
    },
    "cctv-desktop-article.png": {
        "slots": [("headline", "headline", "text", 48), ("byline", "author_source_time", "text", 36),
                  ("body", "body_text", "text", 480), ("media", "media_asset", "image", 0),
                  ("sidebar", "sidebar_items", "card_text", 42)], "preserve": [], "body_limit": 480,
    },
    "peoples-daily-desktop-article.png": {
        "slots": [("headline", "headline", "text", 48), ("byline", "author_source_time", "text", 36),
                  ("body", "body_text", "text", 480), ("media", "media_asset", "image", 0),
                  ("sidebar_media", "sidebar_image", "image", 0),
                  ("sidebar", "sidebar_items", "card_text", 42)], "preserve": [], "body_limit": 480,
    },
    "reuters-desktop-article.png": {
        "slots": [("headline", "headline", "text", 48), ("byline", "author_source_time", "text", 36),
                  ("body", "body_text", "text", 480), ("media", "media_asset", "image", 0)],
        "preserve": [], "body_limit": 480,
    },
    "ap-news-desktop-article.png": {
        "slots": [("headline", "headline", "text", 48), ("byline", "author_source_time", "text", 36),
                  ("body", "body_text", "text", 480), ("media", "media_asset", "image", 0)],
        "preserve": [], "body_limit": 480,
    },
    "bbc-desktop-article.png": {
        "slots": [("headline", "headline", "text", 48), ("byline", "author_source_time", "text", 36),
                  ("body", "body_text", "text", 480), ("media", "media_asset", "image", 0)],
        "preserve": [], "body_limit": 480,
    },
    "cnn-desktop-article.png": {
        "slots": [("headline", "headline", "text", 48), ("byline", "author_source_time", "text", 36),
                  ("body", "body_text", "text", 440), ("media", "media_asset", "image", 0),
                  ("sidebar", "sidebar_items", "card_text", 42)],
        "preserve": [{"name": "intentionally_blank_ad", "rect_norm": [0.79, 0.12, 0.96, 0.46], "fill": "template_pixels"}],
        "body_limit": 440,
    },
}

STATUS_BAR_TEMPLATES = {
    "weibo-mobile-text-post.png", "weibo-mobile-image-post.png", "weibo-mobile-home-image-post.png",
    "weibo-hot-search.png", "xiaohongshu-mobile-text.png", "xiaohongshu-mobile-image.png",
    "wechat-mobile-text-article.png", "wechat-mobile-image-article-v1.png",
    "wechat-mobile-image-article-v2.png", "wechat-mobile-feed.png", "douyin-mobile-video.png",
    "douyin-mobile-comments.png", "x-mobile-text-post.png", "x-mobile-image-post.png",
    "instagram-image-post.png",
}
