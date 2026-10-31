"""Page builders. Run: python3 _build/build.py"""
import json
import re
from html import escape
from icons import icon
from layout import SITE, SERVICES_NAV, render, img, page_hero, org_schema, breadcrumb_schema
from services_data import SERVICES, INDUSTRIES, DEFAULT_PROCESS

CHK = icon("check", "ic ic-xs")

HOME_STATS = [("100", "+", "Projects Completed"), ("50", "+", "Happy Clients"), ("10", "+", "Industries Served"), ("24/7", "", "Technical Support")]

WHY = [("zap", "Fast Delivery", "Agile development process with quick project turnaround and consistent milestone delivery."),
       ("shield", "High Security", "Advanced security standards and scalable infrastructure for your peace of mind."),
       ("headphones", "24/7 Support", "Dedicated support and maintenance for all projects, around the clock."),
       ("award", "Award-Winning Quality", "Pixel-perfect execution with rigorous code reviews and QA processes built in."),
       ("users", "Expert Team", "Seasoned developers, designers, and strategists working together on every project."),
       ("eye", "Transparent Process", "Regular updates, open communication, and no surprises — ever.")]

HOME_SERVICES = [("mobile-app-development", "smartphone", "Mobile App Development", "Android, iOS, Flutter, and React Native applications with modern UI/UX and high performance.", False),
                 ("web-development", "monitor", "Web Development", "Responsive websites and scalable web applications built using modern technologies.", False),
                 ("software-development", "code", "Custom Software", "Enterprise systems, CRM, ERP, and custom business automation solutions.", False),
                 ("ui-ux-design", "pen-tool", "UI/UX Design", "Premium user-centered designs with smooth user experience and modern interfaces.", False),
                 ("ai-solutions", "cpu", "AI Solutions", "AI integrations, automation systems, intelligent chatbots, and smart platforms.", False),
                 ("seo-services", "trending-up", "SEO & Marketing", "Boost your rankings and business visibility with advanced digital marketing solutions.", False),
                 ("social-media-marketing", "share", "Social Media Management", "Plan, publish, and grow your brand presence across social platforms.", True),
                 ("email-marketing", "mail", "Email Marketing", "Reach and retain customers with targeted email campaigns.", True)]

HOME_INDUSTRIES = [("activity", "Healthcare"), ("book", "Education"), ("home", "Real Estate"), ("cart", "E-commerce"),
                   ("dollar", "Finance"), ("truck", "Logistics"), ("navigation", "Travel"), ("heart", "Fitness")]

PROJECTS = [("MedTrack Pro", "Healthcare · Web Platform", "A full-stack patient management system with real-time doctor-patient communication, appointment booking, and EHR integration.", ["React", "Node.js", "MongoDB"], "assets/img/un/mobile-dev.webp", "web design"),
            ("ShopFlow", "E-Commerce · Web App", "High-conversion storefront with Stripe payments, real-time inventory management, and a custom admin dashboard.", ["Next.js", "Stripe", "Firebase"], "assets/img/un/laptop-analytics.webp", "web"),
            ("NexaERP", "Enterprise · ERP System", "End-to-end enterprise resource planning covering HR, finance, inventory, and reporting for a 200-person organization.", ["Laravel", "Vue.js", "MySQL"], "assets/img/un/laptop-code.webp", "web design"),
            ("FitPulse", "Fitness · Mobile App", "A smart fitness tracking app with AI-generated workout plans, wearable integration, and nutrition logging.", ["Flutter", "Firebase", "TensorFlow"], "assets/img/un/phone-app.webp", "mobile ai")]

TESTIMONIALS = [("AK", "Ahmed Khan", "CEO, MedTech", "Zenvix Technologies delivered a modern enterprise platform with excellent performance and outstanding UI. Truly a world-class team."),
                ("SA", "Sarah Ali", "Founder, E-Shop", "Professional team with excellent communication and high-quality development standards. Delivered on time, every time."),
                ("UT", "Usman Tariq", "Director, TravelTech", "Outstanding UI/UX and scalable backend systems. Highly recommended software company for any serious business.")]

BLOG_META = [  # order = PDF order; slug, date, image, short excerpt for cards
    {"slug": "custom-software-development-advantages-benefits-cost", "date": "2026-10-12", "img": "assets/img/un/laptop-code2.webp",
     "card": "What custom software is, how it compares with off-the-shelf products, and what it costs.", "tags": ["Custom Software", "Business", "Costs"]},
    {"slug": "cost-to-build-a-mobile-app-in-2026", "date": "2026-10-16", "img": "assets/img/un/seo-laptop.webp",
     "card": "From a simple MVP to an enterprise-grade platform: what mobile app development costs in 2026.", "tags": ["Mobile Apps", "Flutter", "Costs"]},
    {"slug": "affordable-wordpress-website-design-small-business", "date": "2026-10-22", "img": "assets/img/un/wordpress.webp",
     "card": "How to get a professional, fast, and search-friendly WordPress website without overspending.", "tags": ["WordPress", "Small Business", "Web Design"]},
]
BLOG_CAT_SHORT = {"Custom Software": "Custom Software", "Mobile App Development": "Mobile Apps", "Web Development": "Web Development"}


def load_blogs():
    data = json.load(open(__file__.replace("pages.py", "data/blogs.json")))
    out = []
    for d, m in zip(data, BLOG_META):
        words = len(re.sub(r"<[^>]+>", " ", d["html"]).split())
        b = dict(d, **m)
        b["cat"] = BLOG_CAT_SHORT.get(d["category"], d["category"])
        b["mins"] = max(3, round(words / 220))
        b["title"] = d["title"].replace("Owners", "Owners")
        out.append(b)
    return out


def fmt_date(iso):
    import datetime
    return datetime.date.fromisoformat(iso).strftime("%b %d, %Y")


def sec_head(eyebrow, title, text="", light=False, center=True):
    cls = "sec-head" + (" center" if center else "") + (" light" if light else "")
    ey = f'<span class="eyebrow{" light" if light else ""} reveal">{icon("sparkle", "ic ic-xs")} {eyebrow}</span>' if eyebrow else ""
    p = f'<p class="reveal" style="--d:.12s">{text}</p>' if text else ""
    return f'<div class="{cls}">{ey}<h2 class="reveal" style="--d:.06s">{title}</h2>{p}</div>'


def stat_counter(val, suf, label, cls="stat"):
    if val.isdigit():
        num = f'<span class="count" data-count="{val}">0</span>{suf}'
    else:
        num = f"{val}{suf}"
    return f'<div class="{cls}"><strong>{num}</strong><span>{label}</span></div>'


def process_block(R, steps=None, dark=True):
    """Animated 4-step process (home & services overview)."""
    icons_ = ["compass", "pen-tool", "code", "rocket"]
    steps = steps or DEFAULT_PROCESS["steps"]
    nodes = []
    for i, (t, d) in enumerate(steps[:4]):
        ring = ""
        if i == 3:
            ring = ('<svg class="pnode-ring" viewBox="0 0 200 200" aria-hidden="true"><defs><path id="ringPath" d="M100,100 m-84,0 a84,84 0 1,1 168,0 a84,84 0 1,1 -168,0"/></defs>'
                    '<text><textPath href="#ringPath">HOST • SUPPORT • EVOLVE • HOST • SUPPORT • EVOLVE •</textPath></text></svg>')
        hand = ""
        if i in (0, 2):
            hand = f'<div class="p-link" aria-hidden="true"><span>Personal handoff</span><i></i></div>'
        elif i == 1:
            hand = '<div class="p-link p-link-short" aria-hidden="true"><i></i></div>'
        nodes.append(f'<div class="pnode reveal-pop" style="--d:{i * .18}s"><div class="pnode-circle{" is-last" if i == 3 else ""}">{ring}<span class="pnode-num">0{i + 1}</span>{icon(icons_[i])}<b>{t}</b></div><p>{d}</p></div>{hand}')
    return f'<div class="process-panel{" dark" if dark else ""}"><div class="process-track">{"".join(nodes)}</div></div>'


def faq_block(faqs, idp="faq"):
    items = []
    for i, (q, a) in enumerate(faqs):
        items.append(f'<div class="acc-item reveal" style="--d:{min(i, 5) * .05}s"><h3><button class="acc-btn" aria-expanded="false" aria-controls="{idp}-{i}" id="{idp}-b{i}">{q}<span class="acc-ic">{icon("chevron-down", "ic ic-sm")}</span></button></h3>'
                     f'<div class="acc-panel" id="{idp}-{i}" role="region" aria-labelledby="{idp}-b{i}"><div><p>{a}</p></div></div></div>')
    return f'<div class="accordion">{"".join(items)}</div>'


