# RAG for Educational Systems - Deployment

## Deployment Report (Task 2 - Week 5)

## Application Details
| Item | Details |
|------|---------|
| Project Name | RAG for Educational Systems |
| Backend | Python Flask |
| Frontend | Python Streamlit |
| AI Model | Google Gemini AI |
| Backend Port | 5000 |
| Frontend Port | 8501 |

## Deployment Steps

### Step 1 - Clone Repository
git clone https://github.com/Samiksha-n/rag-for-educational-systems.git
cd rag-for-educational-systems/src

### Step 2 - Install Dependencies
pip install -r requirements.txt

### Step 3 - Run using deploy.py
python deploy.py

### Step 4 - Verify Deployment
Open browser:
- Frontend: http://localhost:8501
- Backend: http://localhost:5000/api/health

## Verification Checklist
✅ Frontend loads at http://localhost:8501
✅ Input box visible
✅ Submit button works
✅ AI response displayed
✅ Conversation history shown
✅ Backend health check returns ok

## Project Structure
rag-for-educational-systems/
├── README.md
├── data/
│   └── README.md
├── src/
│   ├── README.md
│   ├── app.py
│   ├── frontend.py
│   ├── test_api.py
│   ├── deploy.py
│   └── requirements.txt
├── reports/
│   └── README.md
└── deployment/
    └── README.md

## GitHub Repository
https://github.com/Samiksha-n/rag-for-educational-systems

## Technologies Used
- Python 3.x
- Flask
- Streamlit
- Google Gemini AI
