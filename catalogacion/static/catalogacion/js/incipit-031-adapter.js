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

    // console.log("[fillFieldsFromPaeCode] paeCode:", paeCode);
    // console.log("[fillFieldsFromPaeCode] parsed:", parsed);

    // Campo 031 $g (Clave) - buscar por name
    const clefInput = document.querySelector('input[name="incipit_g_0"]');
    if (clefInput && parsed.clef) {
      // // console.log("[fillFieldsFromPaeCode] Rellenando clave:", parsed.clef);
      clefInput.value = parsed.clef;
      clefInput.dispatchEvent(new Event("input", { bubbles: true }));
      clefInput.dispatchEvent(new Event("change", { bubbles: true }));
    } else {
      console.warn("[fillFieldsFromPaeCode] No se encontró input clave o valor vacío");
    }

    // Campo 031 $n (Armadura) - buscar por name
    const armaduraInput = document.querySelector('input[name="incipit_n_0"]');
    if (armaduraInput && parsed.armadura) {
      // console.log("[fillFieldsFromPaeCode] Rellenando armadura:", parsed.armadura);
      armaduraInput.value = parsed.armadura;
      armaduraInput.dispatchEvent(new Event("input", { bubbles: true }));
      armaduraInput.dispatchEvent(new Event("change", { bubbles: true }));
    } else {
      console.warn("[fillFieldsFromPaeCode] No se encontró input armadura o valor vacío");
    }

    // Campo 031 $o (Tiempo/Compás) - buscar por name
    const tiempoInput = document.querySelector('input[name="incipit_o_0"]');
    if (tiempoInput && parsed.tiempo) {
      // console.log("[fillFieldsFromPaeCode] Rellenando tiempo:", parsed.tiempo);
      tiempoInput.value = parsed.tiempo;
      tiempoInput.dispatchEvent(new Event("input", { bubbles: true }));
      tiempoInput.dispatchEvent(new Event("change", { bubbles: true }));
    } else {
      console.warn("[fillFieldsFromPaeCode] No se encontró input tiempo o valor vacío");
    }

    // Campo textarea cuerpo $p
    const cuerpoTextarea = document.getElementById("incipit_p_0");
    if (cuerpoTextarea && parsed.cuerpo) {
      // console.log("[fillFieldsFromPaeCode] Rellenando cuerpo:", parsed.cuerpo);
      cuerpoTextarea.value = parsed.cuerpo;
      cuerpoTextarea.dispatchEvent(new Event("input", { bubbles: true }));
      cuerpoTextarea.dispatchEvent(new Event("change", { bubbles: true }));
    } else {
      console.warn("[fillFieldsFromPaeCode] No se encontró textarea cuerpo o valor vacío");
    }

    return parsed;
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
      // console.log("[TransformIncipitToPAEC] Ejecutando wrapper");

      // Ejecutar lógica original del legacy
      originalTransform(context);

      // Leer el PAE que el legacy escribe en #incipitPaec
      var paecInput = document.getElementById("incipitPaec");
      var paeCode = paecInput ? paecInput.value : "";


      // console.log("[TransformIncipitToPAEC] paeCode obtenido:", paeCode);

      // // Copiar al textarea oficial del 031 $p (primer incipit)
      // var textareaP = document.getElementById("incipit_p_0");
      // if (textareaP && typeof paeCode === "string") {
      //   textareaP.value = paeCode;
      // }

      // Rellenar campos 031$g, 031$n, 031$o desde el paeCode
      fillFieldsFromPaeCode(paeCode);
    };
  }


  // 2) Inicializar el canvas del primer incipit una vez cargado el DOM
  document.addEventListener("DOMContentLoaded", function () {
    // console.log("[DOMContentLoaded] Inicializando adapter");

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

    // Configurar botón Parse manual
    var parseBtn = document.getElementById("parse-inc-p0");
    if (parseBtn) {
      // console.log("[DOMContentLoaded] Encontrado botón Parse");
      parseBtn.addEventListener("click", function (e) {
        e.preventDefault();
        console.log("[Parse Button] Clicked");

        // Obtener el valor del textarea $p
        var textareaPae = document.getElementById("incipit_p_0");
        if (textareaPae) {
          var paeCode = textareaPae.value;
          // console.log("[Parse Button] Valor textarea:", paeCode);
          fillFieldsFromPaeCode(paeCode);
        } else {
          console.warn("[Parse Button] No se encontró textarea incipit_p_0");
        }
      });
    } else {
      console.warn("[DOMContentLoaded] No se encontró botón Parse");
    }
  });

  // 3) Exportar función para que sea accesible globalmente (ej. botón Parse manual)
  window.fillFieldsFromPaeCode = fillFieldsFromPaeCode;
  window.parsePaeCode = parsePaeCode;

})();
