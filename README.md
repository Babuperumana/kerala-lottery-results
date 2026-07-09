# 🎟️ Kerala State Lottery Live 1st Prize Tracker

A real-time, automated web dashboard and background scraper that tracks and displays the Kerala State Lottery 1st prize winning ticket as the draw unfolds. It polls official feeds, parses live results, and displays them on a premium, responsive web interface.

---

## ✨ Features

- **🔄 Real-Time Live Scraping**: A background worker scans the official Blogger feed every 20 seconds for active lottery posts and parses the results dynamically.
- **🏷️ Smart Text Extraction**: Automatically extracts the 1st prize winning ticket (e.g., `XX 123456`), draw date, draw code (e.g., `SS-527`), and lottery name (e.g., `Sthree Sakthi`) using Python's `BeautifulSoup4` and regex.
- **💡 Responsive Modern Dashboard**: A dark-themed dashboard featuring ambient glowing orbs, a starry overlay, and a premium digital display.
- **⚡ Active Polling & Transitions**: The web frontend auto-polls the local API endpoint every 30 seconds and transitions between the "Waiting" (pulsing) and "Winner Announced" (gold glowing) states with smooth CSS fade/blur effects.
- **📜 History Grid**: Shows cards for the previous 3 completed lottery draws for quick reference.
- **⚙️ Multi-thread Safe Execution**: Uses `APScheduler` to run the background job, carefully managed to prevent duplicate thread instantiation in Flask's debug environment.

---

## 🛠️ Technology Stack

### Backend
- **Python 3**: Core application logic.
- **Flask**: Web server framework for serving the dashboard and API endpoint.
- **APScheduler**: Manages the periodic background scraper tasks in a separate thread.
- **BeautifulSoup4 & Requests**: Fetches and parses XHTML/XML blogger feeds for live results.

### Frontend
- **HTML5 & Vanilla CSS3**: Fluid layouts, CSS custom variables, and keyframe animations for a premium user experience.
- **Vanilla JavaScript**: Handles client-side API requests, countdown tickers, and state transitions.
- **Google Fonts**: [Outfit](https://fonts.google.com/specimen/Outfit) for smooth UI copy and [Rajdhani](https://fonts.google.com/specimen/Rajdhani) for a bold digital lottery machine number aesthetic.

---

## 📂 Project Structure

```text
├── LotteryApp/
│   ├── app.py              # Main Flask application with scheduler setup
│   ├── scraper.py          # Blogger RSS parser & HTML parser logic
│   ├── templates/
│   │   └── index.html      # Main dashboard HTML template
│   ├── static/
│   │   ├── style.css       # Custom styles, animations, & design tokens
│   │   └── script.js       # Client polling, countdown & UI updates
│   └── data/
│       └── result.json     # Cached result file containing active draw & history
├── requirements.txt        # Project python packages list
├── .gitignore              # Files to ignore in git repository
└── README.md               # Project documentation
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+ installed on your system.

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

4. **Run the Application**
   ```bash
   python LotteryApp/app.py
   ```
   The application will start, launching both the background scraping daemon and the Flask web server on port `5000`.

5. **Access the Dashboard**
   Open your browser and navigate to:
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📡 API Endpoints

The web application exposes a simple JSON API:

### `GET /api/result`

Returns the active draw state and a list of the 3 most recent historical draws.

**Response Schema (`result.json`):**
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

## ⏰ Schedule Details

Draw announcements in Kerala start around **3:00 PM IST** daily and conclude around **4:30 PM IST**.
- During this window, if the scraper detects a post for today's lottery that hasn't published results yet, it displays a **"Waiting for Live Result..."** state on the screen with an active pulsing animation.
- When the first prize winner is published on the feed, the site automatically receives the update, flashes the green/gold neon lighting, displays the number, and archives the previous active draw to the history view.
- Outside of draw hours, the dashboard displays the latest available completed draw as the active display.

---

## ⚠️ Disclaimer

This application is for informational purposes only. It is an unofficial helper tool and is not associated with or endorsed by the Kerala State Lotteries Department. Always cross-verify the winning numbers with the official Kerala Government Gazette.