# AutoMeet

Bot automatizado para unirse a llamadas de Google Meet utilizando Playwright. Instala Chromium automáticamente, silencia micrófono y cámara, y mantiene la sesión del navegador de forma persistente.

## Requisitos

- Python 3.10 o superior
- pip
- Conexión a internet

## Instalación

```bash
git clone <https://github.com/gfdev10/AutoMeet>
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

Si no pasas `--url`, se utiliza el link por defecto definido en el script.

El script abre el navegador, navega al Meet, silencia micrófono y cámara, y busca el botón de unión. Para cerrar la reunión, presioná `Ctrl+C`.

## Características

- **Instalación automática de Chromium**: ejecuta `playwright install chromium` en la primera ejecución.
- **Perfil de usuario persistente**: guarda la sesión en `user_data/` (ignorado por Git).
- **Silenciar micrófono y cámara**: envía atajos de teclado (`ControlOrMeta+D`, `ControlOrMeta+E`) con fallback por interfaz gráfica.
- **Selectores multilenguaje**: soporta interfaces de Meet en español e inglés.
- **Configuración centralizada**: timeouts, demoras y selectores se definen como constantes al inicio del script.
- **Logs estructurados**: mensajes con timestamp y nivel de severidad en lugar de prints simples.

## Estructura del proyecto

```
AutoMeet/
├── main.py            # Entrypoint y lógica principal
├── requirements.txt   # Dependencias
├── .gitignore         # Ignora user_data/ y .env
└── README.md          # Este archivo
```

## Notas de mantenimiento

- Los timeouts, demoras y selectores están definidos como constantes en el bloque superior de `main.py`.
- La lógica está dividida en funciones pequeñas: `asegurar_playwright`, `desactivar_mic_y_camara`, `_clickear_si_existe`, `unirse_a_reunion` y `main`.
- Para agregar funcionalidades, extendé el bloque de constantes o creá una nueva función llamada desde `unirse_a_reunion`.
- Los argumentos de CLI se definen en `build_parser()` para facilitar futuras extensiones.

## Solución de problemas

- Si Chromium no se instala automáticamente, ejecutá manualmente: `playwright install chromium`
- Si no se encuentra el botón de unión, asegurate de haber iniciado sesión o revisá el formato del enlace de Meet.
- En Linux puede que necesites dependencias adicionales: `playwright install-deps`
