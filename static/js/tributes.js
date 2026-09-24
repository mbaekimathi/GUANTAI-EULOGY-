(function () {
  var page = document.querySelector("[data-tributes-page]");
  if (!page) return;

  var cards = page.querySelectorAll("[data-tribute-card]");
  var filters = page.querySelectorAll("[data-tribute-filter]");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function applyFilter(key) {
    filters.forEach(function (btn) {
      btn.classList.toggle("is-active", btn.getAttribute("data-tribute-filter") === key);
    });
    cards.forEach(function (card) {
      var group = card.getAttribute("data-tribute-group");
      var show = key === "all" || group === key;
      card.classList.toggle("is-hidden", !show);
      if (show && !reduceMotion) {
        card.classList.remove("is-visible");
        window.requestAnimationFrame(function () {
          card.classList.add("is-visible");
        });
      }
    });
  }

  filters.forEach(function (btn) {
    btn.addEventListener("click", function () {
      applyFilter(btn.getAttribute("data-tribute-filter") || "all");
    });
  });

  if (cards.length && "IntersectionObserver" in window && !reduceMotion) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
          }
        });
      },
      { root: null, rootMargin: "0px 0px -8% 0px", threshold: 0.12 }
    );
    cards.forEach(function (card) {
      observer.observe(card);
    });
  } else {
    cards.forEach(function (card) {
      card.classList.add("is-visible");
    });
  }

  var orbs = page.querySelectorAll(".tributes-page__orb");
  if (!reduceMotion && orbs.length && window.matchMedia("(pointer: fine)").matches) {
    var rafId = 0;
    window.addEventListener(
      "mousemove",
      function (event) {
        if (rafId) return;
        rafId = window.requestAnimationFrame(function () {
          rafId = 0;
          var x = event.clientX / window.innerWidth - 0.5;
          var y = event.clientY / window.innerHeight - 0.5;
          orbs.forEach(function (orb, index) {
            var strength = (index + 1) * 10;
            orb.style.transform =
              "translate3d(" + x * strength * 0.02 + "px," + y * strength * 0.015 + "px,0)";
          });
        });
      },
      { passive: true }
    );
  }
})();
