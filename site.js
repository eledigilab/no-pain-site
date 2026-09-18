// no pAIn™ — lingue, menu su telefono, visore immagini, anno nel piè di pagina
//
// Come funzionano le traduzioni
// - Le pagine sono scritte in italiano. Ogni blocco di testo viene riconosciuto
//   da solo e identificato con un codice ricavato dal testo italiano.
// - I file lang/xx.js contengono, per ogni codice, il testo tradotto.
// - Se cambi una frase italiana, il suo codice cambia: finché non viene
//   ritradotta, nelle altre lingue quella frase resta in italiano.
(function () {
  'use strict';

  var LANGS = ['it', 'en', 'fr', 'de', 'es', 'tr', 'el', 'pt', 'ro', 'pl', 'nl', 'sv'];
  var VERSION = '20260918a';
  var root = document.documentElement;
  window.NP_LANGS = window.NP_LANGS || {};

  var IT = {
    ui: { menu: 'Menu', close: 'Chiudi', closeImage: 'Chiudi' },
    mail: {
      privateSubject: 'button4help™ — richiesta di informazioni',
      privateBody: 'Buongiorno,\nvorrei ricevere informazioni su button4help™, prezzo, disponibilità e compatibilità con il mio telefono.\n\nModello del telefono: \n\nCordiali saluti',
      partnerSubject: 'no pAIn™ — richiesta di collaborazione',
      partnerBody: 'Buongiorno,\nvorrei approfondire il progetto no pAIn™ e valutare una possibile collaborazione o dimostrazione.\n\nEnte o azienda: \nNome del referente: \n\nCordiali saluti'
    }
  };

  // ---------- riconoscimento dei testi ----------
  var SKIP = { SCRIPT: 1, STYLE: 1, NOSCRIPT: 1, SELECT: 1, OPTION: 1, TEMPLATE: 1, svg: 1, SVG: 1, VIDEO: 1, IFRAME: 1 };
  var LETTER = /[A-Za-zÀ-ÖØ-öø-ÿ]/;

  function norm(s) { return String(s).replace(/\s+/g, ' ').trim(); }
  function hash(s) {
    var h = 0x811c9dc5;
    for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; }
    return ('0000000' + h.toString(16)).slice(-8);
  }

  function collectUnits(parent, out) {
    for (var el = parent.firstElementChild; el; el = el.nextElementSibling) {
      if (SKIP[el.tagName] || el.hasAttribute('data-no-i18n')) continue;
      var direct = false;
      for (var n = el.firstChild; n; n = n.nextSibling) {
        if (n.nodeType === 3 && LETTER.test(n.nodeValue)) { direct = true; break; }
      }
      if (direct) out.push(el); else collectUnits(el, out);
    }
    return out;
  }

  var units = [], attrs = [], meta = {};
  function scan() {
    collectUnits(document.body, []).forEach(function (el) {
      var html = norm(el.innerHTML);
      units.push({ el: el, key: hash(html), it: el.innerHTML, src: html });
    });
    var inUnit = function (el) {
      for (var i = 0; i < units.length; i++) if (units[i].el.contains(el)) return true;
      return false;
    };
    Array.prototype.forEach.call(document.body.querySelectorAll('[alt],[aria-label],[title]'), function (el) {
      if (el.closest('[data-no-i18n]') || inUnit(el)) return;
      ['alt', 'aria-label', 'title'].forEach(function (name) {
        var v = el.getAttribute(name);
        if (v && LETTER.test(v)) attrs.push({ el: el, name: name, key: hash('@' + norm(v)), it: v, src: norm(v) });
      });
    });
    var desc = document.querySelector('meta[name="description"]');
    meta.title = { it: document.title, key: hash('@' + norm(document.title)), src: norm(document.title) };
    if (desc) meta.desc = { el: desc, it: desc.content, key: hash('@' + norm(desc.content)), src: norm(desc.content) };
  }

  // ---------- applicazione di una lingua ----------
  var current = 'it';

  function dictFor(lang) { return lang === 'it' ? IT : (window.NP_LANGS[lang] || IT); }

  function setLinks(lang) {
    Array.prototype.forEach.call(document.querySelectorAll('a[href]'), function (a) {
      var href = a.getAttribute('href');
      if (!href || /^[a-z]+:|^\/\/|^#/i.test(href)) return;
      var m = href.match(/^([^?#]*\.html)(\?[^#]*)?(#.*)?$/);
      if (!m) return;
      var params = (m[2] || '').replace(/^\?/, '').split('&').filter(function (p) { return p && p.indexOf('lang=') !== 0; });
      if (lang !== 'it') params.push('lang=' + lang);
      a.setAttribute('href', m[1] + (params.length ? '?' + params.join('&') : '') + (m[3] || ''));
    });
  }

  function setMail(dict) {
    var mail = dict.mail || IT.mail;
    Array.prototype.forEach.call(document.querySelectorAll('a[data-mail]'), function (a) {
      var partner = a.getAttribute('data-mail') === 'partner';
      a.setAttribute('href', 'mailto:agostino.giorgio@poliba.it?subject=' +
        encodeURIComponent(partner ? mail.partnerSubject : mail.privateSubject) + '&body=' +
        encodeURIComponent(partner ? mail.partnerBody : mail.privateBody));
    });
  }

  function apply(lang) {
    if (LANGS.indexOf(lang) < 0) lang = 'it';
    current = lang;
    var dict = dictFor(lang), t = lang === 'it' ? {} : (dict.t || {});
    units.forEach(function (u) { var v = t[u.key]; u.el.innerHTML = v != null ? v : u.it; });
    attrs.forEach(function (a) { var v = t[a.key]; a.el.setAttribute(a.name, v != null ? v : a.it); });
    document.title = t[meta.title.key] || meta.title.it;
    if (meta.desc) meta.desc.el.content = t[meta.desc.key] || meta.desc.it;
    root.lang = lang;
    root.setAttribute('data-lang', lang);

    var ui = dict.ui || IT.ui;
    var toggle = document.querySelector('.menu-toggle');
    if (toggle) toggle.textContent = toggle.getAttribute('aria-expanded') === 'true' ? ui.close : ui.menu;
    var code = document.querySelector('.lang-code');
    if (code) code.textContent = lang.toUpperCase();
    var select = document.getElementById('lang-select');
    if (select) select.value = lang;

    // banner ufficiali degli store nella lingua scelta
    Array.prototype.forEach.call(document.querySelectorAll('img[data-badge]'), function (img) {
      var store = img.getAttribute('data-badge');
      img.src = 'assets/badge/' + store + '-' + lang + (store === 'appstore' ? '.svg' : '.png');
    });

    showVisits();
    setMail(dict);
    setLinks(lang);
    try { localStorage.setItem('np-lang', lang); } catch (e) {}
    try {
      var url = new URL(window.location.href);
      if (lang === 'it') url.searchParams.delete('lang'); else url.searchParams.set('lang', lang);
      history.replaceState(null, '', url);
    } catch (e) {}
    root.classList.remove('np-wait');
    fitNav();
  }

  function load(lang, done) {
    if (lang === 'it' || window.NP_LANGS[lang]) { done(lang); return; }
    var s = document.createElement('script');
    s.src = 'lang/' + lang + '.js?v=' + VERSION;
    s.onload = function () { done(window.NP_LANGS[lang] ? lang : 'it'); };
    s.onerror = function () { done('it'); };
    document.head.appendChild(s);
  }

  // ---------- menu ----------
  var toggle = document.querySelector('.menu-toggle');
  var menu = document.getElementById('menu');
  function setOpen(open) {
    if (!toggle || !menu) return;
    menu.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    var ui = dictFor(current).ui || IT.ui;
    toggle.textContent = open ? ui.close : ui.menu;
  }
  if (toggle && menu) {
    toggle.addEventListener('click', function () { setOpen(toggle.getAttribute('aria-expanded') !== 'true'); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') { setOpen(false); toggle.focus(); }
    });
  }

  // se le voci del menu (per esempio in tedesco) non ci stanno, si passa al menu compresso
  function fitNav() {
    var wrap = document.querySelector('.site-header .wrap');
    if (!wrap) return;
    root.classList.remove('nav-collapsed');
    if (window.matchMedia('(max-width: 1180px)').matches) return;
    if (wrap.scrollWidth > wrap.clientWidth + 1) root.classList.add('nav-collapsed');
    else setOpen(false);
  }
  var resizeTimer;
  window.addEventListener('resize', function () { clearTimeout(resizeTimer); resizeTimer = setTimeout(fitNav, 120); });

  // ---------- visore immagini ----------
  var box;
  document.addEventListener('click', function (e) {
    var a = e.target.closest('.media a.zoom');
    if (!a || typeof HTMLDialogElement !== 'function') return;
    e.preventDefault();
    if (!box) {
      box = document.createElement('dialog');
      box.className = 'lightbox';
      box.setAttribute('data-no-i18n', '');
      box.innerHTML = '<button class="close" type="button"></button><figure><img alt=""><figcaption></figcaption></figure>';
      box.addEventListener('click', function (ev) { if (ev.target === box || ev.target.closest('.close')) box.close(); });
      document.body.appendChild(box);
    }
    var img = a.querySelector('img');
    var cap = a.closest('.media').querySelector('figcaption');
    box.querySelector('img').src = a.getAttribute('href');
    box.querySelector('img').alt = img ? img.alt : '';
    box.querySelector('figcaption').innerHTML = cap ? cap.innerHTML : '';
    box.querySelector('.close').textContent = (dictFor(current).ui || IT.ui).closeImage;
    box.showModal();
  });

  // ---------- contatore delle visite ----------
  // Servizio gratuito senza account e senza cookie (abacus.jasoncameron.dev).
  // Conta una visita per sessione del browser e solo sul sito pubblicato:
  // anteprime e prove in locale leggono il numero senza aumentarlo.
  var visits = null;
  function showVisits() {
    var out = document.getElementById('visit-count');
    if (!out || visits == null) return;
    try { out.textContent = visits.toLocaleString(current); } catch (e) { out.textContent = String(visits); }
    out.closest('.visits').hidden = false;
  }
  (function () {
    if (!document.getElementById('visit-count') || !window.fetch) return;
    var live = location.hostname === 'eledigilab.github.io', counted = false;
    try { counted = sessionStorage.getItem('np-visit') === '1'; } catch (e) {}
    var action = live && !counted ? 'hit' : 'get';
    fetch('https://abacus.jasoncameron.dev/' + action + '/eledigilab-no-pain-site/visite')
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        if (!d || typeof d.value !== 'number' || d.value < 1) return;
        if (action === 'hit') { try { sessionStorage.setItem('np-visit', '1'); } catch (e) {} }
        visits = d.value;
        showVisits();
      })
      .catch(function () {});
  })();

  // ---------- avvio ----------
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  scan();
  var select = document.getElementById('lang-select');
  if (select) select.addEventListener('change', function () { load(select.value, apply); });

  var start = root.getAttribute('data-lang') || 'it';
  load(start, function (lang) {
    apply(lang);
    // la pagina era nascosta durante il caricamento: si riporta al punto indicato nel link (#...)
    if (lang !== 'it' && location.hash) {
      var jump = function () {
        try {
          var target = document.querySelector(decodeURIComponent(location.hash));
          if (target) target.scrollIntoView({ behavior: 'instant', block: 'start' });
        } catch (e) {}
      };
      jump();
      if (document.readyState !== 'complete') window.addEventListener('load', jump, { once: true });
    }
  });

  // usato solo per preparare le traduzioni
  window.NP_I18N = {
    collect: function () {
      var out = [[meta.title.key, meta.title.src]];
      if (meta.desc) out.push([meta.desc.key, meta.desc.src]);
      units.forEach(function (u) { out.push([u.key, u.src]); });
      attrs.forEach(function (a) { out.push([a.key, a.src]); });
      return out;
    }
  };
})();
