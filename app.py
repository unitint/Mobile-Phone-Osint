from flask import Flask, render_template, request
from modules.phone_parser import normalize_phone
from modules.osint_engine import investigate
import webbrowser
import threading
import time

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    phone = request.form["phone"]
    normalized = normalize_phone(phone)

    if normalized is None:
        return render_template("index.html", error="Invalid Phone Number")

    report = investigate(normalized)

    return render_template(
        "result.html",
        report=report
    )


def open_browser():
    """Open browser after a short delay"""
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    # Open browser automatically
    threading.Thread(target=open_browser).start()
    app.run(debug=True)