(function () {
  const themeToggle = document.querySelector("[data-theme-toggle]");
  const metaThemeColor = document.getElementById("meta-theme-color");
  const THEME_STORAGE_KEY = "memorial-theme";
  const DEFAULT_THEME = "dark";

  function readStoredTheme() {
    try {
      const stored = localStorage.getItem(THEME_STORAGE_KEY);
      if (stored === "light" || stored === "dark") {
        return stored;
      }
    } catch (e) {
      /* ignore storage errors */
    }
    return DEFAULT_THEME;
  }

  function persistTheme(theme) {
    try {
      localStorage.setItem(THEME_STORAGE_KEY, theme);
    } catch (e) {
      /* ignore storage errors */
    }
  }

  function getActiveTheme() {
    const onRoot = document.documentElement.getAttribute("data-theme");
    if (onRoot === "light" || onRoot === "dark") {
      return onRoot;
    }
    return readStoredTheme();
  }

  function applyTheme(theme) {
    const next = theme === "light" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    if (metaThemeColor) {
      metaThemeColor.setAttribute("content", next === "light" ? "#e8edeb" : "#090c0b");
    }
    if (themeToggle) {
      const label = next === "light" ? "Switch to dark mode" : "Switch to light mode";
      themeToggle.setAttribute("aria-pressed", next === "light" ? "true" : "false");
      const labelEl = themeToggle.querySelector(".theme-toggle__label");
      if (labelEl) {
        labelEl.textContent = label;
      }
    }
  }

  applyTheme(readStoredTheme());

  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      const next = getActiveTheme() === "light" ? "dark" : "light";
      persistTheme(next);
      applyTheme(next);
    });
  }

  const shell = document.querySelector(".site-shell");
  const toggle = document.querySelector(".sidebar-toggle");
  const backdrop = document.querySelector(".sidebar-backdrop");
  const sidebar = document.getElementById("site-sidebar");
  const header = document.querySelector(".site-header");

  const DESKTOP_MQ = window.matchMedia("(min-width: 1024px)");

  function syncHeaderHeight() {
    if (!header) return;
    document.documentElement.style.setProperty(
      "--header-h",
      header.getBoundingClientRect().height + "px"
    );
  }

  function isDrawerMode() {
    return !DESKTOP_MQ.matches;
  }

  function setOpen(open) {
    if (!shell || !toggle) return;
    if (!isDrawerMode() && open) return;

    shell.dataset.sidebarOpen = open ? "true" : "false";
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    if (backdrop) {
      backdrop.hidden = !open || !isDrawerMode();
    }
    document.body.classList.toggle("nav-open", open && isDrawerMode());
  }

  if (!shell || !toggle || !sidebar) return;

  syncHeaderHeight();
  window.addEventListener("resize", syncHeaderHeight, { passive: true });
  window.addEventListener("orientationchange", syncHeaderHeight);
  window.addEventListener("load", syncHeaderHeight);
  if (window.visualViewport) {
    window.visualViewport.addEventListener("resize", syncHeaderHeight, { passive: true });
  }

  if (header && "ResizeObserver" in window) {
    new ResizeObserver(syncHeaderHeight).observe(header);
  }

  toggle.addEventListener("click", function () {
    const isOpen = shell.dataset.sidebarOpen === "true";
    setOpen(!isOpen);
  });

  if (backdrop) {
    backdrop.addEventListener("click", function () {
      setOpen(false);
    });
  }

  sidebar.querySelectorAll("a.sidebar-nav__link").forEach(function (link) {
    link.addEventListener("click", function () {
      if (isDrawerMode()) {
        setOpen(false);
      }
    });
  });

  window.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && shell.dataset.sidebarOpen === "true" && isDrawerMode()) {
      setOpen(false);
      toggle.focus();
    }
  });

  DESKTOP_MQ.addEventListener("change", function () {
    setOpen(false);
    syncHeaderHeight();
  });
})();
