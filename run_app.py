import webbrowser
import threading
from app import create_app

app = create_app()

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Timer(2, open_browser).start()
    app.run(host="127.0.0.1", port=5000)