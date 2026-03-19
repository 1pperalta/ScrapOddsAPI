# ScrapOddsAPI

Full-stack platform that scrapes, stores, and analyzes sports betting odds in real time using AI (Google Gemini).

## Architecture

```
The Odds API --> Python Scraper --> PostgreSQL --> Flask + Gemini --> React Frontend
```

| Layer | Technology |
|-------|-----------|
| Data source | [The Odds API](https://the-odds-api.com/) |
| Scraper | Python 3.11+, httpx, pandas |
| Database | PostgreSQL 15+ (Docker) |
| Backend | Flask, Google Gemini 2.5 Flash, psycopg2 |
| Frontend | React 18, Vite, TailwindCSS |

## Project Structure

```
ScrapOddsAPI/
├── scrapping/                   # Data collection scripts
│   ├── scrapping.py
│   ├── requirements.txt
│   └── .env
├── odds-agent/
│   ├── backend/server_py/       # Flask API + Gemini agent
│   │   ├── app.py
│   │   ├── agent.py
│   │   └── services/
│   └── frontend/                # React application
│       └── src/
├── docker-compose.yml
└── README.md
```

## Supported Leagues

Premier League, La Liga, Serie A, Bundesliga, Ligue 1, Champions League.

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker Desktop
- API keys: [The Odds API](https://the-odds-api.com/), [Google Gemini](https://aistudio.google.com/app/apikey)

## Setup

```bash
git clone <your-repo-url>
cd ScrapOddsAPI

# Environment variables
cd scrapping
cp .env.example .env   # fill in ODDS_API_KEY, GOOGLE_API_KEY, DB_HOST, DB_PASSWORD

# Python dependencies
pip install -r requirements.txt

# Start database
cd ..
docker-compose up -d

# Run scraper
cd scrapping
python scrapping.py

# Frontend dependencies
cd ../odds-agent/frontend
npm install
```

## Running

**Backend:**
```bash
cd odds-agent/backend/server_py
python3 app.py
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
| `/api/agent/analyze-team` | POST | Analyze a specific team |
| `/api/agent/analyze-match` | POST | Analyze a specific match |
| `/api/agent/value-bets` | POST | Get value bets |
| `/api/agent/process` | POST | Natural language query |
| `/api/agent/direct-search` | POST | Direct match search |

## Notes

- The Odds API free tier: 500 requests/month.
- Gemini API has a free tier with generous limits.
- Data persists in Docker volumes.
- This project is for educational purposes.

## License

Educational use. Respect the terms of service of The Odds API and Google Gemini.
