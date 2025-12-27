from flask import Flask, render_template, request, redirect
import sqlite3
import string
import time
from failures import FAILURE_CONFIG
app = Flask(__name__)

# ---------------- DATABASE ----------------

def get_db():
    if FAILURE_CONFIG["db_down"]:
        raise Exception("Simulated DB failure")

    if FAILURE_CONFIG["db_delay_seconds"] > 0:
        time.sleep(FAILURE_CONFIG["db_delay_seconds"])

    return sqlite3.connect("urls.db")

    


# ---------------- BASE62 ----------------
BASE62 = string.ascii_letters + string.digits

def encode_base62(num):
    if num == 0:
        return BASE62[0]

    result = []
    while num > 0:
        num, rem = divmod(num, 62)
        result.append(BASE62[rem])

    return ''.join(reversed(result))


def decode_base62(code):
    num = 0
    for char in code:
        num = num * 62 + BASE62.index(char)
    return num


# ---------------- ROUTES ----------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form.get("url")

        if not url:
            return render_template("index.html", error="URL cannot be empty")

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT id FROM urls WHERE original_url = ?",
            (url,)
        )
        row = cursor.fetchone()

        if row:
            # 🔹 URL already exists
            url_id = row[0]
            print(f"[INFO] [DUPLICATE] url_id={url_id}")
        else:
            # 🔹 New URL → insert
            cursor.execute(
                "INSERT INTO urls (original_url) VALUES (?)",
                (url,)
            )
            db.commit()
            url_id = cursor.lastrowid
            print(f"[INFO] [CREATE] url_id={url_id}")
        db.close()
        
        short_code = encode_base62(url_id)
        print(f"[INFO] [CREATE] url_id={url_id} short_code={short_code}")
        short_url = request.host_url + short_code

        return render_template("index.html", short_url=short_url)

    return render_template("index.html")


@app.route("/<short_code>")
def redirect_short_url(short_code):
    try:
        url_id = decode_base62(short_code)
    except ValueError:
        print(f"[Warning][Decode] invalid short code = {short_code}")
        return "Invalid URL", 404
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "SELECT original_url FROM urls WHERE id = ?",
            (url_id,)
        )
        result = cursor.fetchone()
        db.close()

    except Exception:
        print(f"[Warning][DataBase] Failure {e}")
        return "Service temporarily unavailable", 503

    if result:
        print(f"[INFO] [REDIRECT] short_code={short_code} -> {result[0]}")
        return redirect(result[0])
    print(f"[Warning][LookUp] Url with the url id = {url_id} not found")
    return "URL not found", 404


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
