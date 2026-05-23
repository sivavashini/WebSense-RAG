# WebSense RAG

WebSense RAG is a futuristic safety and responsibility assistant inspired by Spidey Sense and "With great power comes great responsibility."

Users describe dangerous, ethical, cyber, emergency, or suspicious situations. The app retrieves relevant knowledge from uploaded documents, classifies danger, generates grounded advice, and displays a cinematic SpideySense risk dashboard.

## Features

- React + Vite + Tailwind futuristic superhero UI
- FastAPI backend with LangChain, FAISS, SentenceTransformers, SQLite
- PDF, TXT, and DOCX upload with chunking and vector indexing
- Gemini generation with OpenAI fallback and local fallback when no key is configured
- Risk classifier for cyber, physical, emergency, ethics, bullying, theft, suspicious activity, and harassment
- Animated circular SpideySense Risk Meter
- Retrieved evidence cards with source, chunk, and similarity score
- Chat history, incident PDF export, voice input, dark/light mode
- WebSocket live updates for chat and indexing events
- Secure upload validation, CORS, API-key env vars, rate limiting

## Project Structure

```text
frontend/
  src/
    api/
    components/
    hooks/
    pages/
backend/
  routes/
  services/
  uploads/
  vectorstore/
  models/
  data/
```

## Backend Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Add a Gemini key to `backend/.env` for best answers:

```env
GEMINI_API_KEY=your_key_here
LLM_PROVIDER=gemini
```

Or use OpenAI fallback:

```env
OPENAI_API_KEY=your_key_here
LLM_PROVIDER=openai
```

The app still runs without LLM keys using the local rule-based safety fallback.

## Frontend Setup

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## API

- `POST /chat`
- `POST /upload`
- `GET /history`
- `GET /health`
- `GET /stats`
- `GET /reports/{incident_id}.pdf`
- `WS /ws`

## Example Chat Request

```json
{
  "message": "I received an email asking me to share my OTP to avoid account suspension.",
  "top_k": 4
}
```

## Notes

The first backend run downloads the SentenceTransformers embedding model. Keep `backend/uploads`, `backend/vectorstore`, and `backend/data` for local persistence.
