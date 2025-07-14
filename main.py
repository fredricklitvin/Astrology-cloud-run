from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import firestore
import os

app = Flask(__name__)
CORS(app, origins="*", methods=["GET", "POST", "OPTIONS"], allow_headers="*")

# Firestore client (remove database="..." if not needed)
db = firestore.Client()

ZODIAC_SIGNS = [
    ("capricorn", (1, 19)), ("aquarius", (2, 18)), ("pisces", (3, 20)),
    ("aries", (4, 19)), ("taurus", (5, 20)), ("gemini", (6, 20)),
    ("cancer", (7, 22)), ("leo", (8, 22)), ("virgo", (9, 22)),
    ("libra", (10, 22)), ("scorpio", (11, 21)), ("sagittarius", (12, 21)),
    ("capricorn", (12, 31))
]

def get_zodiac(month, day):
    for sign, (m, d) in ZODIAC_SIGNS:
        if (month < m) or (month == m and day <= d):
            return sign
    return "capricorn"

@app.route("/zodiac", methods=["POST", "OPTIONS"])
def zodiac_handler():
    if request.method == "OPTIONS":
        # Preflight CORS request
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response, 204

    # Handle POST request
    data = request.get_json()
    if not data or "month" not in data or "day" not in data:
        return jsonify({"error": "Invalid input"}), 400

    try:
        month = int(data.get("month"))
        day = int(data.get("day"))
    except ValueError:
        return jsonify({"error": "Month and day must be integers"}), 400

    sign = get_zodiac(month, day)
    doc = db.collection("zodiacs").document(sign).get()

    if doc.exists:
        sign_info = doc.to_dict().get("description", "No description found.")
    else:
        sign_info = "Zodiac data not found."

    response = jsonify({"sign": sign, "info": sign_info})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# ✅ Required for Cloud Run to work
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)