def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faqs]}


def cta_band(R, title="Let’s Build Your Next Big Idea", text="Tell us about your project and get premium software solutions designed for growth and scalability.",
             extra="Start with a free assessment. No obligation, written findings either way. Thirty minutes with one of our engineers."):
    return f"""<section class="section-sm"><div class="container"><div class="cta-band reveal">
  <div class="cta-orb o1"></div><div class="cta-orb o2"></div>
  <h2>{title}</h2><p>{text}</p>{f'<p class="cta-extra">{extra}</p>' if extra else ''}
  <div class="cta-actions"><a class="btn btn-light" href="{R}contact.html">Start Your Project {icon('arrow-right', 'ic ic-sm')}</a>
  <a class="btn btn-ghost-light" href="{R}contact.html#contact-form">{icon('calendar', 'ic ic-sm')} Schedule Consultation</a></div>
</div></div></section>"""


def blog_card(R, b, featured=False, lazy=True):
    cls = "post-card reveal" + (" is-featured" if featured else "")
    return f"""<article class="{cls}" data-cat="{escape(b['cat'])}" data-title="{escape(b['title'].lower())}">
  <a class="post-media" href="{R}blog/{b['slug']}.html" tabindex="-1" aria-hidden="true">{img(R, b['img'], b['title'], 1200, 800)}<span class="post-cat">{b['cat']}</span></a>
  <div class="post-body">
    <div class="post-meta"><span>{icon('calendar', 'ic ic-xs')} {fmt_date(b['date'])}</span><span>{icon('clock', 'ic ic-xs')} {b['mins']} min read</span></div>
    <h3><a href="{R}blog/{b['slug']}.html">{b['title']}</a></h3>
    <p>{b['card']}</p>
    <a class="link-arrow" href="{R}blog/{b['slug']}.html" aria-label="Read article: {escape(b['title'])}">Read Article {icon('arrow-right', 'ic ic-sm')}</a>
  </div>
</article>"""


# ═══════════════════════════════════════════════════════════ HOME
def home(blogs):
    R = ""
    stats = "".join(f'<div class="hero-stat reveal" style="--d:{.35 + i * .08}s">' + stat_counter(v, s, l, "stat-in") + '</div>' for i, (v, s, l) in enumerate(HOME_STATS))
    why = "".join(f'<article class="why-card reveal" style="--d:{(i % 3) * .08}s"><span class="ic-badge">{icon(ic)}</span><h3>{t}</h3><p>{d}</p></article>' for i, (ic, t, d) in enumerate(WHY))
    svcs = "".join(
        f'<article class="svc-card reveal" style="--d:{(i % 4) * .07}s"><span class="ic-badge">{icon(ic)}</span>'
        f'<h3><a href="services/{slug}.html">{t}</a></h3><p>{d}</p>'
        f'<div class="svc-foot"><a class="link-arrow" href="services/{slug}.html" aria-label="Learn more about {t}">Learn More {icon("arrow-right", "ic ic-sm")}</a>{"<span class=pill-new>New</span>" if new else ""}</div></article>'
        for i, (slug, ic, t, d, new) in enumerate(HOME_SERVICES))
    inds = "".join(f'<li>{icon(ic, "ic ic-sm")}{n}</li>' for ic, n in HOME_INDUSTRIES)
    projects = "".join(
        f'<article class="proj-card reveal" data-cat="{cats}" style="--d:{i * .08}s"><div class="proj-media">{img(R, im, name + " — " + cat, 1200, 800)}</div>'
        f'<div class="proj-body"><span class="proj-cat">{cat}</span><h3>{name}</h3><p>{d}</p><ul class="tags">{"".join(f"<li>{t}</li>" for t in tags)}</ul></div></article>'
        for i, (name, cat, d, tags, im, cats) in enumerate(PROJECTS))
    pstats = "".join(stat_counter(v, s, l) for v, s, l in [("100", "+", "Projects Delivered"), ("50", "+", "Happy Clients"), ("10", "+", "Industries Served"), ("98", "%", "Client Satisfaction")])
    t_slides = "".join(
        f'<div class="t-slide{" is-active" if i == 0 else ""}" role="group" aria-roledescription="slide" aria-label="{i + 1} of 3">'
        f'<div class="t-stars" aria-label="5 out of 5 stars">{icon("star", "ic ic-sm") * 5}</div><blockquote>“{q}”</blockquote>'
        f'<div class="t-person"><b>{n}</b><span>{r}</span></div></div>' for i, (ini, n, r, q) in enumerate(TESTIMONIALS))
    t_avatars = "".join(f'<div class="t-avatar{" is-active" if i == 0 else ""}"><span>{ini}</span></div>' for i, (ini, n, r, q) in enumerate(TESTIMONIALS))
    order = [1, 2, 0]
    posts = "".join(blog_card(R, blogs[i]) for i in order)

    body = f"""
<section class="hero">
  <div class="hero-bg">
    <picture><source media="(max-width: 760px)" srcset="assets/img/hero-bg-900.webp">
    <img src="assets/img/hero-bg.webp" alt="" width="1377" height="768" fetchpriority="high" decoding="async"></picture>
  </div>
  <div class="hero-shade" aria-hidden="true"></div>
  <div class="hero-dots" aria-hidden="true"></div>
  <div class="container hero-inner">
    <div class="hero-copy">
      <span class="eyebrow anim-up">{icon('sparkle', 'ic ic-xs')} Welcome to Zenvix Technologies</span>
      <h1 class="anim-up" style="--d:.08s">Engineered for Impact. <span class="grad-text">Built to Scale Your Business.</span></h1>
      <p class="hero-sub anim-up" style="--d:.16s">We build custom software, enterprise solutions, and cross-platform mobile apps that streamline business operations, improve efficiency, and drive scalable business growth.</p>
      <div class="hero-actions anim-up" style="--d:.24s">
        <a class="btn btn-primary" href="contact.html">Get Started {icon('arrow-right', 'ic ic-sm')}</a>
        <a class="btn btn-outline" href="#portfolio">{icon('play', 'ic ic-xs')} View Portfolio</a>
      </div>
      <div class="hero-trust anim-up" style="--d:.32s">
        <div class="avatars" aria-hidden="true"><span>AK</span><span>SA</span><span>UT</span><span>+</span></div>
        <p><span class="stars">{icon('star', 'ic ic-xs') * 5}</span> Trusted by 50+ businesses in Pakistan, the US, UK &amp; Gulf</p>
      </div>
    </div>
  </div>
  <div class="container"><div class="hero-stats">{stats}</div></div>
</section>

<section class="section" id="why">
  <div class="container">
    {sec_head('Why us', 'Why <span class="grad-text">Choose Us</span>', 'We combine technical expertise, innovative thinking, and business-focused strategies to build reliable digital solutions that drive long-term growth. We understand the global market and can execute budget-friendly strategies to reach your target audience.')}
    <div class="grid-3">{why}</div>
  </div>
</section>

<section class="section bg-soft" id="services">
  <div class="container">
    {sec_head('Our services', 'Explore Our <span class="grad-text">Customized Services</span>', 'Zenvix Technologies helps you discover new possibilities and unlock endless opportunities through innovative digital solutions. Explore our services to transform your ideas into reality and take your business to the next level.')}
    <div class="grid-4">{svcs}</div>
    <div class="center mt-40 reveal"><a class="btn btn-outline" href="services.html">View All Services {icon('arrow-right', 'ic ic-sm')}</a></div>
  </div>
</section>

<section class="section-sm" id="industries">
  <div class="container">
    {sec_head('', 'Industries <span class="grad-text">We Serve</span>', 'Technology solutions designed for every business sector.')}
    <div class="marquee reveal" aria-label="Industries we serve">
      <ul class="marquee-track">{inds}</ul>
      <ul class="marquee-track" aria-hidden="true">{inds}</ul>
    </div>
  </div>
</section>

<section class="section" id="process">
  <div class="container">
    {sec_head('Our process', 'A proven path from first conversation to <span class="grad-text">long-term partnership</span>', 'Four phases, two personal handoffs, and one team that stays with you long after launch.')}
    {process_block(R)}
  </div>
</section>

{cta_band(R)}

<section class="section" id="portfolio">
  <div class="container">
    {sec_head('Our Work', 'Projects That <span class="grad-text">Speak for Themselves</span>', '100+ digital products delivered across 10+ industries. Every project is built with care, precision, and a focus on real results.')}
    <div class="filters reveal" role="tablist" aria-label="Filter projects">
      <button class="chip is-active" data-filter="all" role="tab" aria-selected="true">All Projects</button>
      <button class="chip" data-filter="web" role="tab" aria-selected="false">Web</button>
      <button class="chip" data-filter="mobile" role="tab" aria-selected="false">Mobile</button>
      <button class="chip" data-filter="ai" role="tab" aria-selected="false">AI</button>
      <button class="chip" data-filter="design" role="tab" aria-selected="false">Design</button>
    </div>
    <div class="grid-4 proj-grid" data-filter-grid>{projects}</div>
    <div class="stats-band reveal">{pstats}</div>
  </div>
</section>

<section class="section testimonials" id="testimonials">
  <div class="t-lines" aria-hidden="true"></div>
  <div class="container">
    <div class="t-head">
      <div>{sec_head('Testimonials', 'What Clients <span class="grad-text-light">Say</span>', '', light=True, center=False)}</div>
      <p class="reveal">Hear from our esteemed clients who have benefited from our expertise in software development, web development, SEO, and digital marketing strategies. <b>The results speak — but hearing it from our clients means even more.</b></p>
    </div>
    <div class="t-grid">
      <ul class="t-stats reveal">
        <li><strong><span class="count" data-count="250">0</span>%</strong> Follower Growth</li>
        <li><strong><span class="count" data-count="80">0</span>%</strong> Increase Sales</li>
        <li><strong><span class="count" data-count="140">0</span>%</strong> Total Engagement</li>
        <li><strong><span class="count" data-count="75">0</span>%</strong> Income Growth</li>
      </ul>
      <div class="t-photo reveal" aria-hidden="true">{t_avatars}<span class="t-quote-ic">{icon('quote')}</span></div>
      <div class="t-slider reveal" data-slider aria-roledescription="carousel" aria-label="Client testimonials">
        <div class="t-slides" aria-live="polite">{t_slides}</div>
        <div class="t-nav">
          <button class="t-btn" data-prev aria-label="Previous testimonial">{icon('arrow-left', 'ic ic-sm')}</button>
          <button class="t-btn is-primary" data-next aria-label="Next testimonial">{icon('arrow-right', 'ic ic-sm')}</button>
          <span class="t-count"><b data-current>1</b> / 3</span>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="blog">
  <div class="container">
    {sec_head('Our Blog', 'Latest <span class="grad-text">Blog &amp; Articles</span>', 'Practical insights on software, mobile apps, websites and digital growth from the Zenvix team.')}
    <div class="grid-3">{posts}</div>
    <div class="center mt-40 reveal"><a class="btn btn-outline" href="blog.html">View All Articles {icon('arrow-right', 'ic ic-sm')}</a></div>
  </div>
</section>
"""
    page = {"path": "index.html", "root": R, "nav": "home", "body": "page-home",
            "title": "Zenvix Technologies | Software, Web & Mobile App Development Company in Lahore, Pakistan",
            "desc": "Zenvix Technologies builds custom software, websites, mobile apps, AI solutions and digital marketing campaigns that scale your business. Based in Lahore, serving Pakistan, the US, UK & Gulf.",
            "preload": ("assets/img/hero-bg.webp", "assets/img/hero-bg-900.webp"),
            "schema": [org_schema(), {"@context": "https://schema.org", "@type": "WebSite", "name": "Zenvix Technologies", "url": SITE["url"] + "/",
                                      "publisher": {"@id": SITE["url"] + "/#organization"}}]}
    return page, body


