"""Prompt renderer.

Assembles the final image-generation prompt from the layout template, the
per-variant field set and the frozen prompt section templates.

Text is written verbatim inside 「」 per the declared convention; layout
sections are marked with 【】.
"""

from common import PROMPT_TEMPLATES, LAYOUTS
from prompt_details import (CAPTURE_DETAIL, CARRIER_VISUAL, DENSITY_RULE,
                            DENSITY_RULE_EN, TAIL_RULES)

SECTION_NAMES = {
    "zh-Hans": {
        "top_bar": "顶部栏", "author_block": "作者信息区", "body": "正文区",
        "interaction_bar": "互动栏", "timestamp": "时间与来源", "watermark": "水印",
        "media": "配图区", "gallery": "图集区", "caption_strip": "图注条",
        "quoted_card": "内嵌引用区", "topic_header": "话题头部", "post_list": "帖子列表",
        "bottom_action": "底部操作栏", "disclaimer_strip": "平台声明条",
        "comment_list": "评论区", "comment_input": "评论输入框",
        "status_bar": "状态栏", "scene": "画面主体", "subtitle_overlay": "字幕叠加区",
        "right_rail": "右侧互动栏", "bottom_left": "左下账号区", "audio_strip": "音频条",
        "progress_bar": "进度条", "top_banner": "顶部大字标题", "subtitle_block": "字幕区",
        "overlay_panel": "叠加信息面板", "inner_screen": "内嵌界面", "commentary_overlay": "解说字幕",
        "live_badge": "直播标识", "live_header": "直播头部", "danmaku_area": "弹幕区",
        "bottom_bar": "底部操作条", "metrics_block": "数据区", "tags_strip": "标签条",
        "link_card": "链接卡片", "action_row": "操作栏", "caption_block": "说明文字区",
        "comment_preview": "评论预览",
        "channel_logo": "频道标识", "lower_third": "下三分字幕条", "ticker": "滚动字幕条",
        "breaking_banner": "突发通栏", "detail_panel": "详情面板", "masthead": "报头",
        "lead_headline": "头条标题", "lead_photo": "主图与图注", "body_columns": "正文分栏",
        "sidebar": "边栏", "running_head": "页眉", "article_headline": "文章标题",
        "inline_photo": "文中配图", "footer_note": "页脚说明", "site_header": "网站页眉",
        "lead_story": "头条区", "secondary_stories": "次级新闻区", "sidebar_list": "排行榜边栏",
        "app_bar": "应用栏", "headline_block": "标题区", "byline_block": "署名区",
        "article_body": "文章正文", "footer_action": "底部操作区",
        "wire_header": "电讯抬头", "slug_line": "电讯标注行", "bulletin_body": "电讯正文",
        "attribution_block": "来源说明区", "footer": "页脚",
        "card_header": "卡片头部", "item_list": "条目列表", "card_footer": "卡片页脚",
        "brand_strip": "品牌条",
        "card_brand": "卡片品牌区", "card_headline": "卡片标题", "card_media": "卡片配图",
        "card_summary": "摘要区", "card_footer_area": "卡片页脚",
        "long_header": "长图页眉", "lead_block": "导语区", "point_block_1": "要点一",
        "point_block_2": "要点二", "point_block_3": "要点三", "conclusion_block": "结论区",
        "long_footer": "长图页脚", "topic_banner": "话题通栏", "case_entry_1": "案例一",
        "case_entry_2": "案例二", "case_entry_3": "案例三", "summary_note": "小结",
        "aggregation_footer": "聚合页脚", "timeline_header": "时间线标题",
        "timeline_nodes": "时间线节点", "status_block": "当前状态", "timeline_footer": "时间线页脚",
        "body_extension": "正文延伸区", "body_extension_2": "正文续页区",
        "detail_panel": "详情面板", "location_line": "地点标识行",
        "caption_block": "图注区", "caption_extra": "图注续行区",
        "article_excerpt": "摘要区", "inline_note": "内嵌说明",
        "extended_body": "正文续区", "commentary_block": "附言区",
        "caption_note": "说明补充区",
        "card_body": "卡片正文", "narration_extra": "解说续区",
        "panel_extra": "面板补充区", "inner_extra": "内屏续区",
        "danmaku_extra": "弹幕续区", "secondary_detail": "次要信息区",
        "item_extra": "条目续区", "bulletin_extra": "电讯续段",
        "article_extra": "正文续段", "summary_extra": "摘要续区",
        "caption_strip": "图注条",
        "quick_header": "速览头部", "key_fact_1": "要点一", "key_fact_2": "要点二",
        "key_fact_3": "要点三", "key_fact_4": "要点四", "quick_footer": "速览页脚",
    },
    "en": {
        "top_bar": "Top bar", "author_block": "Author block", "body": "Post body",
        "interaction_bar": "Interaction bar", "timestamp": "Timestamp and source",
        "watermark": "Watermark", "media": "Media area", "gallery": "Gallery area",
        "caption_strip": "Caption strip", "quoted_card": "Quoted post block",
        "topic_header": "Topic header", "post_list": "Post list",
        "bottom_action": "Bottom action bar", "disclaimer_strip": "Platform statement",
        "comment_list": "Comment list", "comment_input": "Comment input",
        "link_card": "Link card", "action_row": "Action row", "caption_block": "Caption block",
        "comment_preview": "Comment preview", "metrics_block": "Metrics block",
        "tags_strip": "Tags strip",
        "channel_logo": "Channel logo", "lower_third": "Lower third", "ticker": "Ticker",
        "breaking_banner": "Breaking banner", "detail_panel": "Detail panel",
        "masthead": "Masthead", "lead_headline": "Lead headline", "lead_photo": "Lead photo",
        "body_columns": "Body columns", "sidebar": "Sidebar", "running_head": "Running head",
        "article_headline": "Article headline", "inline_photo": "Inline photo",
        "footer_note": "Footer note", "site_header": "Site header", "lead_story": "Lead story",
        "secondary_stories": "Secondary stories", "sidebar_list": "Sidebar list",
        "app_bar": "App bar", "headline_block": "Headline block", "byline_block": "Byline block",
        "article_body": "Article body", "footer_action": "Footer actions",
        "wire_header": "Wire header", "slug_line": "Slug line", "bulletin_body": "Bulletin body",
        "attribution_block": "Attribution block", "footer": "Footer",
        "card_header": "Card header", "item_list": "Item list", "card_footer": "Card footer",
        "brand_strip": "Brand strip",
        "card_brand": "Card brand", "card_headline": "Card headline", "card_media": "Card media",
        "card_summary": "Summary block", "card_footer_area": "Card footer",
        "long_header": "Long-image header", "lead_block": "Lead block",
        "point_block_1": "Point one", "point_block_2": "Point two",
        "point_block_3": "Point three", "conclusion_block": "Conclusion block",
        "long_footer": "Long-image footer", "topic_banner": "Topic banner",
        "case_entry_1": "Case one", "case_entry_2": "Case two", "case_entry_3": "Case three",
        "summary_note": "Summary note", "aggregation_footer": "Aggregation footer",
        "timeline_header": "Timeline header", "timeline_nodes": "Timeline nodes",
        "status_block": "Current status", "timeline_footer": "Timeline footer",
        "body_extension": "Body extension", "body_extension_2": "Body continuation page",
        "detail_panel": "Detail panel", "location_line": "Location line",
        "caption_block": "Caption block", "caption_extra": "Caption continuation",
        "article_excerpt": "Excerpt block", "inline_note": "Inline note",
        "extended_body": "Post body continuation", "commentary_block": "Commentary block",
        "caption_note": "Caption note",
        "card_body": "Card body", "narration_extra": "Narration continuation",
        "panel_extra": "Panel supplement", "inner_extra": "Inner screen continuation",
        "danmaku_extra": "Comment continuation", "secondary_detail": "Secondary detail",
        "item_extra": "Item continuation", "bulletin_extra": "Bulletin continuation",
        "article_extra": "Article continuation", "summary_extra": "Summary continuation",
        "quick_header": "Quick-read header", "key_fact_1": "Fact one", "key_fact_2": "Fact two",
        "key_fact_3": "Fact three", "key_fact_4": "Fact four", "quick_footer": "Quick-read footer",
    },
}

