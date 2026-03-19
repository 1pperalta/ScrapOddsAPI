# ScrapOddsAPI

Full-stack platform that scrapes, stores, and analyzes sports betting odds in real time using a LangGraph AI agent powered by DeepSeek V3.1.

## Architecture

```
The Odds API --> Python Scraper --> PostgreSQL --> Flask + LangGraph Agent --> React Frontend
                                                       |
                                              ChromaDB (RAG) + football-data.org
```

| Layer | Technology |
|-------|-----------|
| Data source | [The Odds API](https://the-odds-api.com/) |
| Scraper | Python 3.11+, httpx, pandas |
| Database | PostgreSQL 15+ (Docker) |
| Backend | Flask, LangGraph, DeepSeek V3.1 (OpenRouter), psycopg2 |
| RAG | ChromaDB, sentence-transformers |
| Live data | [football-data.org](https://www.football-data.org/) (standings, scorers) |
| Frontend | React 18, Vite, TailwindCSS |

## Project Structure

```
ScrapOddsAPI/
├── scrapping/                   # Data collection scripts
│   ├── odds_scraper.py
│   └── rag/                     # RAG context builder
├── odds-agent/
│   ├── backend/server_py/       # Flask API + LangGraph agent
│   │   ├── app.py               # API routes
│   │   ├── graph.py             # LangGraph state graph
│   │   ├── budget.py            # Cost tracking
│   │   ├── tools/               # Agent tools (odds, RAG, football-data)
│   │   └── services/            # Data services
│   └── frontend/                # React application
├── pyproject.toml               # Python dependencies (uv)
├── docker-compose.yml
└── README.md
```

## Supported Leagues

Premier League, La Liga, Serie A, Bundesliga, Ligue 1, Champions League.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (fast Python package manager)
- Node.js 18+
- Docker Desktop
- API keys: [The Odds API](https://the-odds-api.com/), [OpenRouter](https://openrouter.ai/keys), [football-data.org](https://www.football-data.org/client/register)

## Setup

```bash
git clone <your-repo-url>
cd ScrapOddsAPI

# Environment variables
cp .env.example .env   # fill in your API keys

# Install Python dependencies
uv sync

# Start database
docker-compose up -d

# Run scraper
uv run python scrapping/odds_scraper.py

# Frontend dependencies
cd odds-agent/frontend
npm install
```

## Agent Output Format
The LangGraph agent is instructed to return structured markdown sections (headings and short lists), typically using:
- `## Resumen`
- `## Mejores Opciones`
- `## Justificacion`
- `## Datos Usados`

The frontend (`odds-agent/frontend/src/components/OddsDisplay.jsx`) renders these sections into a clean, sorted layout.

## Budget Controls
Budget is enforced server-side before each LLM call, and usage is persisted to `budget_state.json` by the backend.

Configure via environment variables in your `.env`:
- `BUDGET_LIMIT_USD` (default: `5.0`) - total spend cap
- `DAILY_LIMIT_USD` (default: `1.0`) - daily spend cap
- `MAX_OUTPUT_TOKENS` (default: `800`) - cap for LLM output size

Check current status at `GET /api/budget`.

## LangGraph Flow
See the current node/tool loop diagram in [`docs/langgraph-map.md`](docs/langgraph-map.md).

## Running

**Backend:**
```bash
uv run python odds-agent/backend/server_py/app.py
```

**Frontend:**
```bash
cd odds-agent/frontend
npm run dev
```

Access at `http://localhost:3000`.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/budget` | GET | Budget usage and remaining balance |
| `/api/agent/analyze-team` | POST | Analyze a specific team |
| `/api/agent/analyze-match` | POST | Analyze a specific match |
| `/api/agent/value-bets` | POST | Get value bets |
| `/api/agent/process` | POST | Natural language query |
| `/api/agent/direct-search` | POST | Direct match search |

## Notes

- The Odds API free tier: 500 requests/month.
- OpenRouter budget is tracked automatically. Check `/api/budget` for usage.
- Data persists in Docker volumes.
- This project is for educational purposes.

## License

Educational use. Respect the terms of service of The Odds API, OpenRouter, and football-data.org.