# ═══════════════════════════════════════════════════════════ ABOUT
def about():
    R = ""
    body = f"""
<section class="about-hero">
  <div class="container about-hero-grid">
    <div class="about-hero-copy">
      <nav aria-label="Breadcrumb"><ol class="crumbs dark"><li><a href="index.html">Home</a></li><li aria-current="page">About Us</li></ol></nav>
      <h1 class="eyebrow anim-up">{icon('sparkle', 'ic ic-xs')} About Zenvix Technologies</h1>
      <h2 class="display anim-up" style="--d:.08s">Ideas, technology, and <em>real growth.</em></h2>
      <p class="anim-up" style="--d:.16s">We help businesses turn digital opportunities into useful, high-performing experiences—from the first strategy session to the technology that powers what comes next.</p>
      <a class="btn btn-primary anim-up" style="--d:.24s" href="contact.html">Let’s grow together {icon('arrow-right', 'ic ic-sm')}</a>
    </div>
    <div class="about-hero-media anim-fade" style="--d:.2s">
      <div class="media-glow"></div>
      {img(R, 'assets/img/un/team-meeting.webp', 'The Zenvix Technologies team collaborating in the Lahore office', 1200, 800, eager=True)}
      <div class="float-card growth-card"><strong><span class="count" data-count="120">0</span><em>%</em></strong><small>engagement potential<br>through smarter digital work</small></div>
      <div class="float-card tag-card">{icon('sparkle', 'ic ic-xs')} Strategy meets execution</div>
    </div>
  </div>
</section>

<section class="section-sm">
  <div class="container story">
    <div class="story-num reveal"><strong><span class="count" data-count="100">0</span>+</strong><span>projects delivered worldwide</span></div>
    <div class="reveal" style="--d:.06s"><span class="eyebrow">{icon('sparkle', 'ic ic-xs')} Our story</span><h2>Your Vision, Our Technology, <em>Shared Success.</em></h2></div>
    <div class="story-text reveal" style="--d:.12s">
      <p>At Zenvix Technologies, we believe the right digital partner should make growth feel less complicated. We bring together inventive marketing, practical technology, and a clear understanding of what businesses need to move forward.</p>
      <p>Our team works alongside you to develop focused strategies and robust digital solutions that deliver measurable results—whether you need better visibility, stronger engagement, or a product built to scale.</p>
    </div>
  </div>
</section>

<section class="section bg-soft">
  <div class="container focus-grid">
    <div class="focus-media reveal">
      {img(R, 'assets/img/about-workshop.webp', 'Zenvix strategists planning a client project on a whiteboard', 1000, 667)}
      <div class="float-label">Built around your goals</div>
    </div>
    <div class="focus-copy">
      <span class="eyebrow reveal">{icon('sparkle', 'ic ic-xs')} What drives us</span>
      <h2 class="reveal" style="--d:.06s">More than a service provider. <em>Your growth partner.</em></h2>
      <p class="reveal" style="--d:.12s">From optimization and search visibility to software, web, and app development, every Zenvix solution is designed around your business needs—not a one-size-fits-all package.</p>
      <div class="mini-list">
        <div class="reveal" style="--d:.16s"><span class="ic-badge sm">{icon('trending-up', 'ic ic-sm')}</span><p><b>Optimisation &amp; reach</b>Improve visibility, attract the right audience, and turn attention into opportunity.</p></div>
        <div class="reveal" style="--d:.22s"><span class="ic-badge sm">{icon('code', 'ic ic-sm')}</span><p><b>Software &amp; web development</b>Build powerful digital solutions that bring innovation and functionality together.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    {sec_head('Our foundation', 'Guided by what <span class="grad-text">creates lasting value.</span>', '', center=False)}
    <div class="principles">
      <article class="reveal"><span class="ic-badge">{icon('target')}</span><small>01 — Vision</small><h3>See what’s possible</h3><p>To become a global leader in digital marketing and technology by consistently exceeding expectations with innovative, results-led work.</p></article>
      <article class="reveal" style="--d:.08s"><span class="ic-badge">{icon('trending-up')}</span><small>02 — Mission</small><h3>Empower progress</h3><p>To give businesses of every size access to smart digital solutions that build confidence, momentum, and sustainable growth.</p></article>
      <article class="reveal" style="--d:.16s"><span class="ic-badge">{icon('headphones')}</span><small>03 — Support</small><h3>Stay by your side</h3><p>Our dedicated team is here through every step, with practical guidance and reliable support when it matters most.</p></article>
      <article class="reveal" style="--d:.24s"><span class="ic-badge">{icon('award')}</span><small>04 — Excellence</small><h3>Raise the standard</h3><p>We take pride in quality work, continuous improvement, and solutions that set our clients apart.</p></article>
    </div>
  </div>
</section>

<section class="section dark-sec">
  <div class="container why-layout">
    <div class="why-copy">
      <span class="eyebrow light reveal">{icon('sparkle', 'ic ic-xs')} Why businesses choose Zenvix</span>
      <h2 class="reveal" style="--d:.06s">Clear thinking. <em>Meaningful results.</em></h2>
      <p class="reveal" style="--d:.12s">We pair deep technical experience with a client-first approach, creating work that is as purposeful as it is polished — for clients in Pakistan, the US, UK and the Gulf.</p>
      <a class="btn btn-primary reveal" style="--d:.18s" href="contact.html">Start a conversation {icon('arrow-right', 'ic ic-sm')}</a>
      <div class="why-img reveal" style="--d:.2s">{img(R, 'assets/img/about-office.webp', 'Zenvix developers discussing a project in an open-plan office', 1100, 825)}</div>
    </div>
    <div class="reasons">
      <article class="reveal"><b>01</b><h3>Proven expertise</h3><p>Deep understanding of technology and the digital landscape, across 10+ industries.</p></article>
      <article class="reveal" style="--d:.08s"><b>02</b><h3>Client-centred approach</h3><p>We listen closely and build relationships that last beyond launch.</p></article>
      <article class="reveal" style="--d:.16s"><b>03</b><h3>Results-led strategy</h3><p>Better traffic, stronger engagement, and more opportunities for your business.</p></article>
      <article class="reveal" style="--d:.24s"><b>04</b><h3>Innovative solutions</h3><p>Modern tools and practical execution to keep you ahead of the competition.</p></article>
      <article class="reveal" style="--d:.32s"><b>05</b><h3>Transparent process</h3><p>Regular updates, open communication and milestone-based delivery — no surprises.</p></article>
      <article class="reveal" style="--d:.4s"><b>06</b><h3>Local roots, global reach</h3><p>Based in Gulberg, Lahore and trusted by businesses across the world.</p></article>
    </div>
  </div>
</section>

<section class="section-sm">
  <div class="container"><div class="stats-band reveal">{''.join(stat_counter(v, s, l) for v, s, l in [("100", "+", "Projects Delivered"), ("50", "+", "Happy Clients"), ("10", "+", "Industries Served"), ("98", "%", "Client Satisfaction")])}</div></div>
</section>

<section class="section-sm">
  <div class="container"><div class="about-cta reveal">
    <div><span class="eyebrow">{icon('sparkle', 'ic ic-xs')} Let’s grow together</span><h2>Ready to take your business <em>to the next level?</em></h2>
    <p>Whether you have a clear brief or simply a big idea, we’re ready to help you find the right digital path forward.</p></div>
    <div class="about-cta-actions"><a class="btn btn-primary" href="contact.html">Get in touch {icon('arrow-right', 'ic ic-sm')}</a><a class="link-arrow" href="services.html">Explore our services {icon('arrow-up-right', 'ic ic-sm')}</a></div>
  </div></div>
</section>
"""
    page = {"path": "about.html", "root": R, "nav": "about", "body": "page-about",
            "title": "About Us | Zenvix Technologies — Software & Digital Growth Partner in Lahore",
            "desc": "Meet Zenvix Technologies: a Lahore-based software, web, mobile app and digital marketing company helping businesses in Pakistan and worldwide turn ideas into real growth.",
            "schema": [org_schema(), breadcrumb_schema([("Home", ""), ("About Us", "about.html")])]}
    return page, body