ROLE_TO_SECTION = {
    "platform_label": "top_bar", "nav_label": "top_bar",
    "account_name": "author_block", "account_meta": "author_block",
    "verified_label": "author_block", "display_name": "author_block",
    "handle": "author_block", "follow_label": "author_block", "author_name": "author_block",
    "location_label": "author_block", "menu_label": "author_block",
    "body_text": "body", "hashtags": "body", "topic_tag": "tags_strip",
    "comment_metric": "interaction_bar", "repost_metric": "interaction_bar",
    "like_metric": "interaction_bar", "view_metric": "interaction_bar",
    "reply_metric": "interaction_bar", "share_metric": "interaction_bar",
    "save_metric": "interaction_bar",
    "publish_time": "timestamp", "source_label": "timestamp", "post_time": "timestamp",
    "post_datetime": "timestamp",
    "account_handle": "watermark",
    "image_caption": "caption_strip",
    "quoted_account": "quoted_card", "quoted_handle": "quoted_card",
    "quoted_body": "quoted_card", "quoted_time": "quoted_card",
    "quoted_display_name": "quoted_card",
    "topic_title": "topic_header", "topic_metric": "topic_header",
    "topic_status": "topic_header", "topic_period": "topic_banner",
    "post1_account": "post_list", "post1_body": "post_list",
    "post2_account": "post_list", "post2_body": "post_list",
    "post3_account": "post_list", "post3_body": "post_list",
    "join_action": "bottom_action",
    "platform_statement": "disclaimer_strip",
    "comment1_account": "comment_list", "comment1_body": "comment_list",
    "comment1_metric": "comment_list", "comment2_account": "comment_list",
    "comment2_body": "comment_list", "comment2_metric": "comment_list",
    "input_placeholder": "comment_input",
    "caption_text": "caption_block", "hashtag_row": "caption_block",
    "comment_account": "comment_preview", "comment_body": "comment_preview",
    "read_metric": "metrics_block",
    "card_media_caption": "link_card", "card_source": "link_card",
    "card_headline": "link_card", "card_description": "link_card",
    "headline": "headline_block", "subheadline": "headline_block",
    "channel_name": "channel_logo",
    "segment_tag": "lower_third", "headline_banner": "lower_third",
    "ticker_text": "ticker", "ticker_time": "ticker",
    "breaking_tag": "breaking_banner", "breaking_headline": "breaking_banner",
    "detail_line1": "detail_panel", "detail_line2": "detail_panel",
    "detail_line3": "detail_panel",
    "newspaper_name": "masthead", "date_line": "masthead",
    "edition_label": "masthead", "issue_number": "masthead",
    "lead_headline": "lead_headline", "lead_subheadline": "lead_headline",
    "byline": "lead_headline",
    "photo_caption": "lead_photo",
    "column_lead": "body_columns", "column_body": "body_columns",
    "column1_body": "body_columns", "column2_body": "body_columns",
    "column3_body": "body_columns",
    "sidebar_title": "sidebar", "sidebar_item1": "sidebar", "sidebar_item2": "sidebar",
    "sidebar_title2": "sidebar_list",
    "section_name": "running_head", "page_number": "running_head",
    "article_headline": "article_headline",
    "editor_note": "footer_note", "contact_line": "footer_note",
    "site_name": "site_header", "nav_item1": "site_header",
    "nav_item2": "site_header", "nav_item3": "site_header", "search_label": "site_header",
    "lead_summary": "lead_story", "lead_timestamp": "lead_story",
    "story1_headline": "secondary_stories", "story1_timestamp": "secondary_stories",
    "story2_headline": "secondary_stories", "story2_timestamp": "secondary_stories",
    "story3_headline": "secondary_stories", "story3_timestamp": "secondary_stories",
    "rank1": "sidebar_list", "rank2": "sidebar_list",
    "rank3": "sidebar_list", "rank4": "sidebar_list",
    "back_label": "app_bar", "app_name": "app_bar",
    "publisher_name": "byline_block", "publish_time2": "byline_block",
    "paragraph1": "article_body", "paragraph2": "article_body", "quote_line": "article_body",
    "source_note": "footer_action", "comment_metric2": "footer_action",
    "urgency_tag": "wire_header", "agency_name": "wire_header",
    "sequence_number": "wire_header", "filing_time": "wire_header",
    "slug_text": "slug_line", "dateline": "slug_line", "priority_label": "slug_line",
    "paragraph3": "bulletin_body",
    "source_attribution": "attribution_block", "editor_note2": "attribution_block",
    "transmission_note": "footer", "page_ref": "footer",
    "brief_label": "card_header", "issue_label": "card_header", "brief_date": "card_header",
    "item1_title": "item_list", "item1_body": "item_list",
    "item2_title": "item_list", "item2_body": "item_list",
    "item3_title": "item_list", "item3_body": "item_list",
    "compiler_note": "card_footer", "source_line": "card_footer",
    "outlet_name": "card_brand", "card_kind_label": "card_brand",
    "summary_line1": "card_summary", "summary_line2": "card_summary",
    "summary_line3": "card_summary", "qr_hint": "card_footer_area",
    "summary_title": "long_header",
    "lead_body": "lead_block",
    "point1_title": "point_block_1", "point1_body": "point_block_1",
    "point2_title": "point_block_2", "point2_body": "point_block_2",
    "point3_title": "point_block_3", "point3_body": "point_block_3",
    "conclusion_title": "conclusion_block", "conclusion_body": "conclusion_block",
    "case1_title": "case_entry_1", "case1_location": "case_entry_1",
    "case1_date": "case_entry_1", "case1_body": "case_entry_1",
    "case2_title": "case_entry_2", "case2_location": "case_entry_2",
    "case2_date": "case_entry_2", "case2_body": "case_entry_2",
    "case3_title": "case_entry_3", "case3_location": "case_entry_3",
    "case3_date": "case_entry_3", "case3_body": "case_entry_3",
    "summary_line": "summary_note", "review_note": "summary_note",
    "timeline_title": "timeline_header", "timeline_scope": "timeline_header",
    "node1_time": "timeline_nodes", "node1_text": "timeline_nodes",
    "node2_time": "timeline_nodes", "node2_text": "timeline_nodes",
    "node3_time": "timeline_nodes", "node3_text": "timeline_nodes",
    "node4_time": "timeline_nodes", "node4_text": "timeline_nodes",
    "current_status": "status_block", "status_source": "status_block",
    "update_note": "timeline_footer",
    "card_label": "quick_header", "card_index": "quick_header", "card_topic": "quick_header",
    "fact1_label": "key_fact_1", "fact1_value": "key_fact_1", "fact1_note": "key_fact_1",
    "fact2_label": "key_fact_2", "fact2_value": "key_fact_2", "fact2_note": "key_fact_2",
    "fact3_label": "key_fact_3", "fact3_value": "key_fact_3", "fact3_note": "key_fact_3",
    "fact4_label": "key_fact_4", "fact4_value": "key_fact_4", "fact4_note": "key_fact_4",
    "disclaimer_line": "quick_footer",
    # R2 short-video roles
    "device_time": "status_bar", "status_icons": "status_bar",
    "subtitle_line1": "subtitle_block", "subtitle_line2": "subtitle_block",
    "subtitle_line3": "subtitle_block",
    "panel_title": "overlay_panel", "panel_point1": "overlay_panel",
    "panel_point2": "overlay_panel", "panel_point3": "overlay_panel",
    "inner_header": "inner_screen", "inner_body_line1": "inner_screen",
    "inner_body_line2": "inner_screen", "inner_metric": "inner_screen",
    "commentary_line1": "commentary_overlay", "commentary_line2": "commentary_overlay",
    "host_name": "live_header", "viewer_metric": "live_header",
    "live_label": "live_header",
    "danmaku1": "danmaku_area", "danmaku2": "danmaku_area", "danmaku3": "danmaku_area",
    "gift_label": "bottom_bar",
    "audio_name": "audio_strip", "progress_label": "audio_strip",
    # R3 remaining
    "share_label": "app_bar",
}


