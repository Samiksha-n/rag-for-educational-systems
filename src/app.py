"""
Task 3: Develop Backend Server
--------------------------------
Server layer for the AI Client-Server Architecture (Task 1).
Built with Python Flask (instead of Node.js/Express, since this
project uses Python only).

Implements the endpoints designed in Task 2:
  POST /api/chat      -> Send prompts to AI
  GET  /api/history   -> Retrieve conversations
  GET  /api/users      -> Fetch user information
  POST /api/feedback   -> Store ratings
  GET  /api/health     -> Health check

Run with:
    pip install flask flask-cors
    python app.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid
import logging

# ---------------------------------------------------------------
# App setup
# ---------------------------------------------------------------
app = Flask(__name__)
CORS(app)  # allow requests from the frontend (React) layer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rag-backend")

# ---------------------------------------------------------------
# In-memory "database" (replace with a real DB layer later,
# e.g. SQLite/PostgreSQL/MongoDB — see Database layer in Task 1)
# ---------------------------------------------------------------
conversation_history = []   # list of {id, prompt, response, timestamp}
users_db = [
    {"id": 1, "name": "Samiksha", "role": "student"},
    {"id": 2, "name": "Admin", "role": "instructor"},
]
feedback_store = []         # list of {id, conversation_id, rating, comment}


# ---------------------------------------------------------------
# Middleware: simple request logger
# ---------------------------------------------------------------
@app.before_request
def log_request():
    logger.info(f"{request.method} {request.path} - body: {request.get_data()}")


# ---------------------------------------------------------------
# Middleware: global error handler
# ---------------------------------------------------------------
@app.errorhandler(Exception)
def handle_error(e):
    logger.error(f"Unhandled error: {e}")
    return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------
# Helper: placeholder AI-call function.
# Replace this with your actual RAG pipeline call
# (retrieval + generation) from your project's src/ folder.
# ---------------------------------------------------------------
def generate_ai_response(prompt: str) -> str:
    # TODO: plug in your RAG pipeline here, e.g.:
    #   chunks = retriever.search(prompt)
    #   answer = llm.generate(prompt, context=chunks)
    #   return answer
    return f"AI response generated for: '{prompt}'"


# ---------------------------------------------------------------
# Routes
# ---------------------------------------------------------------

@app.route("/api/health", methods=["GET"])
def health_check():
    """Simple health check endpoint."""
    return jsonify({
        "status": "ok",
        "service": "rag-backend",
        "timestamp": datetime.utcnow().isoformat()
    }), 200


@app.route("/api/chat", methods=["POST"])
def chat():
    """Send a prompt to the AI and get a response back."""
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
    """Retrieve all past conversations."""
    return jsonify({"history": conversation_history}), 200


@app.route("/api/users", methods=["GET"])
def get_users():
    """Fetch user information."""
    return jsonify({"users": users_db}), 200


@app.route("/api/feedback", methods=["POST"])
def submit_feedback():
    """Store a rating/comment for a given conversation."""
    data = request.get_json(silent=True) or {}
    conversation_id = data.get("conversation_id")
    rating = data.get("rating")
    comment = data.get("comment", "")

    if conversation_id is None or rating is None:
        return jsonify({
            "error": "Missing required fields: 'conversation_id' and 'rating'"
        }), 400

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
