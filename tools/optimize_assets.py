#!/usr/bin/env python3
"""升捷官网静态资源优化脚本。

用途：在改动文案/新增图片后重新生成轻量资源。
    python tools/optimize_assets.py

做三件事：
1. 从所有 HTML/JS 中收集实际使用到的字符，把 Noto Sans SC / Inter 的 TTF
   裁剪成只含这些字符的 WOFF2（整站 20MB+ 字体 → 约 150KB）。
2. 把大图转成 WebP 并按实际显示尺寸降采样。
3. 生成 logo、favicon、apple-touch-icon。

注意：字体只包含当前页面出现的字符；若页面新增了生僻字，
浏览器会自动回退到系统字体（Microsoft JhengHei / PingFang），
不会出现方框，但重跑本脚本可让新字也用品牌字体。
"""
from __future__ import annotations

import html
import io
import os
import re
import sys
from pathlib import Path

from PIL import Image
from fontTools import subset

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# ---------------------------------------------------------------- 字符集

SAFETY_CHARS = (
    "．，。、；：？！（）【】《》“”‘’—…·￥$%&*+-=/@#"
    "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz "
    "香港九龙新界湾区澳门深圳东莞珠海佛山的士货物运输仓储配送调度客服热线邮箱地址办公时间周一二三四五六日"
    "升捷發展有限公司 人力資源勞務外包物流解決方案報價查詢合作夥伴"
)


def collect_chars() -> str:
    chars: set[str] = set(SAFETY_CHARS)
    for pattern in ("*.html", "details/*.html", "assets/js/*.js"):
        for path in sorted(ROOT.glob(pattern)):
            text = path.read_text(encoding="utf-8", errors="ignore")
            text = re.sub(r"<[^>]+>", " ", text)          # 去掉标签
            text = html.unescape(text)                    # 还原 &amp; 等
            chars.update(ch for ch in text if ch.isprintable() and ch not in "\r\n\t")
    return "".join(sorted(chars))


def subset_font(src: Path, dst: Path, text: str, label: str) -> None:
    if not src.exists():
        print(f"  ! 缺少 {src.name}，跳过")
        return
    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["kern", "liga", "calt"]
    options.name_IDs = ["*"]
    options.recalc_bounds = True
    options.desubroutinize = False

    font = subset.load_font(str(src), options)
    sub = subset.Subsetter(options=options)
    sub.populate(text=text)
    sub.subset(font)
    buf = io.BytesIO()
    font.save(buf)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(buf.getvalue())
    print(f"  字 {label:<26} {len(buf.getvalue()) / 1024:7.1f} KB  ← {src.name}")


# ---------------------------------------------------------------- 图片

def to_webp(src: Path, dst: Path, width: int, quality: int = 80, animated: bool = True) -> None:
    im = Image.open(src)
    if getattr(im, "is_animated", False) and not animated:
        im.seek(0)
        frame = im.convert("RGBA" if "A" in im.mode else "RGB")
        if frame.width > width:
            frame = frame.resize((width, round(frame.height * width / frame.width)), Image.LANCZOS)
        frame.save(dst, "WEBP", quality=quality, method=6)
        print(f"  图 {dst.relative_to(ROOT).as_posix():<46} {src.stat().st_size / 1024:8.0f} → {dst.stat().st_size / 1024:6.1f} KB (静态首帧)")
        return
    if getattr(im, "is_animated", False):
        frames = []
        for i in range(im.n_frames):
            im.seek(i)
            f = im.convert("RGBA" if "A" in im.mode else "RGB")
            frames.append(f.copy())
        frames = [f.resize((width, round(f.height * width / f.width)), Image.LANCZOS) for f in frames]
        frames[0].save(dst, "WEBP", save_all=True, append_images=frames[1:], quality=quality, method=6)
    else:
        im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
        if im.width > width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        im.save(dst, "WEBP", quality=quality, method=6)
    print(f"  图 {dst.relative_to(ROOT).as_posix():<46} {src.stat().st_size / 1024:8.0f} → {dst.stat().st_size / 1024:6.1f} KB")


