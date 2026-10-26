#!/usr/bin/env python3
"""站内链接自检：检查所有 HTML 的本地 href/src/url() 是否指向真实文件，锚点是否存在。"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["index.html", "404.html", "privacy.html"] + [
    "details/" + p.name for p in sorted((ROOT / "details").glob("*.html"))
]

HTML_RE = re.compile(r'(?:href|src)\s*=\s*["\']([^"\']+)["\']', re.I)
CSS_RE = re.compile(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)', re.I)
ID_RE = re.compile(r'\bid\s*=\s*["\']([^"\']+)["\']', re.I)


def ids_of(path: Path) -> set[str]:
    try:
        return set(ID_RE.findall(path.read_text(encoding="utf-8", errors="ignore")))
    except OSError:
        return set()


def main() -> int:
    problems: list[str] = []
    checked = 0
    ids_cache: dict[Path, set[str]] = {}

    for page in PAGES:
        path = ROOT / page
        text = path.read_text(encoding="utf-8", errors="ignore")
        refs = HTML_RE.findall(text) + CSS_RE.findall(text)
        for ref in refs:
            ref = ref.strip()
            if not ref or ref.startswith(("#", "mailto:", "tel:", "data:", "javascript:", "http:", "https:", "//")):
                if ref.startswith("#") and len(ref) > 1:
                    target = path
                    frag = ref[1:]
                    ids = ids_cache.setdefault(target, ids_of(target))
                    if unquote(frag) not in ids:
                        problems.append(f"{page}: 页内锚点不存在 {ref}")
                continue
            checked += 1
            ref_path, _, frag = ref.partition("#")
            if not ref_path:
                continue
            if ref_path.startswith("/"):
                target = (ROOT / unquote(ref_path).lstrip("/")).resolve()
            else:
                target = (path.parent / unquote(ref_path)).resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                problems.append(f"{page}: 文件不存在 → {ref}")
                continue
            if frag and target.suffix == ".html":
                ids = ids_cache.setdefault(target, ids_of(target))
                if unquote(frag) not in ids:
                    problems.append(f"{page}: 锚点不存在 {ref}")

    print(f"检查 {len(PAGES)} 个页面，{checked} 个本地引用")
    if problems:
        print("发现问题：")
        for p in problems:
            print("  [x]", p)
        return 1
    print("[ok] 全部本地链接与锚点有效")
    return 0


if __name__ == "__main__":
    sys.exit(main())
