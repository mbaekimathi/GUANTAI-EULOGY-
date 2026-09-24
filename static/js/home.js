(function () {
  var page = document.querySelector("[data-home-page]");
  if (!page) return;

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function observeReveal(el, options) {
    if (!("IntersectionObserver" in window) || reduceMotion) {
      el.classList.add("is-visible");
      return;
    }
    var obs = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            obs.unobserve(entry.target);
          }
        });
      },
      options || { root: null, rootMargin: "0px 0px -6% 0px", threshold: 0.08 }
    );
    obs.observe(el);
  }

  page.querySelectorAll("[data-reveal]").forEach(function (el) {
    observeReveal(el);
  });

  page.querySelectorAll("[data-reveal-stagger]").forEach(function (el) {
    observeReveal(el, { root: null, rootMargin: "0px 0px -4% 0px", threshold: 0.06 });
  });

  /* Parallax ambient layer (pointer devices) */
  var ambient = page.querySelector(".home-page__ambient");
  if (!reduceMotion && ambient && window.matchMedia("(pointer: fine)").matches) {
    var ambientRaf = 0;
    window.addEventListener(
      "mousemove",
      function (e) {
        if (ambientRaf) return;
        ambientRaf = window.requestAnimationFrame(function () {
          ambientRaf = 0;
          var x = e.clientX / window.innerWidth - 0.5;
          var y = e.clientY / window.innerHeight - 0.5;
          ambient.style.transform =
            "translate3d(" + x * 18 + "px," + y * 12 + "px,0)";
        });
      },
      { passive: true }
    );
  }

  /* Sticky quick nav */
  var quickNav = page.querySelector("[data-home-quick-nav]");
  var quickLinks = quickNav ? quickNav.querySelectorAll("[data-home-section-link]") : [];
  var sections = [];

  quickLinks.forEach(function (link) {
    var id = link.getAttribute("href");
    if (id && id.charAt(0) === "#") {
      var section = document.getElementById(id.slice(1));
      if (section) sections.push({ link: link, section: section });
    }
  });

  if (sections.length && "IntersectionObserver" in window) {
    var activeId = "";
    var headerH =
      parseInt(getComputedStyle(document.documentElement).getPropertyValue("--header-h"), 10) || 72;
    var navObs = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) activeId = entry.target.id;
        });
        sections.forEach(function (item) {
          var on = item.section.id === activeId;
          item.link.classList.toggle("is-active", on);
          if (on) item.link.setAttribute("aria-current", "true");
          else item.link.removeAttribute("aria-current");
        });
      },
      {
        root: null,
        rootMargin: "-" + headerH + "px 0px -55% 0px",
        threshold: 0.05,
      }
    );
    sections.forEach(function (item) {
      navObs.observe(item.section);
    });
  }

  /* Programme tabs */
  var programme = page.querySelector("[data-home-programme]");
  if (programme) {
    var tabs = programme.querySelectorAll("[data-programme-tab]");
    var panels = programme.querySelectorAll("[data-programme-panel]");

    function showPanel(name) {
      tabs.forEach(function (tab) {
        var selected = tab.getAttribute("data-programme-tab") === name;
        tab.setAttribute("aria-selected", selected ? "true" : "false");
      });
      panels.forEach(function (panel) {
        var match = panel.getAttribute("data-programme-panel") === name;
        panel.hidden = !match;
        if (match) {
          panel.querySelectorAll("[data-reveal-stagger]").forEach(function (stagger) {
            stagger.classList.add("is-visible");
          });
          var journey = panel.querySelector("[data-journey-tree]");
          if (journey && typeof journey.refreshJourney === "function") {
            window.requestAnimationFrame(function () {
              journey.refreshJourney();
            });
          }
        }
      });
    }

    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        showPanel(tab.getAttribute("data-programme-tab") || "schedule");
      });
    });

    var tabMq = window.matchMedia("(min-width: 768px)");
    function syncTabLayout() {
      if (tabMq.matches) {
        panels.forEach(function (panel) {
          panel.hidden = false;
        });
      } else {
        var active =
          programme.querySelector('[data-programme-tab][aria-selected="true"]') || tabs[0];
        showPanel(active ? active.getAttribute("data-programme-tab") || "schedule" : "schedule");
      }
    }
    tabMq.addEventListener("change", syncTabLayout);
    syncTabLayout();
  }

  function initJourneyTree(wrap) {
    if (!wrap || wrap.getAttribute("data-journey-init") === "true") return;
    wrap.setAttribute("data-journey-init", "true");

    var nodes = wrap.querySelectorAll(".schedule-tree__node");
    var stepperBtns = wrap.querySelectorAll("[data-stepper-index]");
    var railFill = wrap.querySelector("[data-timeline-rail-fill]");
    var railGlow = wrap.querySelector("[data-timeline-rail-glow]");
    var selectedIndex = -1;
    var scrollActiveIndex = 0;

    function itemAccent(item) {
      return getComputedStyle(item).getPropertyValue("--item-accent").trim() || "";
    }

    function updateRail(index) {
      if (!nodes.length) return;
      var clamped = Math.max(0, Math.min(index, nodes.length - 1));
      var pct = nodes.length <= 1 ? 100 : (clamped / (nodes.length - 1)) * 100;
      if (railFill) railFill.style.height = pct + "%";
      if (railGlow) {
        railGlow.style.top = pct + "%";
        var accent = itemAccent(nodes[clamped]);
        if (accent) wrap.style.setProperty("--rail-glow-color", accent);
      }
    }

    function syncStepper(index) {
      stepperBtns.forEach(function (btn) {
        var idx = parseInt(btn.getAttribute("data-stepper-index") || "0", 10);
        var on = idx === index;
        btn.classList.toggle("is-current", on);
        btn.setAttribute("aria-current", on ? "step" : "false");
      });
    }

    function setSelected(item, options) {
      if (!item) return;
      var opts = options || {};
      selectedIndex = parseInt(item.getAttribute("data-timeline-step") || "0", 10);
      nodes.forEach(function (el) {
        var on = el === item;
        el.classList.toggle("is-selected", on);
        var card = el.querySelector(".schedule-tree__card");
        if (card) card.setAttribute("aria-pressed", on ? "true" : "false");
      });
      syncStepper(selectedIndex);
      updateRail(selectedIndex);
      if (opts.scrollIntoView && item.scrollIntoView) {
        item.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "nearest" });
      }
    }

    function syncActiveFromScroll() {
      var index = selectedIndex >= 0 ? selectedIndex : scrollActiveIndex;
      updateRail(index);
      if (selectedIndex < 0) syncStepper(scrollActiveIndex);
    }

    var revealObs = null;

    function revealNode(node) {
      if (!node || node.classList.contains("is-revealed")) return;
      node.classList.add("is-revealed");
      if (revealObs) revealObs.unobserve(node);
    }

    function initScrollReveal() {
      if (reduceMotion || !("IntersectionObserver" in window)) {
        nodes.forEach(revealNode);
        return;
      }
      revealObs = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) revealNode(entry.target);
          });
        },
        { root: null, rootMargin: "0px 0px -10% 0px", threshold: [0, 0.12, 0.25] }
      );
      nodes.forEach(function (node) {
        revealObs.observe(node);
      });
    }

    wrap.checkReveals = function () {
      if (reduceMotion) {
        nodes.forEach(revealNode);
        return;
      }
      var vh = window.innerHeight || document.documentElement.clientHeight;
      nodes.forEach(function (node) {
        if (node.classList.contains("is-revealed")) return;
        if (node.offsetParent === null && node.closest("[hidden]")) return;
        var rect = node.getBoundingClientRect();
        if (rect.top < vh * 0.92 && rect.bottom > vh * 0.06) revealNode(node);
      });
    };

    wrap.refreshJourney = function () {
      syncActiveFromScroll();
      window.requestAnimationFrame(function () {
        wrap.checkReveals();
      });
    };

    initScrollReveal();

    nodes.forEach(function (item, i) {
      var card = item.querySelector(".schedule-tree__card");
      if (!card) return;

      card.addEventListener("click", function () {
        setSelected(item);
      });

      card.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          setSelected(item);
          return;
        }
        if (e.key === "ArrowDown" || e.key === "ArrowRight") {
          e.preventDefault();
          var next = nodes[Math.min(i + 1, nodes.length - 1)];
          var nextCard = next && next.querySelector(".schedule-tree__card");
          if (nextCard) nextCard.focus();
        }
        if (e.key === "ArrowUp" || e.key === "ArrowLeft") {
          e.preventDefault();
          var prev = nodes[Math.max(i - 1, 0)];
          var prevCard = prev && prev.querySelector(".schedule-tree__card");
          if (prevCard) prevCard.focus();
        }
      });
    });

    stepperBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var idx = parseInt(btn.getAttribute("data-stepper-index") || "0", 10);
        var item = nodes[idx];
        if (item) setSelected(item, { scrollIntoView: true });
      });
    });

    if (nodes.length && "IntersectionObserver" in window && !reduceMotion) {
      var visibleSteps = {};
      var nodeObs = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            var step = parseInt(entry.target.getAttribute("data-timeline-step") || "0", 10);
            if (entry.isIntersecting) {
              visibleSteps[step] = entry.intersectionRatio;
              entry.target.classList.add("is-active");
            } else {
              delete visibleSteps[step];
              entry.target.classList.remove("is-active");
            }
          });
          var best = -1;
          var bestRatio = 0;
          Object.keys(visibleSteps).forEach(function (key) {
            var ratio = visibleSteps[key];
            if (ratio >= bestRatio) {
              bestRatio = ratio;
              best = parseInt(key, 10);
            }
          });
          if (best >= 0) scrollActiveIndex = best;
          syncActiveFromScroll();
        },
        { root: null, rootMargin: "-12% 0px -50% 0px", threshold: [0.15, 0.35, 0.55] }
      );
      nodes.forEach(function (item) {
        nodeObs.observe(item);
      });
    } else {
      nodes.forEach(function (item) {
        item.classList.add("is-active");
        revealNode(item);
      });
      updateRail(0);
    }

    if (nodes.length && selectedIndex < 0) {
      updateRail(0);
      syncStepper(0);
    }
  }

  page.querySelectorAll("[data-journey-tree]").forEach(initJourneyTree);
})();
