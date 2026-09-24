(function () {
  var page = document.querySelector("[data-eulogy-page]");
  if (!page) return;

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var progressFill = page.querySelector("[data-eulogy-progress]");
  var paragraphs = page.querySelectorAll("[data-eulogy-paragraph]");
  var revealBlocks = page.querySelectorAll("[data-eulogy-reveal]");
  var orbs = page.querySelectorAll(".eulogy-shell__orb");

  function revealEl(el) {
    if (!el || el.classList.contains("is-revealed")) return;
    el.classList.add("is-revealed");
  }

  function updateReadingProgress() {
    if (!progressFill) return;
    var doc = document.documentElement;
    var scrollTop = window.scrollY || doc.scrollTop;
    var maxScroll = doc.scrollHeight - window.innerHeight;
    var ratio = maxScroll > 0 ? Math.min(1, Math.max(0, scrollTop / maxScroll)) : 0;
    progressFill.style.width = ratio * 100 + "%";
  }

  if (reduceMotion) {
    paragraphs.forEach(revealEl);
    revealBlocks.forEach(revealEl);
  } else if ("IntersectionObserver" in window) {
    var paraObs = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            revealEl(entry.target);
            paraObs.unobserve(entry.target);
          }
        });
      },
      { root: null, rootMargin: "0px 0px -12% 0px", threshold: 0.08 }
    );

    paragraphs.forEach(function (p) {
      paraObs.observe(p);
    });

    var blockObs = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            revealEl(entry.target);
            blockObs.unobserve(entry.target);
          }
        });
      },
      { root: null, rootMargin: "0px 0px -8% 0px", threshold: 0.12 }
    );

    revealBlocks.forEach(function (block) {
      blockObs.observe(block);
    });
  } else {
    paragraphs.forEach(revealEl);
    revealBlocks.forEach(revealEl);
  }

  window.addEventListener("scroll", updateReadingProgress, { passive: true });
  window.addEventListener("resize", updateReadingProgress, { passive: true });
  updateReadingProgress();

  if (!reduceMotion && orbs.length && window.matchMedia("(pointer: fine)").matches) {
    var orbRaf = 0;
    window.addEventListener(
      "mousemove",
      function (e) {
        if (orbRaf) return;
        orbRaf = window.requestAnimationFrame(function () {
          orbRaf = 0;
          var x = e.clientX / window.innerWidth - 0.5;
          var y = e.clientY / window.innerHeight - 0.5;
          orbs.forEach(function (orb, i) {
            var factor = (i + 1) * 6;
            orb.style.transform =
              "translate3d(" + x * factor + "px," + y * factor * 0.7 + "px,0)";
          });
        });
      },
      { passive: true }
    );
  }
})();
