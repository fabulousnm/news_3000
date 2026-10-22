# UI Reference Templates

Reusable UI reference images generated from the screenshots in `E:/Repos/pictures`. The images preserve recognizable platform/page chrome and replace post/article-specific copy or media with neutral placeholders. They are intended as image attachments for image+text generation; `src/ui_prompt_modes.py` maps compatible layouts to these files.

## Template index

| File | Interface category |
|---|---|
| weibo-mobile-text-post.png | 微博移动端纯文字帖子 |
| weibo-mobile-image-post.png | 微博移动端图文帖子详情 |
| weibo-mobile-home-image-post.png | 微博移动端多帖首页/图文卡片 |
| weibo-hot-search.png | 微博热搜榜 |
| xiaohongshu-mobile-text.png | 小红书移动端文字笔记 |
| xiaohongshu-mobile-image.png | 小红书移动端图文笔记 |
| wechat-mobile-text-article.png | 微信公众号移动端纯文字文章 |
| wechat-mobile-image-article-v1.png | 微信公众号移动端图文文章版式一 |
| wechat-mobile-image-article-v2.png | 微信公众号移动端图文文章版式二 |
| douyin-mobile-video.png | 抖音移动端视频播放 |
| douyin-mobile-comments.png | 抖音移动端评论面板 |
| x-mobile-text-post.png | X/Twitter 移动端纯文字帖子 |
| x-mobile-image-post.png | X/Twitter 移动端图文帖子 |
| facebook-desktop-image-post.png | Facebook 网页端图文帖子 |
| instagram-image-post.png | Instagram 图文帖子 |
| youtube-desktop-watch.png | YouTube 网页端视频播放 |
| xinhua-desktop-article.png | 新华网网页端新闻详情 |
| cctv-desktop-article.png | 央视网网页端新闻详情 |
| peoples-daily-desktop-article.png | 人民网/人民日报网页端新闻详情 |
| reuters-desktop-article.png | Reuters 网页端新闻详情 |
| ap-news-desktop-article.png | AP News 网页端新闻详情 |
| bbc-desktop-article.png | BBC News 网页端新闻详情 |
| cnn-desktop-article.png | CNN 网页端新闻详情 |

These are visual references, not pixel-exact captures. AI editing can introduce small deviations or stray text; review a template before using it as a strict visual target. Original source screenshots remain untouched.
| wechat-mobile-feed.png | 微信公众号移动端多帖封面首页 |

## Prompt-mode allocation

For layout groups backed by one of these real-platform templates, the generator assigns prompt mode once per group and reuses it for all four content variants:

- 60% `image_text`: the prompt asks the image model to use the supplied template image as the visual reference. The JSONL/CSV metadata includes `ui_reference_image` (a repository-relative path), `ui_reference_template`, and `ui_reference_url`. The generation client must attach the local image when calling a model that supports image input.
- 30% `long_quantified`: keeps the existing detailed, measured UI prompt.
- 10% `short_text`: names the specific platform/page and includes the generated copy, with minimal UI direction and no reference image attachment.

Current reference-backed layouts cover 615 of the 1,000 groups; other layout types keep the existing long prompt. The release QA report records the eligible-group allocation and checks the exact 60/30/10 split.
