"""Prompt styles and reusable visual references for real platform UIs."""

from pathlib import Path
import copy
import re

from common import rng_for
from ui_template_specs import STATUS_BAR_TEMPLATES
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

PLATFORM_NAMES_EN = {
    "weibo-mobile-text-post.png": "Weibo mobile text-post interface",
    "weibo-mobile-image-post.png": "Weibo mobile image-post detail interface",
    "weibo-mobile-home-image-post.png": "Weibo mobile feed with image-grid cards",
    "weibo-hot-search.png": "Weibo hot-search ranking page",
    "xiaohongshu-mobile-text.png": "Xiaohongshu mobile text-note interface",
    "xiaohongshu-mobile-image.png": "Xiaohongshu mobile image-note interface",
    "wechat-mobile-text-article.png": "WeChat public-account text article",
    "wechat-mobile-image-article-v1.png": "WeChat public-account image article",
    "wechat-mobile-image-article-v2.png": "WeChat public-account image article with a two-image row",
    "wechat-mobile-feed.png": "WeChat public-account mobile feed",
    "douyin-mobile-video.png": "Douyin mobile video screen",
    "douyin-mobile-comments.png": "Douyin mobile video with its comments drawer open",
    "x-mobile-text-post.png": "X mobile text-post interface",
    "x-mobile-image-post.png": "X mobile image-post interface",
    "facebook-desktop-image-post.png": "Facebook desktop image-post interface",
    "instagram-image-post.png": "Instagram image-post interface",
    "youtube-desktop-watch.png": "YouTube desktop watch page",
    "xinhua-desktop-article.png": "Xinhua desktop news article page",
    "cctv-desktop-article.png": "CCTV desktop news article page",
    "peoples-daily-desktop-article.png": "People's Daily desktop news article page",
    "reuters-desktop-article.png": "Reuters desktop news article page",
    "ap-news-desktop-article.png": "AP News desktop article page",
    "bbc-desktop-article.png": "BBC News desktop article page",
    "cnn-desktop-article.png": "CNN desktop article page",
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
        "补全作者头像、昵称、关注按钮、标题、正文和话题标签；评论区使用虚构普通用户账号和简短口语评论，像读者即时反应、疑问或个人感受，不得复述或扩写正文，不得使用媒体/机构/官方账号。每条评论下方显示随机国内 IP 省份、评论时间及提示词给定的点赞数。所有灰色文字骨架、灰色图片/缩略图占位均须按槽位填入内容或主题相关的虚构配图，不得残留空灰块；保留底部输入栏、语音/图片入口及互动图标。",
        "Fill the creator avatar, name, Follow button, title, body, and supplied hashtags. Use unique fictional ordinary-user accounts and distinct short conversational comments that read as immediate reactions, questions, or personal impressions; do not repeat or extend the article and do not use media, institutional, or official accounts. Add a randomized domestic Chinese province for Chinese copy or an overseas location for English copy, plus a comment time and like count beneath each comment. Fill every gray text skeleton and gray image/thumbnail placeholder with corresponding content or a topic-relevant fictional image; leave no empty gray content placeholder. Preserve the bottom composer, voice/image controls, and engagement icons.",
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
        "把屏幕中央视频画面占位替换为与主题相符的新闻/现场配图；补全发布者头像、账号名、关注加号、视频文案及右侧点赞/评论/收藏/分享数。将屏幕最下方搜索框填入与标题和正文直接相关的简短关键词，文字用白色并清晰可读；关键词内容照录提示中的“搜索框文案”字段。保留抖音竖屏控件、搜索框和底部导航，不把计数写进视频画面。",
        "Replace the central video-area placeholder with a news/editorial image matching the topic. Fill the creator avatar/name, follow-plus control, caption, and right-side like/comment/favorite/share counts. Put a short search phrase directly related to the headline and body in the bottom search box, in clear white text; use the supplied “Search-box text” field verbatim. Preserve Douyin's vertical controls, search box, and bottom navigation; keep UI counts outside the video image.",
    ),
    "douyin-mobile-comments.png": (
        "将评论抽屉上方的大块灰色视频画面替换为与正文事件直接相关的新闻配图，不得保留灰块，也不得生成与事件无关的画面。补全评论面板中各评论者头像、昵称、评论正文、时间/回复信息和点赞数；评论账号必须是虚构普通用户，评论短而口语化，像真实读者的即时反应、疑问或个人感受，不得复述/延伸正文，不使用媒体、机构或官方账号。每条评论下方显示随机国内 IP 省份及评论时间，使用下方提示数据给出的评论点赞数。将“大家都在搜”后的搜索占位填为与标题相关的蓝色关键词，例如“大家都在搜：土耳其地震”。所有灰色文字骨架、图片/视频缩略图占位都必须填满，不得留下空灰块；保留评论抽屉、输入框和图片/@/表情入口，评论文字不得覆盖上方配图。",
        "Replace the large gray video area above the comments drawer with a news image directly related to the story; do not leave it gray or generate unrelated imagery. Fill comment-panel avatars, names, comment text, time/reply details, and like counts. Commenters must be fictional ordinary users; comments should be short and conversational, like immediate reader reactions, questions, or impressions, without repeating/extending the article or using media, institutional, or official accounts. Show a randomized domestic Chinese IP province and comment time beneath each comment, using the comment-like counts supplied in the prompt. Replace the search placeholder after '大家都在搜' with a blue topic keyword derived from the headline. Fill every gray text skeleton and image/video thumbnail placeholder; leave no empty gray blocks. Preserve the comments drawer, composer, and image/@/emoji controls, keeping comments within the drawer and the image above it.",
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
        "在左侧主播放器区域生成与视频主题相符的虚构新闻视频画面；补全视频标题、频道头像/名称、订阅按钮和 CSV 已提供的互动数据。右侧每条可见推荐都须填入完整缩略图、标题、频道名及播放量；不足的推荐文案可根据新闻主题生成简短虚构标题，不得留下灰色骨架条或空白缩略图。保留 YouTube 顶栏和播放器/推荐栏比例。",
        "Create a fictional news-video frame matching the topic in the large left player. Fill the title, channel avatar/name, Subscribe button, and CSV-supplied engagement details. Every visible recommendation must have a complete thumbnail, title, channel name, and view count. If recommendation copy is unavailable, create brief fictional adjacent-topic titles. Do not leave gray skeleton bars or blank thumbnails. Preserve YouTube's top bar and player/recommendation proportions.",
    ),
    "ap-news-desktop-article.png": (
        "将页面上明确写着“Headline placeholder”的位置替换为给定新闻标题，将“Image placeholder”区域替换为主题相关的新闻配图；把正文灰色骨架替换为给定文章内容。右侧灰色广告区块替换为一张带有“Ads”标识的广告图片，保留广告区域原位置和尺寸，不得留下灰块，也不得把广告图当成新闻配图。保留 AP 页眉导航、黑色标题区和页面宽度，不保留 placeholder 字样。",
        "Replace the visible “Headline placeholder” with the supplied headline and the “Image placeholder” region with an editorial image matching the story. Replace gray body skeletons with supplied article text. Replace the gray block on the right with an advertisement image marked “Ads,” retaining the ad area's original position and dimensions; do not leave a gray block or treat the ad as editorial media. Preserve AP's header/navigation, dark headline band, and page width; do not retain placeholder wording.",
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
        "将“此处是标题”、正文骨架和明确标记的“此处是插图”替换为给定标题、文章段落及主题相关的虚构配图；补全右侧排行中的标题与配图。右侧灰色广告位填入虚构广告图文，广告区域保持原位、尺寸和广告标识，不得留空，也不得当作新闻插图。保留人民网标志、导航、收藏/字号控件和右侧工具条。",
        "Replace “此处是标题,” body skeletons, and the explicit “此处是插图” slot with the supplied headline, paragraphs, and a fictional editorial image matching the story. Fill right-side ranking titles/images. Populate any gray ad slot with fictional ad imagery and copy, retaining its original position, dimensions, and ad label; do not leave it blank or treat it as a news image. Preserve the People.cn logo, navigation, save/font controls, and floating tools.",
    ),
    "reuters-desktop-article.png": (
        "将“Headline placeholder”替换为给定标题，将主栏“Image placeholder”替换为主题相关的虚构新闻配图，正文骨架替换为给定段落。保留 Reuters/LSEG 顶栏、导航、书签/字号/分享控件和文章列宽；不要生成额外财经数据或行情图。",
        "Replace “Headline placeholder” with the supplied headline, the main-column “Image placeholder” with a fictional editorial image matching the story, and body skeletons with supplied paragraphs. Preserve the Reuters/LSEG bars, navigation, bookmark/font/share controls, and article-column width; add no financial data or charts.",
    ),
    "cnn-desktop-article.png": (
        "将画面中“Headline placeholder”替换为给定标题，将主栏媒体占位替换为主题相关的新闻配图；正文骨架替换为给定内容。将右上角灰色广告占位替换为一张带有“Ads”标识的广告图片，保留广告区域原位置和尺寸，不得留下灰块，也不得挪作正文图片。保留 CNN 顶部导航、社交分享按钮、右侧栏与图片标题条。",
        "Replace “Headline placeholder” with the supplied headline, the main-column media slot with an editorial image matching the story, and body skeletons with supplied copy. Replace the gray ad placeholder in the upper-right corner with an advertisement image marked “Ads,” preserving its original position and dimensions; do not leave a gray block or use the ad as article media. Preserve CNN's top navigation, social-share buttons, right column, and image-caption bar.",
    ),
    "xinhua-desktop-article.png": (
        "补全新华网页面标题、正文段落和右侧明确的插图/推荐卡片占位；主插图须与报道主题相符，侧栏只使用给定的摘要/推荐字段。保留新华网标志、蓝色顶栏、栏目导航、来源时间、字号与分享控件及二维码区域，不把二维码改写或生成新的可扫描码。",
        "Fill the Xinhua headline, article paragraphs, and explicit right-column image/recommendation slots. The main image should match the story; use only supplied summaries/recommendation fields in the sidebar. Preserve the Xinhua logo, blue masthead, section navigation, source/time, font/share controls, and QR-code area; do not alter or create a scannable code.",
    ),
}


