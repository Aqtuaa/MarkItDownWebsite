import sys
import socket
import threading
import time
import urllib.request
import logging
import webview
from app import app

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]

def run_flask(port):
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)

def wait_for_server(port, timeout=5.0):
    start = time.time()
    url = f"http://127.0.0.1:{port}/"
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=1.0) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(0.1)
    return False

def main():
    port = get_free_port()
    server_thread = threading.Thread(target=run_flask, args=(port,), daemon=True)
    server_thread.start()

    wait_for_server(port)

    # Launch desktop window using pywebview (Microsoft Edge WebView2 backend)
    webview.create_window(
        title="MarkItDown Converter",
        url=f"http://127.0.0.1:{port}",
        width=880,
        height=820,
        min_size=(680, 540),
        text_select=True,
    )
    webview.start()

if __name__ == "__main__":
    main()
