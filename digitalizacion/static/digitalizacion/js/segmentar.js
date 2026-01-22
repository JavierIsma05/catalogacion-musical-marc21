(function(){
  const input = document.getElementById("obraSearch");
  const hidden = document.getElementById("obraIdHidden");
  const results = document.getElementById("obraResults");
  console.log("SEGMENTAR JS CARGADO ✅");

  if (!input || !hidden || !results) return;

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
            btn.className = "list-group-item list-group-item-action";
            btn.textContent = o.label;

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
