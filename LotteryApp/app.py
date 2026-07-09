import os
import json
from datetime import datetime
from flask import Flask, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler

# Import scraper from the local directory
import scraper

app = Flask(__name__)

# Ensure data directory and result.json are initialized
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULT_FILE = os.path.join(BASE_DIR, 'data', 'result.json')

def init_result_file():
    os.makedirs(os.path.join(BASE_DIR, 'data'), exist_ok=True)
    if not os.path.exists(RESULT_FILE):
        with open(RESULT_FILE, 'w') as f:
            json.dump({
                "firstPrize": "Waiting for Live Result...",
                "updated": "Waiting...",
                "lottery": "Today's Draw",
                "date": "",
                "history": []
            }, f, indent=2)

init_result_file()

@app.route('/')
def index():
    """Render the main index page."""
    return render_template('index.html')

@app.route('/api/result')
def get_result():
    """API endpoint to get the latest lottery result and history."""
    try:
        if os.path.exists(RESULT_FILE):
            with open(RESULT_FILE, 'r') as f:
                data = json.load(f)
            return jsonify({
                "firstPrize": data.get("firstPrize", "Waiting for Live Result..."),
                "updated": data.get("updated", "Waiting..."),
                "lottery": data.get("lottery", "Today's Draw"),
                "date": data.get("date", ""),
                "history": data.get("history", [])
            })
    except Exception as e:
        print(f"[Server] Error reading result file: {e}")
        
    return jsonify({
        "firstPrize": "Waiting for Live Result...",
        "updated": "Error reading database",
        "lottery": "Today's Draw",
        "date": "",
        "history": []
    }), 500

def scheduled_scraping_job():
    """Triggered by APScheduler to run a single cycle of the scraper."""
    try:
        scraper.run_scraper_cycle()
    except Exception as e:
        print(f"[Server Scheduler] Error running scraper cycle: {e}")

# APScheduler initialization
# Flask with use_reloader=True spawns a child process. We only want to start the 
# background scheduler in the main worker thread, designated by WERKZEUG_RUN_MAIN.
if os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or not app.debug:
    scheduler = BackgroundScheduler()
    # Run the scraping cycle every 20 seconds as requested
    scheduler.add_job(func=scheduled_scraping_job, trigger="interval", seconds=20, next_run_time=datetime.now())
    scheduler.start()
    print("[Server] Background scraping scheduler started successfully.")

if __name__ == '__main__':
    # Start the Flask app on local port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
