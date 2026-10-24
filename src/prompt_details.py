"""Additional prompt-detail blocks.

The original prompt described the carrier, layout and content but left several
dimensions unspecified, which let the model under-deliver on text density,
mis-render the capture style, or add unrequested visual elements. These blocks
are appended to every prompt.

Everything here is derived from the frozen configuration, so the wording stays
consistent across the 3000 samples.
"""

# Capture-style descriptions, keyed by the value stored in the record.
CAPTURE_DETAIL = {
    "native_screenshot": (
        "整体为设备原生素材截图，界面元素边缘锐利，无拍摄痕迹、无反光、无透视倾斜，"
        "画面四边与设备屏幕边缘对齐"
    ),
    "photo_of_screen": (
        "整体为手机翻拍屏幕的实拍照片，可见轻微的环境反光与约十度的透视倾斜，"
        "屏幕四角略呈梯形，但倾斜不得影响任何文字的辨认"
    ),
    "photo_of_print": (
        "整体为手机翻拍印刷品的实拍照片，纸张带有轻微纹理与柔和阴影，"
        "画面边缘存在轻微的透视变形，但文字仍须逐字可辨认"
    ),
    "broadcast_capture": (
        "整体为电视播出画面的截帧，具有广播级调色与轻微暗角，"
        "画面四周保留播出安全边距"
    ),
    "exported_graphic": (
        "整体为设计软件导出的图像，背景干净，元素对齐精确，"
        "无拍摄或压缩引入的噪声"
    ),
}

# Per-carrier visual detail: palette, typography, spacing, iconography.
CARRIER_VISUAL = {
    "R1": (
        "配色以白色为主背景，主文字近黑色，次要信息用中灰色，分隔线用浅灰色；"
        "字体为系统无衬线字体，账号名与标题采用较粗字重，正文常规字重，"
        "互动数据与小字采用较小字号；各区块之间以细分隔线分隔，卡片带轻微圆角；"
        "头像为圆形，认证标记为小尺寸徽章，互动图标为线性图标并配以数值"
    ),
    "R2": (
        "画面以实景照片为底，字幕叠加在画面中下部，白字配深色描边以保证可读；"
        "顶部与底部为半透明深色条，承载账号名、说明文字与音频信息；"
        "右侧为竖排半透明图标列，配以数值；图标为线性风格，间距均匀；"
        "整体色调随底层照片而定，叠加层不改变底层画面内容"
    ),
    "R3": (
        "配色沉稳，标题区使用深色底或高对比配色，正文区以白底黑字为主；"
        "报头使用衬线字体并加粗，标题字重明显高于正文，正文采用两端对齐的分栏排版；"
        "说明文字采用较小字号并配以细分隔线；"
        "电视类画面叠加电视台标与字幕条，网站类画面带导航栏与卡片式列表"
    ),
    "R4": (
        "配色简洁，主标题使用深色粗体，分区之间以留白或浅色区块区分；"
        "正文使用无衬线字体，字号层级分明；"
        "边框与分隔线较细，卡片整体带轻微圆角与浅阴影；"
        "底部信息条使用较小字号并配以浅灰底色"
    ),
}

# Concrete typography rules. These keep generated images close to real app and
# news-site screenshots instead of drifting into poster-like lettering.
TYPOGRAPHY_DETAIL = {
    "cn_social": (
        "字体与字号须贴近中文社交 App 截图：使用手机系统黑体/苹方/思源黑体一类中性无衬线，"
        "不得使用书法体、艺术字、海报字或过度圆润的儿童字体；顶部导航约为画面高度的2.2%至2.8%，"
        "账号名约2.0%至2.5%且中粗，正文约2.4%至3.2%且常规字重，话题标签同正文但用平台蓝灰色，"
        "时间、来源、互动数约1.4%至1.9%；中文正文行距约为字号的1.35至1.55倍，字距为正常系统字距，"
        "不要把正文压缩成报纸小字，也不要放大成封面海报标题"
    ),
    "en_social": (
        "字体与字号须贴近英文社交 App 截图：使用类似 SF Pro、Roboto、Helvetica Neue 或 Arial 的中性系统无衬线，"
        "不得使用装饰体、窄体海报字、衬线正文或手写体；账号名约为画面高度的2.0%至2.5%且中粗，"
        "用户名、时间、互动数据约1.4%至1.9%，正文约2.4%至3.2%，行距约为字号的1.25至1.45倍；"
        "UI 标签必须小于正文，不要把正文做成横幅标题"
    ),
    "image_social": (
        "字体与字号须贴近图片社交平台笔记详情页：顶部昵称为中粗系统无衬线，约2.0%至2.6%；"
        "图文标题约2.8%至3.6%且加粗，正文约2.2%至2.9%，底部输入框、点赞数、收藏数、评论数约1.6%至2.0%；"
        "封面图上的大字可更粗，但仍应像 App 内图片文字而非广告海报，正文区域不得使用花体、描边字或异常加粗"
    ),
    "short_video": (
        "字体与字号须贴近短视频 App 截图：顶部频道导航为白色中粗系统无衬线，约2.0%至2.6%；"
        "视频中心字幕可使用粗黑体，但应是短视频字幕样式，约4.0%至6.5%，带清晰描边或阴影；"
        "作者名、位置胶囊、说明文字约2.0%至2.8%，右侧互动数字和标签约1.6%至2.1%；"
        "底部导航约2.0%至2.5%；不得把全屏字幕做成新闻海报大标题，也不得让说明文字小到无法辨认"
    ),
    "news_media": (
        "新闻媒体版式的字体须符合对应媒介：网页正文使用新闻网站常见无衬线或宋体/Georgia 类正文字体，"
        "标题约为正文的2.0至2.8倍，副标题约为正文的1.2至1.5倍，正文约1.6%至2.2%，来源、时间、图注约1.0%至1.4%；"
        "报纸版式可用衬线标题和分栏正文，电视字幕用粗体无衬线；所有正文必须保持真实新闻页面的阅读字号，"
        "不得变成 PPT 标题页、宣传海报或社交媒体大字报"
    ),
}

