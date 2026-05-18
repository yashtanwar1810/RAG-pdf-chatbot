# Backend RAG API

FastAPI + LangChain-oriented RAG backend for PDF chat with Pinecone namespace strategy.

## Run

```bash
cd backend
.\.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

## Frontend Connection

CORS and API prefix are configured for local frontend development:

- Frontend origin: `http://localhost:5173`
- API base prefix: `/api/v1`

## Endpoints

- `GET /api/v1/health`
- `POST /api/v1/upload` (multipart form field: `file`)
- `POST /api/v1/chat` (json: `{"document_id":"doc_x","question":"...", "top_k":4}`)
- `GET /api/v1/documents`
- `DELETE /api/v1/documents/{document_id}`

## Gemini AI Studio Setup

Set these environment variables in `backend/.env`:

```env
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_gemini_api_key
MODEL_NAME=gemini-2.0-flash
EMBEDDING_MODEL=text-embedding-004
```

You can get your API key from [Google AI Studio](https://aistudio.google.com/).

## Production Notes

- Uses `pypdf` for text extraction, provider-based embeddings/chat (Gemini or OpenAI), Pinecone vectors, and Cloudinary/S3 object storage.
- Set `STORAGE_BACKEND=cloudinary` or `STORAGE_BACKEND=s3`.
- If you set `REQUIRE_API_KEY=true`, provide `APP_API_KEY` and send it as `x-api-key` header.
