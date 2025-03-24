from flask import Flask, render_template, request, jsonify
import random
import re

app = Flask(__name__)

# Expanded astronomy data
astronomy_data = {
    "planets": {
        "mercury": "Mercury is the smallest planet in the Solar System and the closest to the Sun.",
        "venus": "Venus is the second planet from the Sun and is often called Earth's twin due to its similar size.",
        "earth": "Earth is the third planet from the Sun and the only known planet to support life.",
        "mars": "Mars is the fourth planet from the Sun and is known as the Red Planet due to its reddish appearance.",
        "jupiter": "Jupiter is the largest planet in the Solar System and is known for its Great Red Spot.",
        "saturn": "Saturn is the sixth planet from the Sun and is famous for its stunning ring system.",
        "uranus": "Uranus is the seventh planet from the Sun and is unique for its sideways rotation.",
        "neptune": "Neptune is the eighth planet from the Sun and is known for its strong winds and blue color."
    },
    "stars": {
        "sun": "The Sun is the star at the center of the Solar System and provides energy for life on Earth.",
        "sirius": "Sirius is the brightest star in the night sky and is located in the constellation Canis Major.",
        "betelgeuse": "Betelgeuse is a red supergiant star in the constellation Orion and is one of the largest stars known."
    },
    "constellations": {
        "orion": "Orion is a prominent constellation named after a hunter in Greek mythology. It is visible worldwide.",
        "ursa major": "Ursa Major, also known as the Great Bear, contains the Big Dipper and is visible in the northern hemisphere.",
        "leo": "Leo is a constellation of the zodiac and represents the lion. It is one of the oldest recognized constellations."
    },
    "black hole": {
        "basic": "A black hole is a region of spacetime where gravity is so strong that nothing, not even light, can escape.",
        "facts": [
            "Black holes can form when massive stars collapse at the end of their life cycle.",
            "The center of a black hole is called a singularity, where density becomes infinite.",
            "Supermassive black holes exist at the center of most galaxies, including the Milky Way."
        ]
    },
    "solar system": "The Solar System consists of the Sun, eight planets, their moons, dwarf planets, and other celestial objects.",
    "random_facts": [
        "The Milky Way galaxy is estimated to contain over 100 billion stars.",
        "Neutron stars are so dense that a sugar-cube-sized amount of neutron-star material would weigh about a billion tons.",
        "The Andromeda Galaxy is on a collision course with the Milky Way and will merge in about 4.5 billion years."
    ]
}

# Chatbot logic
def chatbot_response(user_input, context):
    user_input = user_input.lower()

    # Check if the input matches any planet, star, or constellation
    for category in ["planets", "stars", "constellations"]:
        for key, info in astronomy_data[category].items():
            if re.search(rf'\b{key}\b', user_input, re.IGNORECASE):  # Exact word match
                context["last_topic"] = key
                return info

    # Special checks for black hole and solar system
    if re.search(r"\bblack hole\b", user_input, re.IGNORECASE):
        context["last_topic"] = "black hole"
        return astronomy_data["black hole"]["basic"]
    
    if re.search(r"\bsolar system\b", user_input, re.IGNORECASE):
        context["last_topic"] = "solar system"
        return astronomy_data["solar system"]

    # More information request
    if "more" in user_input or "tell me more" in user_input:
        if "last_topic" in context:
            if context["last_topic"] == "black hole":
                return random.choice(astronomy_data["black hole"]["facts"])
            return "Here's more about " + context["last_topic"] + ": " + astronomy_data.get(context["last_topic"], "No additional information available.")
        return "I'm not sure what you want to know more about. Please ask a specific question."

    # Random facts
    if "fact" in user_input or "random" in user_input:
        return "Here's a random fact: " + random.choice(astronomy_data["random_facts"])

    # Default response if input is not recognized
    return "I'm sorry, I didn't understand that. You can ask about planets, stars, constellations, black holes, or the solar system."

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    context = {}  # Simple context storage
    response = chatbot_response(user_input, context)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
