"""Small real-event library used as factual anchors for prompt content.

The generator cycles through these events deterministically. Each event keeps a
source URL and a compact fact set; generated records store the provenance in
metadata so downstream users can separate factual anchors from fabricated
self-consistent rumor variants.
"""

REAL_EVENTS = [
    {
        "event_id": "EVT-WHO-20230505",
        "hazard": "H2",
        "title_zh": "世卫组织结束新冠疫情国际关注的突发公共卫生事件状态",
        "title_en": "WHO ends COVID-19 public health emergency status",
        "date": "2023年5月5日",
        "date_en": "May 5, 2023",
        "place_zh": "日内瓦",
        "place_en": "Geneva",
        "source_name": "World Health Organization",
        "source_url": "https://www.who.int/europe/news/item/05-05-2023-statement-on-the-fifteenth-meeting-of-the-international-health-regulations-%282005%29-emergency-committee-regarding-the-coronavirus-disease-%28covid-19%29-pandemic",
        "facts_zh": [
            "世界卫生组织于2023年5月5日宣布，新冠疫情不再构成国际关注的突发公共卫生事件。",
            "世卫组织同时表示，新冠仍是持续存在的公共卫生问题，各国仍需保持长期管理和监测。",
            "相关决定依据国际卫生条例突发事件委员会第十五次会议建议作出。",
        ],
        "facts_en": [
            "The World Health Organization said on May 5, 2023 that COVID-19 no longer constituted a public health emergency of international concern.",
            "WHO also said COVID-19 remained an established and ongoing public health issue requiring long-term management.",
            "The decision followed advice from the fifteenth meeting of the International Health Regulations Emergency Committee.",
        ],
        "false_claim_zh": "多地网传称世卫组织宣布所有新冠疫苗接种记录即日起失效，并要求各国重新登记健康码。",
        "false_claim_en": "Posts falsely claim WHO invalidated all COVID-19 vaccination records and required countries to restart health-code registration.",
    },
    {
        "event_id": "EVT-NASA-20221116",
        "hazard": "H7",
        "title_zh": "NASA 阿尔忒弥斯一号发射升空",
        "title_en": "NASA launches Artemis I mission",
        "date": "2022年11月16日",
        "date_en": "November 16, 2022",
        "place_zh": "佛罗里达州肯尼迪航天中心",
        "place_en": "Kennedy Space Center, Florida",
        "source_name": "NASA",
        "source_url": "https://www.nasa.gov/news-release/liftoff-nasas-artemis-i-mega-rocket-launches-orion-to-moon/",
        "facts_zh": [
            "NASA 的太空发射系统火箭于2022年11月16日搭载猎户座飞船从肯尼迪航天中心发射升空。",
            "阿尔忒弥斯一号是对深空探索系统的首次综合飞行测试。",
            "任务不载人，主要用于验证火箭、飞船和地面系统。",
        ],
        "facts_en": [
            "NASA's Space Launch System rocket launched the Orion spacecraft from Kennedy Space Center on November 16, 2022.",
            "Artemis I was the first integrated flight test of NASA's deep space exploration systems.",
            "The mission was uncrewed and designed to test the rocket, spacecraft and ground systems.",
        ],
        "false_claim_zh": "社交平台流传称阿尔忒弥斯一号搭载了商业游客并已在月面短暂停留。",
        "false_claim_en": "Social posts falsely claim Artemis I carried commercial tourists and briefly landed on the lunar surface.",
    },
    {
        "event_id": "EVT-USGS-20230206",
        "hazard": "H1",
        "title_zh": "土耳其叙利亚边境附近发生 7.8 级地震",
        "title_en": "Magnitude 7.8 earthquake strikes near the Türkiye-Syria border",
        "date": "2023年2月6日",
        "date_en": "February 6, 2023",
        "place_zh": "土耳其中南部靠近叙利亚边境地区",
        "place_en": "south-central Türkiye near the Syrian border",
        "source_name": "U.S. Geological Survey",
        "source_url": "https://www.usgs.gov/index.php/programs/earthquake-hazards/science/frequently-asked-questions-about-2023-earthquakes-turkiye",
        "facts_zh": [
            "美国地质调查局记录显示，2023年2月6日土耳其中南部靠近叙利亚边境地区发生 7.8 级地震。",
            "地震发生后，土耳其、叙利亚及周边多地均有震感。",
            "美国地质调查局随后发布了关于此次地震序列的科普说明和数据页面。",
        ],
        "facts_en": [
            "USGS recorded a magnitude 7.8 earthquake on February 6, 2023 in south-central Türkiye near the Syrian border.",
            "The earthquake was felt across Türkiye, Syria and surrounding countries.",
            "USGS later published explanatory material and data pages about the earthquake sequence.",
        ],
        "false_claim_zh": "网传消息称此次地震已被权威机构提前三天精确预报到街区，并要求所有居民按截图名单撤离。",
        "false_claim_en": "Viral posts falsely claim authorities predicted the quake down to street level three days in advance and ordered evacuations from a screenshot list.",
    },
]


def event_for(group):
    """Return a deterministic real event compatible with the group hazard."""
    pool = [e for e in REAL_EVENTS if e["hazard"] == group["hazard"]] or REAL_EVENTS
    idx = (int(group["group_id"][1:]) - 1) % len(pool)
    return pool[idx]

