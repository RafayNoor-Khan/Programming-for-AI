from flask import Flask, render_template, request, jsonify
import random
import re

app = Flask(__name__)

astronomy_data = {
    "planets": {
        "mercury": [
            "Mercury is the smallest planet in the Solar System and the closest to the Sun.",
            "Mercury has no atmosphere to retain heat, making it extremely hot during the day and freezing at night.",
            "A year on Mercury (one orbit around the Sun) takes just 88 Earth days."
        ],
        "venus": [
            "Venus is the second planet from the Sun and is often called Earth's twin due to its similar size.",
            "Venus has a thick, toxic atmosphere that traps heat, making it the hottest planet in the Solar System.",
            "A day on Venus is longer than its year, as it takes 243 Earth days to rotate once."
        ],
        "earth": [
            "Earth is the third planet from the Sun and the only known planet to support life.",
            "Earth's atmosphere protects it from meteoroids and harmful solar radiation.",
            "Over 70% of Earth's surface is covered by water."
        ],
        "mars": [
            "Mars is the fourth planet from the Sun and is known as the Red Planet due to its reddish appearance.",
            "Mars has the largest volcano in the Solar System, Olympus Mons.",
            "Scientists believe Mars once had liquid water and may have supported life."
        ],
        "jupiter": [
            "Jupiter is the largest planet in the Solar System and is known for its Great Red Spot.",
            "Jupiter has 79 known moons, the largest being Ganymede.",
            "Jupiter's atmosphere is mostly hydrogen and helium, similar to the Sun."
        ],
        "saturn": [
            "Saturn is the sixth planet from the Sun and is famous for its stunning ring system.",
            "Saturn's rings are made of ice, rock, and dust particles.",
            "Saturn is less dense than water, meaning it would float if placed in a large enough ocean."
        ],
        "uranus": [
            "Uranus is the seventh planet from the Sun and is unique for its sideways rotation.",
            "Uranus appears blue due to the presence of methane in its atmosphere.",
            "It takes Uranus 84 Earth years to complete one orbit around the Sun."
        ],
        "neptune": [
            "Neptune is the eighth planet from the Sun and is known for its strong winds and blue color.",
            "Neptune has a storm system called the Great Dark Spot, similar to Jupiter’s Red Spot.",
            "Neptune's moon Triton orbits in the opposite direction of the planet’s rotation."
        ]
    },
    "stars": {
        "sun": [
            "The Sun is the star at the center of the Solar System and provides energy for life on Earth.",
            "The Sun's core temperature reaches about 15 million degrees Celsius.",
            "The Sun will eventually expand into a red giant before shrinking into a white dwarf."
        ],
        "sirius": [
            "Sirius is the brightest star in the night sky and is located in the constellation Canis Major.",
            "Sirius is actually a binary star system, consisting of Sirius A and Sirius B.",
            "Sirius is about 25 times more luminous than the Sun."
        ],
        "betelgeuse": [
            "Betelgeuse is a red supergiant star in the constellation Orion and is one of the largest stars known.",
            "Betelgeuse is expected to explode as a supernova in the next 100,000 years.",
            "Despite its size, Betelgeuse is cooler than the Sun due to its expanded outer layers."
        ]
    }
}

def chatbot_response(user_input, context):
    user_input = user_input.lower()

    greetings=["hello", "hi", "hey", "how are you", "good morning", "good evening"]
    greeting_responses=["Hello!", "Hi there!", "Hey! How can I help you?", "Greetings!", "Nice to see you!"]
    
    for greeting in greetings:
        if re.search(rf'\b{greeting}\b', user_input, re.IGNORECASE):
            return random.choice(greeting_responses)

    for category in ["planets", "stars"]:
        for key, info_list in astronomy_data[category].items():
            if re.search(rf'\b{key}\b', user_input, re.IGNORECASE):
                context["last_topic"] = key
                return random.choice(info_list)
    if "more" in user_input or "tell me more" in user_input:
        if "last_topic" in context:
            last_topic = context["last_topic"]
            if last_topic in astronomy_data["planets"]:
                return random.choice(astronomy_data["planets"][last_topic])
            elif last_topic in astronomy_data["stars"]:
                return random.choice(astronomy_data["stars"][last_topic])
        return "I'm not sure what you want to know more about. Please ask a specific question."


    random_facts = [
        "The Milky Way galaxy is estimated to contain over 100 billion stars.",
        "Neutron stars are so dense that a sugar-cube-sized amount of neutron-star material would weigh about a billion tons.",
        "The Andromeda Galaxy is on a collision course with the Milky Way and will merge in about 4.5 billion years.",
        "Saturn's moon Titan has lakes of liquid methane and ethane.",
        "A day on Venus is longer than a year on Venus."
    ]
    
    if "fact" in user_input or "random" in user_input:
        return "Here's a random fact: " + random.choice(random_facts)

    return "I'm sorry, I didn't understand that. You can ask about planets, stars, constellations, black holes, or the solar system."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    context = {}    
    response = chatbot_response(user_input, context)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
