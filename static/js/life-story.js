(function () {
  var page = document.querySelector("[data-life-story-page]");
  var root = document.querySelector("[data-life-story]");
  if (!root) return;

  var items = root.querySelectorAll("[data-chapter-item]");
  var navLinks = root.querySelectorAll("[data-chapter-nav]");
  var progressFill = root.querySelector("[data-life-story-progress]");
  var pageProgressFill = page ? page.querySelector("[data-life-page-progress]") : null;
  var paragraphs = root.querySelectorAll("[data-life-paragraph]");
  var revealBlocks = page ? page.querySelectorAll("[data-life-reveal]") : [];
  var revealStagger = page ? page.querySelector("[data-life-reveal-stagger]") : null;
  var orbs = root.querySelectorAll(".life-story__orb");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  root.querySelectorAll(".life-story__tag").forEach(function (tag, index) {
    tag.style.setProperty("--tag-i", String(index % 12));
  });

  function revealEl(el) {
    if (!el || el.classList.contains("is-revealed")) return;
    el.classList.add("is-revealed");
  }

  function setActiveNav(id) {
    navLinks.forEach(function (link) {
      var active = link.getAttribute("data-chapter-target") === id;
      link.classList.toggle("is-active", active);
      if (active) {
        link.setAttribute("aria-current", "true");
      } else {
        link.removeAttribute("aria-current");
      }
    });
  }

  function updateProgress() {
    var doc = document.documentElement;
    var scrollTop = window.scrollY || doc.scrollTop;
    var maxScroll = doc.scrollHeight - window.innerHeight;
    var ratio = maxScroll > 0 ? Math.min(1, Math.max(0, scrollTop / maxScroll)) : 0;
    var pct = ratio * 100 + "%";
    if (progressFill) progressFill.style.width = pct;
    if (pageProgressFill) pageProgressFill.style.width = pct;
  }

  if (reduceMotion) {
    revealBlocks.forEach(revealEl);
    if (revealStagger) revealStagger.classList.add("is-revealed");
    paragraphs.forEach(revealEl);
  } else if ("IntersectionObserver" in window) {
    var blockObs = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            revealEl(entry.target);
            blockObs.unobserve(entry.target);
          }
        });
      },
      { root: null, rootMargin: "0px 0px -10% 0px", threshold: 0.1 }
    );
    revealBlocks.forEach(function (el) {
      blockObs.observe(el);
    });

    if (revealStagger) {
      var staggerObs = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-revealed");
              staggerObs.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.15 }
      );
      staggerObs.observe(revealStagger);
    }

    var paraObs = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            revealEl(entry.target);
            paraObs.unobserve(entry.target);
          }
        });
      },
      { root: null, rootMargin: "0px 0px -14% 0px", threshold: 0.06 }
    );
    paragraphs.forEach(function (p) {
      paraObs.observe(p);
    });
  } else {
    revealBlocks.forEach(revealEl);
    if (revealStagger) revealStagger.classList.add("is-revealed");
    paragraphs.forEach(revealEl);
  }

  if (items.length && "IntersectionObserver" in window) {
    var chapterObs = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            setActiveNav(entry.target.id);
          }
        });
      },
      {
        root: null,
        rootMargin: "-15% 0px -48% 0px",
        threshold: [0.08, 0.2],
      }
    );

    items.forEach(function (item) {
      if (reduceMotion) {
        item.classList.add("is-visible");
      }
      chapterObs.observe(item);
    });
  } else {
    items.forEach(function (item) {
      item.classList.add("is-visible");
    });
  }

  navLinks.forEach(function (link) {
    link.addEventListener("click", function (e) {
      var targetId = link.getAttribute("data-chapter-target");
      var target = targetId ? document.getElementById(targetId) : null;
      if (target) {
        e.preventDefault();
        target.scrollIntoView({
          behavior: reduceMotion ? "auto" : "smooth",
          block: "start",
        });
        target.focus({ preventScroll: true });
        setActiveNav(target.id);
      }
    });
  });

  window.addEventListener("scroll", updateProgress, { passive: true });
  window.addEventListener("resize", updateProgress, { passive: true });
  updateProgress();

  if (items.length && !window.location.hash) {
    setActiveNav(items[0].id);
  } else if (window.location.hash) {
    setActiveNav(window.location.hash.slice(1));
  }

  if (!reduceMotion && orbs.length && window.matchMedia("(pointer: fine)").matches) {
    var pointerX = 0;
    var pointerY = 0;
    var rafId = 0;

    function tick() {
      rafId = 0;
      orbs.forEach(function (orb, index) {
        var strength = (index + 1) * 8;
        var x = pointerX * strength * 0.015;
        var y = pointerY * strength * 0.012;
        orb.style.transform = "translate3d(" + x + "px," + y + "px, 0)";
      });
    }

    window.addEventListener(
      "mousemove",
      function (event) {
        pointerX = event.clientX / window.innerWidth - 0.5;
        pointerY = event.clientY / window.innerHeight - 0.5;
        if (!rafId) {
          rafId = window.requestAnimationFrame(tick);
        }
      },
      { passive: true }
    );
  }
})();
