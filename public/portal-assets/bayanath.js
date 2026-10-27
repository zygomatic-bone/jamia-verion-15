/* Bayanath page: renders the cached list of latest YouTube videos (data/bayanath-videos.json).
   Cards are plain links to YouTube (they work without JavaScript). A click swaps that one card for a YouTube player,
   so only a video the visitor chose is ever loaded. */
(() => {
  "use strict";
  const root = document.querySelector("[data-bayanath]");
  if (!root) return;
  const grid = root.querySelector(".by-grid");
  const status = root.querySelector(".by-status");
  const meta = root.querySelector(".by-meta");
  const ID = /^[A-Za-z0-9_-]{11}$/;
  const channelUrl = root.dataset.channel;
  // The speaker: every video comes from the speaker's official channel, so by default it is attributed to him (name and profile link are on the
  // container). data/bayanath-speakers.json lists exceptions: {"<video id>": "Another Speaker"} prints that name (not linked) and
  // {"<video id>": false} prints no speaker. The static copy of the cards in the HTML (tools/refresh_bayanath_static.py) follows the same rules.
  const speakerName = root.dataset.speaker || "";
  const speakerUrl = /^[A-Za-z0-9_.-]+\.html$/.test(root.dataset.speakerUrl || "") ? root.dataset.speakerUrl : "";
  let exceptions = {};

  // The feed's titles often start with an emoji and end with a run of hashtags (the last one sometimes cut short by YouTube). The card shows the
  // title without them; the link, its tooltip and the screen-reader label keep the full original title, and the video itself is untouched.
  const LEAD = (() => {
    try { return new RegExp("^[\\p{Extended_Pictographic}\\uFE0F\\u200D\\s]+", "u"); }
    catch (e) { return /^[\s\uD800-\uDFFF\u2600-\u27BF\uFE0F\u200D]+/; }
  })();
  const TAGS = /(?:\s*#[^\s#]*)+\s*(?:\.{3}|\u2026)?$/;
  const clean = (t) => {
    const c = String(t).replace(/\s+/g, " ").trim().replace(TAGS, "").replace(LEAD, "").trim();
    return c || String(t).trim();
  };

  const fmt = (iso) => {
    if (!iso) return "";
    const d = new Date(iso);
    return isNaN(d) ? "" : d.toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
  };
  const el = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  };
  const setStatus = (msg, withLink) => {
    status.hidden = !msg;
    status.textContent = msg || "";
    if (msg && withLink) {
      status.append(" ");
      const a = el("a", "", "Open the YouTube channel");
      a.href = channelUrl; a.target = "_blank"; a.rel = "noopener";
      status.append(a, ".");
    }
  };

  const play = (card, v) => {
    const frame = el("div", "by-player");
    const iframe = document.createElement("iframe");
    iframe.src = "https://www.youtube-nocookie.com/embed/" + v.id + "?autoplay=1&rel=0";
    iframe.title = v.title;
    iframe.allow = "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; fullscreen";
    iframe.allowFullscreen = true;
    iframe.referrerPolicy = "strict-origin-when-cross-origin";
    frame.append(iframe);
    const thumbLink = card.querySelector(".by-thumb");
    thumbLink.replaceWith(frame);
    card.classList.add("is-playing");
    iframe.focus();
  };

  const thumbnailUrls = (v) => {
    const canonical = "https://i.ytimg.com/vi/" + v.id + "/hqdefault.jpg";
    const approved = typeof v.thumbnail === "string"
      && /^https:\/\/(?:i\d?\.ytimg\.com|img\.youtube\.com)\//.test(v.thumbnail)
      && v.thumbnail.includes("/" + v.id + "/") ? v.thumbnail : "";
    return [...new Set([approved, canonical].filter(Boolean))];
  };

  const card = (v) => {
    const watch = "https://www.youtube.com/watch?v=" + v.id;
    const li = el("li", "by-card");
    const a = el("a", "by-thumb");
    a.href = watch; a.target = "_blank"; a.rel = "noopener";
    a.setAttribute("aria-label", "Play: " + clean(v.title));
    const img = new Image();
    img.alt = "Thumbnail for " + clean(v.title);
    img.loading = "lazy"; img.decoding = "async"; img.width = 480; img.height = 360;
    img.referrerPolicy = "no-referrer";
    const sources = thumbnailUrls(v);
    img.src = sources.shift();
    img.addEventListener("error", () => {
      const next = sources.shift();
      if (next) img.src = next;
      else { img.remove(); a.classList.add("no-thumb"); }
    });
    const icon = el("span", "by-play");
    icon.setAttribute("aria-hidden", "true");
    a.append(img, icon);
    a.addEventListener("click", (e) => {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return; // let "open in new tab" work normally
      e.preventDefault();
      play(li, v);
    });
    const body = el("div", "by-body");
    const h = el("h3");
    const titleLink = el("a", "by-title", clean(v.title));
    if (clean(v.title) !== v.title) titleLink.title = v.title;
    titleLink.href = watch; titleLink.target = "_blank"; titleLink.rel = "noopener";
    h.append(titleLink);
    const yt = el("a", "by-yt", "Watch on YouTube ↗");
    yt.href = watch; yt.target = "_blank"; yt.rel = "noopener";
    body.append(h);
    const who = Object.prototype.hasOwnProperty.call(exceptions, v.id) ? exceptions[v.id] : speakerName;
    if (typeof who === "string" && who) {
      const sp = el("p", "by-speaker");
      sp.append(el("span", "by-speaker-l", "Speaker:"), " ");
      if (who === speakerName && speakerUrl) {
        const a = el("a", "by-speaker-name", who);
        a.href = speakerUrl;
        sp.append(a);
      } else {
        sp.append(el("span", "by-speaker-name", who));
      }
      body.append(sp);
    }
    if (fmt(v.published)) {
      const d = el("time", "by-date", fmt(v.published));
      d.dateTime = v.published;
      body.append(d);
    }
    body.append(yt);
    li.append(a, body);
    return li;
  };

  // the exceptions file is optional: if it is missing or invalid, every video keeps the default attribution
  const loadExceptions = () => (root.dataset.speakers
    ? fetch(root.dataset.speakers, { cache: "no-cache" })
        .then((r) => (r.ok ? r.json() : {}))
        .then((d) => (d && typeof d === "object" && !Array.isArray(d) ? d : {}))
        .catch(() => ({}))
    : Promise.resolve({}));

  Promise.all([
    fetch(root.dataset.src, { cache: "no-cache" }).then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); }),
    loadExceptions(),
  ])
    .then(([data, ex]) => {
      exceptions = {};
      Object.keys(ex).forEach((k) => { if (ID.test(k)) exceptions[k] = ex[k]; });
      const vids = (Array.isArray(data.videos) ? data.videos : [])
        .filter((v) => v && ID.test(v.id) && typeof v.title === "string" && v.title)
        .sort((a, b) => {
          const ad = Date.parse(a.published || ""), bd = Date.parse(b.published || "");
          if (Number.isFinite(ad) && Number.isFinite(bd)) return bd - ad;
          if (Number.isFinite(bd)) return 1;
          if (Number.isFinite(ad)) return -1;
          return 0; // Cache order is the verified channel order when exact dates are unavailable.
        })
        .slice(0, 10);
      grid.setAttribute("aria-busy", "false");
      grid.replaceChildren(...vids.map(card));
      if (!vids.length) return setStatus("The latest Bayanath videos will appear here shortly.", true);
      setStatus("");
      if (meta && data.updated) meta.textContent = "List last refreshed " + fmt(data.updated) + ".";
    })
    .catch(() => {
      grid.setAttribute("aria-busy", "false");
      // the page already carries the last saved list as plain HTML: keep it when the fresh copy cannot be read
      if (grid.children.length) return;
      grid.replaceChildren();
      setStatus("The video list could not be loaded right now.", true);
    });
})();
