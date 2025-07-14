from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import firestore
import os
import traceback

app = Flask(__name__)
CORS(app, origins="*", methods=["GET", "POST", "OPTIONS"], allow_headers="*")


db = firestore.Client(project="i-agility-465314-p6")

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
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response, 204

    try:
        # Step 1: Parse request data
        data = request.get_json(force=True)
        print("Received JSON:", data)

        if not data or "month" not in data or "day" not in data:
            return jsonify({"error": "Missing 'month' or 'day'"}), 400

        month = int(data["month"])
        day = int(data["day"])

        # Step 2: Determine zodiac
        sign = get_zodiac(month, day)
        print("Calculated sign:", sign)

        # Step 3: Fetch from Firestore
        doc = db.collection("zodiacs").document(sign).get()
        print("Firestore doc exists:", doc.exists)

        if doc.exists:
            sign_info = doc.to_dict().get("description", "No description found.")
        else:
            sign_info = "Zodiac data not found."

        # Step 4: Return response
        response = jsonify({"sign": sign, "info": sign_info})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    except Exception as e:
        print("Exception occurred:", e)
        traceback.print_exc()
        return jsonify({
            "error": "Server Error",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)