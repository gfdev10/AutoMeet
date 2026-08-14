from __future__ import annotations

import argparse
import logging
import subprocess
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# ---------------------------------------------------------------------------
# Configuración general
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
USER_DATA_DIR = BASE_DIR / "user_data"
DEFAULT_MEET_URL = "https://meet.google.com/iqa-uqhn-wzg"
TIMEOUT_NAVEGACION = 30_000
TIMEOUT_BOTON = 10_000
DELAY_POST_CARGA = 3
DELAY_ATAJO = 0.5
DELAY_CLICK_FOCO = 1
DELAY_ATAJO_POST_FOCO = 0.5

SELECTORES_UNION = (
    'button:has-text("Unirse ahora")',
    'button:has-text("Solicitar unirse")',
    'button:has-text("Join now")',
    'button:has-text("Ask to join")',
)

SELECTORES_MIC_APAGADO = (
    '[aria-label="Desactivar micrófono"]',
    '[aria-label="Turn off microphone"]',
    '[aria-label="Micrófono activado"]',
    '[aria-label="Microphone is on"]',
)

SELECTORES_CAM_APAGADO = (
    '[aria-label="Desactivar cámara"]',
    '[aria-label="Turn off camera"]',
    '[aria-label="Cámara activada"]',
    '[aria-label="Camera is on"]',
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def asegurar_playwright() -> None:
    """Instala Chromium si no está presente."""
    logger.info("Verificando binarios de Playwright / Chromium...")
    try:
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        logger.warning("No se pudo verificar la instalación de Playwright: %s", exc)


def _clickear_si_existe(page: "Page", selectores: tuple[str, ...], nombre: str) -> None:
    """Busca el primer selector visible y hace clic."""
    for selector in selectores:
        loc = page.locator(selector)
        if loc.count() > 0:
            try:
                loc.first.click()
                logger.info("%s desactivado/a.", nombre)
                return
            except Exception as exc:
                logger.debug("Fallo al clicar %s: %s", selector, exc)


def desactivar_mic_y_camara(page: "Page") -> None:
    """Desactiva micrófono y cámara por atajo de teclado con fallback por UI."""
    logger.info("Desactivando micrófono y cámara...")

    try:
        page.bring_to_front()
        time.sleep(DELAY_CLICK_FOCO)

        page.keyboard.press("ControlOrMeta+d")
        time.sleep(DELAY_ATAJO_POST_FOCO)
        page.keyboard.press("ControlOrMeta+e")
        time.sleep(DELAY_ATAJO_POST_FOCO)

        logger.info("Atajos de teclado enviados.")
    except Exception as exc:
        logger.warning("No se pudieron enviar atajos de teclado: %s", exc)

    _clickear_si_existe(page, SELECTORES_MIC_APAGADO, "Micrófono")
    _clickear_si_existe(page, SELECTORES_CAM_APAGADO, "Cámara")


# ---------------------------------------------------------------------------
# Flujo principal
# ---------------------------------------------------------------------------
def unirse_a_reunion(url: str) -> None:
    asegurar_playwright()

    with sync_playwright() as playwright:
        logger.info("Lanzando navegador...")
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR),
            headless=False,
            args=[
                "--use-fake-ui-for-media-stream",
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ],
        )

        page = context.pages[0] if context.pages else context.new_page()

        logger.info("Navegando a %s...", url)
        page.goto(url)

        try:
            logger.info("Esperando carga de Meet...")
            page.wait_for_url("https://meet.google.com/*", timeout=TIMEOUT_NAVEGACION)
            logger.info("Página de Meet cargada.")

            time.sleep(DELAY_POST_CARGA)
            desactivar_mic_y_camara(page)

            logger.info("Buscando botón de unión...")
            boton = page.wait_for_selector(
                ", ".join(SELECTORES_UNION), timeout=TIMEOUT_BOTON
            )

            if boton and boton.is_visible():
                boton.click()
                logger.info("¡Unido a la reunión correctamente!")
            else:
                logger.warning(
                    "No se encontró botón de unión directa. "
                    "Verificá si hace falta iniciar sesión."
                )

        except PlaywrightTimeout:
            logger.error("Timeout esperando elementos de Meet.")
        except Exception as exc:
            logger.error("Error en la ejecución: %s", exc)

        logger.info("Reunión activa. Presioná Ctrl+C para finalizar.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Cerrando sesión...")
        finally:
            context.close()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Bot automatizado para unirse a llamadas de Google Meet.",
    )
    parser.add_argument(
        "--url",
        type=str,
        default=DEFAULT_MEET_URL,
        help="Enlace completo de la reunión de Google Meet.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    unirse_a_reunion(args.url)


if __name__ == "__main__":
    main()
