# MLB Signal Analyzer

A Python-based web scraper for analyzing MLB signals from Action Network's Sharp Report.

## Features

- Automatically scrapes MLB game data from Action Network
- Detects blue signal indicators for "Pro Signal Action"
- Saves results to Excel format
- Handles authentication and anti-bot detection
- Takes screenshots for verification

## Requirements

- Python 3.8+
- Chrome browser
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mlb-signal-analyzer.git
cd mlb-signal-analyzer
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your Action Network credentials:
```
ACTION_NETWORK_EMAIL=your_email@example.com
ACTION_NETWORK_PASSWORD=your_password
```

## Usage

Run the scraper:
```bash
python action_network_scraper.py
```

The script will:
1. Log in to Action Network
2. Navigate to the MLB Sharp Report
3. Scrape the specified date's data
4. Save results to an Excel file

## Output

The script generates an Excel file with the following columns:
- Date
- Home / Away
- Team
- Big Money
- Sharp Action
- Systems
- Projections
- Top Experts
- SPREAD (+/-1.5)
- PRICE
- Result

## Notes

- The script includes anti-detection measures to avoid being blocked
- Screenshots are taken for verification purposes
- Logs are generated for debugging

## License

MIT License 