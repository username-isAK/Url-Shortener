from flask import Flask, request, jsonify, redirect
from pymongo import MongoClient
import string, random, datetime
import os

app = Flask(__name__)

client = os.getenv("MONGO_URI")
db = client["url_shortener"]
collection = db["urls"]

collection.create_index("expiry", expireAfterSeconds=0)

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    original_url = data.get("url")

    if not original_url:
        return jsonify({"error": "URL is required"}), 400

    short_code = generate_short_code()

    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(days=7)

    collection.insert_one({
        "short_code": short_code,
        "original_url": original_url,
        "expiry": expiry_time 
    })

    short_url = f"http://localhost:5000/{short_code}"
    return jsonify({"original_url": original_url, "short_url": short_url})

@app.route('/<short_code>')
def redirect_to_url(short_code):
    record = collection.find_one({"short_code": short_code})

    if record:
        return redirect(record["original_url"])
    else:
        return jsonify({"error": "Invalid or expired short URL"}), 404

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
