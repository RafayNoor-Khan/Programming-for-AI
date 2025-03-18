# from flask import Flask, jsonify
# import requests

# app = Flask(__name__)

# NASA_API_KEY = "Gw41GbIQqg00t5XWSiVM54C6LMH7aZGt3RTwzOUG"  # Replace with your actual NASA API key
# NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"

# @app.route("/apod", methods=["GET"])
# def get_apod():
#     params = {"api_key": NASA_API_KEY}
#     response = requests.get(NASA_APOD_URL, params=params)
#     if response.status_code == 200:
#         return jsonify(response.json())  # Return JSON response
#     else:
#         return jsonify({"error": "Failed to fetch data"}), response.status_code

# @app.route("/")
# def home():
#     return get_apod()  # Redirects the homepage to APOD response

# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, jsonify, redirect, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

NASA_API_KEY = "Gw41GbIQqg00t5XWSiVM54C6LMH7aZGt3RTwzOUG"
MARS_API_URL = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"

# Store added Mars photos (mock database)
mars_photos = []

@app.route("/", methods=["GET"])
def home():
    """Redirects the user to the /mars endpoint."""
    return redirect("/mars")

@app.route("/mars", methods=["GET", "POST"])
def mars_photos_api():
    if request.method == "POST":
        # Get JSON data from request body
        data = request.get_json()
        if not data or "image_url" not in data:
            return jsonify({"error": "Invalid data, 'image_url' required"}), 400
        
        # Add image URL to mock database
        mars_photos.append(data["image_url"])
        return jsonify({"message": "Mars photo added successfully", "image_url": data["image_url"]}), 201
    
    elif request.method == "GET":
        # Fetch NASA Mars image if database is empty
        if not mars_photos:
            params = {"sol": 1000, "api_key": NASA_API_KEY}
            response = requests.get(MARS_API_URL, params=params)
            
            if response.status_code == 200:
                data = response.json()
                photos = data.get("photos", [])
                if photos:
                    return jsonify({"image_url": photos[0]["img_src"]})
                else:
                    return jsonify({"error": "No images found"}), 404

        # Return stored Mars photos
        return jsonify({"images": mars_photos})

if __name__ == "__main__":
    app.run(debug=True)
