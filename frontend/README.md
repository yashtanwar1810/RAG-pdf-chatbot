# Frontend (TypeScript + Tailwind + shadcn-style UI)

## Setup

1. `cd frontend`
2. `npm install`
3. Ensure `.env` has:
   - `VITE_API_BASE_URL=http://localhost:8000/api/v1`
4. `npm run dev`

## Backend Connection

The frontend is already wired to call:
- `POST /upload`
- `POST /chat`
- `GET /documents`
- `DELETE /documents/{document_id}`

through `VITE_API_BASE_URL`.

## Environment

- `VITE_API_BASE_URL` backend base URL (`/api/v1` included)
- `VITE_REQUIRE_API_KEY` `true` or `false`
- `VITE_APP_API_KEY` required when API key auth is enabled

## Styling

- Tailwind CSS via `tailwind.config.js` + `postcss.config.js`
- Reusable shadcn-style primitives in `src/components/ui/`

## Quality Gates

- `npm run lint`
- `npm run test`
- `npm run build`