def template_completion_guidance(reference, language):
    """Return template-specific completion instructions for the selected template."""
    instructions = TEMPLATE_COMPLETION_GUIDANCE.get(reference.get("file"))
    if not instructions:
        return ""
    fixed_rules = instructions[1 if language == "en" else 0]
    if reference.get("file") in {"douyin-mobile-comments.png", "xiaohongshu-mobile-text.png"}:
        fixed_rules += (" Every fictional commenter account and every comment body must be unique within this image; "
                        "each comment must include its separately supplied IP location, time, and like count."
                        if language == "en" else
                        " 同一张图内每个虚构账户昵称和评论内容都必须互不重复；每条评论分别使用脚本提供的 IP 属地、时间和点赞数。")
    ad_templates = {"cnn-desktop-article.png", "ap-news-desktop-article.png"}
    blank_rule = (
        " Fill the specified ad slot with its Ads image; preserve only other areas explicitly designated as intentionally blank."
        if language == "en" and reference.get("file") in ad_templates else
        " 广告位必须填入指定的 Ads 广告图片；只有其他明确标注为有意留空的区域才保持空白。"
        if reference.get("file") in ad_templates else
        " Keep any area explicitly described as intentionally blank unchanged."
        if language == "en" else
        "明确说明有意留空的区域保持空白。"
    )
    if language == "en":
        return (
            "For this exact template, " + fixed_rules + " "
            "Fill every gray content placeholder in place, including text skeletons, image panels, and thumbnails." + blank_rule + " "
            "Match the reference composition, slot positions, and proportions; do not add, remove, or move interface elements."
        )
    return (
        "针对这张模板图片：" + fixed_rules + " "
        "把所有表示内容的灰色占位都在原位置补全，包括文字骨架、图片框和缩略图；" + blank_rule + " "
        "按参考图复现整张界面的构图、版位和比例，不要增删或移动界面元素。"
    )


