<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:sm="http://www.sitemaps.org/schemas/sitemap/0.9"
    exclude-result-prefixes="sm">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>

    <xsl:template match="/">
        <html lang="zh-HK">
            <head>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1"/>
                <title>网站地图（XML）｜升捷發展有限公司</title>
                <style>
                    body { margin: 0; font-family: 'Noto Sans SC', 'Microsoft JhengHei', sans-serif; color: #1f2d3d; background: #f6f8fb; }
                    .wrap { max-width: 900px; margin: 0 auto; padding: 40px 20px 80px; }
                    h1 { font-size: 1.6rem; color: #0d1b2a; margin: 0 0 8px; }
                    p.note { color: #5b6b7b; font-size: .92rem; margin: 0 0 24px; }
                    a { color: #1b4965; }
                    table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 10px; overflow: hidden; box-shadow: 0 6px 20px rgba(13,27,42,.06); }
                    th, td { text-align: left; padding: 10px 14px; border-bottom: 1px solid #e6edf3; font-size: .92rem; }
                    th { background: #0d1b2a; color: #fff; font-weight: 600; }
                    tr:last-child td { border-bottom: 0; }
                    td.url { word-break: break-all; }
                </style>
            </head>
            <body>
                <div class="wrap">
                    <h1>网站地图（XML）</h1>
                    <p class="note">本文件供搜索引擎抓取。人读版本请访问 <a href="/sitemap.html">/sitemap.html</a>。</p>
                    <table>
                        <tr><th>页面地址</th><th>更新日期</th><th>优先级</th></tr>
                        <xsl:for-each select="sm:urlset/sm:url">
                            <tr>
                                <td class="url"><a href="{sm:loc}"><xsl:value-of select="sm:loc"/></a></td>
                                <td><xsl:value-of select="sm:lastmod"/></td>
                                <td><xsl:value-of select="sm:priority"/></td>
                            </tr>
                        </xsl:for-each>
                    </table>
                </div>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
