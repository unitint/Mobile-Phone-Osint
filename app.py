from flask import Flask, render_template, request
from modules.phone_parser import normalize_phone
from modules.osint_engine import investigate
from config import Config
import webbrowser
import threading
import time
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    phone = request.form.get("phone", "").strip()
    logger.info(f"🔍 Searching for phone: {phone}")
    
    if not phone:
        return render_template("index.html", error="Please enter a phone number")
    
    normalized = normalize_phone(phone)

    if normalized is None:
        return render_template("index.html", error="Invalid Phone Number. Please enter a valid number (e.g., 09946563099)")

    try:
        report = investigate(normalized)
        logger.info(f"✅ Found {report.get('summary', {}).get('google_matches', 0)} results")
        return render_template("result.html", report=report)
    except Exception as e:
        logger.error(f"❌ Search error: {e}")
        return render_template("index.html", error="Search failed. Please try again.")


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", error="Page not found"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("error.html", error="Server error. Please try again later."), 500


@app.errorhandler(405)
def method_not_allowed(error):
    return render_template("error.html", error="Method not allowed"), 405


def open_browser():
    """Open browser after a short delay"""
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    # Only open browser in development
    if os.environ.get('ENV') != 'production':
        threading.Thread(target=open_browser).start()
    
    app.run(debug=app.config['DEBUG'])