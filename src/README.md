# RAG for Educational Systems - Source Code

## Project Overview
This project implements a Retrieval Augmented Generation (RAG) system for educational purposes. It uses a Python Flask backend connected to Google Gemini AI and a Streamlit frontend.

## Files
| File | Description |
|------|-------------|
| `app.py` | Flask backend server with Gemini AI integration |
| `frontend.py` | Streamlit frontend user interface |
| `test_api.py` | API testing script for all endpoints |
| `deploy.py` | Deployment script to run all services |
| `requirements.txt` | Python dependencies |

## API Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| /api/chat | POST | Send prompt to AI |
| /api/history | GET | Retrieve conversations |
| /api/users | GET | Fetch user information |
| /api/feedback | POST | Store ratings |
| /api/health | GET | Health check |

## How to Run

### Step 1 - Install dependencies
pip install -r requirements.txt

### Step 2 - Start backend
python app.py

### Step 3 - Start frontend
streamlit run frontend.py

### Step 4 - Open browser
http://localhost:8501

### Or run everything at once
python deploy.py

## How to Run Tests
python test_api.py

## Technologies Used
- Python 3.x
- Flask (Backend)
- Streamlit (Frontend)
- Google Gemini AI
- Flask-CORS
- Requests
