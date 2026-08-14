import argparse
import os
import subprocess
import sys
import time
from playwright.sync_api import sync_playwright

# Directorio local para guardar la sesión del usuario que ejecute el script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DATA_DIR = os.path.join(BASE_DIR, "user_data")


def asegurar_instalacion_playwright():
    """Garantiza que el navegador Chromium esté instalado en la máquina objetivo."""
    try:
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as e:
        print(f"Aviso al verificar binarios de Playwright: {e}")


def desactivar_mic_camara(page):
    """Intenta desactivar micrófono y cámara por atajo de teclado, con fallback por selectores."""
    print("Intentando desactivar micrófono y cámara...")

    try:
        page.bring_to_front()
        time.sleep(0.5)

        page.keyboard.press("ControlOrMeta+d")
        time.sleep(0.5)
        page.keyboard.press("ControlOrMeta+e")
        time.sleep(0.5)

        print("Atajos de teclado enviados.")
    except Exception as e:
        print(f"Aviso: no se pudieron enviar los atajos de teclado: {e}")

    selectores_mic = (
        '[aria-label="Desactivar micrófono"], '
        '[aria-label="Turn off microphone"], '
        '[aria-label="Micrófono activado"], '
        '[aria-label="Microphone is on"]'
    )
    selectores_cam = (
        '[aria-label="Desactivar cámara"], '
        '[aria-label="Turn off camera"], '
        '[aria-label="Cámara activada"], '
        '[aria-label="Camera is on"]'
    )

    for selector in selectores_mic.split(", "):
        btn = page.locator(selector)
        if btn.count() > 0:
            try:
                btn.first.click()
                print("Micrófono desactivado.")
                break
            except Exception:
                pass

    for selector in selectores_cam.split(", "):
        btn = page.locator(selector)
        if btn.count() > 0:
            try:
                btn.first.click()
                print("Cámara desactivada.")
                break
            except Exception:
                pass


def entrar_a_meet(url: str):
    asegurar_instalacion_playwright()

    with sync_playwright() as p:
        print("Lanzando navegador...")

        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            args=[
                "--use-fake-ui-for-media-stream",
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ],
        )

        page = context.pages[0] if context.pages else context.new_page()

        print(f"Navegando a {url}...")
        page.goto(url)

        try:
            page.wait_for_url("https://meet.google.com/*", timeout=30000)
            print("Página cargada con éxito.")

            time.sleep(3)

            desactivar_mic_camara(page)

            selector_unirse = (
                'button:has-text("Unirse ahora"), '
                'button:has-text("Solicitar unirse"), '
                'button:has-text("Join now"), '
                'button:has-text("Ask to join")'
            )

            print("Buscando botón para ingresar...")
            btn = page.wait_for_selector(selector_unirse, timeout=10000)

            if btn and btn.is_visible():
                btn.click()
                print("¡Unido a la reunión correctamente!")
            else:
                print(
                    "No se encontró el botón de unión directa. Verifica si requerís iniciar sesión."
                )

        except Exception as e:
            print(f"Estado de la ejecución: {e}")

        print("\nReunión activa. Presioná Ctrl+C para finalizar.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Cerrando sesión...")
            context.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Bot automatizado para unirse a llamadas de Google Meet."
    )
    parser.add_argument(
        "--url",
        type=str,
        default="https://meet.google.com/iqa-uqhn-wzg",
        help="Enlace completo de la reunión de Google Meet.",
    )

    args = parser.parse_args()
    entrar_a_meet(args.url)