def reference_layout_instruction(reference, language):
    """Natural-language direction to generate a complete screenshot from a template."""
    template = reference.get("file", "")
    platform = (PLATFORM_NAMES_EN if language == "en" else PLATFORM_NAMES).get(template, "platform")
    completion = template_completion_guidance(reference, language)
    if language == "en":
        return (f"Create one complete screenshot of the {platform} shown in the attached reference. "
                "Use the reference as the visual guide and recreate the entire screen, including its interface, "
                "rather than making a separate media asset or a cropped component. " + completion)
    return (f"请根据随附参考图，生成一张完整的{platform}截图。参考图用于确定整张界面的外观和布局，"
            "请绘制完整页面，而不是单独生成配图素材或局部裁切。" + completion)


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


def compact_location_label(value, language, limit):
    """Keep a location label concise without cutting a word or parenthesis."""
    value = re.sub(r"\s+", " ", str(value or "")).strip()
    if len(value) <= limit:
        return value
    chinese = language != "en"
    disputed = any(token in value for token in (
        "另有说法", "另有說法", "alternate account", "alternate location",
    ))
    if chinese:
        if "土耳其" in value or "叙利亚" in value:
            base = "土叙边境附近" if disputed else "土耳其叙利亚边境"
        elif "肯尼迪" in value or "佛罗里达" in value:
            base = "肯尼迪航天中心"
        elif "日内瓦" in value:
            base = "日内瓦"
        else:
            return ""
        suffix = "（另有说法）" if disputed else ""
        candidate = base + suffix
    else:
        if "geneva" in value.casefold():
            base = "Geneva"
        elif "kennedy" in value.casefold() or "florida" in value.casefold():
            base = "Kennedy Space Ctr"
        elif "türkiye" in value.casefold() or "turkiye" in value.casefold() or "syria" in value.casefold():
            base = "Türkiye-Syria border"
        else:
            return ""
        candidate = base + (" (disputed)" if disputed else "")
    return candidate if len(candidate) <= limit else ""


