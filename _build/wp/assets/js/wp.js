/* Zenvix theme — Contact Form 7 enhancements (WordPress only) */
(function () {
  "use strict";

  var form = document.querySelector(".wpcf7 form");
  if (!form) return;

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Character counter
  var details = form.querySelector('[name="details"]');
  var counter = form.querySelector("[data-counter]");
  if (details && counter) {
    var count = function () { counter.textContent = details.value.length; };
    details.addEventListener("input", count);
    count();
  }

  // "Other" service → reveal the extra field
  var service = form.querySelector('select[name="service"]');
  var wrap = form.querySelector("[data-other-wrap]");
  var other = form.querySelector('[name="service-other"]');
  function syncOther(focus) {
    if (!service || !wrap || !other) return;
    var on = service.value === "Other";
    wrap.classList.toggle("is-open", on);
    other.tabIndex = on ? 0 : -1;
    other.setAttribute("aria-required", on ? "true" : "false");
    if (on && focus) setTimeout(function () { other.focus(); }, 250);
    if (!on) other.value = "";
  }
  if (service) {
    service.addEventListener("change", function () { syncOther(true); });
    syncOther(false);
  }

  // Show the success panel once CF7 has accepted the message
  document.addEventListener("wpcf7mailsent", function (e) {
    if (!form.contains(e.target) && e.target !== form && e.target !== form.parentNode) return;
    var card = form.closest(".form-card");
    if (!card) return;
    var view = card.querySelector(".form-view");
    var done = card.querySelector(".form-success");
    if (view && done) {
      view.hidden = true;
      done.hidden = false;
      card.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
    }
    syncOther(false);
    if (counter) counter.textContent = "0";
  });

  // Focus the first invalid field after a failed submit
  document.addEventListener("wpcf7invalid", function () {
    setTimeout(function () {
      var bad = form.querySelector(".wpcf7-not-valid");
      if (bad) bad.focus();
    }, 50);
  });
})();
