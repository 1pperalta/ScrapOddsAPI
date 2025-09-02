# Premier League Odds Agent 🏆⚽

A modern React application that uses AI to help users find and compare Premier League betting odds across multiple regions and bookmakers.

## 🚀 Features

- **🤖 AI-Powered Search**: Natural language queries using LangGraph integration
- **📊 Real-time Odds**: Fetches odds from multiple regions (US, UK, AU, EU)
- **🎯 Smart Matching**: Intelligent team name recognition and match finding
- **📱 Responsive Design**: Modern UI with TailwindCSS
- **🔍 Advanced Filtering**: Sort and filter odds by various criteria
- **📈 Odds Comparison**: Detailed comparison with implied probabilities

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **TailwindCSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls

### Backend
- **Express.js** - Node.js web framework
- **LangGraph Integration** - AI agent for natural language processing
- **The Odds API** - Real-time sports betting odds
- **Hugging Face** - Free AI model for text processing

## 📋 Prerequisites

- Node.js 18+ and npm
- The Odds API key (get from [the-odds-api.com](https://the-odds-api.com/))
- Hugging Face API key (optional, for enhanced AI features)

## 🔧 Installation & Setup

### 1. Clone or Navigate to Project
```bash
cd odds-agent-react
```

### 2. Install Dependencies
```bash
# Install both frontend and backend dependencies
npm install
```

### 3. Environment Configuration
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys:
# ODDS_API_KEY=your_odds_api_key_here
# HUGGING_FACE_API_KEY=your_huggingface_api_key_here (optional)
# PORT=5000
```

### 4. Copy Your Existing API Key
```bash
# Copy your API key from the parent directory
cp ../.env .env
# Then edit .env to add any missing variables
```

## 🎯 Running the Application

### Development Mode (Recommended)

**Terminal 1: Start Backend Server**
```bash
npm run server
```
This starts the Express server on http://localhost:5000

**Terminal 2: Start Frontend Development Server**
```bash
npm run dev
```
This starts the React app on http://localhost:3000

### Production Mode
```bash
# Build the frontend
npm run build

# Start the backend (will also serve built frontend)
npm run server
```

## 🎮 Usage

### Natural Language Search
- "Show me odds for Arsenal vs Chelsea"
- "What are the odds for Manchester United's next match?"
- "Give me Liverpool odds"

### Direct Match Search
- "Arsenal vs Chelsea"
- "Man City vs Tottenham"
- "Liverpool vs Arsenal"

## 📁 Project Structure

```
odds-agent-react/
├── src/                          # React frontend
│   ├── components/              # React components
│   │   ├── Header.jsx
│   │   ├── SearchForm.jsx
│   │   ├── OddsDisplay.jsx
│   │   ├── MatchCard.jsx
│   │   ├── OddsComparison.jsx
│   │   └── LoadingSpinner.jsx
│   ├── hooks/                   # Custom React hooks
│   │   └── useOddsData.js
│   ├── services/               # API service layer
│   │   ├── oddsService.js
│   │   └── langGraphAgent.js
│   ├── App.jsx                 # Main App component
│   ├── main.jsx               # React entry point
│   └── index.css              # Global styles
├── server/                      # Express backend
│   ├── routes/                 # API routes
│   │   ├── odds.js
│   │   └── agent.js
│   ├── services/              # Business logic
│   │   ├── OddsService.js
│   │   └── LangGraphOddsAgent.js
│   └── index.js               # Server entry point
├── package.json               # Dependencies and scripts
├── vite.config.js            # Vite configuration
├── tailwind.config.js        # TailwindCSS configuration
└── .env                      # Environment variables
```

## 🔌 API Endpoints

### Odds API
- `GET /api/odds` - Get all odds
- `GET /api/odds?match=Arsenal` - Get odds for specific match
- `GET /api/teams` - Get all available teams
- `GET /api/matches` - Get upcoming matches

### Agent API
- `POST /api/agent/process` - Process natural language query
- `POST /api/agent/suggestions` - Get query suggestions
- `POST /api/agent/validate` - Validate if query is Premier League related

## 🎨 UI Components

### SearchForm
- Toggle between natural language and direct search
- Quick search buttons for popular matches
- Real-time validation and suggestions

### OddsDisplay
- Grid layout showing all matches
- Sorting and filtering options
- Click to expand detailed view

### MatchCard
- Match information with kickoff time
- Best odds preview for each outcome
- Region indicators

### OddsComparison
- Detailed odds table with all bookmakers
- Implied probability calculations
- Best odds highlighting

## 🤖 AI Agent Features

### Natural Language Processing
- Extracts team names from conversational queries
- Handles common team aliases (Man City, Spurs, etc.)
- Provides intelligent suggestions

### Fallback Strategy
1. **Simple Pattern Matching** - Fast regex-based extraction
2. **Hugging Face API** - Enhanced processing (if API key provided)
3. **Rule-based Processing** - Reliable fallback method

## 🔧 Configuration

### Odds API Regions
The app fetches odds from multiple regions:
- **US** - American bookmakers
- **UK** - British bookmakers  
- **AU** - Australian bookmakers
- **EU** - European bookmakers

### Supported Markets
- **H2H (Head-to-Head)** - Match winner odds (Home/Draw/Away)

## 🚀 Deployment

### Using Railway, Vercel, or Heroku
1. Push code to GitHub
2. Connect repository to your deployment platform
3. Set environment variables in the platform
4. Deploy with automatic builds

### Manual Deployment
```bash
# Build the app
npm run build

# Start production server
NODE_ENV=production npm run server
```

## 🐛 Troubleshooting

### Common Issues

**1. API Key Errors (422 Unprocessable Entity)**
- Check that your ODDS_API_KEY is correct
- Verify your API key has remaining requests
- Ensure your API plan supports the requested regions

**2. No Odds Data**
- Check if Premier League season is active
- Try different team names or match queries
- Verify your internet connection

**3. AI Agent Not Working**
- The app works without Hugging Face API key (uses fallback)
- Check HUGGING_FACE_API_KEY format if using enhanced AI
- Natural language processing will use rule-based matching as fallback

**4. Port Conflicts**
- Change PORT in .env file if 5000 is occupied
- Update proxy settings in vite.config.js if needed

## 📊 Performance Notes

- **API Rate Limits**: The Odds API has rate limits, the app caches results
- **Multiple Regions**: Fetching from all regions uses more API calls
- **Real-time Data**: Odds are fetched fresh on each search

## 🎯 Next Steps / Enhancements

- [ ] Add betting calculator
- [ ] Historical odds tracking
- [ ] More sports beyond Premier League
- [ ] Live score integration
- [ ] User favorites and alerts
- [ ] Mobile app version

## 📄 License

MIT License - feel free to use this project for learning or commercial purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Built with ❤️ for Premier League fans and developers learning modern React + AI integration**
