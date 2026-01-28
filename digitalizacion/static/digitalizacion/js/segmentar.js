(function(){
  const input = document.getElementById("obraSearch");
  const hidden = document.getElementById("obraIdHidden");
  const results = document.getElementById("obraResults");

  if (!input || !hidden || !results) return;

  // Obtener IDs de obras ya segmentadas en esta colección
  const segmentedIdsAttr = document.querySelector("[data-segmented-ids]")?.getAttribute("data-segmented-ids") || "";
  const segmentedIds = new Set(
    segmentedIdsAttr.split(",").filter(id => id.trim()).map(id => parseInt(id.trim(), 10))
  );

  let timer = null;

  // Evitar que Enter haga submit
  input.addEventListener("keydown", function(e) {
    if (e.key === "Enter") e.preventDefault();
  });

  // Buscar cuando cambia el valor
  input.addEventListener("input", function() {
    const q = this.value.trim();
    hidden.value = "";

    if (timer) clearTimeout(timer);

    if (q.length < 2) {
      results.style.display = "none";
      results.innerHTML = "";
      return;
    }

    timer = setTimeout(() => {
      const coleccionId = document
        .querySelector("[data-coleccion-id]")
        ?.getAttribute("data-coleccion-id");
      const apiUrl = `/digitalizacion/api/buscar-obras/?q=${encodeURIComponent(
        q
      )}&coleccion_id=${encodeURIComponent(coleccionId || "")}`;


      fetch(apiUrl)
        .then(r => r.json())
        .then(data => {
          results.innerHTML = "";
          const list = data.results || [];

          if (!list.length) {
            results.style.display = "none";
            return;
          }

          list.forEach(o => {
            const btn = document.createElement("button");
            btn.type = "button";

            const isSegmented = segmentedIds.has(o.id);

            if (isSegmented) {
              btn.className = "list-group-item list-group-item-action d-flex justify-content-between align-items-center";
              btn.innerHTML = `
                <span>${o.label}</span>
                <span class="badge bg-success">Ya asignado</span>
              `;
            } else {
              btn.className = "list-group-item list-group-item-action";
              btn.textContent = o.label;
            }

            btn.addEventListener("click", () => {
              hidden.value = o.id;
              input.value = o.label;
              results.style.display = "none";
              results.innerHTML = "";
            });

            results.appendChild(btn);
          });

          results.style.display = "block";
        })
        .catch(() => {
          results.style.display = "none";
          results.innerHTML = "";
        });
    }, 250);
  });
})();
