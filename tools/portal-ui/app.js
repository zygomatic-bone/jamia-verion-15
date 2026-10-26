/* Shared interactions: navigation, themes, reveals, slideshow and lightbox. */
(() => {
  "use strict";

  const root = document.documentElement;
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Theme selection is initialized in the document head to avoid a color flash.
  const themeButton = document.querySelector("[data-theme-toggle]");
  const syncThemeLabel = () => {
    if (!themeButton) return;
    const isDark = root.dataset.theme === "dark";
    themeButton.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
    themeButton.title = isDark ? "Light mode" : "Dark mode";
  };
  syncThemeLabel();
  themeButton?.addEventListener("click", () => {
    const next = root.dataset.theme === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    try { localStorage.setItem("jame-theme", next); } catch (_) { /* storage may be unavailable */ }
    syncThemeLabel();
  });

  // Desktop dropdowns: close peers, close on outside click and Escape.
  const navGroups = [...document.querySelectorAll(".nav-group")];
  navGroups.forEach((group) => group.addEventListener("toggle", () => {
    if (group.open) navGroups.forEach((peer) => { if (peer !== group) peer.open = false; });
  }));
  document.addEventListener("click", (event) => {
    if (!event.target.closest(".nav-group")) navGroups.forEach((group) => { group.open = false; });
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") navGroups.forEach((group) => { group.open = false; });
  });

  // Accessible mobile drawer. Native dialog provides Escape handling and focus return.
  const drawer = document.querySelector("#mobile-drawer");
  const drawerOpen = document.querySelector("[data-menu-open]");
  const drawerClose = document.querySelector("[data-menu-close]");
  drawerOpen?.addEventListener("click", () => drawer?.showModal());
  drawerClose?.addEventListener("click", () => drawer?.close());
  drawer?.addEventListener("click", (event) => {
    const rect = drawer.getBoundingClientRect();
    if (event.clientX < rect.left) drawer.close();
  });

  // Reveal and stagger effects remain fully visible when IntersectionObserver is unavailable.
  const revealItems = [...document.querySelectorAll(".reveal, .stagger, .pf-reveal, .pf-stagger")];
  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealItems.forEach((el) => el.classList.add("is-visible"));
  } else {
    const showOnEnter = (entries, self) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        self.unobserve(entry.target);
      });
    };
    // Normal items are revealed once 12% of them is on screen. A very tall item (for example the Institutions
    // card grid, about 6,700px tall in one column on a phone) can NEVER show 12% of itself at once, so it would stay
    // invisible forever and the page looked blank. Tall items are revealed as soon as any part is on screen instead.
    const fractionObserver = new IntersectionObserver(showOnEnter, { threshold: .12, rootMargin: "0px 0px -5%" });
    const anyPartObserver = new IntersectionObserver(showOnEnter, { threshold: 0, rootMargin: "0px 0px -5%" });
    revealItems.forEach((el) => {
      const tooTallForFraction = el.offsetHeight * .12 > innerHeight * .9;
      (tooTallForFraction ? anyPartObserver : fractionObserver).observe(el);
    });
    // Safety net: if anything is still hidden shortly after load while it is clearly on screen, show it.
    setTimeout(() => {
      revealItems.forEach((el) => {
        const rect = el.getBoundingClientRect();
        if (!el.classList.contains("is-visible") && rect.top < innerHeight && rect.bottom > 0) el.classList.add("is-visible");
      });
    }, 2500);
  }

  // Cards drop their stagger delays once the entrance finishes so hover feels immediate.
  document.querySelectorAll(".stagger, .pf-stagger").forEach((group) => {
    group.addEventListener("transitionend", () => group.classList.add("is-settled"), { once: true });
  });

  // Recognitions gallery: per-card entrance on scroll (touch screens show the details and the link without a first tap).
  const rgItems = [...document.querySelectorAll(".rg-item")];
  if (rgItems.length) {
    if (reduceMotion || !("IntersectionObserver" in window)) {
      rgItems.forEach((el) => el.classList.add("is-in"));
    } else {
      const rgObserver = new IntersectionObserver((entries, self) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-in");
          self.unobserve(entry.target);
        });
      }, { threshold: .06, rootMargin: "0px 0px -4%" });
      rgItems.forEach((el) => rgObserver.observe(el));
    }
  }

  // Decorative layers for the glass look: drifting colour orbs and a scroll progress bar.
  const ambient = document.createElement("div");
  ambient.className = "ambient";
  ambient.setAttribute("aria-hidden", "true");
  ambient.innerHTML = "<span></span><span></span><span></span>";
  document.body.prepend(ambient);
  const progress = document.createElement("div");
  progress.className = "scroll-progress";
  progress.setAttribute("aria-hidden", "true");
  document.body.append(progress);

  const header = document.querySelector(".site-header");
  const backTop = document.querySelector(".back-top");
  let scrollTicking = false;
  const syncScroll = () => {
    scrollTicking = false;
    const max = document.documentElement.scrollHeight - innerHeight;
    progress.style.setProperty("--progress", max > 0 ? Math.min(1, scrollY / max).toFixed(4) : 0);
    header?.classList.toggle("is-scrolled", scrollY > 12);
    backTop?.classList.toggle("is-visible", scrollY > 700);
  };
  addEventListener("scroll", () => {
    if (!scrollTicking) { scrollTicking = true; requestAnimationFrame(syncScroll); }
  }, { passive: true });
  addEventListener("resize", syncScroll, { passive: true });
  syncScroll();

  // Pointer-following spotlight and gentle tilt on glass cards (fine pointers only). One delegated listener; the card under the
  // pointer is updated once per frame, and only the card under the pointer is ever measured.
  if (!reduceMotion && matchMedia("(hover: hover) and (pointer: fine)").matches) {
    const cardSelector = ".card, .contact-item, .contact-cta";
    let activeCard = null;
    let lastEvent = null;
    let frame = 0;
    const paint = () => {
      frame = 0;
      if (!activeCard || !lastEvent) return;
      const rect = activeCard.getBoundingClientRect();
      const x = (lastEvent.clientX - rect.left) / rect.width;
      const y = (lastEvent.clientY - rect.top) / rect.height;
      activeCard.style.setProperty("--mx", `${(x * 100).toFixed(1)}%`);
      activeCard.style.setProperty("--my", `${(y * 100).toFixed(1)}%`);
      if (activeCard.classList.contains("card")) {
        activeCard.style.setProperty("--rx", `${((0.5 - y) * 6).toFixed(2)}deg`);
        activeCard.style.setProperty("--ry", `${((x - 0.5) * 6).toFixed(2)}deg`);
      }
    };
    const release = (card) => {
      card.style.removeProperty("--rx");
      card.style.removeProperty("--ry");
    };
    document.addEventListener("pointermove", (event) => {
      const card = event.target.closest?.(cardSelector) || null;
      if (card !== activeCard) {
        if (activeCard) release(activeCard);
        activeCard = card;
      }
      if (!card) return;
      lastEvent = event;
      if (!frame) frame = requestAnimationFrame(paint);
    }, { passive: true });
    document.documentElement.addEventListener("pointerleave", () => { if (activeCard) release(activeCard); activeCard = null; }, { passive: true });
  }

  // Homepage hero: crossfading slideshow of gallery photographs (sharp photo + blurred backdrop stay in step).
  const heroImage = document.querySelector("[data-hero-images]");
  if (heroImage) {
    const images = (heroImage.dataset.heroImages || "").split(",").map((s) => s.trim()).filter(Boolean);
    const hero = heroImage.closest(".hero");
    const fg = [...hero.querySelectorAll(".hero-media img")];
    const bg = [...hero.querySelectorAll(".hero-backdrop img")];
    const heroTrigger = heroImage.closest("[data-lightbox]");
    let index = Math.max(0, images.indexOf(heroImage.getAttribute("src")));
    let layer = 0;
    let heroOnScreen = true;
    if ("IntersectionObserver" in window) new IntersectionObserver((entries) => { heroOnScreen = entries[entries.length - 1].isIntersecting; }).observe(hero);
    if (!reduceMotion && images.length > 1 && fg.length === 2 && bg.length === 2) setInterval(() => {
      if (document.hidden || !heroOnScreen) return;
      index = (index + 1) % images.length;
      const next = 1 - layer;
      const preload = new Image();
      preload.onload = () => {
        [fg[next], bg[next]].forEach((el) => { if (el.getAttribute("src") !== images[index]) el.src = images[index]; });
        fg[next].classList.add("is-active"); bg[next].classList.add("is-active");
        fg[layer].classList.remove("is-active"); bg[layer].classList.remove("is-active");
        layer = next;
        if (heroTrigger) heroTrigger.dataset.lightbox = images[index]; // full-screen view follows the slideshow
      };
      preload.src = images[index];
    }, 6000);
  }

  // Gallery filtering.
  const filters = [...document.querySelectorAll("[data-gallery-filter]")];
  const galleryItems = [...document.querySelectorAll(".gallery-item")];
  filters.forEach((button) => button.addEventListener("click", () => {
    const category = button.dataset.galleryFilter;
    filters.forEach((peer) => {
      const active = peer === button;
      peer.classList.toggle("is-active", active);
      peer.setAttribute("aria-pressed", String(active));
    });
    galleryItems.forEach((item) => {
      item.hidden = category !== "all" && item.dataset.category !== category;
      item.classList.remove("is-entering");
      if (!item.hidden && !reduceMotion) {
        void item.offsetWidth; // restart the entrance animation
        item.classList.add("is-entering");
      }
    });
  }));

  // Full-screen, keyboard-operable lightbox.
  const lightbox = document.querySelector("#lightbox");
  const lightboxImage = lightbox?.querySelector("[data-lightbox-image]");
  const lightboxTitle = lightbox?.querySelector("[data-lightbox-title]");
  const lightboxMeta = lightbox?.querySelector("[data-lightbox-meta]");
  const lightboxTriggers = [...document.querySelectorAll("[data-lightbox]")];
  let currentLightboxIndex = 0;

  const visibleTriggers = () => lightboxTriggers.filter((trigger) => !trigger.closest(".gallery-item")?.hidden);
  const renderLightbox = (trigger) => {
    if (!lightboxImage || !trigger) return;
    lightboxImage.src = trigger.dataset.lightbox;
    lightboxImage.classList.remove("is-swapping");
    void lightboxImage.offsetWidth;
    lightboxImage.classList.add("is-swapping");
    lightboxImage.alt = trigger.dataset.alt || "";
    if (lightboxTitle) lightboxTitle.textContent = trigger.dataset.title || "";
    if (lightboxMeta) lightboxMeta.textContent = trigger.dataset.meta || "";
  };
  const moveLightbox = (direction) => {
    const visible = visibleTriggers();
    if (!visible.length) return;
    currentLightboxIndex = (currentLightboxIndex + direction + visible.length) % visible.length;
    renderLightbox(visible[currentLightboxIndex]);
  };
  lightboxTriggers.forEach((trigger) => trigger.addEventListener("click", () => {
    const visible = visibleTriggers();
    currentLightboxIndex = Math.max(0, visible.indexOf(trigger));
    renderLightbox(trigger);
    lightbox?.showModal();
  }));
  lightbox?.querySelector("[data-lightbox-close]")?.addEventListener("click", () => lightbox.close());
  lightbox?.querySelector("[data-lightbox-prev]")?.addEventListener("click", () => moveLightbox(-1));
  lightbox?.querySelector("[data-lightbox-next]")?.addEventListener("click", () => moveLightbox(1));
  lightbox?.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft") moveLightbox(-1);
    if (event.key === "ArrowRight") moveLightbox(1);
  });

  // Back-to-top control (its visibility follows the shared scroll handler above).
  backTop?.addEventListener("click", () => scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" }));

  // Current year is decorative; historical page dates remain untouched.
  document.querySelectorAll("[data-current-year]").forEach((el) => { el.textContent = new Date().getFullYear(); });

  // Touch zoom: keep the 20% enlargement visible while a finger is down (and briefly after a quick tap).
  const zoomTargets = ".media-frame, .gallery-item button, .photo-card, .hero-media, .trust-image";
  document.addEventListener("pointerdown", (event) => {
    if (event.pointerType === "mouse") return;
    const el = event.target.closest?.(zoomTargets);
    if (!el) return;
    el.classList.add("is-zoomed");
    const done = () => {
      window.setTimeout(() => el.classList.remove("is-zoomed"), 350);
      ["pointerup", "pointercancel", "pointerleave"].forEach((t) => el.removeEventListener(t, done));
    };
    ["pointerup", "pointercancel", "pointerleave"].forEach((t) => el.addEventListener(t, done));
  }, { passive: true });
})();