def topic_search_phrase(title, language):
    """Create a short, complete topic query from a story headline."""
    title = re.sub(r"\s+", " ", str(title or "")).strip(" \t\r\n，。！？；：、,.!?;:—-()（）[]【】\"'")
    if not title:
        return "热点新闻" if language != "en" else "Latest news"
    normalized = title.casefold()
    # Prefer complete topic phrases. Prefix slicing used to leave dangling
    # fragments such as “发生7.8” and “public health”.
    if language != "en":
        if "阿尔忒弥斯" in title or "nasa" in normalized:
            return "NASA阿尔忒弥斯一号"
        if ("土耳其" in title or "叙利亚" in title) and "地震" in title:
            return "土耳其叙利亚地震"
        if "世卫组织" in title and "新冠" in title:
            return "世卫组织新冠疫情"
    else:
        if "artemis" in normalized or "nasa" in normalized:
            return "NASA launches Artemis I mission"
        if "earthquake" in normalized and any(x in normalized for x in ("türkiye", "turkiye", "syria")):
            return "Türkiye-Syria 7.8 earthquake"
        if "who" in normalized and ("covid" in normalized or "coronavirus" in normalized):
            return "WHO COVID-19 emergency"
    if language != "en":
        compact = re.sub(r"\s+", "", title)
        return compact[:14].rstrip("，。！？；：、,.!?;:—-")
    return " ".join(title.split()[:5]).rstrip(" ,.:;-—")


