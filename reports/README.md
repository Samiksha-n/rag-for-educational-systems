# RAG for Educational Systems - Reports

## API Testing Report (Task 1 - Week 5)

### Test Summary
| Total Tests | Passed | Failed |
|-------------|--------|--------|
| 14 | 14 | 0 |

### Test Results

#### GET /api/health
| Test | Expected | Result |
|------|----------|--------|
| Status code | 200 | ✅ Pass |
| Has 'status' field | True | ✅ Pass |
| Status is 'ok' | True | ✅ Pass |
| Has 'timestamp' field | True | ✅ Pass |

#### POST /api/chat (valid request)
| Test | Expected | Result |
|------|----------|--------|
| Status code | 200 | ✅ Pass |
| Has 'response' field | True | ✅ Pass |
| Has 'conversation_id' | True | ✅ Pass |
| Response is not empty | True | ✅ Pass |

#### POST /api/chat (error condition)
| Test | Expected | Result |
|------|----------|--------|
| Status code | 400 | ✅ Pass |
| Has 'error' field | True | ✅ Pass |

#### GET /api/history
| Test | Expected | Result |
|------|----------|--------|
| Status code | 200 | ✅ Pass |
| Has 'history' field | True | ✅ Pass |
| History is a list | True | ✅ Pass |

#### GET /api/users
| Test | Expected | Result |
|------|----------|--------|
| Status code | 200 | ✅ Pass |
| Has 'users' field | True | ✅ Pass |

#### POST /api/feedback (valid)
| Test | Expected | Result |
|------|----------|--------|
| Status code | 201 | ✅ Pass |
| Has 'message' field | True | ✅ Pass |

#### POST /api/feedback (error condition)
| Test | Expected | Result |
|------|----------|--------|
| Status code | 400 | ✅ Pass |
| Has 'error' field | True | ✅ Pass |

## Sequence Diagram

User types question
↓
Streamlit Frontend
↓
POST /api/chat
↓
Flask Backend
↓
Google Gemini AI
↓
Flask Backend
↓
Streamlit Frontend
↓
User sees answer

## API Documentation

### POST /api/chat
Request:
{"prompt": "What is RAG?"}
Response:
{"response": "RAG stands for...", "conversation_id": "uuid"}

### GET /api/history
Response:
{"history": [...]}

### GET /api/users
Response:
{"users": [...]}

### POST /api/feedback
Request:
{"conversation_id": "uuid", "rating": 5, "comment": "helpful!"}
Response:
{"message": "Feedback stored"}

### GET /api/health
Response:
{"status": "ok", "service": "rag-backend", "timestamp": "..."}
