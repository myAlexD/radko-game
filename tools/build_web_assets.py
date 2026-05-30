#!/usr/bin/env python3
"""Slug + compress the raw Canva PNG exports into web-friendly JPGs.

Reads from scene/ (Cyrillic, spaced filenames, 1920x1080, 2-5 MB PNG) and
writes scene/web/<slug>.jpg (1600x900, quality 88) — URL-safe names, ~100-250 KB
each, suitable for hosting on GitHub + jsDelivr and loading on a tablet.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "scene")
OUT = os.path.join(SRC, "web")
TARGET = (1600, 900)   # 16:9 downscale from the 1920x1080 source
QUALITY = 88

# raw filename -> url-safe slug (no extension)
SLUGS = {
    "1.png": "menu",
    "Ниво 1 - Заглавна.png": "l1-title",
    "Кръстовище 1.png": "l1-s1-reka",
    "Кръстовище 2.png": "l1-s2-darvo",
    "Кръстовище 3.png": "l1-s3-drakon",
    "Кръстовище 4.png": "l1-s4-peshtera",
    "Кръстовище 6.png": "l1-s5-vrata",
    "Кръстовище 7.png": "l1-s6-korona",
    "Финал - Корона.png": "l1-win",
    "Ниво 2 - Заглавна.png": "l2-title",
    "Ниво 2 - 1. Подножието.png": "l2-s1-krepost",
    "Ниво 2 - 2. Намира оръжие.png": "l2-s2",
    "Ниво 2 - 3. Ровът.png": "l2-s3-krokodil",
    "Ниво 2 - 4. Сечи пътя.png": "l2-s4-bradva",
    "Ниво 2 - 5. Самият дракон.png": "l2-s5-drakon",
    "Ниво 2 - 6. Кулата.png": "l2-s6-vrata",
    "Ниво 2 - 7. Финал.png": "l2-s7-printsesa",
    "Ниво 2 - Финал.png": "l2-win",
    "Ниво 3 - Начало (полет).png": "l3-intro",
    "Ниво 3 - Денят на буквите.png": "l3-q1",
}

def main():
    os.makedirs(OUT, exist_ok=True)
    total_in = total_out = 0
    missing = []
    for raw, slug in sorted(SLUGS.items(), key=lambda kv: kv[1]):
        src = os.path.join(SRC, raw)
        if not os.path.exists(src):
            missing.append(raw)
            continue
        dst = os.path.join(OUT, slug + ".jpg")
        try:
            im = Image.open(src).convert("RGB")
            im = im.resize(TARGET, Image.LANCZOS)
            im.save(dst, "JPEG", quality=QUALITY, optimize=True, progressive=True)
        except Exception as e:
            print(f"  ERROR {raw}: {e}")
            continue
        a = os.path.getsize(src); b = os.path.getsize(dst)
        total_in += a; total_out += b
        print(f"  {slug+'.jpg':22} {b/1024:7.0f} KB   (from {a/1024/1024:.1f} MB  {raw})")
    print(f"\nTotal: {total_in/1024/1024:.1f} MB -> {total_out/1024:.0f} KB"
          f" ({total_out/1024/1024:.2f} MB) across {len(SLUGS)-len(missing)} files")
    if missing:
        print("MISSING sources:", missing)

if __name__ == "__main__":
    main()
