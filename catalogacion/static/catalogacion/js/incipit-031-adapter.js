// Adapter mínimo entre el formulario Django (031) y el motor incipitManager.js
// Usa el objeto global CanvasIncipit que crea incipitManager.js.

(function () {
  // Verificamos que el legacy se haya cargado
  if (typeof window.CanvasIncipit === "undefined") {
    console.warn("incipit-031-adapter: CanvasIncipit no está disponible");
    return;
  }

  /**
   * Parsea un paeCode (ej: "%G-2 $xFC@2/2'''4D''xE") y extrae:
   * - clef: "G" (desde %G-2 → la letra)
   * - armadura: "xFC" (desde $xFC → todo lo que sigue a $)
   * - tiempo: "2/2" (desde @2/2 → todo lo que sigue a @)
   */
  function parsePaeCode(paeCode) {
    if (!paeCode || typeof paeCode !== "string") {
      return { clef: "", armadura: "", tiempo: "", cuerpo: "" };
    }

    const dollarIndex = paeCode.indexOf("$");
    const atIndex = paeCode.indexOf("@");

    // Extraer clef desde % hasta $ o @
    let clef = "";
    const endForPercent =
      dollarIndex !== -1 && (atIndex === -1 || dollarIndex < atIndex)
        ? dollarIndex
        : atIndex !== -1
        ? atIndex
        : paeCode.length;
    const percentPart = paeCode.slice(0, endForPercent).trim();
    if (percentPart.startsWith("%")) {
      const match = percentPart.match(/%([GCF](?:-[1-5])?)/);
      if (match) clef = match[1]; // G-2 completo
    }

    // Extraer armadura desde $ hasta @
    let armadura = "";
    if (dollarIndex !== -1) {
      const endForDollar =
        atIndex !== -1 && atIndex > dollarIndex ? atIndex : paeCode.length;
      const dollarPart = paeCode.slice(dollarIndex, endForDollar).trim();
      armadura = dollarPart.replace(/^\$/, "").trim(); // Quita $, mantiene el resto (ej: "xFC")
    }

    // Extraer tiempo desde @
    let tiempo = "";
    let cuerpo = "";
    if (atIndex !== -1) {
      const atPart = paeCode.slice(atIndex).trim();
      // atRest = contenido después de @ (sin quitar espacios ni apóstrofes)
      const atRest = atPart.replace(/^@/, "");
      // Extraer solo la cifra de compás (4/4, 2/2, etc.) desde atRest
      const timeMatch = atRest.match(/^(\d+\/\d+)/);
      if (timeMatch) {
        tiempo = timeMatch[1];
        // El cuerpo es todo lo que va DESPUÉS de la cifra de compás en atRest
        cuerpo = atRest.slice(timeMatch[0].length);
      } else {
        // Si no hay compás, todo atRest es cuerpo
        cuerpo = atRest;
      }
    }

    console.log("[parsePaeCode] tiempo:", tiempo, "| cuerpo extraído:", cuerpo);
    return { clef, armadura, tiempo, cuerpo };
  }

  /**
   * Rellena los campos 031$g (clave), 031$n (armadura), 031$o (tiempo)
   * basándose en el paeCode proporcionado.
   */
  function fillFieldsFromPaeCode(paeCode) {
    const parsed = parsePaeCode(paeCode);

    // Campo 031 $g (Clave) - buscar por name
    const clefInput = document.querySelector('input[name="incipit_g_0"]');
    if (clefInput && parsed.clef) {
      clefInput.value = parsed.clef;
      clefInput.dispatchEvent(new Event("input", { bubbles: true }));
      clefInput.dispatchEvent(new Event("change", { bubbles: true }));
    } else {
      console.warn(
        "[fillFieldsFromPaeCode] No se encontró input clave o valor vacío"
      );
    }

    // Campo 031 $n (Armadura) - buscar por name
    const armaduraInput = document.querySelector('input[name="incipit_n_0"]');
    if (armaduraInput && parsed.armadura) {
      armaduraInput.value = parsed.armadura;
      armaduraInput.dispatchEvent(new Event("input", { bubbles: true }));
      armaduraInput.dispatchEvent(new Event("change", { bubbles: true }));
    } else {
      console.warn(
        "[fillFieldsFromPaeCode] No se encontró input armadura o valor vacío"
      );
    }

    // Campo 031 $o (Tiempo/Compás) - buscar por name
    const tiempoInput = document.querySelector('input[name="incipit_o_0"]');
    if (tiempoInput && parsed.tiempo) {
      tiempoInput.value = parsed.tiempo;
      tiempoInput.dispatchEvent(new Event("input", { bubbles: true }));
      tiempoInput.dispatchEvent(new Event("change", { bubbles: true }));
    } else {
      console.warn(
        "[fillFieldsFromPaeCode] No se encontró input tiempo o valor vacío"
      );
    }

    // Campo textarea cuerpo $p
    const cuerpoTextarea = document.getElementById("incipit_p_0");
    if (cuerpoTextarea && parsed.cuerpo) {
      cuerpoTextarea.value = parsed.cuerpo;
      cuerpoTextarea.dispatchEvent(new Event("input", { bubbles: true }));
      cuerpoTextarea.dispatchEvent(new Event("change", { bubbles: true }));
    } else {
      console.warn(
        "[fillFieldsFromPaeCode] No se encontró textarea cuerpo o valor vacío"
      );
    }

    return parsed;
  }

  /**
   * 🆕 NUEVA FUNCIÓN: Actualiza la cabecera del canvas desde los inputs
   * Lee los valores de clave, armadura y tiempo, y actualiza el primer elemento del canvas
   */
  function updateCanvasHeaderFromInputs() {
    console.log("[updateCanvasHeaderFromInputs] Iniciando...");

    // 1. Leer valores de los inputs
    const clefInput = document.getElementById('incipit_g_0');
    const armaduraInput = document.getElementById('incipit_n_0');
    const tiempoInput = document.getElementById('incipit_o_0');

    const clefValue = clefInput ? clefInput.value.trim() : "";
    const armaduraValue = armaduraInput ? armaduraInput.value.trim() : "";
    const tiempoValue = tiempoInput ? tiempoInput.value.trim() : "";

    console.log("[updateCanvasHeaderFromInputs] Valores leídos:", {
      clef: clefValue,
      armadura: armaduraValue,
      tiempo: tiempoValue
    });

    // 2. Validar que al menos la clave esté presente
    if (!clefValue) {
      alert("⚠️ Por favor ingresa al menos la Clave (031$g) antes de aplicar.");
      return;
    }

    // 3. Mapear el valor de clave a nombre interno del legacy
    // Formato input: "G-2", "C-3", "F-4"
    const clefMap = {
      "G-2": "treble",
      "C-3": "alto",
      "F-4": "bass"
    };

    const clefName = clefMap[clefValue];
    if (!clefName) {
      alert(`⚠️ Clave "${clefValue}" no reconocida. Use: G-2, C-3 o F-4`);
      return;
    }

    // 4. Parsear armadura (ej: "xFC" → sostenido con 2 alteraciones: F, C)
    let qtyAlteration = 0;
    let alterationName = "becuadro";

    if (armaduraValue) {
      // Detectar tipo de alteración
      if (armaduraValue.startsWith("x")) {
        alterationName = "sostenido";
        qtyAlteration = armaduraValue.length - 1; // "xFC" → 2 alteraciones
      } else if (armaduraValue.startsWith("b")) {
        alterationName = "bemol";
        qtyAlteration = armaduraValue.length - 1; // "bBE" → 2 alteraciones
      }
    }

    // 5. Mapear tiempo a nombre interno (ej: "2/2" → "tiempo2")
    const timeMap = {
      "4/4": "tiempo1",
      "2/2": "tiempo2",
      "2/4": "tiempo3",
      "3/4": "tiempo4",
      "3/8": "tiempo5",
      "6/8": "tiempo6",
      "9/8": "tiempo7",
      "12/8": "tiempo8",
      "3/2": "tiempo9"
    };

    const timeName = timeMap[tiempoValue] || null;
    const hasTime = !!timeName;

    console.log("[updateCanvasHeaderFromInputs] Valores procesados:", {
      clefName,
      qtyAlteration,
      alterationName,
      hasTime,
      timeName
    });

    // 6. Actualizar el primer elemento del canvas (la clave)
    if (CanvasIncipit.drawIncipitElements.length === 0) {
      alert("⚠️ El canvas no está inicializado correctamente.");
      return;
    }

    const clefElement = CanvasIncipit.drawIncipitElements[0];

    // Obtener datos de la nota de clave desde el legacy
    const clefNote = CanvasIncipit.incipit.getNoteByName(clefName);

    clefElement.noteName = clefName;
    clefElement.yPosition = clefNote.yPosition;
    clefElement.qtyAlteration = qtyAlteration;
    clefElement.alterationName = alterationName;
    clefElement.hasTime = hasTime;
    clefElement.timeName = timeName;

    // 7. Actualizar armadura por defecto del canvas
    CanvasIncipit.setDefaultClefAlt(
      CanvasIncipit,
      clefName,
      qtyAlteration,
      alterationName
    );

    // 8. Redibujar el canvas
    CanvasIncipit.gDrawingContext.clearRect(
      0,
      0,
      CanvasIncipit.gCanvasElement.width,
      CanvasIncipit.gCanvasElement.height
    );
    CanvasIncipit.drawPentagram(CanvasIncipit);

    // 9. Actualizar el campo oculto incipitPaec con la cabecera
    const paecHeader =
      `%${clefValue}` +
      (armaduraValue ? ` $${armaduraValue}` : "") +
      (tiempoValue ? ` @${tiempoValue}` : "");

    const hiddenPaec = document.getElementById("incipitPaec");
    if (hiddenPaec) {
      hiddenPaec.value = paecHeader;
    }

    console.log(
      "[updateCanvasHeaderFromInputs] ✅ Cabecera aplicada:",
      paecHeader
    );

    // Feedback visual opcional
    showFeedback("✓ Cabecera aplicada correctamente");
  }

  /**
   * 🆕 Mostrar feedback temporal al usuario
   */
  function showFeedback(message) {
    const parseBtn = document.getElementById("parse-inc-p0");
    if (!parseBtn) return;

    const originalText = parseBtn.textContent;
    parseBtn.textContent = message;
    parseBtn.style.backgroundColor = "#4CAF50";
    parseBtn.style.color = "white";

    setTimeout(() => {
      parseBtn.textContent = originalText;
      parseBtn.style.backgroundColor = "";
      parseBtn.style.color = "";
    }, 2000);
  }

  // 1) Envolvemos el método TransformIncipitToPAEC del objeto CanvasIncipit
  var originalTransform = CanvasIncipit.TransformIncipitToPAEC
    ? CanvasIncipit.TransformIncipitToPAEC.bind(CanvasIncipit)
    : null;

  if (!originalTransform) {
    console.warn(
      "incipit-031-adapter: CanvasIncipit.TransformIncipitToPAEC no está definido"
    );
  } else {
    CanvasIncipit.TransformIncipitToPAEC = function (context) {
      // Ejecutar lógica original del legacy
      originalTransform(context);

      // Leer el PAE que el legacy escribe en #incipitPaec
      var paecInput = document.getElementById("incipitPaec");
      var paeCode = paecInput ? paecInput.value : "";

      // Rellenar campos 031$g, 031$n, 031$o desde el paeCode
      fillFieldsFromPaeCode(paeCode);
    };
  }

  // 2) Inicializar el canvas del primer incipit una vez cargado el DOM
  document.addEventListener("DOMContentLoaded", function () {
    var canvasEl = document.getElementById("incipit_canvas_0");
    if (!canvasEl) {
      console.warn("incipit-031-adapter: no se encontró #incipit_canvas_0");
      return;
    }

    // Asegurarnos de que existen los hidden con los ids que espera el legacy
    var hiddenPaec = document.getElementById("incipitPaec");

    if (!hiddenPaec) {
      hiddenPaec = document.createElement("input");
      hiddenPaec.type = "hidden";
      hiddenPaec.id = "incipitPaec";
      hiddenPaec.name = "incipit_paec_0";
      canvasEl.parentNode.appendChild(hiddenPaec);
    }

    var hiddenTransp = document.getElementById("incipitTransposition");
    if (!hiddenTransp) {
      hiddenTransp = document.createElement("input");
      hiddenTransp.type = "hidden";
      hiddenTransp.id = "incipitTransposition";
      hiddenTransp.name = "incipit_transp_0";
      canvasEl.parentNode.appendChild(hiddenTransp);
    }

    // Inicializar el canvas del legacy: 'add' = nuevo incipit editable
    // Tercer parámetro = PAE inicial (vacío al crear)
    CanvasIncipit.initializeCanvas("incipit_canvas_0", "add", "");

    // 🆕 Configurar botón Parse con NUEVA funcionalidad
    var parseBtn = document.getElementById("parse-inc-p0");
    if (parseBtn) {
      console.log("[DOMContentLoaded] ✅ Botón Parse encontrado y configurado");

      parseBtn.addEventListener("click", function (e) {
        e.preventDefault();
        console.log("[Parse Button] 🔄 Click detectado");

        // NUEVA FUNCIONALIDAD: Actualizar cabecera desde inputs
        updateCanvasHeaderFromInputs();
      });
    } else {
      console.warn(
        "[DOMContentLoaded] ⚠️ No se encontró botón Parse (#parse-inc-p0)"
      );
    }
  });

  // 3) Exportar funciones para que sean accesibles globalmente
  window.fillFieldsFromPaeCode = fillFieldsFromPaeCode;
  window.parsePaeCode = parsePaeCode;
  window.updateCanvasHeaderFromInputs = updateCanvasHeaderFromInputs; // 🆕 Nueva exportación
})();
