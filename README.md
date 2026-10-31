# Zenvix Technologies — Website

Static HTML/CSS/JS site for zenvixtechnologies.com. No frameworks, no dependencies at runtime.

## Structure

```
index.html  about.html  services.html  blog.html  contact.html  404.html
services/   8 service pages (web, software, mobile, SMM, SEO, email, UI/UX, AI)
blog/       3 articles (from the 2026 blog collection PDF)
assets/css/style.css   all styles (tokens at the top)
assets/js/main.js      all interactions
assets/img/            WebP images, logo, favicons, og-image
sitemap.xml  robots.txt  site.webmanifest
_build/                page generator (source of truth for the HTML)
```

## Editing content

The HTML files are generated. Edit the sources in `_build/`, then rebuild:

```bash
python3 _build/build.py
```

- `_build/layout.py` — contact details, social links, header, mobile drawer, footer, SEO `<head>`
- `_build/pages.py` — Home, About, Contact, Services overview, Blog list/post templates
- `_build/services_data.py` — all service page content (typed sections + FAQs)
- `_build/data/blogs.json` — blog article bodies

Social links are `#` placeholders — set them in `SITE["social"]` in `layout.py`.

## Local preview

```bash
python3 -m http.server 8090
```

Then open http://localhost:8090.

## Notes for the WordPress theme conversion

- `header()` / `footer()` in `layout.py` map to `header.php` / `footer.php`.
- Each section type in `render_section()` maps to a template part or block.
- The contact form currently validates and opens the visitor's email app (mailto) —
  replace with Contact Form 7 / WPForms or a PHP handler during conversion.
- The footer/blog newsletter forms work the same way until a mailing service is connected.

## WordPress theme

Build the theme from the same templates:

```bash
python3 _build/build_wp.py
```

Output: `wordpress/zenvix-theme.zip` (upload via **Appearance → Themes → Add New → Upload Theme**).
Hand-written theme PHP lives in `_build/wp/`; page templates are generated — don't edit them in WordPress.

After activating:
- **Appearance → Zenvix Setup** — plugin status (Contact Form 7, WP Mail SMTP) and "Run setup"
  (creates missing pages, sets Home/Blog, imports the 3 articles; safe to re-run).
- **Appearance → Zenvix Settings** — email, phone, WhatsApp, address, map, social links.
- **Inquiries** — every contact form submission (also emailed to the settings email).
- On localhost, emails are written to `wp-content/zx-mail-log.txt` instead of being sent,
  until WP Mail SMTP is configured.
