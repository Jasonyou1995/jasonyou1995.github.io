/* Shengwei You site script. No dependencies, no storage, no cookies, no analytics.
   1) Agent X-ray: toggles the agent view and builds the panel from the page's real JSON-LD.
   2) Door picker: one situation, one next step. Works without JS (all panels stack).
   3) Pointer light on the hero and the picker stage (fine pointers only, off for reduced motion).
   4) Digital twin widget. Talks to the proxy in twin/ when data-twin-endpoint is set,
      otherwise degrades to a prefilled email. The browser never holds an API key. */
(function () {
  "use strict";
  var d = document;
  var cfg = d.getElementById("site-js");
  if (!cfg) return;
  var T = {};
  try { T = JSON.parse(cfg.getAttribute("data-i18n") || "{}"); } catch (e) {}
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Agent X-ray ---------- */
  var btn = d.getElementById("xray-toggle");
  var panel = d.getElementById("xray-panel");
  var listEl = d.getElementById("xp-list");
  var jsonEl = d.getElementById("xp-json");
  var countEl = d.getElementById("xp-count");
  var label = d.getElementById("xray-label");
  var nodes = [];
  try {
    var g = JSON.parse(d.getElementById("graph").textContent);
    nodes = g["@graph"] || [];
  } catch (e) {}

  function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function highlight(json) {
    return esc(json).replace(
      /("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g,
      function (m) {
        var c = "jn";
        if (/^"/.test(m)) c = /:$/.test(m) ? "jk" : "js";
        else if (/true|false|null/.test(m)) c = "jb";
        return '<span class="' + c + '">' + m + "</span>";
      }
    );
  }
  function frag(id) { var i = (id || "").indexOf("#"); return i < 0 ? id : id.slice(i + 1); }
  function typeOf(n) { var t = n["@type"]; return Array.isArray(t) ? t[0] : t; }

  function select(i, scroll) {
    var rows = listEl.querySelectorAll(".xp-row");
    for (var k = 0; k < rows.length; k++) rows[k].setAttribute("aria-current", k === i ? "true" : "false");
    jsonEl.innerHTML = highlight(JSON.stringify(nodes[i], null, 2));
    jsonEl.scrollTop = 0;
    if (scroll) {
      var el = d.querySelector('[data-ld="' + frag(nodes[i]["@id"]) + '"]');
      if (el) {
        el.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "center" });
      }
    }
  }
  function buildPanel() {
    if (!listEl || listEl.children.length || !nodes.length) return;
    nodes.forEach(function (n, i) {
      var li = d.createElement("li");
      var b = d.createElement("button");
      b.type = "button";
      b.className = "xp-row";
      b.setAttribute("data-type", typeOf(n));
      var t = d.createElement("b");
      t.textContent = typeOf(n);
      var s = d.createElement("span");
      s.textContent = "#" + frag(n["@id"] || "");
      b.appendChild(t);
      b.appendChild(s);
      b.addEventListener("click", function () { select(i, true); });
      li.appendChild(b);
      listEl.appendChild(li);
    });
    if (countEl) countEl.textContent = nodes.length;
    var start = 0;
    for (var i = 0; i < nodes.length; i++) if (typeOf(nodes[i]) === "Person") start = i;
    select(start, false);
  }
  function setXray(on, silent) {
    d.body.classList.toggle("xray", on);
    if (btn) btn.setAttribute("aria-checked", on ? "true" : "false");
    if (label) label.textContent = on ? T.xray_on : T.xray_off;
    if (panel) {
      if (on) buildPanel();
      panel.hidden = !on;
    }
    if (!silent && window.history && history.replaceState) {
      history.replaceState(null, "", on ? "#xray" : location.pathname + location.search);
    }
  }
  if (btn) {
    btn.addEventListener("click", function () { setXray(!d.body.classList.contains("xray")); });
  }
  var xclose = d.getElementById("xp-close");
  if (xclose) xclose.addEventListener("click", function () { setXray(false); if (btn) btn.focus(); });
  d.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && d.body.classList.contains("xray")) { setXray(false); if (btn) btn.focus(); }
  });
  d.addEventListener("click", function (e) {
    if (!d.body.classList.contains("xray")) return;
    var el = e.target.closest ? e.target.closest("[data-ld]") : null;
    if (!el || (e.target.closest && e.target.closest("a,button,input,summary"))) return;
    var key = el.getAttribute("data-ld");
    for (var i = 0; i < nodes.length; i++) if (frag(nodes[i]["@id"]) === key) { select(i, false); break; }
  });
  if (location.hash === "#xray") setXray(true, true);

  /* ---------- Door picker ---------- */
  var picker = d.getElementById("picker");
  if (picker) {
    var tabs = Array.prototype.slice.call(picker.querySelectorAll("[role=tab]"));
    var panels = tabs.map(function (t) { return d.getElementById(t.getAttribute("aria-controls")); });
    var rtl = d.documentElement.getAttribute("dir") === "rtl";
    var pick = function (i, focus, remember) {
      tabs.forEach(function (t, k) {
        var on = k === i;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        if (panels[k]) panels[k].hidden = !on;
      });
      if (focus) tabs[i].focus();
      if (remember && window.history && history.replaceState && !d.body.classList.contains("xray")) {
        history.replaceState(null, "", "#for-" + tabs[i].getAttribute("data-door"));
      }
    };
    var fromHash = function () {
      var m = /^#for-([a-z]+)$/.exec(location.hash);
      if (!m) return false;
      for (var k = 0; k < tabs.length; k++) {
        if (tabs[k].getAttribute("data-door") === m[1]) { pick(k, false, false); return true; }
      }
      return false;
    };
    picker.classList.add("live");
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { pick(i, false, true); });
      t.addEventListener("keydown", function (e) {
        var dir = 0;
        if (e.key === "ArrowDown") dir = 1;
        else if (e.key === "ArrowUp") dir = -1;
        else if (e.key === "ArrowRight") dir = rtl ? -1 : 1;
        else if (e.key === "ArrowLeft") dir = rtl ? 1 : -1;
        else if (e.key === "Home") { e.preventDefault(); pick(0, true, true); return; }
        else if (e.key === "End") { e.preventDefault(); pick(tabs.length - 1, true, true); return; }
        if (!dir) return;
        e.preventDefault();
        pick((i + dir + tabs.length) % tabs.length, true, true);
      });
    });
    if (!fromHash()) pick(0, false, false);
    window.addEventListener("hashchange", fromHash);
    var stage = picker.querySelector(".pick-stage");
    if (stage && !reduce && window.matchMedia && window.matchMedia("(pointer: fine)").matches) {
      stage.addEventListener("pointermove", function (e) {
        var r = stage.getBoundingClientRect();
        stage.style.setProperty("--px", ((e.clientX - r.left) / r.width * 100).toFixed(1) + "%");
        stage.style.setProperty("--py", ((e.clientY - r.top) / r.height * 100).toFixed(1) + "%");
      });
    }
  }

  /* ---------- Pointer light ---------- */
  var hero = d.querySelector(".hero");
  if (hero && !reduce && window.matchMedia && window.matchMedia("(pointer: fine)").matches) {
    var raf = 0;
    hero.addEventListener("pointermove", function (e) {
      if (raf) return;
      raf = requestAnimationFrame(function () {
        raf = 0;
        var r = hero.getBoundingClientRect();
        hero.style.setProperty("--lx", ((e.clientX - r.left) / r.width * 100).toFixed(1) + "%");
        hero.style.setProperty("--ly", ((e.clientY - r.top) / r.height * 100).toFixed(1) + "%");
      });
    });
  }

  /* ---------- Digital twin ---------- */
  var app = d.getElementById("twin-app");
  if (!app) return;
  var endpoint = cfg.getAttribute("data-twin-endpoint") || "";
  var sitekey = cfg.getAttribute("data-turnstile") || "";
  var mail = cfg.getAttribute("data-mail") || "";
  var locale = d.documentElement.getAttribute("data-locale") || "en";
  var log = d.getElementById("tw-log");
  var form = d.getElementById("tw-form");
  var input = d.getElementById("tw-input");
  var send = d.getElementById("tw-send");
  var hint = d.getElementById("tw-hint");
  var modeBtns = app.querySelectorAll("[data-mode]");
  var mode = "ask";
  var token = "";
  var tsLoaded = false;
  var busy = false;

  function add(role, text) {
    var p = d.createElement("p");
    p.className = "msg " + (role === "me" ? "msg-me" : "msg-bot");
    p.textContent = text;
    log.appendChild(p);
    log.scrollTop = log.scrollHeight;
    return p;
  }
  add("bot", T.twin_hello || "");
  if (!endpoint) add("bot", T.twin_offline || "");

  Array.prototype.forEach.call(modeBtns, function (b) {
    b.addEventListener("click", function () {
      mode = b.getAttribute("data-mode");
      Array.prototype.forEach.call(modeBtns, function (x) {
        x.setAttribute("aria-pressed", x === b ? "true" : "false");
      });
      hint.hidden = mode !== "break";
    });
  });

  function loadTurnstile() {
    if (!sitekey || tsLoaded) return;
    tsLoaded = true;
    var s = d.createElement("script");
    s.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
    s.async = true;
    s.onload = function () {
      var box = d.getElementById("tw-ts");
      if (window.turnstile && box) {
        window.turnstile.render(box, {
          sitekey: sitekey,
          appearance: "interaction-only",
          callback: function (t) { token = t; }
        });
      }
    };
    d.head.appendChild(s);
  }
  input.addEventListener("focus", loadTurnstile, { once: true });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var q = input.value.trim().slice(0, 500);
    if (!q || busy) return;
    if (!endpoint) {
      window.location.href = "mailto:" + mail + "?subject=" + encodeURIComponent("Question for Shengwei") +
        "&body=" + encodeURIComponent(q);
      return;
    }
    add("me", q);
    input.value = "";
    busy = true;
    send.disabled = true;
    var wait = add("bot", (T.twin_wait || "...") + " ...");
    fetch(endpoint, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ message: q, mode: mode, locale: locale, token: token })
    })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (res) {
        if (!res.ok || !res.j || typeof res.j.reply !== "string") throw new Error("bad");
        wait.textContent = res.j.reply;
        if (res.j.breached) add("bot", T.twin_breach || "");
      })
      .catch(function () { wait.textContent = T.twin_error || ""; })
      .then(function () {
        busy = false;
        send.disabled = false;
        token = "";
        if (window.turnstile && sitekey) { try { window.turnstile.reset(); } catch (e2) {} }
        log.scrollTop = log.scrollHeight;
      });
  });
})();
