# ⚡ Quick Start - ScrapOddsAPI

## 🚀 Start Everything (Daily Use)

### One-Time Setup (First Time Only)

```bash
# 1. Install dependencies
cd ScrapOddsAPI/scrapping
pip install -r requirements.txt

cd ../odds-agent/frontend
npm install

# 2. Create .env file
cd ../../scrapping
cat > .env << EOF
ODDS_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=betting_odds
DB_USER=postgres
DB_PASSWORD=oddsupb
EOF

# Copy .env for backend
cp .env ../odds-agent/backend/server_py/.env
```

---

## 📝 Daily Workflow

### Start Services (3 Terminals)

**Terminal 1 - Database:**
```bash
cd ScrapOddsAPI
docker-compose up -d

# Verify it's running
docker ps | grep betting_odds_db
```

**Terminal 2 - Backend:**
```bash
cd ScrapOddsAPI/odds-agent/backend/server_py
python3 app.py
```

Wait for: `🚀 Starting Flask server on port 3001...`

**Terminal 3 - Frontend:**
```bash
cd ScrapOddsAPI/odds-agent/frontend
npm run dev
```

Wait for: `Local: http://localhost:3000/`

### Access Application

Open browser: **http://localhost:3000**

---

## 🔄 Update Odds Data

**Terminal 4 - Run Scrapper:**
```bash
cd ScrapOddsAPI/scrapping
python scrapping.py
```

Run this every few hours to keep odds fresh.

---

## 🛑 Stop Everything

```bash
# Stop frontend: Ctrl+C in Terminal 3
# Stop backend: Ctrl+C in Terminal 2

# Stop database
cd ScrapOddsAPI
docker-compose down
```

---

## 🧪 Quick Tests

```bash
# Test API
curl http://localhost:3001/api/health

# Test database
docker exec -it betting_odds_db psql -U postgres -d betting_odds -c "SELECT COUNT(*) FROM matches;"

# Test scrapper (dry run)
cd scrapping
python -c "from scrapping import test_api_connection; test_api_connection()"
```

---

## 🔧 Quick Fixes

### Port Already in Use

```bash
# Backend port (3001)
kill -9 $(lsof -ti :3001)

# Frontend port (3000)
kill -9 $(lsof -ti :3000)

# PostgreSQL port (5432)
docker-compose down
docker-compose up -d
```

### Database Connection Failed

```bash
# Restart database
docker-compose restart postgres

# Check logs
docker-compose logs postgres
```

### API Key Not Found

```bash
# Check .env exists
ls -la scrapping/.env

# View contents (hide keys)
cat scrapping/.env | grep -v "_KEY"
```

---

## 📊 Useful Commands

```bash
# Check database size
docker exec -it betting_odds_db psql -U postgres -d betting_odds -c "
SELECT 
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"

# Count records
docker exec -it betting_odds_db psql -U postgres -d betting_odds -c "
SELECT 
  'matches' as table, COUNT(*) FROM matches
UNION ALL
SELECT 'odds', COUNT(*) FROM odds
UNION ALL
SELECT 'teams', COUNT(*) FROM teams
UNION ALL
SELECT 'bookmakers', COUNT(*) FROM bookmakers;
"

# Clean old odds (7+ days)
docker exec -it betting_odds_db psql -U postgres -d betting_odds -c "
DELETE FROM odds WHERE collected_at < NOW() - INTERVAL '7 days';
"
```

---

## 🎯 Example Queries

### Frontend UI

**Direct Search:**
- Arsenal vs Chelsea
- Manchester United vs Liverpool
- Real Madrid vs Barcelona

**Natural Language:**
- Analiza el Manchester City
- ¿Cuáles son las mejores apuestas de hoy?
- Dame value bets de la Premier League

### API Calls

```bash
# Analyze team
curl -X POST http://localhost:3001/api/agent/analyze-team \
  -H "Content-Type: application/json" \
  -d '{"team": "Arsenal"}'

# Direct search
curl -X POST http://localhost:3001/api/agent/direct-search \
  -H "Content-Type: application/json" \
  -d '{"home_team": "Arsenal", "away_team": "Chelsea"}'

# Value bets
curl -X POST http://localhost:3001/api/agent/value-bets \
  -H "Content-Type: application/json" \
  -d '{"league": "Premier League"}'
```

---

## 📖 More Info

- **Detailed Setup**: See [SETUP_GUIDE.md](./SETUP_GUIDE.md)
- **Project Overview**: See [README.md](./README.md)
- **Troubleshooting**: See SETUP_GUIDE.md > Troubleshooting section

---

## ⏱️ Time Estimates

- First time setup: ~15 minutes
- Daily startup: ~2 minutes
- Scrapping run: ~3-5 minutes
- Stopping everything: ~30 seconds

---

**💡 Tip:** Keep this file open in a terminal for quick reference!

