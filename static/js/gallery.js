(function () {
  var page = document.querySelector("[data-gallery-page]");
  if (!page) return;

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var tiles = page.querySelectorAll("[data-gallery-tile]");
  var revealBlocks = page.querySelectorAll("[data-gallery-reveal]");
  var lightbox = page.querySelector("[data-gallery-lightbox]");
  var dialog = page.querySelector("[data-gallery-dialog]");
  var lightboxImg = page.querySelector("[data-gallery-lightbox-img]");
  var lightboxCaption = page.querySelector("[data-gallery-lightbox-caption]");
  var lightboxCounter = page.querySelector("[data-gallery-lightbox-counter]");
  var openButtons = page.querySelectorAll("[data-gallery-open]");
  var closeTargets = page.querySelectorAll("[data-gallery-close]");
  var prevBtn = page.querySelector("[data-gallery-prev]");
  var nextBtn = page.querySelector("[data-gallery-next]");

  var items = [];
  var activeIndex = 0;
  var lastFocus = null;

  tiles.forEach(function (tile) {
    var img = tile.querySelector("img");
    var captionEl = tile.querySelector(".gallery-tile__caption");
    if (!img) return;
    items.push({
      src: img.getAttribute("data-full-src") || img.src,
      alt: img.alt || "Memorial photograph",
      caption: captionEl ? captionEl.textContent.trim() : "",
    });
  });

  if (!reduceMotion && "IntersectionObserver" in window) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { root: null, rootMargin: "0px 0px -6% 0px", threshold: 0.08 }
    );
    tiles.forEach(function (tile) {
      observer.observe(tile);
    });
    revealBlocks.forEach(function (block) {
      observer.observe(block);
    });
  } else {
    tiles.forEach(function (tile) {
      tile.classList.add("is-visible");
    });
    revealBlocks.forEach(function (block) {
      block.classList.add("is-visible");
    });
  }

  function showSlide(index) {
    if (!items.length || !lightboxImg) return;
    activeIndex = (index + items.length) % items.length;
    var item = items[activeIndex];
    lightboxImg.src = item.src;
    lightboxImg.alt = item.alt;
    if (lightboxCaption) {
      if (item.caption) {
        lightboxCaption.textContent = item.caption;
        lightboxCaption.hidden = false;
      } else {
        lightboxCaption.textContent = "";
        lightboxCaption.hidden = true;
      }
    }
    if (lightboxCounter) {
      lightboxCounter.textContent = activeIndex + 1 + " / " + items.length;
    }
    if (prevBtn) prevBtn.hidden = items.length < 2;
    if (nextBtn) nextBtn.hidden = items.length < 2;
  }

  function openLightbox(index, trigger) {
    if (!lightbox || !items.length) return;
    lastFocus = trigger || document.activeElement;
    showSlide(index);
    lightbox.hidden = false;
    lightbox.setAttribute("aria-hidden", "false");
    lightbox.classList.add("is-open");
    document.body.style.overflow = "hidden";
    var closeBtn = lightbox.querySelector(".gallery-lightbox__close");
    if (closeBtn) closeBtn.focus();
  }

  function closeLightbox() {
    if (!lightbox) return;
    lightbox.hidden = true;
    lightbox.setAttribute("aria-hidden", "true");
    lightbox.classList.remove("is-open");
    document.body.style.overflow = "";
    if (lightboxImg) lightboxImg.src = "";
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  openButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var tile = btn.closest("[data-gallery-tile]");
      var index = tile ? parseInt(tile.getAttribute("data-gallery-index"), 10) : 0;
      openLightbox(isNaN(index) ? 0 : index, btn);
    });
  });

  closeTargets.forEach(function (el) {
    el.addEventListener("click", closeLightbox);
  });

  if (prevBtn) {
    prevBtn.addEventListener("click", function () {
      showSlide(activeIndex - 1);
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener("click", function () {
      showSlide(activeIndex + 1);
    });
  }

  document.addEventListener("keydown", function (event) {
    if (!lightbox || lightbox.hidden) return;
    if (event.key === "Escape") {
      event.preventDefault();
      closeLightbox();
    } else if (event.key === "ArrowLeft") {
      event.preventDefault();
      showSlide(activeIndex - 1);
    } else if (event.key === "ArrowRight") {
      event.preventDefault();
      showSlide(activeIndex + 1);
    }
  });

  if (lightbox) {
    lightbox.addEventListener("click", function (event) {
      if (event.target === lightbox.querySelector(".gallery-lightbox__backdrop")) {
        closeLightbox();
      }
    });
  }
})();
