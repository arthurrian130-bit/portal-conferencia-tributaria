function warmupModuleLinks() {
  const warmed = new Set();
  const cards = document.querySelectorAll("[data-module-url]");
  cards.forEach((card) => {
    card.addEventListener(
      "mouseenter",
      () => {
        const url = card.getAttribute("data-module-url") || "";
        if (!url || warmed.has(url)) return;
        warmed.add(url);
        try {
          const parsed = new URL(url);
          if (!["http:", "https:"].includes(parsed.protocol)) return;
          const origin = parsed.origin;
          const host = `//${parsed.host}`;

          const preconnect = document.createElement("link");
          preconnect.rel = "preconnect";
          preconnect.href = origin;
          document.head.appendChild(preconnect);

          const dns = document.createElement("link");
          dns.rel = "dns-prefetch";
          dns.href = host;
          document.head.appendChild(dns);

          const prefetch = document.createElement("link");
          prefetch.rel = "prefetch";
          prefetch.href = url;
          document.head.appendChild(prefetch);
        } catch (e) {
          // Ignora URLs invalidas
        }
      },
      { once: true }
    );
  });
}

document.addEventListener("DOMContentLoaded", warmupModuleLinks);
