# Kerala State Lottery Results Scraper

A Python script designed to scrape and extract the latest Kerala State Lottery prize winning numbers. It retrieves live results from target blog feeds, parses the data, and saves the 7 most recent completed draws to a local JSON file.

---

## Features

- **Feed Polling**: Fetches the latest entries from the Blogger feed.
- **Parsing and Extraction**: Extracts the first prize, consolation prizes, and other prize tiers, along with the date, draw code (e.g., SS-527), and name of the lottery using BeautifulSoup and regular expressions.
- **Data Caching**: Saves the most recent 7 completed draws into a `result.json` file.

---

## Technology Stack

- **Python 3**: Application runtime.
- **BeautifulSoup4 & Requests**: Handles fetching and parsing of HTML/feed data.

---

## Project Structure

```text
├── scraper.py              # Data fetching and parsing logic
├── result.json             # JSON cache containing the latest completed draws
├── requirements.txt        # Python package dependencies
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation
```

---

## Setup and Installation

### Prerequisites
- Python 3.8 or higher installed.

### Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd kerala-lottery-results
   ```

2. **Create and Activate Virtual Environment**
   On Windows:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   On macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Scraper**
   ```bash
   python scraper.py
   ```
   This will fetch the latest results and save them to `result.json`. You can set this script up to run periodically using a cron job or task scheduler.

---

## Output Data Format

The scraper saves the data as a JSON list in `result.json`.

**Example Output:**
```json
[
  {
    "lottery": "Bhagyathara",
    "code": "BT-68",
    "date": "24-08-2026",
    "prizes": {
      "1st Prize": {
        "details": "1st Prize :",
        "numbers": [
          "BW 585405"
        ]
      },
      "Consolation Prize": {
        "details": "Consolation Prize",
        "numbers": [
          "BN 585405"
        ]
      }
    }
  }
]
```

---

## Disclaimer

This project is for informational purposes only. It is an unofficial helper tool and is not associated with, authorized, or endorsed by the Kerala State Lotteries Department. Always verify winning numbers with the official Kerala Government Gazette.
