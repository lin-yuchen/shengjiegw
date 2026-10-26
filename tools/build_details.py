#!/usr/bin/env python3
"""生成 details/ 下的公司页与 6 个服务详情页。

页面结构统一（品牌头部 + 面包屑 + 正文 + 侧栏 + 转化区 + 页脚），
内容取自首页既有文案，补充了通用的服务流程与适用场景说明。
修改文案后运行：python tools/build_details.py
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DETAILS = ROOT / "details"
BASE = "https://www.shengjiefazhan.com"

COMPANY = {
    "name": "升捷發展有限公司",
    "phone": "+86 13042079996",
    "tel": "+8613042079996",
    "email": "postmaster@r-quick.cn",
    "email_cs": "Elina@r-quick.cn",
}

NAV = [
    ("../index.html", "首页"),
    ("company.html", "关于我们"),
    ("../index.html#services", "服务项目"),
    ("../index.html#network", "运输网络"),
    ("../index.html#contact", "联系我们"),
]

SERVICES = [
    {
        "file": "company.html",
        "nav_label": "关于我们",
        "title": "关于我们｜升捷發展有限公司",
        "h1": "关于香港升捷發展有限公司",
        "desc": "升捷發展有限公司 2017 年成立于香港，专注劳务外包与综合物流服务，覆盖人力资源、仓储打板、最后一公里配送与中港／港澳跨境运输。",
        "lead": "升捷發展有限公司（GALAXY ELITE DEVELOPMENT LIMITED）2017 年成立于香港，以人力资源为核心，为企业提供劳务外包与综合物流服务。",
        "kind": "company",
        "blocks": [
            ("我们做什么", [
                "劳务外包与人力资源管理：招聘、培训、薪酬代发、现场管理与合规咨询。",
                "仓储与打板：现场作业团队、分拣贴标、出入库流程与品质管控。",
                "最后一公里配送：全港 18 区配送团队与人力外包，含排班与督导。",
                "跨境运输：中港陆运、港澳运输与清关支持，可配套司机与地勤人力。",
            ]),
        ],
        "steps": [
            ("了解现状", "梳理客户的业务场景、人力缺口、时效与合规要求。"),
            ("方案与报价", "给出人力配置、作业流程与费用结构，明确交付标准。"),
            ("派驻与培训", "完成招聘、岗前培训与合规文件，团队进场。"),
            ("运营与复盘", "现场督导、替补机制与月度数据复盘，持续优化。"),
        ],
        "scenarios": [
            "电商与零售企业在港扩编、旺季临时用工",
            "品牌进入香港市场，需要一站式落地人力与物流配套",
            "现有仓配、运输团队需要外包管理与替补机制",
        ],
        "stats": [("2017", "成立年份"), ("500+", "服务企业客户"), ("98%", "客户满意度")],
        "related": [("service-1.html", "香港劳务外包与人力资源"), ("service-2.html", "宅配与城市配送"), ("service-6.html", "定制化解决方案")],
    },
    {
        "file": "service-1.html",
        "nav_label": "劳务外包",
        "title": "香港劳务外包与人力资源｜升捷發展有限公司",
        "h1": "香港劳务外包与人力资源",
        "desc": "提供香港招聘外包、岗前培训、薪酬代发与现场人事管理，帮助雇主快速组建合规团队并降低用人成本。",
        "lead": "以人力资源为核心，提供大规模招聘、岗前培训、薪酬代发与现场人事管理，帮助雇主在香港快速部署团队，并降低用人成本与合规风险。",
        "kind": "service",
        "blocks": [
            ("解决什么问题", [
                "在港招聘周期长、渠道分散，岗位长期空缺影响业务节奏。",
                "劳工法例、强积金与雇佣合约要求细，人事处理耗时且易出错。",
                "旺季与项目制用工波动大，自建团队淡季成本高。",
            ]),
            ("服务内容", [
                "专业人才招聘与筛选",
                "薪酬福利管理外包",
                "员工培训与发展",
                "劳动法规咨询",
                "现场人事管理与替补机制",
            ]),
        ],
        "steps": [
            ("需求梳理", "确认岗位、人数、班次、技能要求与预算区间。"),
            ("招聘与筛选", "本地人才库与多渠道路径投放，完成面试与背景核实。"),
            ("培训与派驻", "岗前培训、合规文件签署，团队按约定时间进场。"),
            ("运营与复盘", "考勤与薪酬结算、离职替补、月度人力数据复盘。"),
        ],
        "scenarios": [
            "电商仓配旺季扩编，短期需要数十人作业团队",
            "零售门店开业，需要店员、理货与后勤人员",
            "物流现场长期驻场，需要稳定的操作与管理人手",
        ],
        "stats": [("48h", "首批候选人响应"), ("全港", "18 区覆盖"), ("98%", "客户满意度")],
        "related": [("service-2.html", "宅配与城市配送"), ("service-3.html", "打板与仓储人力"), ("service-6.html", "定制化解决方案")],
    },
    {
        "file": "service-2.html",
        "nav_label": "宅配城配",
        "title": "香港宅配与城市配送（人力外包支持）｜升捷發展有限公司",
        "h1": "香港宅配与城市配送（人力外包支持）",
        "desc": "覆盖香港全境的最后一公里配送，并提供配送团队的招聘、排班与现场督导人力外包服务。",
        "lead": "覆盖香港全境的最后一公里配送，我们同时提供配送团队的人力外包与管理，承担招聘、排班与现场督导，降低客户的用工与管理压力。",
        "kind": "service",
        "blocks": [
            ("解决什么问题", [
                "配送人力流动率高，招聘与培训持续消耗管理精力。",
                "旺季单量突增，临时运力难以快速到位。",
                "派送异常、客诉与工单处理缺少专人跟进。",
            ]),
            ("服务内容", [
                "快递配送上门",
                "实时在线客服",
                "异常工单处理",
                "优化配送策略",
                "配送团队的招聘、排班与现场督导",
            ]),
        ],
        "steps": [
            ("线路与时效确认", "明确服务区域、时效标准与异常处理规则。"),
            ("团队组建", "按单量配置配送员与督导，完成培训与装备交接。"),
            ("上线运营", "排班调度、实时客服与异常工单闭环处理。"),
            ("数据复盘", "时效、签收率与客诉数据按月复盘并调整配置。"),
        ],
        "scenarios": [
            "电商平台在大促期间需要临时配送运力",
            "零售与连锁品牌需要覆盖全港的上门配送",
            "自建配送团队需要外包管理与替补机制",
        ],
        "stats": [("18 区", "全港覆盖"), ("7×24", "异常响应"), ("当日/次日", "可选时效")],
        "related": [("service-1.html", "劳务外包与人力资源"), ("service-3.html", "打板与仓储人力"), ("service-4.html", "中港跨境运输")],
    },
    {
        "file": "service-3.html",
        "nav_label": "打板仓储",
        "title": "香港打板与仓储人力支持｜升捷發展有限公司",
        "h1": "香港打板与仓储人力支持",
        "desc": "为仓储与装运环节提供打板、分拣、贴标与现场作业团队，负责招聘、培训与流程管理。",
        "lead": "为仓储与装运环节提供操作团队与流程管理，我们负责现场人力的招聘与培训，确保出货效率与品质控制，减少企业现场管理负担。",
        "kind": "service",
        "blocks": [
            ("解决什么问题", [
                "出货高峰集中，现场人手不足导致装运延误。",
                "打板与贴标标准不统一，装运差错与返工频繁。",
                "现场管理依赖客户自有主管，难以弹性扩缩。",
            ]),
            ("服务内容", [
                "标准化货物打板",
                "香港本地提货",
                "货物分拣与标签",
                "仓储管理服务",
                "现场作业团队与流程督导",
            ]),
        ],
        "steps": [
            ("现场勘测", "确认仓库动线、设备条件与作业标准。"),
            ("团队配置", "按出货量配置操作员、组长与质检。"),
            ("标准落地", "统一打板与贴标规范，培训后进场作业。"),
            ("效率复盘", "装运效率、差错率与人力投入按月复盘。"),
        ],
        "scenarios": [
            "生产与贸易企业需要现场装箱与打板团队",
            "电商仓在旺季需要临时分拣与贴标人手",
            "香港本地提货与仓到仓转运需要配套作业团队",
        ],
        "stats": [("25%", "装箱效率提升案例"), ("全港", "提货与派送"), ("按量", "弹性配置")],
        "related": [("service-1.html", "劳务外包与人力资源"), ("service-2.html", "宅配与城市配送"), ("service-4.html", "中港跨境运输")],
    },
    {
        "file": "service-4.html",
        "nav_label": "中港运输",
        "title": "中港跨境运输（含人力运维）｜升捷發展有限公司",
        "h1": "中港跨境运输（含人力运维）",
        "desc": "提供中港陆运、报关清关与仓到仓运输，并可配套司机与地勤团队的人力外包，保障旺季运力稳定。",
        "lead": "提供中港陆运与跨境运输服务，并可为客户配备驾驶与地勤团队的人力外包服务，确保节假日与旺季运输能力稳定。",
        "kind": "service",
        "blocks": [
            ("解决什么问题", [
                "节假日与旺季司机紧缺，运力价格波动大。",
                "报关与清关环节衔接不顺，影响整体时效。",
                "跨境线路多、单据杂，缺少统一对接窗口。",
            ]),
            ("服务内容", [
                "中港陆路运输",
                "香港存柜服务",
                "报关清关服务",
                "实时在线客服",
                "司机与地勤人力外包",
            ]),
        ],
        "steps": [
            ("线路与货型确认", "明确起运地、目的地、货型与时效要求。"),
            ("方案与报价", "给出运输方式、班次与费用结构。"),
            ("运输执行", "提货、报关、过境与派送全过程跟踪。"),
            ("异常与结算", "异常件快速处理，按月对账结算。"),
        ],
        "scenarios": [
            "跨境电商在大促期间需要稳定的中港运力",
            "珠三角工厂出货至香港仓或口岸",
            "需要司机与地勤团队外包以降低自营成本",
        ],
        "stats": [("中港", "干线直达"), ("仓到仓", "门到门可选"), ("旺季", "运力保障")],
        "related": [("service-5.html", "港澳运输"), ("service-3.html", "打板与仓储人力"), ("service-6.html", "定制化解决方案")],
    },
    {
        "file": "service-5.html",
        "nav_label": "港澳运输",
        "title": "港澳运输与末端人力支持｜升捷發展有限公司",
        "h1": "港澳运输与末端人力支持",
        "desc": "经港珠澳大桥与海运通道提供香港至澳门跨境运输，配套末端派送与客服人力外包。",
        "lead": "提供香港至澳门的跨境运输服务，并在终端提供派送与客服的人力外包支持，帮助连锁与零售客户快速展开本地服务。",
        "kind": "service",
        "blocks": [
            ("解决什么问题", [
                "澳门开店与铺货节奏紧，本地人手与运力都要临时搭建。",
                "清关与末端派送衔接不畅，影响上架与销售。",
                "连锁门店补货频次高，需要稳定的固定班次。",
            ]),
            ("服务内容", [
                "港珠澳大桥陆路运输",
                "海运快速通道",
                "澳门清关服务",
                "仓到仓配送",
                "末端派送与客服人力外包",
            ]),
        ],
        "steps": [
            ("需求确认", "确认货量、频次、时效与澳门收货条件。"),
            ("通道选择", "按货物属性选择陆路或海运通道并报价。"),
            ("运输与清关", "安排班次、报关文件与过境衔接。"),
            ("末端交付", "门店或仓库交付，异常件跟进处理。"),
        ],
        "scenarios": [
            "连锁零售在澳门开店期间的铺货与补货",
            "品牌需要在澳门配置临时派送与客服人员",
            "香港仓至澳门仓的定期转运",
        ],
        "stats": [("3-5h", "桥运时效"), ("澳门", "清关与派送"), ("定期", "班次可选")],
        "related": [("service-4.html", "中港跨境运输"), ("service-2.html", "宅配与城市配送"), ("service-6.html", "定制化解决方案")],
    },
    {
        "file": "service-6.html",
        "nav_label": "定制方案",
        "title": "定制化人力与物流解决方案｜升捷發展有限公司",
        "h1": "定制化人力与物流解决方案",
        "desc": "根据业务场景定制人力配置与物流配套，从入港人员配置到末端配送与客服一体化交付。",
        "lead": "根据客户业务场景定制人力配置与物流配套，从入港人员配置到末端配送与客户服务一体化交付，帮助企业以更轻的模式进入香港市场。",
        "kind": "service",
        "blocks": [
            ("解决什么问题", [
                "进入香港市场需要同时解决人手、仓储、配送与合规。",
                "多供应商各自对接，责任边界与时效难以统一。",
                "业务模式尚未稳定，不适合一次性重投入自建团队。",
            ]),
            ("服务内容", [
                "业务流程分析",
                "定制化解决方案设计",
                "项目实施与管理",
                "持续优化与支持",
                "人力、仓储与配送的一体化交付",
            ]),
        ],
        "steps": [
            ("业务诊断", "梳理业务流程、成本结构与关键时效节点。"),
            ("方案设计", "组合人力、仓储、配送与运输模块，给出实施路径。"),
            ("落地实施", "按里程碑推进招聘、进场、系统与流程对接。"),
            ("持续运营", "按月复盘指标，动态调整配置与流程。"),
        ],
        "scenarios": [
            "品牌首次进入香港，需要一站式落地配套",
            "业务快速扩张，现有人力与物流体系承载不足",
            "需要把分散的供应商整合为单一责任窗口",
        ],
        "stats": [("3 周", "快速启动案例"), ("一体化", "人力＋物流"), ("按月", "数据复盘")],
        "related": [("service-1.html", "劳务外包与人力资源"), ("service-4.html", "中港跨境运输"), ("company.html", "关于我们")],
    },
]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def render(s: dict) -> str:
    related = "\n".join(
        f'          <a href="{href}">{esc(label)}</a>' for href, label in s["related"]
    )
    blocks = []
    for title, items in s["blocks"]:
        if len(items) == 4 and title in ("服务内容",):
            lst = "\n".join(f'            <li>{esc(i)}</li>' for i in items)
            blocks.append(f'        <h2>{esc(title)}</h2>\n        <ul class="dp-list">\n{lst}\n        </ul>')
        else:
            lst = "\n".join(f'            <li>{esc(i)}</li>' for i in items)
            blocks.append(f'        <h2>{esc(title)}</h2>\n        <ul class="dp-list">\n{lst}\n        </ul>')
    steps = "\n".join(
        f'          <li><strong>{esc(t)}</strong><br>{esc(d)}</li>' for t, d in s["steps"]
    )
    scenarios = "\n".join(f'            <li>{esc(i)}</li>' for i in s["scenarios"])
    stats = "\n".join(
        f'            <div class="dp-stat"><span class="n">{esc(n)}</span><span class="l">{esc(l)}</span></div>'
        for n, l in s["stats"]
    )
    nav = "\n".join(
        f'        <a href="{href}"' + (' class="is-current"' if label == s["nav_label"] else "") + f'>{esc(label)}</a>'
        for href, label in NAV
    )
    canonical = f'{BASE}/details/{s["file"]}'
    jsonld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": s["h1"], "item": canonical},
        ],
    }
    service_ld = ""
    if s["kind"] == "service":
        service_ld = """
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Service",
      "name": "%s",
      "serviceType": "%s",
      "provider": { "@type": "Organization", "name": "升捷發展有限公司", "url": "https://www.shengjiefazhan.com/" },
      "areaServed": ["香港", "澳门", "珠三角"],
      "url": "%s"
    }
    </script>""" % (s["h1"], s["h1"], canonical)

    return f"""<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{esc(s["title"])}</title>
    <meta name="description" content="{esc(s["desc"])}">
    <link rel="canonical" href="{canonical}">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta name="theme-color" content="#0d1b2a">
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="升捷發展有限公司">
    <meta property="og:title" content="{esc(s["title"])}">
    <meta property="og:description" content="{esc(s["desc"])}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{BASE}/assets/images/og-cover.png">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" href="/favicon.ico" sizes="any">
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/icon-32.png">
    <link rel="apple-touch-icon" href="/assets/icon-180.png">
    <link rel="stylesheet" href="../assets/css/font-awesome/all.min.css">
    <link rel="stylesheet" href="../assets/css/fonts/fonts.css">
    <link rel="stylesheet" href="../assets/css/detail.css">
    <script type="application/ld+json">
    {json.dumps(jsonld, ensure_ascii=False, indent=2)}
    </script>{service_ld}