def _parse_comment_line(line, chinese):
    parts = line.split(" | ")
    if chinese:
        return {
            "account": parts[0].split(":", 1)[0],
            "body": parts[0].split(":", 1)[1].strip(),
            "ip_location": parts[1].removeprefix("IP属地 "),
            "time": parts[2].removeprefix("评论时间 "),
            "likes": int(parts[3].removeprefix("评论赞数 ")),
        }
    return {
        "account": parts[0].split(":", 1)[0],
        "body": parts[0].split(":", 1)[1].strip(),
        "ip_location": parts[1].removeprefix("Location "),
        "time": parts[2].removeprefix("Time "),
        "likes": int(parts[3].removeprefix("Likes ")),
    }


def reference_overrides(group, fields, reference, language, image_key=None):
    """Make synthetic device/comment metadata without changing CSV publication data."""
    template = reference.get("file", "")
    status_templates = {
        "weibo-mobile-text-post.png", "weibo-mobile-image-post.png", "weibo-mobile-home-image-post.png",
        "weibo-hot-search.png", "xiaohongshu-mobile-text.png", "xiaohongshu-mobile-image.png",
        "wechat-mobile-text-article.png", "wechat-mobile-image-article-v1.png",
        "wechat-mobile-image-article-v2.png", "wechat-mobile-feed.png", "douyin-mobile-video.png",
        "douyin-mobile-comments.png", "x-mobile-text-post.png", "x-mobile-image-post.png",
        "instagram-image-post.png",
    }
    comment_templates = {"douyin-mobile-comments.png", "xiaohongshu-mobile-text.png"}
    if template not in status_templates and template not in comment_templates:
        return ""
    rng = rng_for("reference-ui-details", group["group_id"], image_key or group["group_id"], template)
    chinese = language != "en"
    provinces = ["北京", "上海", "广东", "四川", "浙江", "江苏", "湖北", "陕西", "山东", "福建"]
    places = ["London", "Toronto", "Sydney", "Berlin", "Singapore", "New York", "Paris", "Seoul"]
    reactions_zh = ["刚刷到这个消息，等后续更新。", "希望有更清楚的说明。", "先看看后面怎么发展。", "这个时间点确实挺让人意外。", "有人知道后续情况吗？"]
    reactions_en = ["Just saw this update; waiting for more details.", "Hope they share a clearer update soon.", "Let's see what the next update says.", "That timing is surprising.", "Does anyone know what happens next?"]
    aliases_zh = ["路过的阿岚", "柚子汽水", "海边散步", "小周同学", "云朵慢慢", "橘子汽水"]
    aliases_en = ["Maya R.", "Alex K.", "Sam Rivera", "Jamie L.", "Taylor W.", "Casey M."]
    comments = []
    comment_accounts, comment_bodies = [], []
    if template in comment_templates:
        for field in fields:
            key = field.get("key", "").lower()
            is_xhs_post = template == "xiaohongshu-mobile-text.png" and key.startswith("post")
            if ("comment" in key or is_xhs_post) and (key.endswith("_account") or key.endswith("_author") or key == "comment_account"):
                comment_accounts.append(field)
            elif ("comment" in key or is_xhs_post) and (key.endswith("_body") or key.endswith("_text") or key == "comment_body"):
                comment_bodies.append(field)
    alias_pool = aliases_en if not chinese else aliases_zh
    reaction_pool = reactions_en if not chinese else reactions_zh
    needed = max(len(comment_accounts), len(comment_bodies), 3 if template in comment_templates else 0)
    aliases = rng.sample(alias_pool, min(needed, len(alias_pool)))
    reactions = rng.sample(reaction_pool, min(needed, len(reaction_pool)))
    for index in range(max(len(comment_accounts), len(comment_bodies))):
        alias = aliases[index % len(aliases)]
        reaction = reactions[index % len(reactions)]
        if index < len(comment_accounts):
            comment_accounts[index]["value"] = alias
        if index < len(comment_bodies):
            comment_bodies[index]["value"] = reaction
        ip = rng.choice(places if not chinese else provinces)
        when = f"{rng.randrange(1, 12)}mo" if not chinese else f"{rng.randrange(1, 13)}月{rng.randrange(1, 29)}日"
        likes = rng.randrange(3, 500)
        comments.append((f"{alias}: {reaction} | IP属地 {ip} | 评论时间 {when} | 评论赞数 {likes}") if chinese
                        else f"{alias}: {reaction} | Location {ip} | Time {when} | Likes {likes}")
    if template in comment_templates and not comments:
        for index in range(3):
            alias = aliases[index]
            reaction = reactions[index]
            ip = rng.choice(places if not chinese else provinces)
            when = f"{rng.randrange(1, 12)}mo" if not chinese else f"{rng.randrange(1, 13)}月{rng.randrange(1, 29)}日"
            likes = rng.randrange(3, 500)
            comments.append((f"{alias}: {reaction} | IP属地 {ip} | 评论时间 {when} | 评论赞数 {likes}") if chinese
                            else f"{alias}: {reaction} | Location {ip} | Time {when} | Likes {likes}")
    # These template assets show a status time and battery, but no date slot.
    # Publication timestamps remain source data and are never randomized.
    status_data = ({"time": f"{rng.randrange(24):02d}:{rng.randrange(60):02d}",
                    "battery_percent": rng.randrange(28, 100)} if template in STATUS_BAR_TEMPLATES else None)
    status = f"{status_data['time']}, {status_data['battery_percent']}% battery" if status_data else ""
    status_line = ((f"设备状态栏值（供准确排版）：{status}；模板无状态栏日期字段，不生成日期，不改变 CSV 新闻发布时间。")
                   if chinese and status_data else
                   (f"Status-bar values for exact layout: {status}; this template has no status-bar date slot, and the CSV publication timestamp stays unchanged.")
                   if status_data else "")
    search_phrase = (
        group["meta"].get("subject_title", "") if template == "douyin-mobile-comments.png"
        else topic_search_phrase(group["meta"].get("subject_title", ""), language)
        if template == "douyin-mobile-video.png" else ""
    )
    group["_ui_render_data"] = {
        "status_bar": status_data,
        "publication_time_source": "csv",
        "engagement_metrics_source": "csv",
        "comments": [_parse_comment_line(line, chinese) for line in comments],
        "search_phrase": search_phrase,
        "search_phrase_color": ("platform_blue" if template == "douyin-mobile-comments.png" else "platform_white") if search_phrase else None,
    }
    if comments:
        if template == "xiaohongshu-mobile-text.png":
            label = "虚构普通用户评论及逐条随机 IP 属地、时间、赞数" if chinese else "Fictional ordinary-user comments with per-comment randomized IP location, time, and likes"
        else:
            label = "虚构普通用户评论及逐条随机 IP 属地、时间、赞数" if chinese else "Fictional ordinary-user comments with per-comment randomized IP location, time, and likes"
        search = (f"蓝色搜索词：{search_phrase}" if search_phrase and chinese
                  else f"Blue search phrase: {search_phrase}" if search_phrase else "")
        return status_line + "\n" + label + ":\n" + "\n".join(comments) + ("\n" + search if search else "")
    return status_line