VISUAL_STYLE_BY_FAMILY_EN = {
    "cn_social": "a Chinese social platform interface with clear information hierarchy, card layout, rounded corners and light grey dividers",
    "en_social": "an English-language social platform interface with generous whitespace, hairline dividers and a clear type hierarchy",
    "image_social": "a photo-sharing platform interface with the author bar on top, a row of action icons and the caption immediately below",
    "short_video": "a vertical short-form video interface with centred overlaid captions and translucent UI elements floating above the footage",
    "news_media": "a news media broadcast and print style with distinct blocks, heavy headline weights and a restrained palette",
}

HAZARD_EN = {
    "H1": "disaster and emergency situations",
    "H2": "public health",
    "H3": "policy and public services",
    "H4": "public safety and incidents",
    "H5": "finance and economy",
    "H6": "consumer and health claims",
    "H7": "international affairs",
    "H8": "people and organisations",
    "H9": "public order and supply",
}

REGION_EN = {
    "CN": "mainland China", "NA": "North America", "UK": "the United Kingdom",
    "AU": "Australia", "TW": "Taiwan", "HK": "Hong Kong", "SG": "Singapore",
}


# Fallback order used only when a role is not declared by the layout at hand.
_FALLBACK_SECTIONS = ("body_extension", "body_extension_2", "extended_body", "body",
                      "article_body", "bulletin_body", "caption_block", "scene", "media")