TYPOGRAPHY_DETAIL_EN = {
    "cn_social": (
        "Typography: match a Chinese social app screenshot with a neutral mobile system sans-serif, similar to "
        "PingFang SC, Microsoft YaHei or Noto Sans CJK. Do not use calligraphic, poster, decorative or childlike "
        "rounded fonts. Top navigation is about 2.2%-2.8% of frame height; account names 2.0%-2.5% semibold; "
        "body text 2.4%-3.2%; timestamps, sources and metrics 1.4%-1.9%. Use normal tracking and 1.35-1.55 "
        "line height for Chinese body text"
    ),
    "en_social": (
        "Typography: match an English social app screenshot using a neutral system sans-serif such as SF Pro, "
        "Roboto, Helvetica Neue or Arial. Do not use decorative, condensed poster, serif or handwriting fonts. "
        "Author names are semibold at 2.0%-2.5% of frame height; handles, timestamps and metrics 1.4%-1.9%; "
        "post body 2.4%-3.2% with normal tracking and 1.25-1.45 line height"
    ),
    "image_social": (
        "Typography: match a photo-sharing note detail page. User names are semibold system sans-serif at "
        "2.0%-2.6%; note titles 2.8%-3.6% bold; body copy 2.2%-2.9%; bottom input and engagement counts "
        "1.6%-2.0%. Text inside images may be heavier but must still look like in-app content, not a poster"
    ),
    "short_video": (
        "Typography: match a short-video app screenshot. Top channel tabs use white semibold system sans-serif "
        "at 2.0%-2.6%; central captions may be bold at 4.0%-6.5% with outline or shadow; author, location and "
        "caption text 2.0%-2.8%; right-side counts and labels 1.6%-2.1%; bottom navigation 2.0%-2.5%"
    ),
    "news_media": (
        "Typography: match the relevant news medium. Web articles use newsroom-style sans-serif or serif body "
        "fonts; headlines are 2.0-2.8x body size, subheads 1.2-1.5x, body text 1.6%-2.2% of frame height, "
        "metadata and captions 1.0%-1.4%. The result must read as a real article page, not a slide or poster"
    ),
}

