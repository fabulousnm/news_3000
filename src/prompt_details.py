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
        "表格与图注使用较小字号并配以细边框；"
        "电视类画面叠加电视台标与字幕条，网站类画面带导航栏与卡片式列表"
    ),
    "R4": (
        "配色简洁，主标题使用深色粗体，分区之间以留白或浅色区块区分；"
        "正文使用无衬线字体，字号层级分明；"
        "边框与分隔线较细，卡片整体带轻微圆角与浅阴影；"
        "底部信息条使用较小字号并配以浅灰底色"
    ),
}

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
一致性要求：同一段落内的文字须保持统一的字体、字号与颜色；相同层级的信息须使用相同的排版样式；数值与单位之间保留适当间距。
禁止事项：不得出现任何未在上列「」中指定的可读文字；不得出现乱码、伪汉字、无意义符号或占位符；不得添加任何未在分区中指定的水印、日期戳、相机参数叠加或其他叠加信息；上列分区中明确给出的平台标识内容属于画面组成部分，应当呈现；不得使用模糊、变形或不可辨认的方式处理指定文字；不得擅自改写、增删、纠正或"优化"任何给定的数字、日期、编号与文字内容。"""


# English equivalents of DENSITY_RULE, with the tier name spelled out.
DENSITY_RULE_EN = {
    "Low": "Text volume: the image should carry roughly {n} characters of readable text \u2014 a low-density layout in which imagery dominates and text plays a supporting role.",
    "Medium": "Text volume: the image should carry roughly {n} characters of readable text \u2014 a medium-density layout balancing text and imagery.",
    "High": "Text volume: the image should carry roughly {n} characters of readable text \u2014 a high-density layout in which text occupies most of the frame.",
    "VeryHigh": "Text volume: the image should carry roughly {n} characters of readable text \u2014 a very high-density layout in which text fills the text-bearing sections and information dominates the frame.",
}
