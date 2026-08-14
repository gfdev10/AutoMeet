# AutoMeet

Bot automatizado para unirse a llamadas de Google Meet con Playwright. Instala Chromium automáticamente, silencia micrófono y cámara, y mantiene la sesión de forma persistente.

## Requisitos

- Python 3.10 o superior
- pip
- Conexión a internet

## Instalación

```bash
git clone <URL_DEL_REPO>
cd AutoMeet

python -m venv venv
venv\Scripts\activate  # En Windows
# source venv/bin/activate  # En Linux/macOS

pip install -r requirements.txt
```

## Uso

```bash
python main.py --url https://meet.google.com/abc-defg-hij
```

Si no pasas `--url`, usa el link por defecto definido en el script.

El script abre el navegador, navega al Meet, silencia micrófono y cámara, y busca el botón de unión. Para cerrar la reunión, presioná `Ctrl+C`.

## Notas

- La carpeta `user_data/` se ignora por seguridad. No subas tus cookies ni datos de sesión.
- Si falla la instalación de Chromium, ejecutá manualmente: `playwright install chromium`.
- Las flags `--use-fake-ui-for-media-stream` y `--disable-blink-features=AutomationControlled` ayudan a evitar diálogos y detección de automatización.
- El script intenta desactivar micrófono y cámara primero por atajos de teclado (`ControlOrMeta+d` y `ControlOrMeta+e`) y luego por selectores en la interfaz, por si los atajos no funcionan.