# Real-platform UI anchors. These are appended by layout_id so the generated
# prompt names the concrete UI being replicated, instead of only describing an
# abstract platform family.
UI_REPLICA_DETAIL = {
    "cn_social_text_only": (
        "真实平台 UI 复刻目标：高度复刻微博移动端单条纯文字帖详情页，包含手机状态栏、返回栏、作者头像昵称与认证标识、"
        "关注按钮、正文区、时间来源行、转发评论点赞操作栏和底部输入/导航区域；整体应像真实微博 App 截图"
    ),
    "cn_social_image_post": (
        "真实平台 UI 复刻目标：高度复刻微博移动端图文帖信息流/详情页，包含顶部推荐/关注导航、作者区、正文区、"
        "多图图片区、热度标签、互动栏和底部导航；橙色强调色、白底和细灰分隔线须贴近真实微博 App"
    ),
    "cn_social_grid_gallery": (
        "真实平台 UI 复刻目标：高度复刻微博移动端九宫格图文帖，作者区、正文区、九宫格缩略图、话题标签、"
        "互动栏和底部导航均按微博 App 的真实层级呈现"
    ),
    "cn_social_quote_repost": (
        "真实平台 UI 复刻目标：高度复刻微博移动端引用转发帖，主帖正文与内嵌转发卡片须有浅灰底、圆角边界和真实微博转发层级"
    ),
    "cn_social_topic_aggregation": (
        "真实平台 UI 复刻目标：高度复刻微博热搜/话题聚合页，包含话题标题、热度数据、帖子列表、参与按钮、榜单或声明条"
    ),
    "cn_social_embedded_comment": (
        "真实平台 UI 复刻目标：高度复刻微博移动端评论区展开状态，主帖上方、评论列表、评论输入框和互动小图标须贴近真实微博"
    ),
    "cn_social_html_post": (
        "真实平台 UI 复刻目标：高度复刻微信公众号文章阅读页，包含微信内置浏览器状态栏、返回栏、公众号头像与名称、"
        "文章标题、来源时间、正文长段落、配图、阅读量、赞/在看和写留言区域；页面必须像真实微信公众号文章，而不是普通社交卡片"
    ),
    "en_social_text_only": (
        "真实平台 UI 复刻目标：高度复刻 X 移动端单条文字帖详情页，包含返回栏、作者头像、display name、handle、"
        "verified badge、正文、时间与浏览量、reply/repost/like/view 图标和回复输入框"
    ),
    "en_social_image_post": (
        "真实平台 UI 复刻目标：高度复刻 X 移动端图文帖详情页，包含作者区、正文、大圆角媒体卡、来源行、时间浏览量和回复输入框"
    ),
    "en_social_quote_repost": (
        "真实平台 UI 复刻目标：高度复刻 X 移动端 quote post，主帖正文与引用帖卡片须有真实 X 的细灰边框、圆角和层级关系"
    ),
    "en_social_news_card": (
        "真实平台 UI 复刻目标：高度复刻 X 移动端新闻链接卡片帖，包含作者行、链接预览大图、来源域名、标题摘要和互动图标"
    ),
    "image_social_post": (
        "真实平台 UI 复刻目标：高度复刻小红书移动端笔记详情页，包含返回箭头、作者头像昵称、粉红关注按钮、分享按钮、"
        "大图/封面、标题正文、评论预览、底部说点什么输入框以及点赞收藏评论图标"
    ),
    "image_social_grid": (
        "真实平台 UI 复刻目标：高度复刻小红书移动端多图笔记页，包含顶部作者栏、多图区域、标题正文、话题标签、评论预览和底部互动栏"
    ),
    "short_video_scene_frame": (
        "真实平台 UI 复刻目标：高度复刻抖音短视频播放页，包含顶部频道导航、全屏视频画面、右侧竖排头像/点赞/评论/收藏/分享栏、"
        "左下账号与说明、地点胶囊、相关搜索条和底部首页/朋友/加号/消息/我导航"
    ),
    "short_video_caption_narration": (
        "真实平台 UI 复刻目标：高度复刻抖音字幕解说类视频页，字幕应叠加在真实视频画面上，右侧互动栏和底部导航须贴近抖音 App"
    ),
    "short_video_overlay_graphic": (
        "真实平台 UI 复刻目标：高度复刻抖音图文叠加类短视频页，半透明信息面板必须像视频内浮层，而不是独立海报卡片"
    ),
    "short_video_screen_in_screen": (
        "真实平台 UI 复刻目标：高度复刻抖音录屏/屏中屏视频页，内嵌界面、解说字幕、右侧互动栏和底部账号说明须保持抖音真实布局"
    ),
    "short_video_live_capture": (
        "真实平台 UI 复刻目标：高度复刻抖音直播间画面，包含直播头部、弹幕区、礼物/输入栏、右侧互动入口和半透明叠层"
    ),
    "news_site_home": (
        "真实平台 UI 复刻目标：高度复刻新华社/央视网/Reuters/BBC/CNN 等新闻网站网页端首页或频道页，包含官网页眉、频道导航、"
        "头条区、次级新闻列表、右侧榜单/推荐栏和网页式留白；不要做成手机 App 或抽象信息卡"
    ),
    "news_app_detail": (
        "真实平台 UI 复刻目标：高度复刻新华社/央视新闻/人民网等新闻客户端文章详情页，包含返回栏、标题区、来源时间、正文、配图、"
        "评论/分享底栏和移动端新闻阅读字号"
    ),
    "wire_bulletin": (
        "真实平台 UI 复刻目标：高度复刻 Reuters/AP/新华社电讯稿页面，包含通讯社抬头、slug line、时间、正文段落、来源说明和简洁黑白排版"
    ),
    "tv_broadcast": (
        "真实平台 UI 复刻目标：高度复刻央视新闻/地方电视新闻播出截帧，包含台标、新闻画面、下三分标题条和底部滚动字幕"
    ),
    "tv_breaking_interrupt": (
        "真实平台 UI 复刻目标：高度复刻电视新闻突发插播画面，包含台标、红色突发通栏、现场画面、详情面板和滚动字幕"
    ),
    "newspaper_front_page": (
        "真实平台 UI 复刻目标：高度复刻报纸头版，包含报头、日期版次、头条标题、主图、分栏正文和边栏新闻"
    ),
    "newspaper_inner_page": (
        "真实平台 UI 复刻目标：高度复刻报纸内页新闻版，包含页眉、文章标题、分栏正文、内嵌图片、图注和页脚说明"
    ),
    "news_brief_card": (
        "真实平台 UI 复刻目标：高度复刻新闻机构简报卡片，包含机构品牌条、日期期号、条目列表和底部来源说明"
    ),
    "share_card": (
        "真实平台 UI 复刻目标：高度复刻社交媒体分享卡片，包含品牌头部、标题、摘要、配图、来源和底部操作区"
    ),
    "summary_long_image": (
        "真实平台 UI 复刻目标：高度复刻微信公众号文章阅读页或新闻机构长图摘要页，包含标题、来源时间、长段落、分节要点、配图和页脚来源；"
        "如果呈现为文章页，必须像真实微信公众号长文阅读界面"
    ),
    "topic_aggregation_long_image": (
        "真实平台 UI 复刻目标：高度复刻微博热搜/小红书话题聚合长图，包含话题通栏、案例列表、热度/讨论数和聚合页脚"
    ),
    "timeline_image": (
        "真实平台 UI 复刻目标：高度复刻新闻客户端或微信公众号中的事件时间线长图，包含标题、时间节点、状态区和来源页脚"
    ),
    "quick_read_card": (
        "真实平台 UI 复刻目标：高度复刻小红书/新闻客户端速览卡片，包含顶部品牌区、四个关键信息块和底部免责声明"
    ),
}

