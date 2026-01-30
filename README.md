# Second Brain Research Dashboard

A generative UI application that transforms Markdown research documents into dynamic, personalized dashboards. Upload research content from your AI assistant and watch it automatically generate an optimal visual layout using intelligent component selection and arrangement.

## Overview

Second Brain Dashboard solves a key problem: Markdown documents are hard to scan, important insights get buried in text, and plain text lacks visual hierarchy. This application takes raw Markdown research and transforms it into beautiful, interactive dashboards.

**Key Innovation: Section-Based Rendering**

Instead of forcing a single layout on entire documents, the dashboard:

1. Parses Markdown into sections (split on H2 headers)
2. Analyzes each section independently to determine its type
3. Selects appropriate components and layout for each section
4. Wraps everything in a flexible document container

This means a single document can have a news section with HeadlineCards, followed by statistics with StatCards, followed by tutorials with StepCards - each rendered optimally for its content type.

## Tech Stack

**Frontend:**
- React with TypeScript
- CopilotKit for generative UI capabilities
- A2UI component library
- TailwindCSS for styling
- Vite as build tool

**Backend:**
- FastAPI (Python)
- Pydantic AI for intelligent content analysis
- OpenRouter API integration with Claude Sonnet 4
- PostgreSQL for data persistence

**Infrastructure:**
- Node.js for frontend development
- Python 3.9+ for backend
- Docker support (optional)

## Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.9+)
- PostgreSQL (optional, for persistence)
- OpenRouter API key for Claude Sonnet 4

### Environment Setup

1. Copy the `.env` file to your project root (provided separately)
2. Required environment variables:
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `OPENROUTER_MODEL`: Model identifier (default: anthropic/claude-sonnet-4)

3. Optional environment variables:
   - `BACKEND_PORT`: FastAPI server port (default: 8000)
   - `NODE_ENV`: Development/production mode (default: development)

### Development Setup

**Option 1: Run both servers together**
```bash
./init.sh
```

**Option 2: Run servers separately**

Frontend (React):
```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:3010
```

Backend (FastAPI):
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
# Runs on http://localhost:8000
```

### Project Structure

```
second-brain-research-dashboard/
├── frontend/               # React TypeScript application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── types/         # TypeScript type definitions
│   │   └── App.tsx        # Main application component
│   ├── package.json
│   └── vite.config.ts
├── backend/                # FastAPI application
│   ├── main.py            # FastAPI entry point
│   ├── agents/            # AI agents for content analysis
│   ├── models/            # Data models
│   ├── routes/            # API endpoints
│   ├── requirements.txt
│   └── .env              # Environment variables
├── .gitignore
├── README.md
└── init.sh               # Development setup script
```

## Configuration

**Frontend dev server:** http://localhost:3010 (Note: not 3000)
**Backend server:** http://localhost:8000
**AG-UI endpoint:** http://localhost:8000/ag-ui/stream

## Contributing

This is a sponsored YouTube demonstration project showcasing CopilotKit's generative UI capabilities with A2UI + AG-UI integration.

## License

See LICENSE file for details.
