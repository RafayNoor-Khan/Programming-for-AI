from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# NASA API Details
NASA_API_KEY = "Gw41GbIQqg00t5XWSiVM54C6LMH7aZGt3RTwzOUG"
NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"

@app.route("/")
def home():
    return render_template("index.html")  # Load frontend

@app.route("/apod", methods=["GET"])
def get_apod():
    """Fetch APOD data from NASA API"""
    params = {"api_key": NASA_API_KEY}
    response = requests.get(NASA_APOD_URL, params=params)

    if response.status_code == 200:
        return jsonify(response.json())  # Return JSON response
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code

if __name__ == "__main__":
    app.run(debug=True)
