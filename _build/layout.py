"""Site-wide config and shared layout: <head>, header, mobile drawer, footer."""
import json
from html import escape
from icons import icon, sprite

SITE = {
    "name": "Zenvix Technologies",
    "url": "https://zenvixtechnologies.com",
    "email": "zenvixtechnologies7@gmail.com",
    "phone": "+92 326 4549778",
    "phone_href": "+923264549778",
    "whatsapp": "https://wa.me/923264549778",
    "address": "Gulberg, Lahore, Punjab, Pakistan",
    "map": "https://share.google/JHnFjofZhqNVF7J7r",
    "map_embed": "https://www.google.com/maps?q=Gulberg,+Lahore,+Punjab,+Pakistan&output=embed",
    "hours": "Mon–Sat, 9am–7pm PKT",
    "social": [
        ("Facebook", "facebook", "#"),
        ("Instagram", "instagram", "#"),
        ("X", "x-twitter", "#"),
        ("LinkedIn", "linkedin", "#"),
    ],
    "tagline": "Software, web, mobile & digital marketing company in Lahore, Pakistan — serving clients in Pakistan, the US, UK and the Gulf.",
}

# Order = order in the Services mega menu
SERVICES_NAV = [
    ("web-development", "Web Development", "monitor", "Fast, SEO-ready websites & web apps"),
    ("software-development", "Software Development", "code", "Custom software, CRM & ERP systems"),
    ("mobile-app-development", "Mobile App Development", "smartphone", "Android, iOS & Flutter apps"),
    ("social-media-marketing", "Social Media Marketing", "share", "Grow, engage & convert on social"),
    ("seo-services", "SEO Services", "trending-up", "Rank higher, win organic traffic"),
    ("email-marketing", "Email Marketing", "mail", "Campaigns that land & convert"),
    ("ui-ux-design", "UI/UX Design", "pen-tool", "Research-led, conversion-focused design"),
    ("ai-solutions", "AI Solutions", "cpu", "Chatbots, automation & LLM integration"),
]

NAV = [("index.html", "Home", "home"), ("about.html", "About", "about"), ("services.html", "Services", "services"),
       ("blog.html", "Blog", "blog"), ("contact.html", "Contact", "contact")]


def jsonld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'


def org_schema():
    s = SITE
    return {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "@id": s["url"] + "/#organization",
        "name": s["name"],
        "url": s["url"] + "/",
        "logo": s["url"] + "/assets/img/logo.png",
        "image": s["url"] + "/assets/img/og-image.jpg",
        "email": s["email"],
        "telephone": s["phone"],
        "priceRange": "$$",
        "description": "Zenvix Technologies is a software development and digital marketing company in Lahore, Pakistan, building custom software, websites, mobile apps, AI solutions and growth campaigns for clients worldwide.",
        "address": {"@type": "PostalAddress", "addressLocality": "Gulberg, Lahore", "addressRegion": "Punjab", "addressCountry": "PK"},
        "geo": {"@type": "GeoCoordinates", "latitude": 31.5204, "longitude": 74.3487},
        "areaServed": ["Pakistan", "United States", "United Kingdom", "United Arab Emirates", "Saudi Arabia", "Qatar", "Worldwide"],
        "openingHours": "Mo-Sa 09:00-19:00",
        "sameAs": [],
        "contactPoint": {"@type": "ContactPoint", "telephone": s["phone"], "email": s["email"], "contactType": "sales", "availableLanguage": ["English", "Urdu"]},
    }


def breadcrumb_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE["url"] + "/" + u}
                            for i, (n, u) in enumerate(items)],
    }


def head(page):
    R = page["root"]
    url = SITE["url"] + "/" + page["path"].replace("index.html", "")
    title = page["title"]
    desc = page["desc"]
    og_img = SITE["url"] + "/" + page.get("og", "assets/img/og-image.jpg")
    preload = ""
    if page.get("preload"):
        p = page["preload"]
        preload = f'<link rel="preload" as="image" href="{R}{p[0]}" imagesrcset="{R}{p[1]} 900w, {R}{p[0]} 1400w" imagesizes="100vw" fetchpriority="high">'
    schemas = "".join(jsonld(s) for s in page.get("schema", []))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<meta name="robots" content="{page.get('robots', 'index,follow,max-image-preview:large')}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#7c3aed">