def section_for_role(role, layout):
    """Resolve a role to a section **within this layout**.

    The mapping must come from the layout itself: the same role can belong to
    different sections in different layouts (``hashtags`` sits in ``body`` for a
    short post but in ``body_extension`` for a gallery post). Resolving through a
    single global index let the last layout traversed win, which silently moved
    fields such as ``like_metric`` and ``publish_time`` into an unrelated body
    section.
    """
    for sec in layout["sections"]:
        if role in sec["text_roles"]:
            return sec["role"]
    declared = {s["role"] for s in layout["sections"]}
    for preferred in _FALLBACK_SECTIONS:
        if preferred in declared:
            return preferred
    return layout["sections"][-1]["role"]


def _section_name(role, language):
    if language == "en":
        return SECTION_NAMES["en"].get(role, role)
    return SECTION_NAMES["zh-Hans"].get(role, role)


ROLE_LABELS = {
    # 社交
    "platform_label": "平台名称", "nav_label": "导航",
    "account_name": "账号名称", "account_meta": "账号简介", "verified_label": "认证标识",
    "display_name": "显示名称", "author_name": "作者名称", "handle": "用户标识",
    "follow_label": "关注按钮", "location_label": "地点", "menu_label": "菜单",
    "body_text": "正文", "hashtags": "话题标签", "hashtag_row": "话题标签",
    "topic_tag": "话题", "caption_text": "配文", "caption_line1": "配文", "caption_line2": "配文",
    "comment_metric": "评论数", "repost_metric": "转发数", "like_metric": "点赞数",
    "reply_metric": "回复数", "view_metric": "浏览量", "share_metric": "分享数",
    "save_metric": "收藏数", "read_metric": "阅读量",
    "publish_time": "发布时间", "source_label": "核实单位", "post_time": "发布时间",
    "post_datetime": "发布时间", "account_handle": "账号标识",
    "quoted_account": "被引账号", "quoted_handle": "被引账号标识",
    "quoted_body": "被引内容", "quoted_time": "被引时间",
    "quoted_display_name": "被引账号", "comment_account": "评论者",
    "comment_body": "评论内容", "input_placeholder": "输入框提示",
    "image_caption": "图注",
    # 话题聚合
    "topic_title": "话题名称", "topic_metric": "话题热度", "topic_status": "话题状态",
    "topic_period": "统计周期", "join_action": "参与按钮",
    "platform_statement": "平台声明", "disclaimer_line": "免责说明",
    "post1_account": "帖子一账号", "post1_body": "帖子一内容",
    "post2_account": "帖子二账号", "post2_body": "帖子二内容",
    "post3_account": "帖子三账号", "post3_body": "帖子三内容",
    # 新闻媒体
    "channel_name": "频道名称", "segment_tag": "栏目标签",
    "headline": "标题", "subheadline": "副标题", "headline_banner": "大字标题",
    "ticker_text": "滚动字幕", "ticker_time": "字幕时间",
    "breaking_tag": "突发标签", "breaking_headline": "突发标题",
    "detail_line1": "详情一", "detail_line2": "详情二", "detail_line3": "详情三",
    "detail_line4": "详情四", "detail_line5": "详情五", "detail_line6": "详情六",
    "detail_line7": "详情七", "detail_line8": "详情八", "detail_line9": "详情九",
    "detail_line10": "详情十", "detail_line11": "详情十一", "detail_line12": "详情十二",
    "detail_line13": "详情十三", "detail_line14": "详情十四", "detail_line15": "详情十五",
    "newspaper_name": "报头", "date_line": "日期", "edition_label": "版次",
    "issue_number": "期号", "lead_headline": "头条标题", "lead_subheadline": "头条副标题",
    "byline": "署名", "photo_caption": "图片说明", "column_lead": "导语",
    "column_body": "正文", "column1_body": "正文一栏", "column2_body": "正文二栏",
    "column3_body": "正文三栏", "column4_body": "正文四栏", "column5_body": "正文五栏",
    "column6_body": "正文六栏", "column7_body": "正文七栏", "column8_body": "正文八栏",
    "column_body2": "正文", "column_body3": "正文", "column_body4": "正文",
    "column_body5": "正文", "column_body6": "正文",
    "sidebar_title": "边栏标题", "sidebar_item1": "边栏条目一", "sidebar_item2": "边栏条目二",
    "section_name": "版面名称", "page_number": "版号", "running_head": "页眉",
    "article_headline": "文章标题", "article_body": "文章正文",
    "editor_note": "责任编辑", "editor_note2": "责任编辑", "contact_line": "联系方式",
    "site_name": "网站名称", "nav_item1": "导航一", "nav_item2": "导航二",
    "nav_item3": "导航三", "search_label": "搜索框",
    "lead_summary": "导语摘要", "lead_timestamp": "发布时刻",
    "story1_headline": "新闻一标题", "story1_timestamp": "新闻一时刻",
    "story2_headline": "新闻二标题", "story2_timestamp": "新闻二时刻",
    "story3_headline": "新闻三标题", "story3_timestamp": "新闻三时刻",
    "story4_headline": "新闻四标题", "story4_timestamp": "新闻四时刻",
    "story5_headline": "新闻五标题", "story5_timestamp": "新闻五时刻",
    "story6_headline": "新闻六标题", "story6_timestamp": "新闻六时刻",
    "story7_headline": "新闻七标题", "story7_timestamp": "新闻七时刻",
    "rank1": "排行一", "rank2": "排行二", "rank3": "排行三", "rank4": "排行四",
    "back_label": "返回", "app_name": "应用名称", "share_label": "分享",
    "publisher_name": "发布方", "publish_time2": "发布时间",
    "paragraph1": "段落一", "paragraph2": "段落二", "paragraph3": "段落三",
    "paragraph4": "段落四", "paragraph5": "段落五", "paragraph6": "段落六",
    "paragraph7": "段落七", "paragraph8": "段落八", "paragraph9": "段落九",
    "paragraph10": "段落十", "paragraph11": "段落十一", "paragraph12": "段落十二",
    "quote_line": "引述", "source_note": "来源说明", "comment_metric2": "评论数",
    "urgency_tag": "电讯等级", "agency_name": "发稿机构", "sequence_number": "稿件编号",
    "filing_time": "发稿时间", "slug_text": "标注行", "dateline": "电头发稿地",
    "priority_label": "优先级", "source_attribution": "来源机构",
    "transmission_note": "传输说明", "page_ref": "页码",
    "brief_label": "简报标识", "issue_label": "期号", "brief_date": "简报日期",
    "item1_title": "条目一标题", "item1_body": "条目一内容",
    "item2_title": "条目二标题", "item2_body": "条目二内容",
    "item3_title": "条目三标题", "item3_body": "条目三内容",
    "item4_title": "条目四标题", "item4_body": "条目四内容",
    "item5_title": "条目五标题", "item5_body": "条目五内容",
    "item6_title": "条目六标题", "item6_body": "条目六内容",
    "item7_title": "条目七标题", "item7_body": "条目七内容",
    "compiler_note": "整理人", "source_line": "来源",
    # 短视频
    "device_time": "设备时间", "status_icons": "状态栏",
    "subtitle_line1": "字幕一", "subtitle_line2": "字幕二", "subtitle_line3": "字幕三",
    "panel_title": "面板标题", "panel_point1": "要点一", "panel_point2": "要点二",
    "panel_point3": "要点三", "panel_point4": "要点四", "panel_point5": "要点五",
    "panel_point6": "要点六", "panel_point7": "要点七", "panel_point8": "要点八",
    "panel_point9": "要点九", "panel_point10": "要点十",
    "inner_header": "内屏标题", "inner_body_line1": "内屏正文一",
    "inner_body_line2": "内屏正文二", "inner_body_line3": "内屏正文三",
    "inner_body_line4": "内屏正文四", "inner_body_line5": "内屏正文五",
    "inner_body_line6": "内屏正文六", "inner_body_line7": "内屏正文七",
    "inner_body_line8": "内屏正文八", "inner_body_line9": "内屏正文九",
    "inner_metric": "内屏数据",
    "commentary_line1": "解说一", "commentary_line2": "解说二",
    "commentary_line3": "解说三", "commentary_line4": "解说四",
    "commentary_line5": "解说五", "commentary_line6": "解说六",
    "host_name": "主播名称", "viewer_metric": "观看人数", "live_label": "直播标识",
    "danmaku1": "弹幕一", "danmaku2": "弹幕二", "danmaku3": "弹幕三",
    "danmaku4": "弹幕四", "danmaku5": "弹幕五", "danmaku6": "弹幕六",
    "danmaku7": "弹幕七", "danmaku8": "弹幕八", "danmaku9": "弹幕九", "danmaku10": "弹幕十",
    "gift_label": "礼物按钮", "audio_name": "音频名称", "progress_label": "进度时间",
    # 图文卡
    "card_brand": "卡片来源", "card_kind_label": "卡片类型",
    "card_headline": "卡片标题", "card_description": "卡片描述",
    "card_media_caption": "卡片图注", "card_source": "卡片来源",
    "summary_line1": "摘要一", "summary_line2": "摘要二", "summary_line3": "摘要三",
    "summary_line4": "摘要四", "summary_line5": "摘要五", "summary_line6": "摘要六",
    "summary_line7": "摘要七", "summary_line8": "摘要八", "summary_line9": "摘要九",
    "summary_line10": "摘要十",
    "qr_hint": "扫码提示", "summary_title": "摘要标题", "lead_body": "导语",
    "point1_title": "要点一标题", "point1_body": "要点一内容",
    "point2_title": "要点二标题", "point2_body": "要点二内容",
    "point3_title": "要点三标题", "point3_body": "要点三内容",
    "point4_title": "要点四标题", "point4_body": "要点四内容",
    "point5_title": "要点五标题", "point5_body": "要点五内容",
    "point6_title": "要点六标题", "point6_body": "要点六内容",
    "conclusion_title": "结论标题", "conclusion_body": "结论内容",
    "case1_title": "案例一标题", "case1_location": "案例一地点",
    "case1_date": "案例一日期", "case1_body": "案例一内容",
    "case2_title": "案例二标题", "case2_location": "案例二地点",
    "case2_date": "案例二日期", "case2_body": "案例二内容",
    "case3_title": "案例三标题", "case3_location": "案例三地点",
    "case3_date": "案例三日期", "case3_body": "案例三内容",
    "case4_title": "案例四标题", "case4_location": "案例四地点",
    "case4_date": "案例四日期", "case4_body": "案例四内容",
    "case5_title": "案例五标题", "case5_body": "案例五内容",
    "case6_title": "案例六标题", "case6_body": "案例六内容",
    "summary_line": "小结", "review_note": "复核说明",
    "timeline_title": "时间线标题", "timeline_scope": "时间范围",
    "node1_time": "节点一时间", "node1_text": "节点一内容",
    "node2_time": "节点二时间", "node2_text": "节点二内容",
    "node3_time": "节点三时间", "node3_text": "节点三内容",
    "node4_time": "节点四时间", "node4_text": "节点四内容",
    "node5_time": "节点五时间", "node5_text": "节点五内容",
    "node6_time": "节点六时间", "node6_text": "节点六内容",
    "node7_time": "节点七时间", "node7_text": "节点七内容",
    "node8_time": "节点八时间", "node8_text": "节点八内容",
    "current_status": "当前状态", "status_source": "状态来源",
    "update_note": "更新说明",
    "card_label": "速览标识", "card_index": "期号", "card_topic": "主题",
    "fact1_label": "数据一名称", "fact1_value": "数据一数值", "fact1_note": "数据一说明",
    "fact2_label": "数据二名称", "fact2_value": "数据二数值", "fact2_note": "数据二说明",
    "fact3_label": "数据三名称", "fact3_value": "数据三数值", "fact3_note": "数据三说明",
    "fact4_label": "数据四名称", "fact4_value": "数据四数值", "fact4_note": "数据四说明",
    "fact5_label": "数据五名称", "fact5_value": "数据五数值", "fact5_note": "数据五说明",
    "fact6_label": "数据六名称", "fact6_note": "数据六说明",
    "fact7_label": "数据七名称", "fact7_note": "数据七说明",
    "card_body_line1": "卡片正文一", "card_body_line2": "卡片正文二",
    "card_body_line3": "卡片正文三", "card_body_line4": "卡片正文四",
    "card_body_line5": "卡片正文五",
    "excerpt_line1": "摘要一", "excerpt_line2": "摘要二", "excerpt_line3": "摘要三",
    "excerpt_line4": "摘要四", "excerpt_line5": "摘要五", "excerpt_line6": "摘要六",
    "excerpt_line7": "摘要七", "excerpt_line8": "摘要八", "excerpt_line9": "摘要九",
    "note_line1": "说明一", "note_line2": "说明二", "note_line3": "说明三",
    "note_line4": "说明四", "note_line5": "说明五", "note_line6": "说明六",
    "note_line7": "说明七",
    "narration_line3": "解说三", "narration_line4": "解说四",
    "narration_line5": "解说五", "narration_line6": "解说六",
    "narration_line7": "解说七", "narration_line8": "解说八", "narration_line9": "解说九",
    "body_line2": "正文第二段", "body_line3": "正文第三段", "body_line4": "正文第四段",
    "body_line5": "正文第五段", "body_line6": "正文第六段", "body_line7": "正文第七段",
    "body_line8": "正文第八段", "body_line9": "正文第九段", "body_line10": "正文第十段",
    "body_1": "正文", "body_2": "正文", "body_3": "正文", "body_4": "正文", "body_5": "正文",
    "outlet_name": "发布方", "brand_strip": "品牌条",
    "long_header": "页眉", "case_entry_1": "案例标题",
    "comment1_account": "评论一作者", "comment1_body": "评论一内容",
    "comment1_metric": "评论一数据",
    "comment2_account": "评论二作者", "comment2_body": "评论二内容",
    "comment2_metric": "评论二数据",
    "comment3_account": "评论三作者", "comment3_body": "评论三内容",
    "comment4_account": "评论四作者", "comment4_body": "评论四内容",
    "comment1_body2": "评论一补充", "comment2_body2": "评论二补充",
    "card_footer": "卡片页脚",
    "news_source": "信息来源",
}


