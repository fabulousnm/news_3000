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

# Image+text templates are skeleton mockups. Each entry names the actual
# semantic slots visible in that file; surrounding chrome remains UI.
TEMPLATE_COMPLETION_GUIDANCE = {
    "weibo-mobile-image-post.png": (
        "补全顶部帖子账号头像、账号名/简介与关注按钮；将正文骨架替换为下方给定文本，并在主图占位处生成与帖子主题相符的虚构配图。补全评论卡片中的头像、昵称、评论和互动数；保留微博导航、底部操作栏及其图标。",
        "Fill the post author's avatar, name/bio, and Follow button. Replace the body skeleton with the supplied copy and create a fictional editorial image matching the post topic in the main media slot. Fill comment-card avatars, names, comments, and counts; preserve Weibo navigation and the bottom action bar.",
    ),
    "weibo-mobile-text-post.png": (
        "补全信息流中各帖的头像、账号名、正文和互动数字；主帖使用下方提供的内容，其他卡片只用提示词提供的字段，不要编造额外新闻。保留顶部微博导航、功能入口、标签栏和底部操作栏。",
        "Fill the feed posts' avatars, account names, copy, and engagement counts. Use the supplied content for the main post; populate other cards only from supplied fields and do not invent additional news. Preserve Weibo navigation, feature shortcuts, tabs, and bottom actions.",
    ),
    "weibo-hot-search.png": (
        "把榜单中每条灰色标题/热度占位替换为下方提供的话题名称和对应热度数值，按原有行序和排名呈现；保留热搜横幅、分类标签、排名序号与彩色趋势标记，不添加未提供的话题。",
        "Replace each gray topic-title and heat-count slot with the supplied topic names and matching heat values, preserving row order and rank. Keep the hot-search banner, category tabs, rank numbers, and colored trend markers; add no unsupplied topics.",
    ),
    "weibo-mobile-home-image-post.png": (
        "补全信息流帖子的头像、账号名、认证标志、关注按钮和正文；将六宫格图片区按帖子主题填入协调一致的虚构配图，只有在提示词明确提供多图内容时才分别呈现。保留推荐/关注导航、关闭控件和底部标签栏。",
        "Fill feed-post avatars, account names, verification marks, Follow buttons, and copy. Populate the six-tile media grid with a coherent fictional image set matching the post topic; use distinct images only when the prompt supplies multiple image subjects. Preserve the feed tabs, dismiss control, and bottom navigation.",
    ),
    "xiaohongshu-mobile-image.png": (
        "补全作者头像和昵称、关注按钮、笔记标题与正文；在大幅主图占位处生成与笔记主题相符的虚构配图，并填入已提供的话题标签。补全底部评论输入提示及点赞、收藏、评论数；保留分享图标和小红书版式。",
        "Fill the creator avatar and name, Follow button, note title, and body. Create a fictional image matching the note topic in the large media slot and include supplied hashtags. Fill the bottom comment hint and like, save, and comment counts; preserve the share icon and Xiaohongshu layout.",
    ),
    "xiaohongshu-mobile-text.png": (
        "补全作者头像、昵称、关注按钮、标题、正文和话题标签；评论区只填入提示词明确提供的评论与账号信息。不要把灰色骨架条误当作图片，也不要凭空插入配图；保留底部输入栏、语音/图片入口及互动图标。",
        "Fill the creator avatar, name, Follow button, title, body, and supplied hashtags. Populate comments only with explicitly supplied comment and account fields. Do not treat gray text skeletons as images or invent media; preserve the bottom composer, voice/image controls, and engagement icons.",
    ),
    "wechat-mobile-feed.png": (
        "补全公众号信息流卡片的标题、摘要、封面图及来源/时间等已提供信息；有明确图片占位时生成与对应卡片主题相符的虚构封面。保留卡片数量、卡片顺序、搜索/个人入口和留白，不新增广告或推荐卡片。",
        "Fill each public-account feed card's title, summary, cover, and supplied source/time details. Create a fictional cover matching that card's topic wherever a media slot is shown. Preserve the number and order of cards, search/profile controls, and spacing; add no ads or recommendation cards.",
    ),
    "wechat-mobile-text-article.png": (
        "把顶部标题、作者/来源/时间和正文灰色文字骨架替换为下方给定字段，按文章阅读顺序排版；这张模板是纯文字文章，不要添加图片。补全底部作者信息和已提供的操作数据，保留微信文章工具栏。",
        "Replace the headline, author/source/time, and gray body-text skeletons with the supplied fields in article reading order. This is a text-only article template; add no images. Fill the bottom author details and supplied action counts while preserving the WeChat article toolbar.",
    ),
    "wechat-mobile-image-article-v1.png": (
        "在中央大图占位处生成与文章主题相符的虚构配图；将标题、作者/时间及各段正文骨架替换为给定内容，保留图片轮播指示点。补全底部公众号头像/名称和已提供的互动数据，不增加未提供的段落。",
        "Create a fictional editorial image matching the article topic in the large central media slot. Replace the headline, author/time, and body-text skeletons with supplied content, preserving the image-carousel dots. Fill the bottom account avatar/name and supplied engagement counts; add no unsupplied paragraphs.",
    ),
    "wechat-mobile-image-article-v2.png": (
        "将顶部标题与正文骨架替换为给定内容；两处并排图片占位分别生成与文章主题相符、彼此协调的虚构配图，并用已提供图注填在图片下方。保留段落间距、滚动条和底部公众号互动栏，不把灰色文字条变成图片。",
        "Replace the headline and body skeletons with supplied content. Create two coordinated fictional editorial images matching the article topic in the side-by-side media slots, with supplied captions beneath them. Preserve paragraph spacing, scrollbar, and bottom account/action bar; do not turn gray text bars into images.",
    ),
    "douyin-mobile-video.png": (
        "把屏幕中央视频画面占位替换为与主题相符的虚构新闻/现场画面；补全发布者头像、账号名、关注加号、视频文案及右侧点赞/评论/收藏/分享数。保留抖音竖屏控件、搜索栏和底部导航，不把计数写进视频画面。",
        "Replace the central video-area placeholder with a fictional news/editorial scene matching the topic. Fill the creator avatar/name, follow-plus control, caption, and right-side like/comment/favorite/share counts. Preserve Douyin's vertical controls, search bar, and bottom navigation; keep UI counts outside the video image.",
    ),
    "douyin-mobile-comments.png": (
        "补全评论面板中各评论者头像、昵称、评论正文、时间/回复信息和点赞数，只使用提示词给出的字段；保留上方视频背景、评论抽屉、输入框和图片/@/表情入口。不要将评论文字铺到视频画面上。",
        "Fill comment-panel avatars, names, comment text, time/reply details, and like counts using only supplied fields. Preserve the video background, comments drawer, composer, and image/@/emoji controls. Keep comment text inside the panel, not over the video scene.",
    ),
    "x-mobile-text-post.png": (
        "补全主帖及下方信息流卡片的头像、显示名、账号标识、正文、时间和互动数；关注按钮使用 X 风格的深色胶囊按钮并填入正确语言的按钮文字。保留 X 标志性图标、书签和分享操作，不添加图片。",
        "Fill the main post and feed-card avatars, display names, handles, copy, timestamps, and engagement counts. Use the X-style dark pill for Follow and add its localized label. Preserve X icons, bookmark, and share actions; do not add images.",
    ),
    "x-mobile-image-post.png": (
        "补全作者头像、显示名、账号标识和关注按钮；在中央大幅媒体占位处生成与帖子主题相符的虚构配图，并替换正文骨架及已提供的互动数据。保留 X 的深色关注按钮、回复/转发/点赞/书签/分享图标。",
        "Fill the author avatar, display name, handle, and Follow button. Create a fictional image matching the post topic in the large central media slot, and replace body skeletons and engagement counts with supplied content. Preserve X's dark Follow button and reply/repost/like/bookmark/share icons.",
    ),
    "facebook-desktop-image-post.png": (
        "补全右侧帖子作者头像、姓名、时间、正文、互动摘要和评论列表；中央黑色查看器中的大图占位替换为与帖子主题相符的虚构配图。保留 Facebook 顶栏、查看器背景、右侧栏和评论输入控件；不要将模板中的灰色骨架条作为文字输出。",
        "Fill the right-panel author avatar, name, timestamp, post copy, engagement summary, and comments. Replace the large media slot in the central dark viewer with a fictional image matching the post topic. Preserve Facebook's top bar, viewer background, right panel, and comment composer; do not render gray skeleton bars as literal text.",
    ),
    "instagram-image-post.png": (
        "在左侧大幅媒体区域生成与帖子主题相符的虚构图片；补全右侧作者头像/账号名、配文、评论及点赞/评论/转发/收藏数据。保留 Instagram 左侧导航和帖子卡片布局，不让文字覆盖主图。",
        "Create a fictional image matching the post topic in the large left media area. Fill the right-panel avatar/username, caption, comments, and like/comment/share/save counts. Preserve Instagram's left navigation and post-card layout; keep text out of the main image.",
    ),
    "youtube-desktop-watch.png": (
        "在左侧主播放器区域生成与视频主题相符的虚构新闻视频画面；补全视频标题、频道头像/名称、订阅按钮和已提供的互动数据。右侧推荐列表补全缩略图、标题与频道信息，内容只从已给字段推导。保留 YouTube 顶栏和播放器/推荐栏比例。",
        "Create a fictional news-video frame matching the topic in the large left player. Fill the title, channel avatar/name, Subscribe button, and supplied engagement details. Populate right-side recommendations with thumbnails, titles, and channel details derived only from supplied fields. Preserve YouTube's top bar and player/recommendation proportions.",
    ),
    "ap-news-desktop-article.png": (
        "将页面上明确写着“Headline placeholder”的位置替换为给定新闻标题，将“Image placeholder”区域替换为主题相关的虚构新闻配图；把正文灰色骨架替换为给定文章内容。保留 AP 页眉导航、黑色标题区、广告栏位置和页面宽度，不保留 placeholder 字样。",
        "Replace the visible “Headline placeholder” with the supplied headline and the “Image placeholder” region with a fictional editorial image matching the story. Replace gray body skeletons with supplied article text. Preserve AP's header/navigation, dark headline band, ad-column position, and page width; do not retain placeholder wording.",
    ),
    "bbc-desktop-article.png": (
        "将“Headline placeholder”替换为给定标题，将中央“Image placeholder”替换为与报道主题相符的虚构新闻图片；正文骨架只替换为给定段落。保留 BBC 页眉、标题字体层级、分享/收藏控件和文章列宽，不添加侧栏或多余新闻卡片。",
        "Replace “Headline placeholder” with the supplied headline and the central “Image placeholder” with a fictional editorial image matching the story. Use supplied paragraphs for the body skeletons. Preserve the BBC masthead, headline hierarchy, share/save controls, and article-column width; add no sidebar or extra news cards.",
    ),
    "cctv-desktop-article.png": (
        "把标题区“此处是标题”和中央“此处是插图”分别替换为给定标题及主题相关的虚构新闻配图；正文灰色骨架替换为给定文章内容。保留央视网双层导航、栏目路径、来源时间、右侧悬浮工具和原有版心。",
        "Replace “此处是标题” with the supplied headline and the central “此处是插图” with a fictional editorial image matching the story. Replace gray body skeletons with supplied article text. Preserve CCTV's two-level navigation, breadcrumbs, source/time line, floating side tools, and content width.",
    ),
    "peoples-daily-desktop-article.png": (
        "将“此处是标题”、正文骨架和明确标记的“此处是插图”替换为给定标题、文章段落及主题相关的虚构配图；补全右侧排行中的标题与配图，仅使用提供的内容。保留人民网标志、导航、收藏/字号控件、右侧工具条与广告区域原位，不把广告位当成新闻插图。",
        "Replace “此处是标题,” body skeletons, and the explicit “此处是插图” slot with the supplied headline, paragraphs, and a fictional editorial image matching the story. Fill right-side ranking titles/images only from supplied content. Preserve the People.cn logo, navigation, save/font controls, floating tools, and ad slot in place; do not treat the ad slot as a news image.",
    ),
    "reuters-desktop-article.png": (
        "将“Headline placeholder”替换为给定标题，将主栏“Image placeholder”替换为主题相关的虚构新闻配图，正文骨架替换为给定段落。保留 Reuters/LSEG 顶栏、导航、书签/字号/分享控件和文章列宽；不要生成额外财经数据或行情图。",
        "Replace “Headline placeholder” with the supplied headline, the main-column “Image placeholder” with a fictional editorial image matching the story, and body skeletons with supplied paragraphs. Preserve the Reuters/LSEG bars, navigation, bookmark/font/share controls, and article-column width; add no financial data or charts.",
    ),
    "cnn-desktop-article.png": (
        "将画面中“Headline placeholder”替换为给定标题，将主栏媒体占位替换为与报道主题相符的虚构新闻配图；正文骨架替换为给定内容。保留 CNN 顶部导航、社交分享按钮、右侧栏与图片标题条，不将右侧空广告框改成正文图片。",
        "Replace “Headline placeholder” with the supplied headline, the main-column media slot with a fictional editorial image matching the story, and body skeletons with supplied copy. Preserve CNN's top navigation, social-share buttons, right column, and image-caption bar; do not turn the empty right-side ad box into the article image.",
    ),
    "xinhua-desktop-article.png": (
        "补全新华网页面标题、正文段落和右侧明确的插图/推荐卡片占位；主插图须与报道主题相符，侧栏只使用给定的摘要/推荐字段。保留新华网标志、蓝色顶栏、栏目导航、来源时间、字号与分享控件及二维码区域，不把二维码改写或生成新的可扫描码。",
        "Fill the Xinhua headline, article paragraphs, and explicit right-column image/recommendation slots. The main image should match the story; use only supplied summaries/recommendation fields in the sidebar. Preserve the Xinhua logo, blue masthead, section navigation, source/time, font/share controls, and QR-code area; do not alter or create a scannable code.",
    ),
}


