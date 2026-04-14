"""SafetyCulture Tools — Desktop Launcher.

Starts the Streamlit server in a background thread and opens a native
desktop window. Close the window to stop the app.

Works both in development (python launcher.py) and when bundled as a
standalone executable via PyInstaller.
"""

import os
import socket
import sys
import threading
import time
import urllib.error
import urllib.request


def get_app_dir():
    """Return the app root — handles both dev and PyInstaller-bundled modes."""
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def find_free_port():
    """Find an available TCP port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def wait_for_server(url, timeout=120):
    """Poll until the Streamlit server responds or timeout is reached."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            urllib.request.urlopen(url, timeout=2)
            return True
        except (urllib.error.URLError, OSError):
            time.sleep(0.5)
    return False


def run_streamlit_server(app_path, port):
    """Run the Streamlit server (called in a daemon thread)."""
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--server.port",
        str(port),
        "--server.address",
        "localhost",
        "--server.headless",
        "true",
        "--browser.gatherUsageStats",
        "false",
        "--server.maxUploadSize",
        "200",
        "--theme.primaryColor",
        "#6C63FF",
        "--theme.backgroundColor",
        "#FFFFFF",
        "--theme.secondaryBackgroundColor",
        "#F5F5F5",
        "--theme.textColor",
        "#333333",
        "--theme.font",
        "sans serif",
    ]
    try:
        from streamlit.web.cli import main

        main()
    except SystemExit:
        pass


def main():
    app_dir = get_app_dir()
    port = find_free_port()
    url = f"http://localhost:{port}"
    app_path = os.path.join(app_dir, "app", "Home.py")

    # Start Streamlit in a daemon thread so it dies when the main thread exits
    server_thread = threading.Thread(
        target=run_streamlit_server,
        args=(app_path, port),
        daemon=True,
    )
    server_thread.start()

    if not wait_for_server(url):
        sys.exit("Error: Streamlit server failed to start.")

    # Native desktop window, with browser fallback
    try:
        import webview

        webview.create_window(
            "SafetyCulture Tools",
            url,
            width=1280,
            height=900,
            min_size=(800, 600),
        )
        webview.start()
    except Exception:
        import webbrowser

        webbrowser.open(url)
        print(f"SafetyCulture Tools is running at {url}")
        print("Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
