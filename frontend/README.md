# SuperDocs Frontend

React frontend for the SuperDocs document-analysis application.

## Tech Stack
- React
- Vite
- JavaScript
- Tailwind CSS
- Axios

## Responsibilities
- Creating document piles
- Uploading documents
- Managing selected files before upload
- Asking questions about documents
- Viewing generated answers
- Viewing document sources
- Viewing findings
- Monitoring agent progress
- Approving or rejecting human-review requests

## Project Structure

```text
frontend/
├── src/
│   ├── api/
│   ├── components/
│   ├── context/
│   └── ...
├── public/
├── package.json
└── README.md
```

## Setup

```bash
npm install
```

## Run

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## Backend Connection

The frontend communicates with the FastAPI backend through Axios.

API configuration is centralized in:

```text
src/api/
```

Shared application state is managed through:

```text
src/context/
```

## Main User Flow

```text
Create Pile
    ↓
Upload Documents
    ↓
Ask Question
    ↓
View Agent Progress
    ↓
View Answer + Sources
    ↓
Review Finding
    ↓
Approve / Reject
```

## Production Build

```bash
npm run build
```

Preview locally:

```bash
npm run preview
```