<meta name="author" content="Zenvix Technologies">
<meta property="og:type" content="{page.get('og_type', 'website')}">
<meta property="og:site_name" content="Zenvix Technologies">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(title)}">
<meta name="twitter:description" content="{escape(desc)}">
<meta name="twitter:image" content="{og_img}">
<meta name="geo.region" content="PK-PB">
<meta name="geo.placename" content="Lahore">
<link rel="icon" href="{R}favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="{R}assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="{R}assets/img/favicon-180.png">
<link rel="manifest" href="{R}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap">
{preload}
<script>document.documentElement.classList.add("js")</script>
<link rel="stylesheet" href="{R}assets/css/style.css?v=1">
{schemas}
</head>"""


def header(page):
    R = page["root"]
    active = page.get("nav", "")
    mega = "".join(
        f'<a class="mega-item" href="{R}services/{slug}.html"><span class="mega-ic">{icon(ic)}</span>'
        f'<span><b>{name}</b><small>{d}</small></span></a>'
        for slug, name, ic, d in SERVICES_NAV)
    links = []
    for href, label, key in NAV:
        cls = ' class="is-active" aria-current="page"' if key == active else ""
        if key == "services":
            links.append(
                f'<li class="has-mega"><a href="{R}{href}"{cls}>Services {icon("chevron-down", "ic ic-sm caret")}</a>'
                f'<div class="mega" role="menu"><div class="mega-inner"><div class="mega-grid">{mega}</div>'
                f'<div class="mega-promo"><span class="eyebrow light">Free assessment</span><h3>Not sure where to start?</h3>'
                f'<p>Book a 30-minute call with one of our engineers. Written findings, no obligation.</p>'
                f'<a class="btn btn-light btn-sm" href="{R}contact.html">Book a free call {icon("arrow-right", "ic ic-sm")}</a></div></div></div></li>')
        else:
            links.append(f'<li><a href="{R}{href}"{cls}>{label}</a></li>')
    drawer_services = "".join(f'<a href="{R}services/{s}.html">{icon(ic, "ic ic-sm")}{n}</a>' for s, n, ic, _ in SERVICES_NAV)
    drawer_links = []
    for href, label, key in NAV:
        cls = ' class="is-active"' if key == active else ""
        if key == "services":
            drawer_links.append(
                f'<li class="d-acc"><div class="d-acc-row"><a href="{R}{href}"{cls}>Services</a>'
                f'<button class="d-acc-btn" aria-expanded="false" aria-label="Show services">{icon("chevron-down")}</button></div>'
                f'<div class="d-acc-panel"><div>{drawer_services}</div></div></li>')
        else:
            drawer_links.append(f'<li><a href="{R}{href}"{cls}>{label}</a></li>')
    social = "".join(f'<a href="{u}" aria-label="{n}" rel="noopener">{icon(ic, "ic ic-sm")}</a>' for n, ic, u in SITE["social"])
    return f"""<body class="{page.get('body', '')}">
{sprite()}
<a class="skip-link" href="#main">Skip to content</a>
<div class="progress-bar" aria-hidden="true"></div>
<header class="site-header" id="top">
  <div class="topbar">
    <div class="container topbar-inner">
      <div class="topbar-info">
        <a href="mailto:{SITE['email']}">{icon('mail', 'ic ic-sm')}{SITE['email']}</a>
        <a href="tel:{SITE['phone_href']}">{icon('phone', 'ic ic-sm')}{SITE['phone']}</a>
        <span class="hide-md">{icon('map-pin', 'ic ic-sm')}Gulberg, Lahore · Serving clients worldwide</span>
      </div>
      <div class="topbar-social">{social}</div>
    </div>
  </div>
  <div class="navbar">
    <div class="container navbar-inner">
      <a class="brand" href="{R}index.html" aria-label="Zenvix Technologies — Home">
        <img src="{R}assets/img/logo.webp" alt="Zenvix Technologies" width="188" height="60">
      </a>
      <nav class="main-nav" aria-label="Main"><ul>{''.join(links)}</ul></nav>
      <div class="nav-actions">
        <a class="nav-call" href="tel:{SITE['phone_href']}" aria-label="Call us">
          <span class="nav-call-ic">{icon('phone', 'ic ic-sm')}</span>
          <span class="nav-call-txt"><small>Talk to an expert</small><b>{SITE['phone']}</b></span>
        </a>
        <a class="btn btn-primary btn-sm nav-cta" href="{R}contact.html"><span>Get a Free Quote</span>{icon('arrow-up-right', 'ic ic-sm')}</a>
        <button class="burger" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
      </div>
    </div>
  </div>