def template_completion_guidance(reference, language):
    """Return template-specific instructions for the attached-image mode."""
    instructions = TEMPLATE_COMPLETION_GUIDANCE.get(reference.get("file"))
    if not instructions:
        return ""
    return instructions[1 if language == "en" else 0]


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
    completion = template_completion_guidance(reference, language)
    common_completion_zh = (
        "将模板中明确表示内容占位的灰色骨架文字替换为下方给出的对应内容；明确的媒体/封面/视频画面占位应补入与主题相符的虚构配图。"
        "只替换内容占位，保留灰色背景、分隔线、按钮底色、图标、导航和控件。严格使用给定正文、标题、标签及数字，不删改、不重排、不自行添加事实或数据。"
        "忽略参考图上的生图工具水印、压缩痕迹或其他后期叠加标记，不要复刻进结果。"
    )
    common_completion_en = (
        "Replace gray skeletons that clearly mark content slots with the corresponding supplied copy; fill explicit media/cover/video slots with a fictional image relevant to the topic. "
        "Replace content placeholders only; preserve gray backgrounds, separators, button fills, icons, navigation, and controls. Use supplied headlines, body, tags, and numbers exactly without omission, reordering, or invented facts/data. "
        "Ignore image-generator watermarks, compression artifacts, and other post-production overlays in the reference; do not reproduce them. "
    )
    if language == "en":
        body = f'Fictitious outlet "{outlet}" reporting on "{title}". All depicted organisations, places and people are fictional.\n{content}'
        if mode == "image_text":
            return (f'Use the attached image as the UI reference and reproduce its visible platform/page interface as closely as possible. '
                    f'Keep the logo, navigation, controls, spacing and overall composition. {common_completion_en}{completion} '
                    f'Replace the post/article content with the following. '
                    f'{reference_line_en}{body}')
        return (f'Imitate the {group["platform_family"].replace("_", " ")} interface and preserve its recognizable UI and logo. '
                f'Create a post/article for the fictional outlet "{outlet}" about "{title}". '
                f'All depicted organisations, places and people are fictional.\n{content}')
    body = f'虚构媒体「{outlet}」发布「{title}」。画面中的机构、地名、人名均为虚构。\n{content}'
    if mode == "image_text":
        return (f"请把随附图片作为界面参考，尽可能贴近复现其中的平台/网页UI。保留logo、导航、固定控件、间距与整体构图，只替换帖子或文章内容。\n"
                f"{common_completion_zh}{completion}\n{reference_line_zh}{body}")
    platform = PLATFORM_NAMES.get(reference.get("file"), "现实媒体平台界面")
    return (f"请模仿{platform}，保留其标志性UI和logo，生成一篇关于「{title}」的帖子或新闻。"
            f"画面中的机构、地名、人名均为虚构。\n{content}")