def optimize_images() -> None:
    jobs = [
        # (源, 目标, 宽度, 质量)
        ("assets/images/slides/slide-1.jpg", "assets/images/slides/slide-1.webp", 1600, 76),
        ("assets/images/slides/slide-2.jpg", "assets/images/slides/slide-2.webp", 1600, 76),
        ("assets/images/slides/slide-3.jpg", "assets/images/slides/slide-3.webp", 1600, 80),
        ("assets/images/slides/slide-4.jpg", "assets/images/slides/slide-4.webp", 1600, 80),
        ("assets/images/slides/slide-5.jpg", "assets/images/slides/slide-5.webp", 1600, 80),
        ("assets/images/network/network-1.jpg", "assets/images/network/network-1.webp", 800, 78),
        ("assets/images/network/network-2.jpg", "assets/images/network/network-2.webp", 900, 78),
        ("assets/images/network/network-3.jpg", "assets/images/network/network-3.webp", 800, 78),
        ("assets/images/network/network-4.jpg", "assets/images/network/network-4.webp", 900, 78),
        ("assets/images/services/service-1.jpg", "assets/images/services/service-1.webp", 720, 78),
        ("assets/images/services/service-2.jpg", "assets/images/services/service-2.webp", 720, 78),
        ("assets/images/services/service-3.jpg", "assets/images/services/service-3.webp", 720, 78),
        ("assets/images/services/service-4.jpg", "assets/images/services/service-4.webp", 720, 78),
        ("assets/images/services/service-5.jpg", "assets/images/services/service-5.webp", 720, 78),
        ("assets/images/services/service-6.jpg", "assets/images/services/service-6.webp", 720, 78),
        ("assets/images/advantages/advantage-1.jpg", "assets/images/advantages/advantage-1.webp", 240, 82),
        ("assets/images/advantages/advantage-2.jpg", "assets/images/advantages/advantage-2.webp", 240, 82),
        ("assets/images/advantages/advantage-3.jpg", "assets/images/advantages/advantage-3.webp", 240, 82),
        ("assets/images/advantages/advantage-4.jpg", "assets/images/advantages/advantage-4.webp", 240, 82),
        ("assets/images/advantages/advantage-5.jpg", "assets/images/advantages/advantage-5.webp", 240, 82),
        ("assets/images/advantages/advantage-6.jpg", "assets/images/advantages/advantage-6.webp", 240, 82),
        ("assets/images/partners/cainiao.gif", "assets/images/partners/cainiao.webp", 320, 88, False),
        ("assets/images/partners/pdd.png", "assets/images/partners/pdd.webp", 320, 88),
        ("assets/images/partners/shein.png", "assets/images/partners/shein.webp", 320, 88),
        ("assets/images/partners/ouhua.png", "assets/images/partners/ouhua.webp", 320, 88),
        ("assets/images/partners/sf-express.png", "assets/images/partners/sf-express.webp", 320, 88),
        ("assets/images/partners/honghaihui.png", "assets/images/partners/honghaihui.webp", 320, 88),
    ]
    for job in jobs:
        src_rel, dst_rel, width, q = job[:4]
        animated = job[4] if len(job) > 4 else True
        src, dst = ROOT / src_rel, ROOT / dst_rel
        if not src.exists():
            print(f"  ! 缺少 {src_rel}")
            continue
        to_webp(src, dst, width, q, animated)


def build_brand_assets() -> None:
    logo_src = ASSETS / "logo" / "公司LOGO.png"
    im = Image.open(logo_src).convert("RGBA")
    # 去白底，保留透明（LOGO 为白底方形图，页面在深色导航栏上使用）
    if im.mode == "RGBA":
        px = im.load()
        w, h = im.size
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if r > 244 and g > 244 and b > 244:
                    px[x, y] = (r, g, b, 0)
    for width, name in ((480, "logo.webp"), (96, "logo-96.webp")):
        out = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        out.save(ASSETS / "logo" / name, "WEBP", quality=90, method=6)
        print(f"  图 assets/logo/{name:<38} {width}px")

    # favicon 用方图裁切
    fav = Image.open(logo_src).convert("RGBA")
    side = min(fav.size)
    left = (fav.width - side) // 2
    fav = fav.crop((left, 0, left + side, side))
    for size in (32, 180, 192):
        fav.resize((size, size), Image.LANCZOS).save(ASSETS / f"icon-{size}.png", "PNG", optimize=True)
    fav.resize((48, 48), Image.LANCZOS).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("  图 favicon.ico / icon-32.png / icon-180.png / icon-192.png")


