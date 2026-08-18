/* Minimal progressive enhancement. The site works fine with JS disabled. */
(function () {
  'use strict';

  /* --- Theme toggle -------------------------------------------------------
     Default follows the OS. Once the user clicks, their choice is remembered
     in localStorage and wins over the OS preference via [data-theme] on <html>. */
  var root = document.documentElement;
  var toggle = document.getElementById('theme-toggle');
  var stored = null;

  try { stored = localStorage.getItem('theme'); } catch (e) { /* private mode */ }
  if (stored === 'light' || stored === 'dark') root.setAttribute('data-theme', stored);

  if (toggle) {
    toggle.addEventListener('click', function () {
      var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      var current = root.getAttribute('data-theme') || (prefersDark ? 'dark' : 'light');
      var next = current === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) { /* ignore */ }
    });
  }

  /* --- Mobile nav --------------------------------------------------------- */
  var navToggle = document.querySelector('.nav__toggle');
  var navMenu = document.getElementById('nav-menu');

  if (navToggle && navMenu) {
    navToggle.addEventListener('click', function () {
      var open = navMenu.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', String(open));
    });
    // Close after tapping a link, so the anchor jump is visible
    navMenu.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        navMenu.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* --- Footer year -------------------------------------------------------- */
  var year = document.getElementById('year');
  if (year) year.textContent = String(new Date().getFullYear());
})();
