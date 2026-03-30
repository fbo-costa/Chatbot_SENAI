import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

PERSONALIDADE = """
Você é Aetherius.

- Sarcástico
- Impaciente
- Inteligente
- Estilo palmeirense raiz
- Respostas provocativas e diretas

Nunca seja ofensivo extremo.
"""

chat_history = []

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    global chat_history

    data = request.json
    user_message = data.get("message")

    chat_history.append(f"Usuário: {user_message}")

    contexto = PERSONALIDADE + "\n" + "\n".join(chat_history)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contexto
    )

    resposta = response.text

    chat_history.append(f"Aetherius: {resposta}")

    return jsonify({"reply": resposta})


if __name__ == "__main__":
    app.run(debug=True)