def build_reference_prompt(group, fields, reference, language, mode, image_key=None):
    """Build either attachment-led prose or the deliberately short text prompt."""
    fields = copy.deepcopy(fields)
    if reference.get("file") == "douyin-mobile-video.png":
        from render import _trim_coherent

        short_keys = {"body_text", "caption_text", "location", "location_label", "audio_name",
                      "like_metric", "comment_metric", "share_metric", "save_metric", "view_metric",
                      "search_phrase"}
        fields = [f for f in fields if f.get("key") in short_keys]
        for field in fields:
            if field.get("key") in {"body_text", "caption_text"}:
                field["value"] = _trim_coherent(
                    field.get("value", ""), 42 if language != "en" else 42, language
                )
            elif field.get("key") in {"location", "location_label"}:
                field["value"] = compact_location_label(
                    field.get("value", ""), language, 18 if language != "en" else 32
                )
            elif field.get("key") == "audio_name":
                cap = 24 if language != "en" else 40
                value = str(field.get("value", "")).strip()
                field["value"] = value if len(value) <= cap else ("原声" if language != "en" else "Original audio")
        fields = [f for f in fields if f.get("value")]
    if reference.get("file") == "xiaohongshu-mobile-text.png":
        fields = [f for f in fields if not (f.get("key", "").startswith("post") and f.get("key", "").endswith("_body2"))]
    status_templates = {
        "weibo-mobile-text-post.png", "weibo-mobile-image-post.png", "weibo-mobile-home-image-post.png",
        "weibo-hot-search.png", "xiaohongshu-mobile-text.png", "xiaohongshu-mobile-image.png",
        "wechat-mobile-text-article.png", "wechat-mobile-image-article-v1.png",
        "wechat-mobile-image-article-v2.png", "wechat-mobile-feed.png", "douyin-mobile-video.png",
        "douyin-mobile-comments.png", "x-mobile-text-post.png", "x-mobile-image-post.png",
        "instagram-image-post.png",
    }
    if reference.get("file") in status_templates:
        fields = [f for f in fields if f.get("key") not in {"device_time", "status_icons"}]
    extra_content = reference_overrides(group, fields, reference, language, image_key=image_key)
    content = concise_content(fields, language)
    if extra_content:
        content += "\n" + extra_content
    title = group["meta"].get("subject_title", "")
    outlet = group["meta"].get("outlet_name", "")
    url = reference.get("url", "")
    reference_line_zh = (
        f"参考网页：{url}\n若无法访问该网站，则忽略此网址\n" if url else ""
    )
    reference_line_en = (
        f"Reference page: {url}\nIf the page cannot be accessed, ignore this URL.\n" if url else ""
    )
    layout_instruction = reference_layout_instruction(reference, language)
    if mode == "short_text":
        guide = TEMPLATE_COMPLETION_GUIDANCE.get(reference.get("file"), ("", ""))[0 if language != "en" else 1]
        guide = guide.split("；", 1)[0].split(". ", 1)[0].rstrip("。.")
        template = reference.get("file")
        platform = PLATFORM_NAMES_EN.get(template, "social-media interface") if language == "en" else PLATFORM_NAMES.get(template, "社交平台界面")
        special = {
            "douyin-mobile-video.png": "Put the supplied search-box text in clear white lettering." if language == "en" else "底部搜索框使用白色文字呈现下方搜索框文案。",
            "cnn-desktop-article.png": "Replace the upper-right gray ad slot with an image marked ‘Ads’." if language == "en" else "右上角灰色广告位替换为带有“Ads”标识的广告图片。",
            "ap-news-desktop-article.png": "Replace the right-side gray block with an image marked ‘Ads’." if language == "en" else "右侧灰色区块替换为带有“Ads”标识的广告图片。",
        }.get(template, "")
        if language == "en":
            return (f"Please recreate the {platform.removesuffix(' interface')} screenshot as a 1:1 match. {guide} {special} "
                    f"Use the supplied headline and visible copy exactly; keep publication time and engagement counts unchanged.\n{content}")
        platform = platform.removesuffix("界面")
        return (f"请你1：1复刻{platform}界面截图。{guide}。{special}标题及下方可见内容按提供文字呈现，新闻发布时间和互动数字保持原值。\n{content}")
    if language == "en":
        body = f'"{outlet}" reporting on "{title}". All depicted organisations, places and people are fictional.\n{content}'
        return (f"{layout_instruction}\n{reference_line_en}{body}\n"
                "Render the supplied visible text as written. Keep the CSV publication time and engagement counts unchanged; "
                "use only the separately supplied randomized device status values where the template has those fields. "
                "Do not reproduce generator watermarks or unrelated marks from the reference.")
    body = f'「{outlet}」发布「{title}」。画面中的机构、地名、人名均为虚构。\n{content}'
    return (f"{layout_instruction}\n{reference_line_zh}{body}\n"
            "请把下方可见文字按给定内容呈现在画面中。CSV 新闻发布时间和互动数字保持原值；"
            "只有模板确有对应状态栏字段时才使用单独提供的随机设备状态值。不要把生成器水印或参考图上的无关痕迹画进结果。")