# ═══════════════════════════════════════════════════════════ CONTACT
CONTACT_FAQS = [("How long does a typical project take?", "It depends on scope. A simple website can be done in 2–3 weeks. A full mobile app typically takes 8–14 weeks. Enterprise systems can take 4–6 months. We'll give you a detailed timeline after our discovery call."),
                ("What's your development process like?", "We follow agile sprints with bi-weekly demos. You're involved at every stage — from discovery and design review to QA sign-off. No black boxes here."),
                ("Do you offer post-launch support?", "Yes. Every project includes at least 1 month of post-launch support. We also offer ongoing maintenance retainers for clients who need long-term technical partnership."),
                ("Can I see examples of similar work?", "Absolutely. Browse our recent projects on the home page, or we can share examples relevant to your industry during a consultation call."),
                ("What payment methods do you accept?", "We accept bank transfer, PayPal, Wise, and major credit cards. We work on a milestone-based payment schedule — you pay as we deliver."),
                ("Do you sign NDAs?", "Yes, we're happy to sign an NDA before any detailed discussions. Client confidentiality is something we take seriously on every project.")]


def contact():
    R = ""
    opts = "".join(f'<option>{n}</option>' for _, n, _, _ in SERVICES_NAV)
    info = [("mail", "Email Us", f'<a href="mailto:{SITE["email"]}">{SITE["email"]}</a>', "We reply within one business day"),
            ("phone", "Call Us", f'<a href="tel:{SITE["phone_href"]}">{SITE["phone"]}</a>', SITE["hours"]),
            ("map-pin", "Visit Us", f'<a href="{SITE["map"]}" target="_blank" rel="noopener">Gulberg, Lahore,<br>Punjab, Pakistan</a>', "Open in Google Maps"),
            ("whatsapp", "WhatsApp", f'<a href="{SITE["whatsapp"]}" target="_blank" rel="noopener">{SITE["phone"]}</a>', "Usually responds within an hour")]
    cards = "".join(f'<div class="info-card reveal" style="--d:{i * .06}s"><span class="ic-badge">{icon(ic)}</span><div><h3>{t}</h3>{v}<small>{s}</small></div></div>' for i, (ic, t, v, s) in enumerate(info))
    body = page_hero(R, "Get in Touch", 'Let’s Talk About <span class="grad-text-light">Your Project</span>',
                     "Whether you have a clear brief or just the seed of an idea, we're here. Tell us what you're building and we'll get back to you within 24 hours.",
                     [("Home", "index.html"), ("Contact", None)]) + f"""
<section class="section contact-sec">
  <div class="container contact-grid">
    <div class="contact-info">
      {sec_head('Contact details', 'We’d Love to <span class="grad-text">Hear From You</span>', 'Fill out the form and our team will be in touch within one business day. Prefer a call? Schedule one directly — we work with clients in Pakistan, the US, UK and the Gulf.', center=False)}
      <div class="info-cards">{cards}</div>
      <div class="social-row reveal"><span>Follow us</span>{''.join(f'<a href="{u}" aria-label="{n}" rel="noopener">{icon(ic, "ic ic-sm")}</a>' for n, ic, u in SITE['social'])}</div>
    </div>
    <div class="form-card reveal" id="contact-form">
      <div class="form-view">
        <h2>Send Us a Message</h2>
        <p class="muted">All fields marked with <span class="req">*</span> are required.</p>
        <form class="contact-form" novalidate data-contact-form>
          <div class="hp" aria-hidden="true"><label for="website">Website</label><input id="website" name="website" tabindex="-1" autocomplete="off"></div>
          <div class="f-row">
            <div class="field"><label for="fname">First Name <span class="req">*</span></label><input id="fname" name="first_name" autocomplete="given-name" required><small class="err">Please enter your first name.</small></div>
            <div class="field"><label for="lname">Last Name <span class="req">*</span></label><input id="lname" name="last_name" autocomplete="family-name" required><small class="err">Please enter your last name.</small></div>
          </div>
          <div class="f-row">
            <div class="field"><label for="email">Email Address <span class="req">*</span></label><input id="email" name="email" type="email" autocomplete="email" required><small class="err">Please enter a valid email address.</small></div>
            <div class="field"><label for="phone">Phone Number</label><input id="phone" name="phone" type="tel" autocomplete="tel" pattern="[0-9+()\\-\\s]{{7,20}}"><small class="err">Please enter a valid phone number.</small></div>
          </div>
          <div class="field"><label for="company">Company / Organization</label><input id="company" name="company" autocomplete="organization"></div>
          <div class="field"><label for="service">Service Needed <span class="req">*</span></label><select id="service" name="service" required><option value="">Select a service...</option>{opts}<option>Other</option></select><small class="err">Please select a service.</small></div>
          <div class="field-reveal" data-other-wrap><div><div class="field"><label for="service_other">Which service do you need? <span class="req">*</span></label><input id="service_other" name="service_other" placeholder="e.g. Shopify store, Chrome extension, IT consultancy..." data-other-input><small class="err">Please tell us which service you need.</small></div></div></div>
          <div class="f-row">
            <div class="field"><label for="budget">Project Budget</label><select id="budget" name="budget"><option value="">Select a budget range...</option><option>Under $1,000</option><option>$1,000 – $5,000</option><option>$5,000 – $15,000</option><option>$15,000 – $50,000</option><option>$50,000+</option></select></div>
            <div class="field"><label for="timeline">Timeline</label><select id="timeline" name="timeline"><option value="">Select a timeline...</option><option>ASAP (within 1 month)</option><option>1–3 months</option><option>3–6 months</option><option>6+ months</option><option>Not sure yet</option></select></div>
          </div>
          <div class="field"><label for="details">Project Details <span class="req">*</span></label><textarea id="details" name="details" rows="5" maxlength="1000" minlength="20" required></textarea>
            <div class="field-foot"><small class="err">Please describe your project (minimum 20 characters).</small><small class="counter"><span data-counter>0</span> / 1000 characters</small></div></div>
          <div class="field check"><input type="checkbox" id="consent" required><label for="consent">I agree to be contacted by Zenvix Technologies about this inquiry.</label><small class="err">You must agree to continue.</small></div>
          <button class="btn btn-primary btn-block" type="submit">{icon('send', 'ic ic-sm')} Send Message</button>
        </form>
      </div>
      <div class="form-success" hidden>
        <span class="success-ic">{icon('check')}</span>
        <h2>Almost there!</h2>
        <p>Your email app has opened with your message ready to send to <b>{SITE['email']}</b>. Hit send and our team will get back to you within <strong>24 hours</strong>.</p>
        <p class="muted">Email app didn't open? Write to us directly at <a href="mailto:{SITE['email']}">{SITE['email']}</a> or <a href="{SITE['whatsapp']}" target="_blank" rel="noopener">message us on WhatsApp</a>.</p>
        <div class="success-actions"><a class="btn btn-outline btn-sm" href="index.html#portfolio">View Portfolio</a><a class="btn btn-primary btn-sm" href="blog.html">Read Blog</a></div>
      </div>
    </div>
  </div>
</section>

<section class="section-sm">
  <div class="container"><div class="map-wrap reveal">
    <iframe src="{SITE['map_embed']}" title="Zenvix Technologies location — Gulberg, Lahore" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
    <div class="map-card"><span class="ic-badge">{icon('map-pin')}</span><div><b>Zenvix Technologies</b><span>Gulberg, Lahore, Punjab, Pakistan</span><a class="link-arrow" href="{SITE['map']}" target="_blank" rel="noopener">Get directions {icon('arrow-up-right', 'ic ic-sm')}</a></div></div>
  </div></div>
</section>

<section class="section" id="faq">
  <div class="container narrow">
    {sec_head('FAQ', 'Common <span class="grad-text">Questions</span>', 'Quick answers to what most clients ask before reaching out.')}
    {faq_block(CONTACT_FAQS)}
  </div>
</section>
"""
    page = {"path": "contact.html", "root": R, "nav": "contact", "body": "page-contact",
            "title": "Contact Zenvix Technologies | Get a Free Quote — Lahore, Pakistan",
            "desc": "Contact Zenvix Technologies in Gulberg, Lahore. Call +92 326 4549778, email zenvixtechnologies7@gmail.com or send your project details for a free quote within 24 hours.",
            "schema": [org_schema(), breadcrumb_schema([("Home", ""), ("Contact", "contact.html")]), faq_schema(CONTACT_FAQS)]}
    return page, body


