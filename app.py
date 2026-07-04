from flask import Flask, render_template, request
from modules.google_search import google_dorks
from modules.phone_parser import normalize_phone
from modules.osint_engine import investigate

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():

    phone = request.form["phone"]

    normalized = normalize_phone(phone)

    if normalized is None:
        return "Invalid Phone Number"

    report = investigate(normalized)

    return render_template(
        "results.html",
        report=report
    )


if __name__ == "__main__":
    app.run(debug=True)