def _role_label(role, language):
    if language == "en":
        return ""
    return ROLE_LABELS.get(role, "")



CAPTURE_DESC = {
    "native_screenshot": (
        "原生素材截图：界面元素边缘锐利，无拍摄痕迹、无反光、无透视倾斜，"
        "文字抗锯齿自然，色彩准确，如同设备直接导出的画面"
    ),
    "photo_of_screen": (
        "手机翻拍屏幕：可见轻微的环境反光与约10度的透视倾斜，屏幕边缘可见，"
        "但光线均匀、对焦准确，所有文字仍完全清晰可辨"
    ),
    "photo_of_print": (
        "手机翻拍印刷品：纸张有轻微纹理与柔和阴影，边缘略有透视变形，"
        "印刷网点隐约可见，但文字笔画完整清晰"
    ),
    "broadcast_capture": (
        "电视播出截帧：具有广播级调色与轻微暗角，画面经过广播链路压缩，"
        "边缘略软，但字幕与图形元素完整可读"
    ),
    "exported_graphic": (
        "设计导出图：背景干净，元素对齐精确，文字为矢量渲染质感，"
        "无任何拍摄或压缩痕迹"
    ),
}

CAPTURE_DESC_EN = {
    "native_screenshot": (
        "a native screenshot: crisp interface edges, no capture artefacts, no reflection, "
        "no perspective tilt, natural text anti-aliasing and accurate colour, as if exported "
        "directly from the device"
    ),
    "photo_of_screen": (
        "a phone photograph of a screen: mild ambient reflection and roughly 10 degrees of "
        "perspective tilt, screen edges visible, but even lighting and accurate focus so that "
        "every character remains fully legible"
    ),
    "photo_of_print": (
        "a phone photograph of a printed page: light paper texture and a soft shadow, slight "
        "perspective distortion, faint halftone dots, but complete and legible strokes"
    ),
    "broadcast_capture": (
        "a captured broadcast frame: broadcast-grade grading with slight vignetting, softened "
        "edges from the transmission chain, but subtitles and graphic elements fully readable"
    ),
    "exported_graphic": (
        "an exported design graphic: clean background, precise alignment, vector-quality text, "
        "no capture or compression artefacts"
    ),
}

