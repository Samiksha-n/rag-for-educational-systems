from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid
import logging
import google.generativeai as genai

# ---------------------------------------------------------------
# App setup
# ---------------------------------------------------------------
app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rag-backend")

# ---------------------------------------------------------------
# Gemini AI setup (Task 2: Integrate AI Model Layer)
# ---------------------------------------------------------------
genai.configure(api_key="AQ.Ab8RN6LYUM2Tjx-KSu-pN1XODmFfqjjVgrJs0AhR7I1MxqxiKQ")
model = genai.GenerativeModel("gemini-pro")

# ---------------------------------------------------------------
# In-memory database
# ---------------------------------------------------------------
conversation_history = []
users_db = [
    {"id": 1, "name": "Samiksha", "role": "student"},
    {"id": 2, "name": "Admin", "role": "instructor"},
]
feedback_store = []

# ---------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------
@app.before_request
def log_request():
    logger.info(f"{request.method} {request.path} - body: {request.get_data()}")

@app.errorhandler(Exception)
def handle_error(e):
    logger.error(f"Unhandled error: {e}")
    return jsonify({"error": str(e)}), 500

# ---------------------------------------------------------------
# AI Response Function (Task 2)
# ---------------------------------------------------------------
def generate_ai_response(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI error: {str(e)}"

# ---------------------------------------------------------------
# Routes
# ---------------------------------------------------------------
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "service": "rag-backend",
        "timestamp": datetime.utcnow().isoformat()
    }), 200

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "Missing required field: 'prompt'"}), 400
    response_text = generate_ai_response(prompt)
    entry = {
        "id": str(uuid.uuid4()),
        "prompt": prompt,
        "response": response_text,
        "timestamp": datetime.utcnow().isoformat()
    }
    conversation_history.append(entry)
    return jsonify({
        "response": response_text,
        "conversation_id": entry["id"]
    }), 200

@app.route("/api/history", methods=["GET"])
def get_history():
    return jsonify({"history": conversation_history}), 200

@app.route("/api/users", methods=["GET"])
def get_users():
    return jsonify({"users": users_db}), 200

@app.route("/api/feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json(silent=True) or {}
    conversation_id = data.get("conversation_id")
    rating = data.get("rating")
    comment = data.get("comment", "")
    if conversation_id is None or rating is None:
        return jsonify({"error": "Missing required fields"}), 400
    feedback_entry = {
        "id": str(uuid.uuid4()),
        "conversation_id": conversation_id,
        "rating": rating,
        "comment": comment,
        "timestamp": datetime.utcnow().isoformat()
    }
    feedback_store.append(feedback_entry)
    return jsonify({"message": "Feedback stored", "feedback": feedback_entry}), 201

# ---------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