# ═══════════════════════════════════════════════════════════ SERVICES OVERVIEW
def services_overview():
    R = ""
    cards = []
    for i, s in enumerate(SERVICES):
        pts = s["hero"]["checks"][:3]
        cards.append(f"""<article class="svc-big reveal" style="--d:{(i % 2) * .08}s">
  <div class="svc-big-top"><span class="ic-badge lg">{icon(s['icon'])}</span>{'<span class="pill-new">New</span>' if s.get('new') else ''}</div>
  <h2><a href="services/{s['slug']}.html">{s['name']}</a></h2>
  <p>{s['summary']}</p>
  <ul class="mini-checks">{''.join(f'<li>{icon("check", "ic ic-xs")}{p}</li>' for p in pts)}</ul>
  <a class="link-arrow" href="services/{s['slug']}.html" aria-label="Explore {s['name']}">Explore service {icon('arrow-right', 'ic ic-sm')}</a>
</article>""")
    why = "".join(f'<article class="why-card reveal" style="--d:{(i % 3) * .08}s"><span class="ic-badge">{icon(ic)}</span><h3>{t}</h3><p>{d}</p></article>' for i, (ic, t, d) in enumerate(WHY))
    body = page_hero(R, "What we do", 'Digital Services Built to <span class="grad-text-light">Scale Your Business</span>',
                     "Software, web and mobile development, UI/UX, AI and growth marketing — everything you need to build, launch and grow, delivered by one expert team in Lahore.",
                     [("Home", "index.html"), ("Services", None)], bg="assets/img/un/team-students.webp",
                     actions=f'<a class="btn btn-light" href="contact.html">Get a Free Quote {icon("arrow-right", "ic ic-sm")}</a><a class="btn btn-ghost-light" href="#all-services">Browse services</a>') + f"""
<section class="section" id="all-services">
  <div class="container">
    {sec_head('Our services', 'Explore Our <span class="grad-text">Customized Services</span>', 'Zenvix Technologies helps you discover new possibilities and unlock endless opportunities through innovative digital solutions.')}
    <div class="grid-2 svc-big-grid">{''.join(cards)}</div>
  </div>
</section>
<section class="section bg-soft">
  <div class="container">
    {sec_head('Our process', 'A proven path from first conversation to <span class="grad-text">long-term partnership</span>', DEFAULT_PROCESS['text'])}
    {process_block(R)}
  </div>
</section>
<section class="section">
  <div class="container">
    {sec_head('Why us', 'Why <span class="grad-text">Choose Zenvix</span>', 'Technical expertise, innovative thinking and business-focused strategy — with budget-friendly execution for local and global clients.')}
    <div class="grid-3">{why}</div>
  </div>
</section>
{cta_band(R)}
"""
    page = {"path": "services.html", "root": R, "nav": "services", "body": "page-services",
            "title": "Our Services | Software, Web, Mobile, SEO & Marketing | Zenvix Technologies",
            "desc": "Explore Zenvix Technologies services: web development, custom software, mobile apps, UI/UX design, AI solutions, SEO, social media and email marketing for businesses worldwide.",
            "schema": [org_schema(), breadcrumb_schema([("Home", ""), ("Services", "services.html")]),
                       {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
                           {"@type": "ListItem", "position": i + 1, "url": f"{SITE['url']}/services/{s['slug']}.html", "name": s["name"]} for i, s in enumerate(SERVICES)]}]}
    return page, body