def render_content_blocks(fields, layout, language):
    """Render the 【section】「text」 blocks in layout order."""
    by_section = {}
    # Fallback: keys not mapped to a section go to the layout's first section.
    default_role = layout["sections"][0]["role"]

    for f in fields:
        if not f.get("value"):
            continue
        role = section_for_role(f["key"], layout)
        by_section.setdefault(role, []).append(f)

    lines = []
    for sec in layout["sections"]:
        items = by_section.get(sec["role"], [])
        if not items:
            continue
        name = _section_name(sec["role"], language)
        parts = []
        for it in items:
            lbl = _role_label(it["key"], language)
            parts.append(f"{lbl}「{it['value']}」" if lbl else f"「{it['value']}」")
        lines.append(f"【{name}】" + "、".join(parts) + "。")
    return "\n".join(lines)


def render_layout_structure(layout, language):
    names = [_section_name(s["role"], language) for s in layout["sections"]]
    joiner = " → " if language == "en" else " → "
    return joiner.join(names)


EN_CARRIER_DESC = {
    "R1": "a screenshot of a social media post",
    "R2": "a vertical frame captured from a short-form video platform",
    "R3": "a news media layout image",
    "R4": "a graphic information card published by a news organisation",
}

EN_REALISM = {
    "native_screenshot": "presented as a native device screenshot with crisp interface edges and no capture artefacts",
    "photo_of_screen": "presented as a phone photograph of a screen, with mild ambient reflection and a slight perspective tilt that does not impair legibility",
    "photo_of_print": "presented as a phone photograph of a printed page, with light paper texture and a soft shadow",
    "broadcast_capture": "presented as a captured broadcast frame with broadcast-grade colour grading and slight vignetting",
    "exported_graphic": "presented as an exported design graphic with a clean background and precise alignment",
}