</head>
<body>
    <header class="dp-header">
        <div class="inner">
            <a class="dp-brand" href="../index.html">
                <img src="../assets/logo/logo-96.webp" width="40" height="40" alt="升捷發展有限公司">
                <span>升捷發展有限公司<small>GALAXY ELITE DEVELOPMENT LIMITED</small></span>
            </a>
            <nav class="dp-nav">
{nav}
            </nav>
        </div>
    </header>

    <main class="dp-main">
        <nav class="dp-crumb" aria-label="面包屑">
            <a href="../index.html"><i class="fas fa-arrow-left"></i> 返回首页</a>
            <span class="sep">/</span>
            <span>{esc(s["h1"])}</span>
        </nav>

        <div class="dp-grid">
            <article>
                <h1>{esc(s["h1"])}</h1>
                <p class="dp-lead">{esc(s["lead"])}</p>

{chr(10).join(blocks)}

                <h2>服务流程</h2>
                <ol class="dp-steps">
{steps}
                </ol>

                <h2>适用场景</h2>
                <ul class="dp-list">
{scenarios}
                </ul>

                <div class="dp-cta">
                    <h2>需要报价或落地方案？</h2>
                    <p>告诉我们业务场景与预计人数／货量，我们会在一个工作日内给出初步方案与费用结构。</p>
                    <a class="dp-btn" href="tel:{COMPANY["tel"]}"><i class="fas fa-phone-alt"></i> {COMPANY["phone"]}</a>
                    <a class="dp-btn dp-btn-ghost" href="../index.html#contact">在线咨询</a>
                </div>
            </article>

            <aside>
                <div class="dp-card">
                    <h3>关键数据</h3>
{stats}
                </div>
                <div class="dp-card">
                    <h3>联系我们</h3>
                    <p><i class="fas fa-phone"></i> <a href="tel:{COMPANY["tel"]}" style="color:inherit;text-decoration:none">{COMPANY["phone"]}</a>（24 小时客服）</p>
                    <p><i class="fas fa-envelope"></i> {COMPANY["email"]}</p>
                    <p><i class="fas fa-clock"></i> 周一至周五 9:00–18:00</p>
                </div>
                <div class="dp-card">
                    <h3>相关服务</h3>
                    <div class="dp-related">
{related}
                    </div>
                </div>
            </aside>
        </div>
    </main>

    <footer class="dp-footer">
        <div class="inner">
            <p>© 2026 升捷發展有限公司 GALAXY ELITE DEVELOPMENT LIMITED</p>
            <p><a href="../index.html">首页</a> · <a href="../index.html#services">服务项目</a> · <a href="../privacy.html">隐私政策</a> · <a href="../sitemap.html">网站地图</a></p>
        </div>
    </footer>
</body>
</html>
"""


def main() -> int:
    DETAILS.mkdir(exist_ok=True)
    for s in SERVICES:
        (DETAILS / s["file"]).write_text(render(s), encoding="utf-8")
        print("wrote details/" + s["file"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
