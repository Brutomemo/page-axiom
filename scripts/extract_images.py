#!/usr/bin/env python3
import base64
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
backup = SITE / "index.html.backup"
index = SITE / "index.html"
images_dir = SITE / "assets" / "images"
images_dir.mkdir(parents=True, exist_ok=True)

html = backup.read_text(encoding="utf-8")
urls = re.findall(r'src="(data:image/[^"]+)"', html)
names = ["logo-nav", "hero-visual", "profile-marcos"]
ext_map = {}

for url, name in zip(urls, names):
    m = re.match(r"data:image/([\w+.-]+);base64,(.+)", url)
    if not m:
        print("skip", name)
        continue
    mime, b64 = m.group(1), m.group(2)
    if "webp" in mime:
        ext = "webp"
    elif "jpeg" in mime or "jpg" in mime:
        ext = "jpg"
    else:
        ext = "png"
    path = images_dir / f"{name}.{ext}"
    path.write_bytes(base64.b64decode(b64))
    ext_map[name] = ext
    print("wrote", path, path.stat().st_size)

idx = index.read_text(encoding="utf-8")
for name, ext in ext_map.items():
    idx = re.sub(
        rf'assets/images/{name}\.png',
        f"assets/images/{name}.{ext}",
        idx,
    )
index.write_text(idx, encoding="utf-8")
print("done", list(images_dir.glob("*")))