EN_NORMAL = {
    "R1": "social media post",
    "R2": "short-form video frame",
    "R3": "news layout",
    "R4": "information card design",
}

EN_SECTION_NAMES = SECTION_NAMES["en"]


def render_content_blocks_en(fields, layout):
    """Render the English content blocks."""
    by_section = {}
    default_role = layout["sections"][0]["role"]
    for f in fields:
        if not f.get("value"):
            continue
        role = section_for_role(f["key"], layout)
        by_section.setdefault(role, []).append(f)
    lines = []
    for sec in layout["sections"]:
        items = by_section.get(sec["role"], [])
        if not items:
            continue
        name = EN_SECTION_NAMES.get(sec["role"], sec["role"])
        content = ", ".join('"' + it["value"] + '"' for it in items)
        lines.append(f"[{name}] {content}.")
    return "\n".join(lines)


CAPTURE_DETAIL_EN = {k: v for k, v in {
    "native_screenshot": "presented as a native device screenshot; interface edges are crisp with no capture artefacts, no glare and no perspective tilt; the frame aligns with the device screen edges",
    "photo_of_screen": "presented as a phone photograph of a screen, with mild ambient glare and roughly ten degrees of perspective tilt; corners form a slight trapezoid but legibility must not be affected",
    "photo_of_print": "presented as a phone photograph of a printed page, with light paper texture and a soft shadow; edges show mild perspective distortion but text must remain legible character by character",
    "broadcast_capture": "presented as a captured broadcast frame with broadcast-grade grading and slight vignetting, keeping the broadcast safe margin",
    "exported_graphic": "presented as an exported design graphic with a clean background and precise alignment, free of capture or compression noise",
}.items()}

TAIL_RULES_EN = (
    "Information density: every section listed above must actually appear; none may be omitted. "
    "Text within each section must be laid out completely and fill the section's available space, "
    "leaving no large blank areas. Section order and relative position must be respected, with "
    "proportions distributed naturally in the order given. "
    "Permitted visual elements: platform interface chrome, platform and channel logos and icons, "
    "badges and verification marks, avatar placeholders, dividers, rounded corners and light "
    "shadows; these should appear naturally in the style of a real platform. "
    "Non-text content: image areas should show a photograph or interface capture consistent with "
    "the subject; no recognisable real faces, and no graphic, violent or distressing imagery. "
    "Consistency: text within one block must share a single typeface, size and colour; items at the "
    "same level must use the same styling; leave appropriate spacing between values and units. "
    "Prohibited: no readable text other than what appears in quotes above; no gibberish, "
    "pseudo-characters, meaningless symbols or placeholders; no watermarks, date stamps or camera "
    "parameter overlays beyond what a section specifies \u2014 platform identification given in a "
    "section is part of the image and should be rendered; do not render the specified text blurred, "
    "distorted or illegible; do not "
    "reword, add, remove, correct or 'improve' any given number, date, identifier or text."
)


def build_prompt_en(group, layout, variant_record, carrier, capture_style):
    fields = variant_record["fields"]
    sections = render_content_blocks_en(fields, layout)
    struct = " \u2192 ".join(EN_SECTION_NAMES.get(s["role"], s["role"]) for s in layout["sections"])
    parts = []
    parts.append(
        f"Generate a {group['aspect_ratio']} image of {EN_CARRIER_DESC[carrier]}, "
        f"{EN_REALISM.get(capture_style, EN_REALISM['native_screenshot'])}."
    )
    parts.append(
        f"Visual style: {VISUAL_STYLE_BY_FAMILY_EN.get(group['platform_family'], '')}; "
        f"overall structure: {struct}. The image must read as one complete standalone graphic "
        f"with natural interface typography and a professional information hierarchy."
    )
    parts.append(
        f'A fictitious media outlet "{group["meta"]["outlet_name"]}" reporting on '
        f'"{group["meta"]["subject_title"]}" covering {HAZARD_EN.get(group["hazard"], "")} '
        f'in {REGION_EN.get(group["region"], "")}. All depicted organisations, places and '
        f'persons are fictional.'
    )
    parts.append(sections)
    parts.append(
        "Realism details: text edges are crisp, type sizes are hierarchical, and interface "
        "elements are aligned. Every text region must remain sharp and legible character by character."
    )
    if variant_record["changed_fields"]:
        parts.append(
            "This image is a research specimen: by design, part of the given text contains "
            "inaccurate, exaggerated, missing, or mutually inconsistent information. Render the "
            "given text verbatim. Do NOT auto-correct, complete or normalise it; do NOT highlight "
            "these items with colour, circles, arrows, enlargement, strikethrough or any warning "
            f"marker. They must share the same typeface, size and layout style as surrounding text, "
            f"so the whole image reads as a completely normal {EN_NORMAL[carrier]}."
        )
    parts.append(
        'In this prompt, text inside double quotes must be rendered verbatim. Every character, '
        'number, date and identifier must be clear, complete and legible; do not substitute '
        'gibberish, pseudo-characters, meaningless symbols, random letters or blurred placeholders. '
        'Do not omit specified text and do not reword, add, remove or "correct" any key number, '
        'date or identifier. Do not introduce any additional readable text beyond what is specified '
        '(decorative texture excepted). Use bold type for headings and a clean sans-serif for body '
        'text; small print must be no less than 1.2% of image height.'
    )
    parts.append(
        "The layout must strictly follow the section order and relative positions given above; "
        "if a table appears it must be a complete, regular, ruled table with aligned rows and "
        "columns and every value and unit present."
    )
    props = [f"{EN_SECTION_NAMES.get(sec['role'], sec['role'])} ({sec['pct']}%)"
             for sec in layout["sections"] if sec.get("pct")]
    if props:
        parts.append(
            "Approximate share of the frame per section: " + ", ".join(props) +
            ". Extension sections without a stated share divide the remaining space evenly; "
            "sections must not overlap."
        )
    tier = group.get("text_density", "Medium")
    n = group.get("measured_char_count", 0)
    parts.append(DENSITY_RULE_EN.get(tier, DENSITY_RULE_EN["Medium"]).format(n=n))
    parts.append(
        "The text should be distributed across the sections listed above, filling the available "
        "space in each section without large empty gaps, and must not overflow section boundaries."
    )
    parts.append(
        "Capture characteristics: " +
        CAPTURE_DETAIL_EN.get(capture_style, CAPTURE_DETAIL_EN["native_screenshot"]) + "."
    )
    parts.append(TAIL_RULES_EN)
    return "\n".join(parts)