</header>
<div class="drawer-overlay" data-close-drawer></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true">
  <div class="drawer-head">
    <a class="brand" href="{R}index.html"><img src="{R}assets/img/logo.webp" alt="Zenvix Technologies" width="150" height="48" loading="lazy"></a>
    <button class="drawer-close" data-close-drawer aria-label="Close menu">{icon('x')}</button>
  </div>
  <nav class="drawer-nav" aria-label="Mobile"><ul>{''.join(drawer_links)}</ul></nav>
  <a class="btn btn-primary btn-block" href="{R}contact.html">Get a Free Quote {icon('arrow-right', 'ic ic-sm')}</a>
  <div class="drawer-contact">
    <a href="tel:{SITE['phone_href']}">{icon('phone', 'ic ic-sm')}{SITE['phone']}</a>
    <a href="mailto:{SITE['email']}">{icon('mail', 'ic ic-sm')}{SITE['email']}</a>
    <a href="{SITE['map']}" target="_blank" rel="noopener">{icon('map-pin', 'ic ic-sm')}Gulberg, Lahore, Pakistan</a>
  </div>
  <div class="drawer-social">{social}</div>
</aside>
<main id="main">"""


def footer(page):
    R = page["root"]
    social = "".join(f'<a href="{u}" aria-label="Zenvix on {n}" rel="noopener">{icon(ic, "ic ic-sm")}</a>' for n, ic, u in SITE["social"])
    svc = "".join(f'<li><a href="{R}services/{s}.html">{n}</a></li>' for s, n, _, _ in SERVICES_NAV)
    return f"""</main>