# ═══════════════════════════════════════════════════════════ SERVICE DETAIL
def render_section(R, s, idx, svc):
    t = s["type"]
    bg = " bg-soft" if idx % 2 == 1 and not s.get("dark") else ""
    fix = lambda x: x.replace("{R}", R)

    if t == "split":
        rev = " reverse" if s.get("reverse") else ""
        bl = ""
        if s.get("bullets"):
            bt = f'<h3 class="bl-title">{s["bullets_title"]}</h3>' if s.get("bullets_title") else ""
            bl = bt + '<ul class="check-list">' + "".join(f'<li>{b}</li>' for b in s["bullets"]) + "</ul>"
        paras = "".join(f'<p>{fix(p)}</p>' for p in s["paras"])
        return f"""<section class="section{bg}"><div class="container split{rev}">
  <div class="split-media reveal"><div class="split-frame">{img(R, s['img'], s['alt'], s['w'], s['h'])}</div><div class="split-deco" aria-hidden="true"></div></div>
  <div class="split-copy">
    <span class="eyebrow reveal">{icon('sparkle', 'ic ic-xs')} {s['eyebrow']}</span>
    <h2 class="reveal" style="--d:.06s">{s['title']}</h2>
    <div class="reveal prose-sm" style="--d:.12s">{paras}{bl}</div>
    <a class="btn btn-primary reveal" style="--d:.18s" href="{R}contact.html">Get a Free Quote {icon('arrow-right', 'ic ic-sm')}</a>
  </div>
</div></section>"""

    if t == "cards":
        dark = s.get("dark")
        cols = s.get("cols", 3)
        style = s.get("style", "")
        items = []
        for i, it in enumerate(s["items"]):
            ic, ti, tx = it[0], it[1], it[2]
            extra = ""
            if len(it) > 3 and it[3]:
                extra = '<ul class="mini-checks">' + "".join(f'<li>{icon("check", "ic ic-xs")}{x}</li>' for x in it[3]) + "</ul>"
            items.append(f'<article class="card {style} reveal" style="--d:{(i % cols) * .07}s"><span class="ic-badge">{icon(ic)}</span><h3>{ti}</h3><p>{tx}</p>{extra}</article>')
        cls = "section dark-sec" if dark else f"section{bg}"
        return f"""<section class="{cls}"><div class="container">
  {sec_head(s.get('eyebrow', ''), s['title'], s.get('text', ''), light=bool(dark))}
  <div class="grid-{cols} cards-{style or 'plain'}">{''.join(items)}</div>
</div></section>"""

    if t == "numbered":
        items = "".join(f'<article class="num-card reveal" style="--d:{(i % 4) * .06}s"><span class="num">{i + 1:02d}</span><h3>{a}</h3><p>{b}</p></article>' for i, (a, b) in enumerate(s["items"]))
        return f"""<section class="section{bg}"><div class="container">
  {sec_head(s.get('eyebrow', ''), s['title'], s.get('text', ''))}
  <div class="num-grid">{items}</div>
</div></section>"""

    if t == "checks":
        items = "".join(f'<div class="check-card reveal" style="--d:{(i % 3) * .06}s"><span class="check-dot">{icon("check", "ic ic-sm")}</span><div><h3>{a}</h3><p>{b}</p></div></div>' for i, (a, b) in enumerate(s["items"]))
        return f"""<section class="section{bg}"><div class="container">
  {sec_head(s.get('eyebrow', ''), s['title'], s.get('text', ''))}
  <div class="check-grid">{items}</div>
</div></section>"""

    if t == "tabs":
        uid = f"tabs{idx}"
        btns, panels = [], []
        for i, (lab, items) in enumerate(s["tabs"]):
            sel = "true" if i == 0 else "false"
            btns.append(f'<button class="tab{" is-active" if i == 0 else ""}" role="tab" id="{uid}-t{i}" aria-controls="{uid}-p{i}" aria-selected="{sel}" tabindex="{0 if i == 0 else -1}">{lab}</button>')
            cards = "".join(f'<div class="tech-card"><span class="tech-ic">{escape(n[:2]).upper()}</span><div><h3>{n}</h3><p>{d}</p></div></div>' for n, d in items)
            panels.append(f'<div class="tab-panel{" is-active" if i == 0 else ""}" role="tabpanel" id="{uid}-p{i}" aria-labelledby="{uid}-t{i}"{"" if i == 0 else " hidden"}><div class="tech-grid">{cards}</div></div>')
        return f"""<section class="section{bg}"><div class="container">
  {sec_head(s.get('eyebrow', ''), s['title'], s.get('text', ''))}
  <div class="tabs reveal" data-tabs><div class="tab-list" role="tablist" aria-label="{escape(s['title'])}">{''.join(btns)}</div>{''.join(panels)}</div>
</div></section>"""

    if t == "process":
        p = s if s.get("steps") else DEFAULT_PROCESS
        steps = "".join(f'<li class="tl-step reveal" style="--d:{i * .06}s"><span class="tl-num">{i + 1:02d}</span><div><h3>{a}</h3><p>{b}</p></div></li>' for i, (a, b) in enumerate(p["steps"]))
        return f"""<section class="section{bg}"><div class="container">
  {sec_head(p.get('eyebrow', 'Our process'), p['title'], p.get('text', ''))}
  <ol class="timeline">{steps}</ol>
</div></section>"""

    if t == "pricing":
        uid = f"price{idx}"
        btns, panels = [], []
        for i, (g, plans) in enumerate(s["groups"]):
            btns.append(f'<button class="tab{" is-active" if i == 0 else ""}" role="tab" id="{uid}-t{i}" aria-controls="{uid}-p{i}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{g}</button>')
            cards = "".join(
                f'<div class="price-card{" is-featured" if j == 1 else ""}">{"<span class=price-badge>Most popular</span>" if j == 1 else ""}<h3>{n}</h3><span class="price-scope">{sc}</span>'
                f'<strong class="price">{pr}</strong><ul class="mini-checks">{"".join(f"<li>{CHK}{f}</li>" for f in fe)}</ul>'
                f'<a class="btn {"btn-primary" if j == 1 else "btn-outline"} btn-block" href="{R}contact.html">Get Started</a></div>' for j, (n, sc, pr, fe) in enumerate(plans))
            panels.append(f'<div class="tab-panel{" is-active" if i == 0 else ""}" role="tabpanel" id="{uid}-p{i}" aria-labelledby="{uid}-t{i}"{"" if i == 0 else " hidden"}><div class="price-grid">{cards}</div></div>')
        return f"""<section class="section{bg}"><div class="container">
  {sec_head(s.get('eyebrow', ''), s['title'], s.get('text', ''))}
  <div class="tabs center-tabs reveal" data-tabs><div class="tab-list" role="tablist" aria-label="Pricing categories">{''.join(btns)}</div>{''.join(panels)}</div>
  <p class="price-note reveal">{icon('globe', 'ic ic-sm')} {s.get('note', '')}</p>
</div></section>"""

    if t == "plans":
        cards = "".join(
            f'<div class="price-card reveal{" is-featured" if feat else ""}" style="--d:{i * .08}s">{"<span class=price-badge>Most popular</span>" if feat else ""}<h3>{n} Plan</h3>'
            f'<strong class="price">{pr}<small>/month</small></strong><ul class="mini-checks">{"".join(f"<li>{CHK}{f}</li>" for f in fe)}</ul>'
            f'<a class="btn {"btn-primary" if feat else "btn-outline"} btn-block" href="{R}contact.html">Get Started</a></div>' for i, (n, pr, fe, feat) in enumerate(s["plans"]))
        return f"""<section class="section{bg}"><div class="container">
  {sec_head(s.get('eyebrow', ''), s['title'], s.get('text', ''))}
  <div class="price-grid">{cards}</div>
  <p class="price-note reveal">{icon('globe', 'ic ic-sm')} {s.get('note', '')}</p>
</div></section>"""

    if t == "compare":
        us = "".join(f'<li>{icon("check", "ic ic-sm")}{x}</li>' for x in s["us"])
        them = "".join(f'<li>{icon("x", "ic ic-sm")}{x}</li>' for x in s["them"])
        return f"""<section class="section{bg}"><div class="container">
  {sec_head(s.get('eyebrow', ''), s['title'], s.get('text', ''))}
  <div class="compare">
    <div class="compare-col us reveal"><h3><img src="{R}assets/img/logo-light.webp" alt="Zenvix Technologies" width="140" height="45" loading="lazy"></h3><ul>{us}</ul></div>
    <div class="compare-vs" aria-hidden="true">VS</div>
    <div class="compare-col them reveal" style="--d:.1s"><h3>Other SEO Providers</h3><ul>{them}</ul></div>
  </div>
</div></section>"""

    if t == "metrics":
        items = "".join(f'<div class="metric reveal" style="--d:{i * .08}s"><strong>{v}</strong><span>{l}</span></div>' for i, (v, l) in enumerate(s["items"]))
        return f"""<section class="section{bg}"><div class="container">
  {sec_head(s.get('eyebrow', ''), s['title'], s.get('text', ''))}
  <div class="metrics">{items}</div>
</div></section>"""

    if t == "solution":
        items = "".join(f'<li class="reveal" style="--d:{i * .05}s">{icon("check-circle", "ic")}<span>{x}</span></li>' for i, x in enumerate(s["items"]))
        return f"""<section class="section{bg}"><div class="container split reverse">
  <div class="split-media reveal"><div class="split-frame">{img(R, s['img'], s['alt'], s['w'], s['h'])}</div><div class="split-deco" aria-hidden="true"></div></div>
  <div class="split-copy">
    <span class="eyebrow reveal">{icon('sparkle', 'ic ic-xs')} {s['eyebrow']}</span>
    <h2 class="reveal" style="--d:.06s">{s['title']}</h2>
    <p class="reveal lead-p" style="--d:.1s">{s['text']}</p>
    <ul class="solution-list">{items}</ul>
  </div>
</div></section>"""

    if t == "chips":
        items = "".join(f'<li class="reveal" style="--d:{(i % 5) * .04}s">{icon(ic, "ic ic-sm")}{n}</li>' for i, (ic, n) in enumerate(s["items"]))
        return f"""<section class="section{bg}"><div class="container">
  {sec_head(s.get('eyebrow', ''), s['title'], s.get('text', ''))}
  <ul class="chip-cloud">{items}</ul>
</div></section>"""

    if t == "industries":
        items = "".join(f'<li class="reveal" style="--d:{(i % 6) * .04}s"><span class="ic-badge sm">{icon(ic, "ic ic-sm")}</span>{n}</li>' for i, (ic, n) in enumerate(INDUSTRIES))
        return f"""<section class="section{bg}"><div class="container">
  {sec_head('Industries we serve', s.get('title', 'Built for Every Major Industry'), 'Domain knowledge matters. We bring context and best practices from projects across these sectors.')}
  <ul class="industry-grid">{items}</ul>
</div></section>"""

    raise ValueError(t)


