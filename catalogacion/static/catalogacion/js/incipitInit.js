/**
 * ============================================
 * incipitInit.js
 * Script global para inicializar canvas de incipits
 * Requiere: incipitManager.js cargado previamente
 * ============================================
 */

(function () {
  "use strict";

  /**
   * Configuración global
   */
  const IncipitConfig = {
    fontFamily: "Maestro",
    canvasSelector: "canvas.incipit-view-canvas[data-paec-json-id]",
    debug: false // Cambiar a true para ver logs detallados
  };

  /**
   * Logger condicional
   */
  const log = {
    info: (...args) =>
      IncipitConfig.debug && console.log("🎵 [INCIPIT]", ...args),
    warn: (...args) => console.warn("⚠️ [INCIPIT]", ...args),
    error: (...args) => console.error("❌ [INCIPIT]", ...args),
    success: (...args) =>
      IncipitConfig.debug && console.log("✅ [INCIPIT]", ...args)
  };

  /**
   * Espera a que la fuente Maestro esté cargada
   */
  async function waitForFont() {
    try {
      if (document.fonts && document.fonts.load) {
        log.info("Cargando fuente Maestro...");
        await document.fonts.load(`16px "${IncipitConfig.fontFamily}"`);
        await document.fonts.ready;
        log.success("Fuente Maestro cargada");
        return true;
      }
    } catch (e) {
      log.warn("Error al cargar fuente:", e);
    }
    return false;
  }

  /**
   * Verifica que CanvasIncipit esté disponible
   */
  function checkCanvasIncipit() {
    if (typeof CanvasIncipit === "undefined") {
      log.error(
        "CanvasIncipit no está definido. Verifica que incipitManager.js esté cargado."
      );
      return false;
    }
    log.success("CanvasIncipit disponible");
    return true;
  }

  /**
   * Obtiene el PAEC desde el script JSON
   */
  function getPaecFromScript(jsonId) {
    const scriptElement = document.getElementById(jsonId);

    if (!scriptElement) {
      log.error(`No se encontró script con id="${jsonId}"`);
      return null;
    }

    const rawContent =
      scriptElement.textContent || scriptElement.innerText || "";

    if (!rawContent || rawContent.trim() === "") {
      log.error(`El script "${jsonId}" está vacío`);
      return null;
    }

    // Intentar parsear como JSON primero
    try {
      return JSON.parse(rawContent);
    } catch (e) {
      // Si no es JSON válido, usar como string directo
      return rawContent.trim();
    }
  }

  /**
   * Valida el formato PAEC básico
   */
  function validatePaec(paec) {
    if (!paec) {
      return { valid: false, error: "PAEC vacío" };
    }

    if (!paec.includes("%")) {
      return {
        valid: false,
        warning: "PAEC no contiene clave (%). Esto puede causar errores."
      };
    }

    return { valid: true };
  }

  /**
   * Muestra error en el canvas
   */
  function showCanvasError(canvas, message) {
    try {
      const ctx = canvas.getContext("2d");
      ctx.fillStyle = "#dc3545";
      ctx.font = "14px Arial";
      ctx.textAlign = "center";
      ctx.fillText(
        "Error al renderizar íncipit",
        canvas.width / 2,
        canvas.height / 2 - 10
      );
      ctx.font = "12px Arial";
      ctx.fillStyle = "#666";
      ctx.fillText(message, canvas.width / 2, canvas.height / 2 + 10);
    } catch (e) {
      log.error("No se pudo mostrar error en canvas:", e);
    }
  }

  /**
   * Renderiza un canvas individual
   */
  function renderCanvas(canvas, index, total) {
    const canvasId = canvas.id;
    const jsonId = canvas.dataset.paecJsonId;

    log.info(`\n--- Canvas ${index + 1}/${total} ---`);
    log.info(`Canvas ID: ${canvasId}`);
    log.info(`JSON ID: ${jsonId}`);

    try {
      // Obtener PAEC
      const paecFull = getPaecFromScript(jsonId);

      if (!paecFull) {
        throw new Error("No se pudo obtener PAEC");
      }

      log.info(
        `PAEC: ${paecFull.substring(0, 80)}${paecFull.length > 80 ? "..." : ""}`
      );

      // Validar PAEC
      const validation = validatePaec(paecFull);
      if (!validation.valid) {
        throw new Error(validation.error);
      }
      if (validation.warning) {
        log.warn(`[${canvasId}] ${validation.warning}`);
      }

      // Crear nueva instancia de CanvasClass para cada canvas
      const canvasInstance = new CanvasClass();
      canvasInstance.initializeCanvas(canvasId, "list", paecFull);

      log.success(`[${canvasId}] Canvas renderizado correctamente`);
      return true;
    } catch (error) {
      log.error(`[${canvasId}] Error al renderizar:`, error.message);
      log.error("Stack:", error.stack);
      showCanvasError(canvas, error.message);
      return false;
    }
  }

  /**
   * Inicializa todos los canvas de incipits en la página
   */
  async function initializeAllIncipits() {
    log.info("Iniciando carga de incipits musicales...");

    // Esperar fuente
    await waitForFont();

    // Verificar CanvasIncipit
    if (!checkCanvasIncipit()) {
      return;
    }

    // Buscar todos los canvas
    const canvases = document.querySelectorAll(IncipitConfig.canvasSelector);
    log.info(`Canvas encontrados: ${canvases.length}`);

    if (canvases.length === 0) {
      log.warn("No se encontraron canvas para renderizar");
      return;
    }

    // Renderizar cada canvas
    let successCount = 0;
    let errorCount = 0;

    canvases.forEach((canvas, index) => {
      const success = renderCanvas(canvas, index, canvases.length);
      if (success) {
        successCount++;
      } else {
        errorCount++;
      }
    });

    // Resumen
    log.info("\n=================================");
    log.info("Proceso completado");
    log.success(`Exitosos: ${successCount}`);
    if (errorCount > 0) {
      log.error(`Errores: ${errorCount}`);
    }
    log.info("=================================\n");
  }

  /**
   * Función pública para refrescar un canvas específico
   */
  window.refreshIncipitCanvas = function (canvasId) {
    log.info(`Refrescando canvas: ${canvasId}`);

    const canvas = document.getElementById(canvasId);
    if (!canvas) {
      log.error(`No se encontró canvas con id="${canvasId}"`);
      return false;
    }

    const jsonId = canvas.dataset.paecJsonId;
    if (!jsonId) {
      log.error("Canvas no tiene data-paec-json-id");
      return false;
    }

    const paecFull = getPaecFromScript(jsonId);
    if (!paecFull) {
      return false;
    }

    try {
      const canvasInstance = new CanvasClass();
      canvasInstance.initializeCanvas(canvasId, "list", paecFull);
      log.success("Canvas refrescado correctamente");
      return true;
    } catch (error) {
      log.error("Error al refrescar:", error);
      return false;
    }
  };

  /**
   * Función pública de depuración
   */
  window.debugIncipits = function () {
    console.log("\n========== DEBUG INCIPITS ==========");

    // Verificar CanvasIncipit
    console.log(
      "1. CanvasIncipit definido:",
      typeof CanvasIncipit !== "undefined"
    );

    // Verificar fuente Maestro
    if (document.fonts && document.fonts.check) {
      const maestroLoaded = document.fonts.check(
        `16px ${IncipitConfig.fontFamily}`
      );
      console.log("2. Fuente Maestro cargada:", maestroLoaded);
    }

    // Listar canvas
    const canvases = document.querySelectorAll("canvas.incipit-view-canvas");
    console.log("3. Canvas encontrados:", canvases.length);

    canvases.forEach((canvas, i) => {
      const jsonId = canvas.dataset.paecJsonId;
      const scriptEl = jsonId ? document.getElementById(jsonId) : null;
      const paecContent = scriptEl
        ? scriptEl.textContent.substring(0, 80)
        : "NO SCRIPT";

      console.log(`\n   Canvas ${i + 1}:`);
      console.log(`   - ID: ${canvas.id}`);
      console.log(`   - JSON ID: ${jsonId || "NO DATA-PAEC-JSON-ID"}`);
      console.log(`   - Script existe: ${!!scriptEl}`);
      console.log(`   - PAEC: ${paecContent}...`);
    });

    console.log("\n====================================\n");
  };

  /**
   * Función para habilitar/deshabilitar debug
   */
  window.toggleIncipitDebug = function (enabled) {
    IncipitConfig.debug = enabled;
    console.log(
      `Debug de incipits ${enabled ? "habilitado" : "deshabilitado"}`
    );
  };

  /**
   * Inicialización automática cuando el DOM está listo
   */
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeAllIncipits);
  } else {
    // DOM ya está listo
    initializeAllIncipits();
  }

  // Exportar para uso manual si es necesario
  window.initializeAllIncipits = initializeAllIncipits;
})();
