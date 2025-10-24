# 🏆 ScrapOddsAPI - Complete Setup Guide

A comprehensive sports betting odds platform with AI-powered analysis using Gemini.

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the Project](#running-the-project)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)
8. [Project Structure](#project-structure)

---

## 🎯 Project Overview

**ScrapOddsAPI** is a three-tier application that:

- **Scraps** live betting odds from The Odds API
- **Stores** data in PostgreSQL database
- **Analyzes** matches using Google's Gemini AI
- **Displays** odds comparisons in a beautiful React frontend

### Architecture

```
The Odds API → Python Scrapper → PostgreSQL → Backend APIs → React Frontend
                                      ↓
                                  Gemini AI Agent
```

### Covered Leagues

- ⚽ **Premier League** (English)
- ⚽ **La Liga** (Spanish)
- ⚽ **Serie A** (Italian)
- ⚽ **Bundesliga** (German)
- ⚽ **Ligue 1** (French)
- ⚽ **Champions League** (European)

---

## 🔧 Prerequisites

Before starting, ensure you have:

### Required Software

- **Python 3.11+** (Python 3.13 recommended)
- **Node.js 18+** and **npm**
- **Docker Desktop** (for PostgreSQL)
- **Git**

### API Keys Needed

1. **The Odds API Key**
   - Sign up at: https://the-odds-api.com/
   - Free tier: 500 requests/month
   
2. **Google Gemini API Key**
   - Get it from: https://aistudio.google.com/app/apikey
   - Free tier available

---

## 📦 Installation

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd ScrapOddsAPI
```

### Step 2: Install Python Dependencies

```bash
# Navigate to scrapping directory
cd scrapping

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

cd ..
```

### Step 3: Install Node.js Dependencies

```bash
# Install frontend dependencies
cd odds-agent/frontend
npm install

cd ../..
```

### Step 4: Install Python Backend Dependencies

```bash
cd odds-agent/backend/server_py
pip install flask flask-cors psycopg2-binary python-dotenv google-generativeai

cd ../../..
```

---

## ⚙️ Configuration

### Step 1: Create Environment File for Scrapping

```bash
cd scrapping
```

Create a file named `.env` with the following content:

```env
# The Odds API Key
ODDS_API_KEY=your_odds_api_key_here

# Google Gemini API Key
GOOGLE_API_KEY=your_gemini_api_key_here

# PostgreSQL Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=betting_odds
DB_USER=postgres
DB_PASSWORD=oddsupb
```

**Replace** `your_odds_api_key_here` and `your_gemini_api_key_here` with your actual API keys!

### Step 2: Create Environment File for Backend Agent

```bash
cd ../odds-agent/backend/server_py
```

Create a file named `.env` with the same content:

```env
# Google Gemini API Key
GOOGLE_API_KEY=your_gemini_api_key_here

# PostgreSQL Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=betting_odds
DB_USER=postgres
DB_PASSWORD=oddsupb
```

---

## 🚀 Running the Project

### Step 1: Start PostgreSQL Database

From the project root directory:

```bash
cd ScrapOddsAPI
docker-compose up -d
```

**Verify it's running:**

```bash
docker ps
```

You should see a container named `betting_odds_db` running.

**Check logs if needed:**

```bash
docker-compose logs postgres
```

### Step 2: Run the Scrapper (First Time)

This will fetch odds data from The Odds API and populate your database.

```bash
cd scrapping

# If using virtual environment, activate it first
source venv/bin/activate  # or: source testenv/bin/activate

# Run the scrapper
python scrapping.py
```

**What to expect:**
- The script will test API connection ✅
- Test database connection ✅
- Fetch odds for all 6 leagues
- Save data to PostgreSQL
- Takes ~2-5 minutes depending on API response time

**Output example:**
```
✅ API working! Found 105 sports
✅ Database connected!
🚀 Starting odds collection at 2025-10-24 20:30:00
📊 Processing league 1/6: Premier League
...
✅ Matches saved: 48
✅ Odds records saved: 1,234
```

### Step 3: Start the Backend Agent (Flask)

Open a **new terminal window**:

```bash
cd ScrapOddsAPI/odds-agent/backend/server_py

# Run the Flask server
python3 app.py
```

**Expected output:**
```
🚀 Starting Flask server on port 3001...
🌐 Server will be available at: http://localhost:3001
🏥 Health check: http://localhost:3001/api/health
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:3001
```

**Test the agent:**

Open your browser and go to: http://localhost:3001/api/health

You should see:
```json
{
  "status": "healthy",
  "agent": "gemini",
  "functions": ["analyze_team", "analyze_match", "value_bets", "process_general"]
}
```

### Step 4: Start the Frontend (React)

Open **another new terminal window**:

```bash
cd ScrapOddsAPI/odds-agent/frontend

# Start the development server
npm run dev
```

**Expected output:**
```
VITE v7.1.12  ready in 237 ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
➜  press h + enter to show help
```

### Step 5: Access the Application

Open your browser and navigate to:

**🌐 http://localhost:3000**

You should see the Odds-Agent interface with:
- Search modes (Natural Language / Direct Search)
- Quick search buttons with real matches
- Beautiful odds comparison UI

---

## ✅ Testing

### Test 1: API Health Check

```bash
curl http://localhost:3001/api/health
```

Expected: `{"status": "healthy", ...}`

### Test 2: Direct Match Search

Try searching in the frontend:
- Click "Búsqueda Directa" (Direct Search)
- Enter: `Arsenal vs Chelsea`
- Click search

You should see:
- Match details
- Kickoff time
- Odds from multiple bookmakers

### Test 3: Natural Language Query

- Switch to "Lenguaje Natural" mode
- Type: `Analiza el Arsenal`
- The AI agent should provide analysis and betting recommendations

### Test 4: Value Bets

```bash
curl -X POST http://localhost:3001/api/agent/value-bets \
  -H "Content-Type: application/json" \
  -d '{"league": "Premier League", "min_value_threshold": 1.05}'
```

Should return AI analysis of best value betting opportunities.

---

## 🐛 Troubleshooting

### Issue: Docker container not starting

**Solution:**
```bash
# Check if Docker Desktop is running
docker --version

# Stop and restart containers
docker-compose down
docker-compose up -d

# Check logs
docker-compose logs postgres
```

### Issue: Port 3001 already in use

**Solution:**
```bash
# Find process using the port
lsof -ti :3001

# Kill the process
kill -9 $(lsof -ti :3001)

# Or change the port in app.py:
# port = int(os.getenv('PORT', 3002))  # Use 3002 instead
```

### Issue: Port 3000 already in use

**Solution:**
```bash
# Kill process on port 3000
kill -9 $(lsof -ti :3000)

# Or run Vite on different port
npm run dev -- --port 3002
```

### Issue: "No module named 'psycopg2'"

**Solution:**
```bash
cd scrapping
pip install psycopg2-binary
```

### Issue: "API key not found"

**Solution:**
- Check that `.env` file exists in `scrapping/` directory
- Verify the file contains `ODDS_API_KEY=...`
- Make sure there are no spaces around the `=` sign
- Check the file is not named `.env.txt` (show hidden files)

### Issue: "Database connection failed"

**Solution:**
```bash
# Check if PostgreSQL container is running
docker ps | grep postgres

# Restart database
docker-compose restart postgres

# Check database logs
docker-compose logs postgres

# Try connecting manually
docker exec -it betting_odds_db psql -U postgres -d betting_odds
```

### Issue: Frontend shows "Network Error"

**Solution:**
- Check that backend is running on port 3001
- Verify in browser console for CORS errors
- Check `.env` variables in frontend if any

### Issue: Scrapper gets rate limited (429 error)

**Solution:**
- The Odds API has rate limits (500 requests/month on free tier)
- Wait a few minutes between runs
- Check your usage at: https://the-odds-api.com/account/
- The script has retry logic built-in

### Issue: No matches found in database

**Solution:**
```bash
# Run the scrapper to populate data
cd scrapping
python scrapping.py

# Check if data was saved
docker exec -it betting_odds_db psql -U postgres -d betting_odds -c "SELECT COUNT(*) FROM matches;"
```

---

## 📁 Project Structure

```
ScrapOddsAPI/
├── scrapping/                      # Data collection layer
│   ├── scrapping.py               # Main scrapper script
│   ├── test.py                    # Test script for API
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # Environment variables (create this!)
│   └── docker-compose.yml         # Local PostgreSQL setup
│
├── odds-agent/
│   ├── backend/
│   │   └── server_py/            # Python/Flask backend
│   │       ├── app.py            # Flask API server
│   │       ├── agent.py          # Gemini AI agent logic
│   │       ├── services/
│   │       │   └── odds_service.py  # Database service layer
│   │       ├── .env              # Backend environment (create this!)
│   │       └── requirements.txt
│   │
│   └── frontend/                 # React frontend
│       ├── src/
│       │   ├── App.jsx           # Main app component
│       │   ├── components/       # UI components
│       │   ├── services/         # API services
│       │   └── hooks/            # React hooks
│       ├── package.json
│       └── vite.config.js
│
├── docker-compose.yml            # Full stack orchestration
├── README.md                     # Project overview
└── SETUP_GUIDE.md               # This file!
```

---

## 🔄 Regular Usage Workflow

### Daily Development Workflow

**1. Start everything:**

```bash
# Terminal 1: Start database
docker-compose up -d

# Terminal 2: Start backend agent
cd odds-agent/backend/server_py
python3 app.py

# Terminal 3: Start frontend
cd odds-agent/frontend
npm run dev
```

**2. Update odds data (run every few hours):**

```bash
# Terminal 4
cd scrapping
python scrapping.py
```

**3. Stop everything when done:**

```bash
# Stop frontend: Ctrl+C in Terminal 3
# Stop backend: Ctrl+C in Terminal 2

# Stop database
docker-compose down
```

### Weekend/Weekly Maintenance

```bash
# Update odds data
cd scrapping
python scrapping.py

# Check database size
docker exec -it betting_odds_db psql -U postgres -d betting_odds -c "SELECT COUNT(*) FROM odds;"

# Optional: Clean old odds data (older than 7 days)
# docker exec -it betting_odds_db psql -U postgres -d betting_odds -c "DELETE FROM odds WHERE collected_at < NOW() - INTERVAL '7 days';"
```

---

## 📊 API Endpoints Reference

### Backend (Port 3001)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/agent/analyze-team` | POST | Analyze a specific team |
| `/api/agent/analyze-match` | POST | Analyze a specific match |
| `/api/agent/value-bets` | POST | Get value betting opportunities |
| `/api/agent/process` | POST | Natural language query |
| `/api/agent/direct-search` | POST | Direct match search |

### Example Requests

**Analyze Team:**
```bash
curl -X POST http://localhost:3001/api/agent/analyze-team \
  -H "Content-Type: application/json" \
  -d '{"team": "Arsenal"}'
```

**Direct Search:**
```bash
curl -X POST http://localhost:3001/api/agent/direct-search \
  -H "Content-Type: application/json" \
  -d '{"home_team": "Arsenal", "away_team": "Chelsea"}'
```

---

## 🎓 Learning Resources

### Understanding the Stack

- **The Odds API**: https://the-odds-api.com/liveapi/guides/v4/
- **Flask**: https://flask.palletsprojects.com/
- **React**: https://react.dev/
- **Gemini AI**: https://ai.google.dev/docs
- **PostgreSQL**: https://www.postgresql.org/docs/

### Next Steps

- Set up automated scrapping with cron jobs
- Deploy to production (Heroku, Railway, or AWS)
- Add user authentication
- Implement favorites/watchlist
- Add historical data visualization
- Set up alerts for value bets

---

## 📝 Notes

- **API Costs**: The Odds API free tier has 500 requests/month. Each scrapping run uses ~24 requests (6 leagues × 4 regions). Plan accordingly!
- **Gemini API**: Free tier has generous limits, but monitor usage at https://aistudio.google.com/
- **Database**: PostgreSQL data persists in Docker volumes. To reset: `docker-compose down -v`
- **Development**: The frontend and backend support hot-reload during development

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📧 Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Check Docker logs: `docker-compose logs`
3. Check backend logs in the terminal
4. Check browser console for frontend errors
5. Open an issue on GitHub with detailed error messages

---

## ⚖️ License

This project is for educational purposes. Always respect:
- The Odds API terms of service
- Google Gemini API terms of service
- Responsible gambling practices

---

**Happy Coding! ⚽💰🤖**