def service_page(svc, blogs):
    R = "../"
    h = svc["hero"]
    checks = "".join(f'<li>{icon("check-circle", "ic ic-sm")}{c}</li>' for c in h["checks"])
    hero = page_hero(R, h["eyebrow"], h["h1"], h["text"], [("Home", "index.html"), ("Services", "services.html"), (svc["name"], None)], bg=h["bg"],
                     actions=f'<a class="btn btn-light" href="{R}contact.html">Get a Free Quote {icon("arrow-right", "ic ic-sm")}</a>'
                             f'<a class="btn btn-ghost-light" href="tel:{SITE["phone_href"]}">{icon("phone", "ic ic-sm")} {SITE["phone"]}</a>')
    hero = hero.replace("</section>", f'<div class="container"><ul class="ph-checks anim-up" style="--d:.32s">{checks}</ul></div></section>', 1)
    secs = "".join(render_section(R, s, i, svc) for i, s in enumerate(svc["sections"]))
    others = [s for s in SERVICES if s["slug"] != svc["slug"]][:4]
    related = "".join(f'<a class="rel-svc reveal" style="--d:{i * .06}s" href="{R}services/{o["slug"]}.html"><span class="ic-badge sm">{icon(o["icon"], "ic ic-sm")}</span><span><b>{o["name"]}</b><small>{o["summary"][:70].rsplit(" ", 1)[0]}…</small></span>{icon("arrow-up-right", "ic ic-sm")}</a>' for i, o in enumerate(others))
    body = hero + secs + f"""
<section class="section bg-soft" id="faq">
  <div class="container narrow">
    {sec_head('FAQs', f'Frequently Asked Questions About <span class="grad-text">{svc["name"]}</span>', '')}
    {faq_block(svc['faqs'])}
  </div>
</section>
<section class="section-sm">
  <div class="container">
    <div class="rel-head reveal"><h2>Explore more services</h2><a class="link-arrow" href="{R}services.html">All services {icon('arrow-right', 'ic ic-sm')}</a></div>
    <div class="rel-grid">{related}</div>
  </div>
</section>
{cta_band(R, title=f"Ready to Start Your {svc['name']} Project?", text="Tell us about your goals and get a detailed proposal — timeline, recommended approach and transparent pricing — within 48 hours.")}
"""
    path = f"services/{svc['slug']}.html"
    schema = [org_schema(), breadcrumb_schema([("Home", ""), ("Services", "services.html"), (svc["name"], path)]),
              {"@context": "https://schema.org", "@type": "Service", "serviceType": svc["name"], "name": svc["name"],
               "description": svc["desc"], "url": f"{SITE['url']}/{path}", "provider": {"@id": SITE["url"] + "/#organization"},
               "areaServed": ["Pakistan", "United States", "United Kingdom", "United Arab Emirates", "Saudi Arabia", "Worldwide"]},
              faq_schema(svc["faqs"])]
    page = {"path": path, "root": R, "nav": "services", "body": "page-service", "title": svc["title"], "desc": svc["desc"], "schema": schema,
            "og": h["bg"]}
    return page, body


# ═══════════════════════════════════════════════════════════ BLOG LIST
def blog_list(blogs):
    R = ""
    ordered = sorted(blogs, key=lambda b: b["date"], reverse=True)
    cats = sorted({b["cat"] for b in blogs})
    chips = '<button class="chip is-active" data-filter="all" aria-pressed="true">All Articles</button>' + "".join(f'<button class="chip" data-filter="{escape(c)}" aria-pressed="false">{c}</button>' for c in cats)
    cards = "".join(blog_card(R, b, featured=(i == 0)) for i, b in enumerate(ordered))
    topics = "".join(f'<a class="topic" href="services/{s}.html">{icon(ic, "ic ic-sm")}{n}</a>' for s, n, ic, _ in SERVICES_NAV[:6])
    body = page_hero(R, "Blog & Insights", 'Insights to Build, Launch &amp; <span class="grad-text-light">Grow Smarter</span>',
                     "Practical guides on custom software, mobile app costs, websites and digital marketing — written by the engineers and strategists at Zenvix Technologies.",
                     [("Home", "index.html"), ("Blog", None)], bg="assets/img/un/flatlay.webp") + f"""
<section class="section">
  <div class="container">
    <div class="blog-toolbar reveal">
      <div class="filters left" role="group" aria-label="Filter by category">{chips}</div>
      <label class="search"><span class="sr-only">Search articles</span>{icon('search', 'ic ic-sm')}<input type="search" placeholder="Search articles..." data-blog-search></label>
    </div>
    <div class="blog-grid" data-blog-grid>{cards}</div>
    <p class="empty-state" hidden data-empty>{icon('search', 'ic')} No articles match your search. Try another keyword.</p>
  </div>
</section>
<section class="section-sm">
  <div class="container">
    <div class="newsletter-band reveal">
      <div><span class="ic-badge lg">{icon('mail')}</span></div>
      <div><h2>Get new articles in your inbox</h2><p>One useful email a month on software, apps, SEO and growth. No spam — unsubscribe anytime.</p></div>
      <form class="newsletter big" data-newsletter novalidate><label for="nl-blog" class="sr-only">Email address</label><input id="nl-blog" type="email" placeholder="you@company.com" required><button class="btn btn-primary" type="submit">Subscribe</button><small class="newsletter-msg" role="status" aria-live="polite"></small></form>
    </div>
    <div class="topics reveal"><span>Explore services:</span>{topics}</div>
  </div>
</section>
"""
    page = {"path": "blog.html", "root": R, "nav": "blog", "body": "page-blog",
            "title": "Blog | Software, App Development & Digital Marketing Insights | Zenvix Technologies",
            "desc": "Read the Zenvix Technologies blog: guides on custom software development costs, mobile app pricing in 2026, affordable WordPress websites and digital growth.",
            "schema": [org_schema(), breadcrumb_schema([("Home", ""), ("Blog", "blog.html")]),
                       {"@context": "https://schema.org", "@type": "Blog", "name": "Zenvix Technologies Blog", "url": SITE["url"] + "/blog.html",
                        "blogPost": [{"@type": "BlogPosting", "headline": b["title"], "url": f"{SITE['url']}/blog/{b['slug']}.html", "datePublished": b["date"]} for b in ordered]}]}
    return page, body


# ═══════════════════════════════════════════════════════════ BLOG POST
def localize_links(html_, R):
    html_ = re.sub(r'<a href="https://zenvixtechnologies\.com/contact/">[^<]*</a>', f'<a href="{R}contact.html">our contact page</a>', html_)
    html_ = re.sub(r'<a href="https://zenvixtechnologies\.com/services/">[^<]*</a>', f'<a href="{R}services.html">our services page</a>', html_)
    html_ = re.sub(r'<a href="https://zenvixtechnologies\.com/">[^<]*</a>', f'<a href="{R}index.html">zenvixtechnologies.com</a>', html_)
    # contextual internal links for SEO
    repl = [("custom software development services", "services/software-development.html"), ("iOS app development", "services/mobile-app-development.html"),
            ("Android app development", "services/mobile-app-development.html"), ("UI/UX design", "services/ui-ux-design.html"),
            ("AI solutions", "services/ai-solutions.html"), ("SEO", "services/seo-services.html")]
    for phrase, href in repl:
        html_ = re.sub(r'(<p>[^<]*?)\b(' + re.escape(phrase) + r')\b', lambda m: f'{m.group(1)}<a href="{R}{href}">{m.group(2)}</a>', html_, count=1)
    return html_