<footer class="site-footer">
  <div class="footer-glow" aria-hidden="true"></div>
  <div class="container">
    <div class="footer-cta reveal">
      <div>
        <span class="eyebrow light">{icon('sparkle', 'ic ic-xs')} Let's work together</span>
        <h2>Have a project in mind? <span class="grad-text-light">Let's talk.</span></h2>
        <p>Tell us what you're building. You'll hear back from a real engineer within one business day.</p>
      </div>
      <div class="footer-cta-actions">
        <a class="btn btn-light" href="{R}contact.html">Start Your Project {icon('arrow-right', 'ic ic-sm')}</a>
        <a class="btn btn-ghost-light" href="{SITE['whatsapp']}" target="_blank" rel="noopener">{icon('whatsapp', 'ic ic-sm')} WhatsApp us</a>
      </div>
    </div>
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="{R}index.html"><img src="{R}assets/img/logo-light.webp" alt="Zenvix Technologies" width="188" height="60" loading="lazy"></a>
        <p>Premium software development and digital marketing company delivering world-class digital products for businesses in Pakistan, the US, UK and the Gulf.</p>
        <form class="newsletter" data-newsletter novalidate>
          <label for="nl-email-{page['path']}" class="sr-only">Email address</label>
          <input id="nl-email-{page['path']}" type="email" placeholder="Your email for insights" required>
          <button type="submit" aria-label="Subscribe">{icon('send', 'ic ic-sm')}</button>
          <small class="newsletter-msg" role="status" aria-live="polite"></small>
        </form>
        <div class="footer-social">{social}</div>
      </div>
      <div>
        <h3>Services</h3>
        <ul>{svc}</ul>
      </div>
      <div>
        <h3>Company</h3>
        <ul>
          <li><a href="{R}about.html">About Us</a></li>
          <li><a href="{R}services.html">All Services</a></li>
          <li><a href="{R}index.html#portfolio">Our Work</a></li>
          <li><a href="{R}blog.html">Blog &amp; Insights</a></li>
          <li><a href="{R}contact.html">Contact</a></li>
          <li><a href="{R}contact.html#faq">FAQs</a></li>
        </ul>
      </div>
      <div>
        <h3>Get in touch</h3>
        <ul class="footer-contact">
          <li><a href="mailto:{SITE['email']}"><span>{icon('mail', 'ic ic-sm')}</span>{SITE['email']}</a></li>
          <li><a href="tel:{SITE['phone_href']}"><span>{icon('phone', 'ic ic-sm')}</span>{SITE['phone']}</a></li>
          <li><a href="{SITE['map']}" target="_blank" rel="noopener"><span>{icon('map-pin', 'ic ic-sm')}</span>Gulberg, Lahore,<br>Punjab, Pakistan</a></li>
          <li><span class="fc-static"><span>{icon('clock', 'ic ic-sm')}</span>{SITE['hours']}</span></li>
        </ul>
      </div>
    </div>
    <div class="footer-regions">
      <span>{icon('globe', 'ic ic-sm')} Serving clients in</span>
      <ul><li>Pakistan</li><li>United States</li><li>United Kingdom</li><li>UAE</li><li>Saudi Arabia</li><li>Qatar</li><li>Worldwide</li></ul>
    </div>
    <div class="footer-bottom">
      <p>© <span data-year>2026</span> Zenvix Technologies. All rights reserved.</p>
    </div>
  </div>
</footer>
<a class="float-wa" href="{SITE['whatsapp']}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{icon('whatsapp')}</a>
<button class="to-top" aria-label="Back to top"><svg class="to-top-ring" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="22"/></svg>{icon('arrow-up', 'ic ic-sm')}</button>
<script src="{R}assets/js/main.js?v=1" defer></script>
</body>
</html>"""


def render(page, body):
    return head(page) + "\n" + header(page) + "\n" + body + "\n" + footer(page)


def img(R, src, alt, w, h, cls="", eager=False, sizes=None):
    lazy = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="{R}{src}" alt="{escape(alt)}" width="{w}" height="{h}" {lazy} decoding="async"{c}>'


def page_hero(R, eyebrow, title, text, crumbs, bg=None, actions=""):
    """Inner-page hero with breadcrumb. crumbs: [(label, href or None)]"""
    bc = []
    for i, (lab, href) in enumerate(crumbs):
        if href:
            bc.append(f'<li><a href="{R}{href}">{lab}</a></li>')
        else:
            bc.append(f'<li aria-current="page">{lab}</li>')
    bg_html = f'<div class="ph-bg"><img src="{R}{bg}" alt="" width="1600" height="900" fetchpriority="high" decoding="async"></div>' if bg else ""
    return f"""<section class="page-hero">
  {bg_html}
  <div class="ph-grid" aria-hidden="true"></div>
  <div class="container ph-inner">
    <nav aria-label="Breadcrumb"><ol class="crumbs">{''.join(bc)}</ol></nav>
    <span class="eyebrow light anim-up">{icon('sparkle', 'ic ic-xs')} {eyebrow}</span>
    <h1 class="anim-up" style="--d:.08s">{title}</h1>
    <p class="anim-up" style="--d:.16s">{text}</p>
    {f'<div class="ph-actions anim-up" style="--d:.24s">{actions}</div>' if actions else ''}
  </div>
</section>"""
