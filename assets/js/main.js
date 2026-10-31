/* Zenvix Technologies — site interactions (no dependencies) */
(function () {
  "use strict";

  var doc = document;
  var root = doc.documentElement;
  var body = doc.body;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };

  root.classList.add("js");

  /* ---------- Header scroll state, progress bar, back-to-top ---------- */
  var header = $(".site-header");
  var toTop = $(".to-top");
  var ring = toTop && $(".to-top-ring circle", toTop);
  var progress = $(".progress-bar");
  var ticking = false;

  function onScroll() {
    var y = window.pageYOffset;
    var max = root.scrollHeight - window.innerHeight;
    var pct = max > 0 ? Math.min(y / max, 1) : 0;
    if (header) header.classList.toggle("is-scrolled", y > 40);
    if (toTop) toTop.classList.toggle("is-visible", y > 600);
    if (ring) ring.style.strokeDashoffset = String(138.2 * (1 - pct));
    if (progress) progress.style.transform = "scaleX(" + pct + ")";
    ticking = false;
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { window.requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" }); });

  /* ---------- Mega menu: close on Escape ---------- */
  $$(".has-mega").forEach(function (li) {
    li.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { li.classList.remove("is-open"); var a = $("a", li); if (a) a.focus(); a && a.blur(); }
    });
  });

  /* ---------- Mobile drawer (slides in from the left) ---------- */
  var drawer = $("#drawer");
  var burger = $(".burger");
  var lastFocus = null;

  function focusables() {
    return $$('a[href], button:not([disabled]), input, [tabindex]:not([tabindex="-1"])', drawer)
      .filter(function (el) { return el.offsetParent !== null; });
  }
  function openDrawer() {
    lastFocus = doc.activeElement;
    body.classList.add("drawer-open");
    drawer.setAttribute("aria-hidden", "false");
    burger.setAttribute("aria-expanded", "true");
    setTimeout(function () { var f = $(".drawer-close", drawer); if (f) f.focus(); }, 60);
  }
  function closeDrawer() {
    body.classList.remove("drawer-open");
    drawer.setAttribute("aria-hidden", "true");
    burger.setAttribute("aria-expanded", "false");
    if (lastFocus) lastFocus.focus();
  }
  if (drawer && burger) {
    burger.addEventListener("click", openDrawer);
    $$("[data-close-drawer]").forEach(function (el) { el.addEventListener("click", closeDrawer); });
    doc.addEventListener("keydown", function (e) {
      if (!body.classList.contains("drawer-open")) return;
      if (e.key === "Escape") closeDrawer();
      if (e.key === "Tab") {
        var f = focusables(); if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && doc.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && doc.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    $$(".d-acc-btn", drawer).forEach(function (btn) {
      btn.addEventListener("click", function () {
        var li = btn.closest(".d-acc");
        var open = li.classList.toggle("is-open");
        btn.setAttribute("aria-expanded", String(open));
      });
    });
    $$(".drawer-nav a", drawer).forEach(function (a) {
      a.addEventListener("click", function () { if (a.getAttribute("href").indexOf("#") > -1) closeDrawer(); });
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 991 && body.classList.contains("drawer-open")) closeDrawer(); });
  }

  /* ---------- Lazy images: fade in when loaded ---------- */
  $$('img[loading="lazy"]').forEach(function (img) {
    if (img.complete && img.naturalWidth) { img.classList.add("is-loaded"); return; }
    img.addEventListener("load", function () { img.classList.add("is-loaded"); }, { once: true });
    img.addEventListener("error", function () { img.classList.add("is-loaded"); }, { once: true });
  });

  /* ---------- Counters ---------- */
  function animateCount(el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    if (reduceMotion || isNaN(target)) { el.textContent = target; return; }
    var dur = 1600, start = null;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) window.requestAnimationFrame(step);
    }
    window.requestAnimationFrame(step);
  }

  /* ---------- Reveal on scroll ---------- */
  var revealEls = $$(".reveal, .reveal-pop, .tl-step");
  var counters = $$("[data-count]");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("is-visible");
        io.unobserve(en.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    revealEls.forEach(function (el) { io.observe(el); });

    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        animateCount(en.target);
        cio.unobserve(en.target);
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { cio.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
    counters.forEach(function (el) { el.textContent = el.getAttribute("data-count"); });
  }

  /* ---------- Portfolio filter ---------- */
  var grid = $("[data-filter-grid]");
  if (grid) {
    var chips = $$(".filters [data-filter]");
    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        var f = chip.getAttribute("data-filter");
        chips.forEach(function (c) { var on = c === chip; c.classList.toggle("is-active", on); c.setAttribute("aria-selected", String(on)); });
        $$(".proj-card", grid).forEach(function (card) {
          var show = f === "all" || (" " + card.getAttribute("data-cat") + " ").indexOf(" " + f + " ") > -1;
          card.classList.toggle("is-hidden", !show);
          card.classList.remove("is-entering");
          if (show) { void card.offsetWidth; card.classList.add("is-entering"); card.classList.add("is-visible"); }
        });
      });
    });
  }

  /* ---------- Testimonial slider ---------- */
  $$("[data-slider]").forEach(function (slider) {
    var slides = $$(".t-slide", slider);
    var avatars = $$(".t-avatar", slider.parentNode);
    var current = $("[data-current]", slider);
    var i = 0, timer = null;
    function go(n) {
      i = (n + slides.length) % slides.length;
      slides.forEach(function (s, k) { s.classList.toggle("is-active", k === i); s.setAttribute("aria-hidden", String(k !== i)); });
      avatars.forEach(function (a, k) { a.classList.toggle("is-active", k === i); });
      if (current) current.textContent = i + 1;
    }
    function play() { if (!reduceMotion) { stop(); timer = setInterval(function () { go(i + 1); }, 6500); } }
    function stop() { if (timer) clearInterval(timer); }
    $("[data-next]", slider).addEventListener("click", function () { go(i + 1); play(); });
    $("[data-prev]", slider).addEventListener("click", function () { go(i - 1); play(); });
    slider.addEventListener("mouseenter", stop);
    slider.addEventListener("mouseleave", play);
    var sx = null;
    slider.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; }, { passive: true });
    slider.addEventListener("touchend", function (e) {
      if (sx === null) return;
      var dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 40) { go(dx < 0 ? i + 1 : i - 1); play(); }
      sx = null;
    });
    go(0); play();
  });

  /* ---------- Tabs ---------- */
  $$("[data-tabs]").forEach(function (wrap) {
    var tabs = $$('[role="tab"]', wrap);
    function select(tab) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.classList.toggle("is-active", on);
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        var panel = doc.getElementById(t.getAttribute("aria-controls"));
        if (panel) { panel.hidden = !on; panel.classList.toggle("is-active", on); }
      });
      $$('#' + tab.getAttribute("aria-controls") + ' img[loading="lazy"]').forEach(function (im) { im.classList.add("is-loaded"); });
    }
    tabs.forEach(function (t, k) {
      t.addEventListener("click", function () { select(t); });
      t.addEventListener("keydown", function (e) {
        var n = null;
        if (e.key === "ArrowRight") n = tabs[(k + 1) % tabs.length];
        if (e.key === "ArrowLeft") n = tabs[(k - 1 + tabs.length) % tabs.length];
        if (n) { e.preventDefault(); select(n); n.focus(); }
      });
    });
  });

  /* ---------- Accordion (FAQ) ---------- */
  $$(".acc-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var item = btn.closest(".acc-item");
      var open = !item.classList.contains("is-open");
      $$(".acc-item.is-open", item.parentNode).forEach(function (o) {
        if (o !== item) { o.classList.remove("is-open"); $(".acc-btn", o).setAttribute("aria-expanded", "false"); }
      });
      item.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", String(open));
    });
  });

  /* ---------- Blog filter + search ---------- */
  var blogGrid = $("[data-blog-grid]");
  if (blogGrid) {
    var cards = $$(".post-card", blogGrid);
    var bchips = $$(".blog-toolbar [data-filter]");
    var search = $("[data-blog-search]");
    var empty = $("[data-empty]");
    var cat = "all";
    function apply() {
      var q = (search && search.value || "").trim().toLowerCase();
      var shown = 0;
      cards.forEach(function (c) {
        var ok = (cat === "all" || c.getAttribute("data-cat") === cat) && (!q || c.getAttribute("data-title").indexOf(q) > -1 || c.textContent.toLowerCase().indexOf(q) > -1);
        c.classList.toggle("is-hidden", !ok);
        if (ok) { shown++; c.classList.add("is-visible"); }
      });
      blogGrid.classList.toggle("is-filtered", cat !== "all" || !!q);
      if (empty) empty.hidden = shown > 0;
    }
    bchips.forEach(function (ch) {
      ch.addEventListener("click", function () {
        cat = ch.getAttribute("data-filter");
        bchips.forEach(function (c) { var on = c === ch; c.classList.toggle("is-active", on); c.setAttribute("aria-pressed", String(on)); });
        apply();
      });
    });
    if (search) search.addEventListener("input", apply);
  }

  /* ---------- Table of contents scrollspy ---------- */
  var toc = $("[data-toc]");
  if (toc && "IntersectionObserver" in window) {
    var links = $$("a", toc);
    var map = {};
    links.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var heads = Object.keys(map).map(function (id) { return doc.getElementById(id); }).filter(Boolean);
    var sio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          links.forEach(function (l) { l.classList.remove("is-active"); });
          var a = map[en.target.id];
          if (a) { a.classList.add("is-active"); }
        }
      });
    }, { rootMargin: "-90px 0px -70% 0px" });
    heads.forEach(function (h) { sio.observe(h); });
  }

  /* ---------- Copy link ---------- */
  $$("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var url = btn.getAttribute("data-copy");
      var done = function () { btn.classList.add("is-copied"); setTimeout(function () { btn.classList.remove("is-copied"); }, 1600); };
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, done); else done();
    });
  });

  /* ---------- Contact form (validates, then opens the visitor's email app) ---------- */
  var TO = "zenvixtechnologies7@gmail.com";
  var form = $("[data-contact-form]");
  if (form) {
    var details = $("#details", form);
    var counter = $("[data-counter]", form);
    if (details && counter) details.addEventListener("input", function () { counter.textContent = details.value.length; });

    var emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
    function validField(el) {
      var v = (el.value || "").trim();
      if (el.type === "checkbox") return el.checked;
      if (el.required && !v) return false;
      if (el.type === "email" && v && !emailRe.test(v)) return false;
      if (el.type === "tel" && v && !/^[0-9+()\-\s]{7,20}$/.test(v)) return false;
      if (el.minLength > 0 && v && v.length < el.minLength) return false;
      return true;
    }
    function check(el) {
      var ok = validField(el);
      var f = el.closest(".field");
      if (f) f.classList.toggle("is-invalid", !ok);
      el.setAttribute("aria-invalid", String(!ok));
      return ok;
    }
    var inputs = $$("input:not(#website), select, textarea", form);
    inputs.forEach(function (el) {
      el.addEventListener("blur", function () { if (el.value || el.type === "checkbox") check(el); });
      el.addEventListener("input", function () { var f = el.closest(".field"); if (f && f.classList.contains("is-invalid")) check(el); });
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if ($("#website", form).value) return; // honeypot
      var bad = inputs.filter(function (el) { return !check(el); });
      if (bad.length) { bad[0].focus(); return; }
      var val = function (id) { var el = $("#" + id, form); return el ? el.value.trim() : ""; };
      var lines = [
        "Name: " + val("fname") + " " + val("lname"),
        "Email: " + val("email"),
        "Phone: " + (val("phone") || "-"),
        "Company: " + (val("company") || "-"),
        "Service: " + val("service"),
        "Budget: " + (val("budget") || "-"),
        "Timeline: " + (val("timeline") || "-"),
        "",
        "Project details:",
        val("details")
      ];
      var subject = "New project inquiry — " + val("service") + " (" + val("fname") + " " + val("lname") + ")";
      window.location.href = "mailto:" + TO + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(lines.join("\n"));
      var card = form.closest(".form-card");
      $(".form-view", card).hidden = true;
      $(".form-success", card).hidden = false;
      card.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
    });
  }

  /* ---------- Newsletter (opens email app until a mailing service is connected) ---------- */
  $$("[data-newsletter]").forEach(function (nf) {
    nf.addEventListener("submit", function (e) {
      e.preventDefault();
      var input = $("input", nf), msg = $(".newsletter-msg", nf);
      var v = input.value.trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) { msg.textContent = "Please enter a valid email address."; input.focus(); return; }
      window.location.href = "mailto:" + TO + "?subject=" + encodeURIComponent("Newsletter subscription") + "&body=" + encodeURIComponent("Please add " + v + " to the Zenvix newsletter.");
      msg.textContent = "Thanks! Send the email that just opened to confirm.";
      input.value = "";
    });
  });

  /* ---------- Footer year ---------- */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
