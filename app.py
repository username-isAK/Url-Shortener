from flask import Flask, request, render_template, redirect
from pymongo import MongoClient
import string, random, datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["url_shortener"]
collection = db["urls"]

collection.create_index("expiry", expireAfterSeconds=0)

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/shorten", methods=["POST"])
def shorten():
    original_url = request.form.get("url")

    if not original_url:
        return render_template("index.html", error="URL is required")

    while True:
        short_code = generate_short_code()
        if not collection.find_one({"short_code": short_code}):
            break 

    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(days=7)

    collection.insert_one({
        "short_code": short_code,
        "original_url": original_url,
        "expiry": expiry_time
    })

    short_url = f"http://localhost:5000/{short_code}"
    expiry_str = expiry_time.strftime("%Y-%m-%d %H:%M:%S UTC")

    return render_template("index.html", short_url=short_url, expiry=expiry_str)

@app.route("/<short_code>")
def redirect_to_url(short_code):
    record = collection.find_one({"short_code": short_code})
    if record:
        return redirect(record["original_url"])
    else:
        return render_template("index.html", error="Invalid or expired short URL")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
