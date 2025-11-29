(function () {
    "use strict";

    const DEFAULT_OPTIONS = {
        minChars: 2,
        debounce: 250,
        allowCreate: true,
        endpoint: null,
        queryParam: "q",
        fetchOptions: {},
        transformResults: (data) => data?.results || [],
        renderItem: null,
        renderCreateItem: null,
        onSelect: null,
        onCreate: null,
        onClear: null,
        hiddenInput: null,
        extraElements: {},
    };

    function setupAutocomplete(userOptions) {
        const opts = Object.assign({}, DEFAULT_OPTIONS, userOptions || {});
        const input = opts.input;
        const suggestions = opts.suggestionsContainer;

        if (!input || !suggestions) {
            console.warn("Autocomplete: input o contenedor no encontrado");
            return null;
        }

        suggestions.classList.remove("is-visible");
        input.setAttribute("autocomplete", "off");

        let debounceTimer = null;
        let currentItems = [];
        let selectedIndex = -1;

        const elements = () => ({
            input,
            hiddenInput: opts.hiddenInput,
            extra: opts.extraElements || {},
        });

        input.addEventListener("input", handleInput);
        input.addEventListener("keydown", handleKeydown);
        document.addEventListener("click", handleDocumentClick);

        function handleInput(e) {
            const query = e.target.value.trim();

            if (query.length < opts.minChars) {
                hideSuggestions();
                if (query.length === 0 && typeof opts.onClear === "function") {
                    opts.onClear(elements());
                }
                return;
            }

            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => search(query), opts.debounce);
        }

        function search(query) {
            const url =
                typeof opts.endpoint === "function"
                    ? opts.endpoint(query)
                    : `${opts.endpoint}?${
                          opts.queryParam || "q"
                      }=${encodeURIComponent(query)}`;

            fetch(url, opts.fetchOptions)
                .then((response) => response.json())
                .then((data) => {
                    currentItems = opts.transformResults(data, query) || [];
                    renderSuggestions(query);
                })
                .catch((error) => {
                    console.error("Autocomplete: error al buscar", error);
                });
        }

        function renderSuggestions(query) {
            suggestions.innerHTML = "";
            selectedIndex = -1;

            const fragment = document.createDocumentFragment();

            currentItems.forEach((item) => {
                const optionEl = document.createElement("div");
                optionEl.className = "autocomplete-item";
                optionEl.innerHTML =
                    typeof opts.renderItem === "function"
                        ? opts.renderItem(item)
                        : defaultRender(item);
                optionEl.addEventListener("click", () => selectItem(item));
                fragment.appendChild(optionEl);
            });

            if (opts.allowCreate && query) {
                const createEl = document.createElement("div");
                createEl.className = "autocomplete-item autocomplete-item-new";
                createEl.innerHTML =
                    typeof opts.renderCreateItem === "function"
                        ? opts.renderCreateItem(query)
                        : defaultCreateRender(query);
                createEl.addEventListener("click", () => handleCreate(query));
                fragment.appendChild(createEl);
            }

            if (!fragment.childNodes.length) {
                hideSuggestions();
                return;
            }

            suggestions.appendChild(fragment);
            suggestions.classList.add("is-visible");
        }

        function handleCreate(query) {
            if (typeof opts.onCreate === "function") {
                opts.onCreate(query, elements());
            } else {
                defaultCreateAction(query, elements());
            }
            hideSuggestions();
        }

        function selectItem(item) {
            if (typeof opts.onSelect === "function") {
                opts.onSelect(item, elements());
            } else {
                defaultSelect(item, elements());
            }
            hideSuggestions();
        }

        function handleKeydown(e) {
            if (!suggestions.classList.contains("is-visible")) return;

            const items = suggestions.querySelectorAll(".autocomplete-item");
            if (!items.length) return;

            switch (e.key) {
                case "ArrowDown":
                    e.preventDefault();
                    selectedIndex = Math.min(
                        selectedIndex + 1,
                        items.length - 1
                    );
                    updateSelection(items);
                    break;
                case "ArrowUp":
                    e.preventDefault();
                    selectedIndex = Math.max(selectedIndex - 1, 0);
                    updateSelection(items);
                    break;
                case "Enter":
                    e.preventDefault();
                    if (selectedIndex >= 0 && items[selectedIndex]) {
                        items[selectedIndex].click();
                    }
                    break;
                case "Escape":
                    hideSuggestions();
                    break;
            }
        }

        function updateSelection(items) {
            items.forEach((item, index) => {
                if (index === selectedIndex) {
                    item.classList.add("selected");
                    item.scrollIntoView({ block: "nearest" });
                } else {
                    item.classList.remove("selected");
                }
            });
        }

        function handleDocumentClick(e) {
            if (input.contains(e.target) || suggestions.contains(e.target)) {
                return;
            }
            hideSuggestions();
        }

        function hideSuggestions() {
            suggestions.classList.remove("is-visible");
            suggestions.innerHTML = "";
            currentItems = [];
            selectedIndex = -1;
        }

        function defaultSelect(item, elements) {
            elements.input.value = item?.label || "";
            if (elements.hiddenInput) {
                elements.hiddenInput.value = item?.id || "";
            }
        }

        function defaultCreateAction(query, elements) {
            elements.input.value = query;
            if (elements.hiddenInput) {
                elements.hiddenInput.value = "";
            }
        }

        function defaultRender(item) {
            return `<strong>${escapeHtml(item?.label || "")}</strong>`;
        }

        function defaultCreateRender(query) {
            return `Crear nuevo: "${escapeHtml(query || "")}"`;
        }

        function escapeHtml(text) {
            const div = document.createElement("div");
            div.textContent = text || "";
            return div.innerHTML;
        }

        return {
            destroy() {
                input.removeEventListener("input", handleInput);
                input.removeEventListener("keydown", handleKeydown);
                document.removeEventListener("click", handleDocumentClick);
            },
            hide: hideSuggestions,
        };
    }

    window.CatalogacionAutocomplete = Object.freeze({
        setup: setupAutocomplete,
    });
})();
