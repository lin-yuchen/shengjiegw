# 升捷發展有限公司 · 官网

升捷發展有限公司（GALAXY ELITE DEVELOPMENT LIMITED）官方网站：<https://www.shengjiefazhan.com>

纯静态站点，由 GitHub Pages 托管，`main` 分支根目录即线上代码。推送到 `main` 后 1–2 分钟自动发布，无需构建。

---

## 一、站点结构

```
index.html            首页（轮播 / 关于 / 服务 / 网络 / 优势 / 合作 / 联系）
404.html              404 页
privacy.html          隐私政策
robots.txt            搜索引擎抓取规则
sitemap.xml           站点地图（新增页面后需手动添加）
CNAME                 自定义域名
details/              详情页
  company.html        关于我们
  service-1.html      劳务外包与人力资源
  service-2.html      宅配与城市配送
  service-3.html      打板与仓储人力
  service-4.html      中港跨境运输
  service-5.html      港澳运输
  service-6.html      定制化解决方案
assets/
  css/style.css       首页样式
  css/detail.css      详情页样式
  css/fonts/          字体样式 + WOFF2 子集
  css/font-awesome/   图标库
  js/main.js          轮播、导航、二维码预览
  images/             WebP 图片（slides / network / services / advantages / partners）
  logo/               LOGO
  qr/                 微信、WhatsApp、小红书二维码
tools/                维护脚本（见下）
```

---

## 二、日常运营怎么做

### 改文字

直接编辑对应 HTML。注意：**改完中文文案后必须重新生成字体子集**，否则新增的字会回退成系统字体（不会乱码，但字形不一致）。

```powershell
git checkout HEAD -- assets/css/fonts/noto-sans-sc assets/css/fonts/inter   # 临时取回原始字体
python tools/optimize_assets.py                                            # 重新生成子集
Remove-Item -Recurse assets/css/fonts/noto-sans-sc, assets/css/fonts/inter  # 用完删除
```

### 换图片

把新图放进 `assets/images/` 下对应目录，然后：

```powershell
python tools/optimize_assets.py     # 会自动按目录规则转 WebP 并压缩
```

脚本里 `jobs` 列表规定了每张图的目标宽度与质量；新增图片需要在该列表登记一行。

### 改服务页文案

服务页由 `tools/build_details.py` 生成，文案集中在文件顶部的 `SERVICES` 列表里。
改完运行：

```powershell
python tools/build_details.py
```

### 发布前自检

```powershell
python tools/check_links.py     # 检查所有本地链接、锚点是否有效
```

---

## 三、发布与回滚

```powershell
git add -A
git commit -m "说明这次改了什么"
git push origin main
```

> 建议先推到 `ops/...` 分支，确认无误再合并到 `main`。

GitHub Pages 构建需要 1–2 分钟。回滚：

```powershell
git revert <commit>
```

---

## 四、当前已知待办

- 公司详细地址仍是「香港特别行政区（到访请提前预约）」，需补充真实地址；地址确认后再放地图（原 OpenStreetMap 内嵌框已撤除，它指向中环且国内常打不开）。
- 原有「在线咨询（AI 助手）」为前端模拟回复，已于 2026-10-26 移除；如需在线转化，建议改用表单或客服系统。
- 全站电话已统一为 +86 13042079996（原香港号码 +852 95790010 已停用），如恢复香港线路需同步更新首页、7 个详情页、404 页、隐私页与 JSON-LD。
- Font Awesome 图标库约 380KB，可进一步裁剪到只含实际使用的 20 余个图标。
- 合作伙伴（SHEIN、菜鸟、顺丰、拼多多等）LOGO 的使用需确认已获授权。
