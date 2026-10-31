"""Static site generator for zenvixtechnologies.com.

Usage:  python3 _build/build.py
Writes all HTML pages, sitemap.xml, robots.txt and site.webmanifest into the project root.
"""
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from layout import SITE, render  # noqa: E402
import pages  # noqa: E402
from services_data import SERVICES  # noqa: E402


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)


def og_image():
    """1200x630 social share image from the hero artwork + logo."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return
    out = os.path.join(ROOT, "assets/img/og-image.jpg")
    bg = Image.open(os.path.join(ROOT, "assets/img/hero-bg.webp")).convert("RGB")
    ratio = max(1200 / bg.width, 630 / bg.height)
    bg = bg.resize((round(bg.width * ratio), round(bg.height * ratio)))
    bg = bg.crop((bg.width - 1200, 0, bg.width, 630))
    shade = Image.new("RGBA", (1200, 630))
    d = ImageDraw.Draw(shade)
    for x in range(1200):
        a = int(max(0, 235 - x * 0.32))
        d.line([(x, 0), (x, 630)], fill=(255, 255, 255, a))
    bg = Image.alpha_composite(bg.convert("RGBA"), shade)
    logo = Image.open(os.path.join(ROOT, "assets/img/logo.png")).convert("RGBA")
    logo = logo.resize((round(logo.width * 1.6), round(logo.height * 1.6)))
    bg.alpha_composite(logo, (70, 245))
    bg.convert("RGB").save(out, quality=86)


def main():
    blogs = pages.load_blogs()
    built = []

    def emit(page_body):
        page, body = page_body
        write(page["path"], render(page, body))
        built.append(page)

    emit(pages.home(blogs))
    emit(pages.about())
    emit(pages.services_overview())
    for s in SERVICES:
        emit(pages.service_page(s, blogs))
    emit(pages.blog_list(blogs))
    for b in blogs:
        emit(pages.blog_post(b, blogs))
    emit(pages.contact())
    emit(pages.not_found())

    today = datetime.date.today().isoformat()
    prio = {"index.html": "1.0", "services.html": "0.9", "contact.html": "0.8", "about.html": "0.7", "blog.html": "0.7"}
    urls = []
    for p in built:
        if p["path"] == "404.html":
            continue
        loc = SITE["url"] + "/" + p["path"].replace("index.html", "")
        pr = prio.get(p["path"], "0.8" if p["path"].startswith("services/") else "0.6")
        urls.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: {SITE['url']}/sitemap.xml\n")
    write("site.webmanifest", json.dumps({
        "name": "Zenvix Technologies", "short_name": "Zenvix", "start_url": "/", "display": "standalone",
        "background_color": "#ffffff", "theme_color": "#7c3aed",
        "icons": [{"src": "/assets/img/favicon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/img/favicon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2))
    og_image()
    print(f"Built {len(built)} pages.")


if __name__ == "__main__":
    main()
