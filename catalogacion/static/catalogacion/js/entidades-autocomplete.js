document.addEventListener("input", function (e) {
    const input = e.target.closest(".entidad-autocomplete");
    if (!input) return;

    const row = input.closest(".formset-row");
    const hiddenId = row.querySelector('input[type="hidden"]');
    const suggestions = row.querySelector(".autocomplete-list");

    const query = input.value.trim();
    hiddenId.value = "";

    if (query.length < 2) {
        suggestions.innerHTML = "";
        suggestions.classList.remove("show");
        return;
    }

    fetch(`/catalogacion/api/autocompletar/entidad/?q=${encodeURIComponent(query)}`)
        .then(r => r.json())
        .then(data => {
            suggestions.innerHTML = "";

            data.results.forEach(ent => {
                const div = document.createElement("div");
                div.className = "autocomplete-item";
                div.innerHTML = ent.text;
                div.addEventListener("click", () => {
                    input.value = ent.text;
                    hiddenId.value = ent.id;
                    suggestions.innerHTML = "";
                    suggestions.classList.remove("show");
                });
                suggestions.appendChild(div);
            });

            // Crear NUEVA si no existe
            const newOption = document.createElement("div");
            newOption.className = "autocomplete-item new-item";
            newOption.innerHTML = `<strong>+ Crear nuevo:</strong> "${query}"`;
            newOption.addEventListener("click", () => {
                input.value = query;
                hiddenId.value = "";
                suggestions.innerHTML = "";
                suggestions.classList.remove("show");
            });
            suggestions.appendChild(newOption);

            suggestions.classList.add("show");
        });
});

// Ocultar listas al hacer clic afuera
document.addEventListener("click", function(e) {
    if (!e.target.closest(".entidad-autocomplete")) {
        document.querySelectorAll(".autocomplete-list.show")
            .forEach(el => el.classList.remove("show"));
    }
});
