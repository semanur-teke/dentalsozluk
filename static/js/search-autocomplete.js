document.addEventListener("DOMContentLoaded", () => {
  const form  = document.querySelector(".navbar-search");
  if (!form) return;

  const input = form.querySelector("#search-input");
  if (!input) return;

  const ENDPOINT = form.dataset.endpoint || "/autocomplete/";
  let t = null, idx = -1;

  // Öneri kutusu
  let box = document.getElementById("suggestions-box");
  if (!box) {
    box = document.createElement("div");
    box.id = "suggestions-box";
    form.style.position = "relative";
    form.appendChild(box);
  }

  // DEĞİŞİKLİK 1: Artık [{title, url}] bekliyoruz
  const fetchSuggest = (q) =>
    fetch(ENDPOINT + "?q=" + encodeURIComponent(q))
      .then(r => {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      });

  // DEĞİŞİKLİK 2: Tıklayınca direkt detay sayfasına git
  const render = (items) => {
    box.innerHTML = "";
    idx = -1;
    if (!items || !items.length) { box.style.display = "none"; return; }

    items.forEach((it) => {
      // backend güvenliği: string dönerse eski davranışla devam
      const title = typeof it === "string" ? it : (it.title || "");
      const url   = (it && it.url) ? it.url : null;

      const div = document.createElement("div");
      div.className = "item";
      div.textContent = title;

      // mousedown, form submit’ten önce yakalar
      div.addEventListener("mousedown", (e) => {
        e.preventDefault();
        if (url) {
          window.location.href = url;   // ← doğrudan detaya
        } else {
          input.value = title;          // yedek davranış
          box.style.display = "none";
          form.submit();
        }
      });

      box.appendChild(div);
    });

    box.style.display = "block";
  };

  input.addEventListener("input", () => {
    const q = input.value.trim();
    if (q.length < 2) { box.style.display = "none"; return; }
    clearTimeout(t);
    t = setTimeout(() => {
      fetchSuggest(q).then(render).catch(() => { box.style.display = "none"; });
    }, 150);
  });

  // Enter seçiliyken aynı yönlendirme
  input.addEventListener("keydown", (e) => {
    const items = Array.from(box.querySelectorAll(".item"));
    if (!items.length) return;

    if (e.key === "ArrowDown") { e.preventDefault(); idx = (idx + 1) % items.length; }
    else if (e.key === "ArrowUp") { e.preventDefault(); idx = (idx - 1 + items.length) % items.length; }
    else if (e.key === "Enter" && idx > -1) {
      e.preventDefault();
      items[idx].dispatchEvent(new MouseEvent("mousedown"));
      return;
    } else if (e.key === "Escape") {
      box.style.display = "none"; return;
    }

    items.forEach(el => el.classList.remove("active"));
    if (idx > -1) items[idx].classList.add("active");
  });

  document.addEventListener("click", (e) => {
    if (!form.contains(e.target)) box.style.display = "none";
  });
});