UI_REPLICA_DETAIL_EN = UI_REPLICA_DETAIL

# Text-density instruction templates.
DENSITY_RULE = {
    "Low": "图中可读文字总量约 {n} 个字符，属较低密度，画面以图像为主、文字为辅。",
    "Medium": "图中可读文字总量约 {n} 个字符，属中等密度，文字与图像比重相当。",
    "High": "图中可读文字总量约 {n} 个字符，属较高密度，文字应占据画面的主要面积。",
    "VeryHigh": "图中可读文字总量约 {n} 个字符，属高密度，文字应铺满各文字分区，画面以文字信息为主。",
}

# The trailing invariant block, shared by every prompt.
TAIL_RULES = """画面信息量要求：上列各分区均须实际呈现，不得省略任何一个分区；各分区内的文字须完整排布、填满该分区的可用空间，不得留有大片空白；分区之间的相对位置与先后顺序须严格遵守，占比按上列顺序自然分配。
允许出现的视觉元素：平台界面框架、平台与频道的标识与图标、徽章与认证标记、头像占位图形、分隔线、圆角与浅阴影等界面装饰元素；这些元素应按真实平台的样式自然呈现。
文字以外的画面内容：配图位置应呈现与该话题相符的实景照片或界面截图内容，画面中不得出现可辨认的真实人物面部，不得出现血腥、暴力或令人不适的画面。
一致性要求：同一段落内的文字须保持统一的字体、字号与颜色；相同层级的信息须使用相同的排版样式；数值与单位之间保留适当间距；字号必须服从真实平台截图的层级，不得为了填满空间随意放大正文或把小字缩到不可读。
禁止事项：不得出现任何未在上列「」中指定的可读文字；不得出现乱码、伪汉字、无意义符号或占位符；不得添加任何未在分区中指定的水印、日期戳、相机参数叠加或其他叠加信息；上列分区中明确给出的平台标识内容属于画面组成部分，应当呈现；不得使用模糊、变形或不可辨认的方式处理指定文字；不得擅自改写、增删、纠正或"优化"任何给定的数字、日期、编号与文字内容。"""


# English equivalents of DENSITY_RULE, with the tier name spelled out.
DENSITY_RULE_EN = {
    "Low": "Text volume: the image should carry roughly {n} characters of readable text \u2014 a low-density layout in which imagery dominates and text plays a supporting role.",
    "Medium": "Text volume: the image should carry roughly {n} characters of readable text \u2014 a medium-density layout balancing text and imagery.",
    "High": "Text volume: the image should carry roughly {n} characters of readable text \u2014 a high-density layout in which text occupies most of the frame.",
    "VeryHigh": "Text volume: the image should carry roughly {n} characters of readable text \u2014 a very high-density layout in which text fills the text-bearing sections and information dominates the frame.",
}