def blog_post(b, blogs):
    R = "../"
    body_html = localize_links(b["html"], R)
    cta = f"""<div class="post-cta"><div><h3>Ready to start your project?</h3><p>Tell us about your idea and get a free consultation and estimate from the Zenvix team — we reply within one business day.</p></div>
<div class="post-cta-actions"><a class="btn btn-light btn-sm" href="{R}contact.html">Get a Free Quote {icon('arrow-right', 'ic ic-sm')}</a><a class="btn btn-ghost-light btn-sm" href="{SITE['whatsapp']}" target="_blank" rel="noopener">{icon('whatsapp', 'ic ic-sm')} WhatsApp</a></div></div>"""
    body_html = body_html.replace("<!--CTA-->", cta, 1).replace("<!--CTA-->", "")
    # remove "Sources and Notes" heading from body; render sources separately
    body_html = re.sub(r'<h2 id="sources-and-notes">.*?</h2>', "", body_html)
    toc = [t for t in b["toc"] if t[0] != "sources-and-notes"]
    toc_html = "".join(f'<li><a href="#{i}">{escape(t)}</a></li>' for i, t in toc)
    srcs = "".join(f'<li><a href="{escape(u)}" target="_blank" rel="nofollow noopener">{escape(u.split("//")[-1].split("/")[0])}</a></li>' for u in b["sources"] if u.startswith("http"))
    url = f"{SITE['url']}/blog/{b['slug']}.html"
    share = (f'<a href="https://www.facebook.com/sharer/sharer.php?u={url}" target="_blank" rel="noopener" aria-label="Share on Facebook">{icon("facebook", "ic ic-sm")}</a>'
             f'<a href="https://x.com/intent/post?url={url}" target="_blank" rel="noopener" aria-label="Share on X">{icon("x-twitter", "ic ic-sm")}</a>'
             f'<a href="https://www.linkedin.com/sharing/share-offsite/?url={url}" target="_blank" rel="noopener" aria-label="Share on LinkedIn">{icon("linkedin", "ic ic-sm")}</a>'
             f'<a href="https://wa.me/?text={url}" target="_blank" rel="noopener" aria-label="Share on WhatsApp">{icon("whatsapp", "ic ic-sm")}</a>'
             f'<button data-copy="{url}" aria-label="Copy link">{icon("copy", "ic ic-sm")}</button>')
    others = [o for o in blogs if o["slug"] != b["slug"]]
    related = "".join(blog_card(R, o) for o in others)
    idx = blogs.index(b)
    prev_b, next_b = blogs[idx - 1] if idx > 0 else None, blogs[idx + 1] if idx < len(blogs) - 1 else None
    pn = '<nav class="post-nav" aria-label="More articles">'
    pn += f'<a class="pn prev" href="{R}blog/{prev_b["slug"]}.html"><small>{icon("arrow-left", "ic ic-xs")} Previous</small><b>{prev_b["title"]}</b></a>' if prev_b else "<span></span>"
    pn += f'<a class="pn next" href="{R}blog/{next_b["slug"]}.html"><small>Next {icon("arrow-right", "ic ic-xs")}</small><b>{next_b["title"]}</b></a>' if next_b else "<span></span>"
    pn += "</nav>"
    tags = "".join(f'<li>#{t}</li>' for t in b["tags"])
    svc_link = {"Custom Software": "software-development", "Mobile Apps": "mobile-app-development", "Web Development": "web-development"}[b["cat"]]
    body = f"""
<article class="post" itemscope itemtype="https://schema.org/BlogPosting">
  <header class="post-hero">
    <div class="ph-grid" aria-hidden="true"></div>
    <div class="container narrow-lg">
      <nav aria-label="Breadcrumb"><ol class="crumbs dark"><li><a href="{R}index.html">Home</a></li><li><a href="{R}blog.html">Blog</a></li><li aria-current="page">{b['cat']}</li></ol></nav>
      <span class="post-cat static anim-up">{b['cat']}</span>
      <h1 class="anim-up" style="--d:.06s" itemprop="headline">{b['title']}</h1>
      <p class="post-excerpt anim-up" style="--d:.12s" itemprop="description">{b['excerpt']}</p>
      <div class="post-byline anim-up" style="--d:.18s">
        <span class="byline-avatar"><img src="{R}assets/img/favicon-192.png" alt="" width="40" height="40"></span>
        <span><b itemprop="author">Zenvix Editorial Team</b><small><time datetime="{b['date']}" itemprop="datePublished">{fmt_date(b['date'])}</time> · {b['mins']} min read</small></span>
        <div class="share">{share}</div>
      </div>
    </div>
  </header>
  <div class="container narrow-lg">
    <figure class="post-cover anim-fade" style="--d:.2s">{img(R, b['img'], b['title'], 1200, 800, eager=True)}</figure>
  </div>
  <div class="container post-layout">
    <aside class="post-aside">
      <div class="toc" data-toc><h2>{icon('list', 'ic ic-sm')} On this page</h2><ol>{toc_html}</ol></div>
      <div class="aside-cta"><span class="ic-badge">{icon('rocket')}</span><h3>Need a quote?</h3><p>Get a free, no-obligation estimate for your project.</p><a class="btn btn-primary btn-sm btn-block" href="{R}contact.html">Talk to an expert</a></div>
    </aside>
    <div class="post-content prose" itemprop="articleBody">
      {body_html}
      {f'<details class="sources"><summary>{icon("file-text", "ic ic-sm")} Sources &amp; notes</summary><ul>{srcs}</ul></details>' if srcs else ''}
      <div class="post-foot">
        <ul class="tags">{tags}</ul>
        <div class="share"><span>Share:</span>{share}</div>
      </div>
      <div class="author-box"><img src="{R}assets/img/favicon-192.png" alt="" width="64" height="64" loading="lazy"><div><b>Written by the Zenvix Editorial Team</b><p>Engineers, designers and strategists at Zenvix Technologies in Lahore, sharing what we learn building software, apps and websites for clients worldwide. Need help with this topic? <a href="{R}services/{svc_link}.html">See our {b['cat'].lower()} services</a>.</p></div></div>
      {pn}
    </div>
  </div>
</article>
<section class="section bg-soft">
  <div class="container">
    {sec_head('Keep reading', 'Related <span class="grad-text">Articles</span>', '')}
    <div class="grid-2 related-posts">{related}</div>
  </div>
</section>
"""
    path = f"blog/{b['slug']}.html"
    schema = [org_schema(), breadcrumb_schema([("Home", ""), ("Blog", "blog.html"), (b["title"], path)]),
              {"@context": "https://schema.org", "@type": "BlogPosting", "headline": b["title"], "description": b["excerpt"],
               "image": f"{SITE['url']}/{b['img']}", "datePublished": b["date"], "dateModified": b["date"],
               "author": {"@type": "Organization", "name": "Zenvix Technologies", "url": SITE["url"] + "/"},
               "publisher": {"@id": SITE["url"] + "/#organization"}, "mainEntityOfPage": url,
               "articleSection": b["cat"], "keywords": ", ".join(b["tags"]), "wordCount": len(re.sub(r"<[^>]+>", " ", b["html"]).split())}]
    page = {"path": path, "root": R, "nav": "blog", "body": "page-post", "og_type": "article",
            "title": f"{b['title']} | Zenvix Technologies", "desc": b["excerpt"][:158], "schema": schema, "og": b["img"]}
    return page, body


def not_found():
    R = "/"
    body = f"""<section class="nf"><div class="container nf-inner">
  <span class="nf-code">404</span>
  <h1>Page not found</h1>
  <p>The page you're looking for has moved or doesn't exist. Let's get you back on track.</p>
  <div class="hero-actions center"><a class="btn btn-primary" href="/index.html">Back to Home {icon('arrow-right', 'ic ic-sm')}</a><a class="btn btn-outline" href="/contact.html">Contact Us</a></div>
</div></section>"""
    page = {"path": "404.html", "root": R, "nav": "", "body": "page-404", "robots": "noindex,follow",
            "title": "Page Not Found | Zenvix Technologies", "desc": "The page you are looking for could not be found."}
    return page, body
