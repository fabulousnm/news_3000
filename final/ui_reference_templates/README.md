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

For image+text and long prompt modes, the matching PNG is attached as a visual reference. Short prompts identify the exact platform and ask for a 1:1 recreation without attaching a template image. Prompts supply visible copy, randomized device status values, and unique fictional comments where applicable. The model generates the complete screenshot in one image; there is no separate media-only queue or post-generation UI compositor. Douyin video prompts fill the bottom search box with a white story-related phrase. CNN's upper-right and AP News' right-side gray ad blocks are filled with Ads images.

## Image+text placeholder completion

The image+text mode exports complete-image prompts with the matching reference PNG attached. Each template has its own written guidance so the model can fill the visible text skeletons, image panels, and thumbnails while retaining the page structure. CNN and AP News ad blocks are designated for Ads images, not left as gray placeholders.
| wechat-mobile-feed.png | 微信公众号移动端多帖封面首页 |

## Prompt-mode allocation

For layout groups backed by one of these real-platform templates, the generator assigns prompt mode once per group and reuses it for all four content variants:

- 60% `image_text`: a full natural-language screenshot prompt with a template-specific completion guide and attached reference image.
- 30% `long_quantified`: retains the detailed body and adds the same template-specific visual direction and attached reference image.
- 10% `short_text`: a concise natural-language prompt naming the specific template and includes the generated copy; its matching reference image is attached as well.

Current reference-backed layouts cover 615 of the 1,000 groups; other layout types keep the existing long prompt. The release QA report records the eligible-group allocation and checks the exact 60/30/10 split.
