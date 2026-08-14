# AutoMeet

Automated bot to join Google Meet calls using Playwright. Automatically installs Chromium, mutes microphone and camera, and maintains a persistent browser session.

## Requirements

- Python 3.10+
- pip
- Internet connection

## Installation

```bash
git clone <https://github.com/gfdev10/AutoMeet>
cd AutoMeet

python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

pip install -r requirements.txt
```

## Usage

```bash
python main.py --url https://meet.google.com/abc-defg-hij
```

Omitting `--url` uses the default URL defined in the script.

The script opens the browser, navigates to Meet, mutes mic/cam, and clicks the join button. Press `Ctrl+C` to end the session.

## Features

- **Automatic Chromium installation**: runs `playwright install chromium` on first execution.
- **Persistent user profile**: saves session data in `user_data/` (ignored by Git).
- **Mic/cam mute**: sends keyboard shortcuts (`ControlOrMeta+D`, `ControlOrMeta+E`) with a UI fallback.
- **Multi-language selectors**: supports Spanish and English Meet interfaces.
- **Configurable timeouts and delays**: all timing values are centralized as constants.
- **Structured logging**: timestamped logs with severity levels instead of raw prints.

## Project Structure

```
AutoMeet/
├── main.py            # Entrypoint and core logic
├── requirements.txt   # Dependencies
├── .gitignore         # Ignores user_data/ and .env
└── README.md          # This file
```

## Maintenance Notes

- Timeouts, delays, and selectors are defined as module-level constants at the top of `main.py`.
- Core logic is split into small functions: `asegurar_playwright`, `desactivar_mic_y_camara`, `unirse_a_reunion`, `main`.
- To add new features, extend the constants block or add new functions called from `unirse_a_reunion`.
- CLI arguments are defined in `build_parser()` for easy extension.

## Troubleshooting

- If Chromium fails to install, run manually: `playwright install chromium`
- If the join button is not found, ensure you are logged in or check the Meet URL format.
- On Linux, you may need additional dependencies: `playwright install-deps`
