# Kerala State Lottery Live Prize Tracker

A web-based dashboard and scraper designed to monitor and display the Kerala State Lottery prize winning numbers in real-time. It retrieves live results from target blog feeds, updates a local data cache, and serves a modern single-page dashboard.

---

## Features

- **Live Scraping**: Runs a background worker that polls the Blogger feed every 20 seconds to fetch updates during active draw hours.
- **Parsing and Extraction**: Extracts the first prize ticket number, date, draw code (e.g., SS-527), and name of the lottery using BeautifulSoup and regular expressions.
- **Web Dashboard**: Displays the active draw status with a countdown timer showing the next automated refresh.
- **State Handling**: Transitions automatically between a waiting state (when a draw is active but results are not yet published) and a completed state (when the winning ticket is extracted).
- **Recent History**: Keeps track of the last three lottery draws.
- **Background Scheduler**: Managed via APScheduler, configured to run safely within Flask's development server without spawning duplicate threads.

---

## Technology Stack

### Backend
- **Python 3**: Application runtime.
- **Flask**: Serves the frontend web pages and API.
- **APScheduler**: Manages the periodic scraping cycles.
- **BeautifulSoup4 & Requests**: Handles fetching and parsing of HTML/feed data.

### Frontend
- **HTML5 & CSS3**: Responsive styling, custom fonts, layout, and visual transitions.
- **Vanilla JavaScript**: Controls the polling timer, fetches data, and updates page content.
- **Google Fonts**: Uses Outfit for general layout text and Rajdhani for the large prize numbers.

---

## Project Structure

```text
├── LotteryApp/
│   ├── app.py              # Flask server and background scheduler
│   ├── scraper.py          # Data fetching and parsing logic
│   ├── templates/
│   │   └── index.html      # Main dashboard HTML template
│   ├── static/
│   │   ├── style.css       # Layout styles and animations
│   │   └── script.js       # Client-side polling and DOM updates
│   └── data/
│       └── result.json     # JSON cache containing active draw and history
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

4. **Run the Server**
   ```bash
   python LotteryApp/app.py
   ```
   This will start both the Flask web server on port `5000` and the background scraper thread.

5. **Open the Dashboard**
   Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

---

## API Endpoints

### GET /api/result

Returns the current active draw status and a list of the three most recent historical draws.

**Example Response:**
```json
{
  "firstPrize": "ST 308060",
  "updated": "07:59 PM",
  "lottery": "Sthree Sakthi (SS-527)",
  "date": "07-07-2026",
  "history": [
    {
      "lottery": "Bhagyathara",
      "code": "BT-61",
      "date": "06-07-2026",
      "firstPrize": "BG 906028"
    },
    ...
  ]
}
```

---

## Draw Schedule and Behavior

Kerala State Lottery draws generally start around **3:00 PM IST** daily and conclude around **4:30 PM IST**.
- During the draw window, if a blog post exists for the day's lottery but the final result is pending, the dashboard displays a "Waiting for Live Result..." status with a loading indicator.
- Once the first prize winning ticket is published on the source feed, the scraper updates the JSON cache, the frontend displays the new prize number, and the previous active draw is added to the history view.
- Outside of active draw hours, the dashboard displays the most recent completed draw.

---

## Disclaimer

This project is for informational purposes only. It is an unofficial helper tool and is not associated with, authorized, or endorsed by the Kerala State Lotteries Department. Always verify winning numbers with the official Kerala Government Gazette.