def build_og_cover() -> None:
    """生成 1200x630 的社交分享封面图。"""
    font_path = ASSETS / "css/fonts/noto-sans-sc/NotoSansSC-Bold.ttf"
    if not font_path.exists():
        print("  ! 缺少 NotoSansSC-Bold.ttf，跳过 og-cover")
        return
    from PIL import ImageDraw, ImageFont

    W, H = 1200, 630
    img = Image.new("RGB", (W, H), "#0d1b2a")
    draw = ImageDraw.Draw(img)
    # 斜向渐变底 + 强调色块
    for x in range(W):
        t = x / W
        draw.line([(x, 0), (x, H)], fill=(int(13 + 8 * t), int(27 + 20 * t), int(42 + 34 * t)))
    draw.ellipse([W - 420, -160, W + 120, 380], fill=(0, 140, 170))
    draw.ellipse([-180, H - 240, 260, H + 160], fill=(0, 96, 120))

    logo = Image.open(ASSETS / "logo" / "公司LOGO.png").convert("RGBA")
    logo.thumbnail((150, 150), Image.LANCZOS)
    img.paste(logo, (90, 80), logo)

    f_brand = ImageFont.truetype(str(font_path), 54)
    f_title = ImageFont.truetype(str(font_path), 68)
    f_sub = ImageFont.truetype(str(font_path), 34)

    draw.text((262, 96), "升捷發展有限公司", font=f_brand, fill="#ffffff")
    draw.text((262, 166), "GALAXY ELITE DEVELOPMENT LIMITED", font=f_sub, fill="#9adbe8")
    draw.text((90, 300), "香港勞務外包與物流配送", font=f_title, fill="#ffffff")
    draw.text((90, 396), "人力資源 ・ 倉儲打板 ・ 最後一公里配送 ・ 中港港澳運輸", font=f_sub, fill="#cfe8f3")
    draw.text((90, 510), "www.shengjiefazhan.com", font=f_sub, fill="#90e0ef")

    out = ASSETS / "images" / "og-cover.png"
    img.save(out, "PNG", optimize=True)
    print(f"  图 assets/images/og-cover.png  {out.stat().st_size / 1024:.0f} KB")


def main() -> int:
    text = collect_chars()
    print(f"字符集：{len(text)} 个字符")
    print("字体子集化：")
    subset_font(ASSETS / "css/fonts/noto-sans-sc/NotoSansSC-Regular.ttf",
                ASSETS / "css/fonts/NotoSansSC-Regular.woff2", text, "Noto Sans SC 400")
    subset_font(ASSETS / "css/fonts/noto-sans-sc/NotoSansSC-Bold.ttf",
                ASSETS / "css/fonts/NotoSansSC-Bold.woff2", text, "Noto Sans SC 700")
    subset_font(ASSETS / "css/fonts/inter/Inter-Regular.ttf",
                ASSETS / "css/fonts/Inter-Regular.woff2", text, "Inter 400")
    subset_font(ASSETS / "css/fonts/inter/Inter-SemiBold.ttf.ttf",
                ASSETS / "css/fonts/Inter-SemiBold.woff2", text, "Inter 600")
    subset_font(ASSETS / "css/fonts/inter/Inter-Bold.ttf",
                ASSETS / "css/fonts/Inter-Bold.woff2", text, "Inter 700")

    print("图片优化：")
    optimize_images()

    print("品牌图：")
    build_brand_assets()
    build_og_cover()
    return 0


if __name__ == "__main__":
    sys.exit(main())
