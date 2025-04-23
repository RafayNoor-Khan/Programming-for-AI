from flask import Flask, render_template, request, jsonify
import json
from difflib import get_close_matches

app = Flask(__name__)

with open("library_data.json", encoding="utf-8") as f:
    library_data = json.load(f)


def find_answer(question):
    question = question.lower()
    
    if question in library_data["questions"]:
        return library_data["questions"][question]
    
    matches = get_close_matches(question, library_data["questions"].keys(), n=1, cutoff=0.6)
    if matches:
        return library_data["questions"][matches[0]]
    
    return "I'm sorry, I don't have information about that. Please ask a librarian for assistance."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.form.get('question')
    answer = find_answer(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)