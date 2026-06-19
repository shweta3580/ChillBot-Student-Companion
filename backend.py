from flask import Flask, request, jsonify
import datetime
import csv
import os
from transformers import pipeline

# Flask App
app = Flask(__name__)

# Load Hugging Face Model using Pipeline (Faster & Simpler)
#chatbot_pipeline = pipeline("text2text-generation", model="facebook/blenderbot-3B")
chatbot_pipeline = pipeline("text2text-generation", model="facebook/blenderbot-400M-distill")


# Ensure chat log exists
CHAT_LOG_FILE = "chat_log.csv"
if not os.path.exists(CHAT_LOG_FILE):
    with open(CHAT_LOG_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["User Input", "Chatbot Response", "Timestamp"])

def chatbot(user_input):
    """Generate response using BlenderBot 3B."""
    try:
        bot_reply = chatbot_pipeline(user_input, max_length=100)[0]["generated_text"]
    except Exception as e:
        bot_reply = "Sorry, I couldn't generate a response."
        print(f"Error: {e}")

    return bot_reply

@app.route("/", methods=["GET"])
def home():
    return "Chatbot is running!"

@app.route("/chat", methods=["POST"])
def chat():
    """Handle user input and return chatbot response."""
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    response = chatbot(user_input)

    # Save chat history
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CHAT_LOG_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([user_input, response, timestamp])

    return jsonify({"user_input": user_input, "chatbot_response": response, "timestamp": timestamp})

@app.route("/history", methods=["GET"])
def history():
    """Return chat history."""
    with open(CHAT_LOG_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        history = [{"user": row[0], "bot": row[1], "time": row[2]} for row in reader]

    return jsonify(history)

if __name__ == "__main__":
    app.run(debug=True)
