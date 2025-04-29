from flask import Flask, render_template, jsonify, request, session
import os
from openai import OpenAI
from dotenv import load_dotenv
from prompt import SYSTEM_PROMPT, PROMPT_TEMPLATES

load_dotenv()
app=Flask(__name__)
app.secret_key=os.getenv("FLASK_SECRET_KEY",'DEFAULT-SECRET_KEY')
client=OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_URL')
)

def get_prompt_type(question):
    question=question.lower()
    if 'explain' in question or 'detail' in question:
        return 'explain'
    elif 'list' in question or 'point' in question or 'feature' in question:
        return 'list'
    return 'general'

@app.route('/', methods=['GET','POST'])
def home():
    if 'conversation' not in session:
        session['conversation']=[{
            "role": "assistant",
            "content": "Hello! I'm your study assistant. Ask me anything or say 'explain' for details!"
        }]

    if request.method=='POST':
        question=request.form.get('question', '').strip()
        if not question:
            return jsonify({"error": "Please enter a question"}), 400
        try:
            session['conversation'].append({"role": "user", "content": question})
            session.modified=True
            prompt_type=get_prompt_type(question)
            if prompt_type=="explain" and len(session['conversation']) > 1:
                last_q=session['conversation'][-2]['content']
                prompt=PROMPT_TEMPLATES["explain"].format(last_question=last_q)
            elif prompt_type=="list" and len(session['conversation']) > 1:
                last_q=session['conversation'][-2]['content']
                prompt=PROMPT_TEMPLATES["list"].format(last_question=last_q)
            else:
                history="\n".join(
                    f"{msg['role']}: {msg['content']}" 
                    for msg in session['conversation'][-3:]
                )
                prompt = PROMPT_TEMPLATES["general"].format(
                    history=history,
                    question=question
                )
            response=client.chat.completions.create(
                model=os.getenv("MODEL", "llama3-70b-8192"),
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=500
            )            
            answer=format_response(response.choices[0].message.content)
            session['conversation'].append({"role": "assistant", "content": answer})
            return jsonify({"response": answer})
        
        except Exception as e:
            return jsonify({"error": f"Error: {str(e)}"}), 500
    
    return render_template('index.html')

def format_response(text):
    text=text.replace('**', '').replace('* ', '• ')
    for phrase in ["Key points:", "Main features:", "Advantages:"]:
        if phrase in text:
            text=text.replace(phrase, phrase + "\n")
    return text.strip()
if __name__ == '__main__':
    app.run(debug=True)