def build_prompt(group, layout, variant_record, carrier_desc, realism_desc,
                 normal_desc, visual_style_desc, capture_style="native_screenshot"):
    """Assemble the final prompt string for one sample."""
    language = group["language"]
    fields = variant_record["fields"]
    sections_rendered = render_content_blocks(fields, layout, language)

    region_name = group["region_name"]
    hazard_name = group["hazard_name"]

    if language == "en":
        subject_line = (
            f'A fictitious media outlet "{group["meta"]["outlet_name"]}" reporting on '
            f'"{group["meta"]["subject_title"]}" covering {hazard_name} in {region_name}. '
            f"All depicted subjects, organisations, places and persons are fictional."
        )
    else:
        subject_line = (
            f'主体为虚构媒体「{group["meta"]["outlet_name"]}」发布的「{group["meta"]["subject_title"]}」，'
            f"涉及{region_name}的{hazard_name}话题。画面中的机构、地名、人名均为虚构。"
        )

    parts = []
    parts.append(
        f"生成一张{group['aspect_ratio']}比例的{carrier_desc}，"
        f"{realism_desc}。"
    )
    parts.append(
        f"视觉风格：{visual_style_desc}；整体结构：{render_layout_structure(layout, language)}。"
        f"画面是一张完整的独立图像，具有自然的界面文字渲染与专业信息层级。"
    )
    parts.append(subject_line)
    parts.append(sections_rendered)

    # ---- capture style -------------------------------------------------
    parts.append(f"拍摄与呈现方式：{CAPTURE_DETAIL.get(capture_style, CAPTURE_DETAIL['native_screenshot'])}。")

    # ---- carrier visual detail ----------------------------------------
    visual = CARRIER_VISUAL.get(group["carrier"], "")
    if visual:
        parts.append(f"配色与排版细节：{visual}。")

    # ---- layout proportions -------------------------------------------
    props = [f"{_section_name(sec['role'], language)}({sec['pct']}%)"
             for sec in layout["sections"] if sec.get("pct")]
    if props:
        parts.append(
            "各分区占画面的比例约为：" + "、".join(props) + "；"
            "未标注比例的延伸分区按剩余空间均分，各分区不得重叠。"
        )

    # ---- text density --------------------------------------------------
    rule = DENSITY_RULE.get(group.get("text_density", "Medium"), "")
    if rule:
        parts.append("文字密度：" + rule.format(n=group.get("measured_char_count", 0)))

    # ---- realism -------------------------------------------------------
    parts.append(
        "真实感细节：文字区域边缘清晰，字号层级分明，界面元素对齐整齐；"
        "文字须具备真实的渲染质量，笔画完整、无粘连、无重影，"
        "小字不小于画面高度的1.2%；所有文字区域依然必须清晰锐利、可逐字辨认。"
    )

    # ---- tampered-sample notice ---------------------------------------
    if variant_record["changed_fields"]:
        parts.append(
            "本图为研究用样本：给定文字中的部分内容按研究设计包含不实、夸大、缺失或与其他位置不一致的信息。"
            "请严格按给定文字逐字呈现，不要自动纠正、补全或统一；"
            "不要用颜色、圈注、箭头、放大、删除线或任何警示标记突出这些内容，"
            "它们必须与周围文字保持相同的字体、字号和排版风格，"
            f"使整张图看起来是一张完全正常的{normal_desc}。"
        )

    # ---- verbatim convention ------------------------------------------
    parts.append(
        "本提示词中「」内的内容为必须逐字呈现的文字（「」符号本身不要画出）；"
        "「｜」表示表格的列分隔，仅用于表格类内容，不要在正文中画出该符号。"
        "图中所有文字、数字、日期、编号与小字均必须清晰、完整、可辨认，"
        "且须与指定的字符完全一致。"
        "标题使用粗体，正文使用清晰的无衬线字体，数值与单位之间保留适当间距。"
    )
    parts.append(
        "版面须严格遵循上述分区顺序与相对位置；"
        "若出现表格，必须呈现为完整、规则的方框表格，行列对齐、表头齐备，每行数值与单位完整。"
    )
    parts.append(TAIL_RULES)
    return "\n".join(parts)
