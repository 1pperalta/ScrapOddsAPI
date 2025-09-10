# Premier League Odds Scraper

A Python web scraper that fetches Premier League football odds from The Odds API across multiple regions and bookmakers.

## Features

- 🏈 Scrapes Premier League match odds from multiple regions (US, UK, AU, EU)
- 📊 Exports data to CSV format for analysis
- 🔄 Handles multiple bookmakers and odds formats
- 🌍 Multi-region support for comprehensive odds coverage
- 📈 Structured data output with match details, odds, and bookmaker information

## Setup

### 1. Clone the repository
```bash
git clone <your-repository-url>
cd ScrapOddsAPI
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
ODDS_API_KEY=your_actual_api_key_here
```

### 5. Get API Key
1. Visit [The Odds API](https://the-odds-api.com/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add it to your `.env` file

## Usage

### Run the scraper
```bash
python test.py
```

### Output
The scraper generates CSV files with odds data:
- `premier_league_odds.csv` - Main odds data
- `premier_league_odds_all_regions.csv` - Comprehensive multi-region data

## Data Structure

The CSV output includes:
- **Home Team**: Home team name
- **Away Team**: Away team name
- **Kickoff**: Match start time (ISO format)
- **Bookmaker**: Bookmaker name
- **Outcome**: Match outcome (Home/Away/Draw)
- **Odds**: Decimal odds value
- **Region**: Region code (us/uk/au/eu)

## Example Output
```csv
Home,Away,Kickoff,Bookmaker,Outcome,Odds
Arsenal,Chelsea,2025-09-13T15:00:00Z,Bet365,Arsenal,2.10
Arsenal,Chelsea,2025-09-13T15:00:00Z,Bet365,Chelsea,3.40
Arsenal,Chelsea,2025-09-13T15:00:00Z,Bet365,Draw,3.20
```

## Configuration

### Regions
The scraper supports multiple regions:
- `us` - United States bookmakers
- `uk` - United Kingdom bookmakers  
- `au` - Australian bookmakers
- `eu` - European bookmakers

### Markets
Currently supports:
- `h2h` - Head to Head (Match Winner: Home/Draw/Away)

## API Limits

The Odds API has rate limits:
- Free tier: 500 requests/month
- Monitor your usage in the API dashboard
- The scraper is optimized to minimize API calls

## Dependencies

- `httpx` - HTTP client for API requests
- `pandas` - Data manipulation and CSV export
- `python-dotenv` - Environment variable management
- `numpy` - Numerical operations

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your `.env` file has the correct API key
2. **Rate Limit**: Check your API usage on The Odds API dashboard
3. **Network Issues**: Ensure stable internet connection
4. **CSV Encoding**: Files are saved in UTF-8 format

### Debug Mode
To see detailed API responses, check the console output while the script runs.

## License

This project is for educational and personal use. Please respect The Odds API terms of service.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Note**: This scraper is for educational purposes. Always comply with the terms of service of the APIs you're using.
