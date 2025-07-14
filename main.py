from flask import Flask, request, jsonify
from google.cloud import firestore

app = Flask(__name__)
db = firestore.Client(database="astrology-db-test")

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

@app.route("/zodiac", methods=["POST"])
def zodiac_handler():
    data = request.get_json()
    month = int(data.get("month"))
    day = int(data.get("day"))
    
    sign = get_zodiac(month, day)
    
    doc = db.collection("zodiacs").document("zodiacs").get()
    if doc.exists:
        sign_info = doc.to_dict().get(sign, "No data found for this sign.")
    else:
        sign_info = "Zodiac data not found."
    
    return jsonify({"sign": sign, "info": sign_info})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
