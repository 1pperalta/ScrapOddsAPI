# Team Setup Guide 🚀

## Quick Setup Commands for Team

### 1. Database Setup
```bash
docker-compose up -d
docker-compose ps
```

### 2. Scraping Data
```bash
cd scrapping/
pip install requests psycopg2-binary python-dotenv pandas
echo "ODDS_API_KEY=your_key_here" > .env
echo "DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/odds_db" >> .env
python scraper.py
cd ..
```

### 3. Backend API
```bash
cd odds-agent/backend/server_py/
pip install flask flask-cors psycopg2-binary python-dotenv google-generativeai
echo "GOOGLE_API_KEY=your_gemini_key_here" > .env
echo "DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/odds_db" >> .env
python app.py
```

### 4. Frontend (New Terminal)
```bash
cd odds-agent/frontend/
npm install
npm start
```

### 5. Verification Commands
```bash
# Check database
docker-compose logs postgres

# Test API health
curl http://localhost:3001/api/health

# Test team analysis
curl -X POST http://localhost:3001/api/agent/analyze-team -H "Content-Type: application/json" -d '{"team": "Arsenal"}'
```

### 6. Access Points
- Frontend: http://localhost:3000
- API: http://localhost:3001  
- Database Admin: http://localhost:8080 (admin@odds.com / admin123)

### 7. API Keys Needed
- Odds API key: https://the-odds-api.com/
- Gemini API key: https://console.cloud.google.com/

### 8. Stop Everything
```bash
docker-compose down
# Ctrl+C in server terminals
```

### 9. Full Restart Script
```bash
# Kill all processes
pkill -f python
pkill -f npm

# Restart database
docker-compose down && docker-compose up -d

# Start backend (in new terminal)
cd odds-agent/backend/server_py/ && python app.py

# Start frontend (in new terminal) 
cd odds-agent/frontend/ && npm start
```

### 10. Troubleshooting
```bash
# If port is busy
lsof -ti :3001
kill -9 $(lsof -ti :3001)

# If database connection fails
docker-compose down
docker-compose up -d

# If import errors
export PYTHONPATH=$PWD:$PYTHONPATH
```
