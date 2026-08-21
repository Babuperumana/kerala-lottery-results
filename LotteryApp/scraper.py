import os
import re
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timezone, timedelta

# Define paths relative to this script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULT_FILE = os.path.join(BASE_DIR, 'data', 'result.json')

# Target patterns
TICKET_PATTERN = re.compile(r'\b([A-Za-z]{2})\s?(\d{6})\b')
DATE_PATTERN = re.compile(r'\b\d{2}-\d{2}-\d{4}\b')

# Standard weekly lotteries list for lookup/fallback
LOTTERY_NAMES = [
    "Sthree Sakthi", "Akshaya", "Karunya Plus", "Karunya", 
    "Fifty Fifty", "Bhagyathara", "Win Win", "Nirmal", 
    "Samrudhi", "Suvarna Keralam", "Dhanalekshmi"
]

def parse_result_from_html(html_content):
    """
    Parse the 1st prize ticket number from the post body HTML.
    Finds the '1st Prize' text label and locates the closest ticket pattern after it.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style tags to clear garbage strings
    for s in soup(["script", "style"]):
        s.decompose()
        
    all_elements = list(soup.find_all(string=True))
    
    first_prize = None
    for idx, el in enumerate(all_elements):
        text_lower = el.lower().strip()
        if "1st prize" in text_lower:
            # Look ahead in the DOM (up to 20 text elements) for a ticket number match
            for j in range(1, 20):
                if idx + j < len(all_elements):
                    candidate = all_elements[idx + j].strip()
                    if not candidate:
                        continue
                    match = TICKET_PATTERN.search(candidate)
                    if match:
                        # Format standard ticket number: 'XX 123456'
                        first_prize = f"{match.group(1).upper()} {match.group(2)}"
                        break
            if first_prize:
                break
    return first_prize

def get_feed_data():
    """
    Fetch the latest entries from the Blogger feed.
    Parses and returns a list of dictionaries with draw metadata.
    """
    url = "https://www.keralalotteries.net/feeds/posts/default?alt=json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"[Scraper] Failed to fetch feed. Status code: {response.status_code}")
            return []
            
        data = response.json()
        entries = data.get("feed", {}).get("entry", [])
        parsed_draws = []
        
        for entry in entries:
            title = entry.get("title", {}).get("$t", "")
            # We only parse posts that contain a draw date in the title
            if not DATE_PATTERN.search(title):
                continue
                
            content_obj = entry.get("content", {})
            html_content = content_obj.get("$t", "")
            if not html_content:
                continue
                
            # Extract winning 1st prize
            first_prize = parse_result_from_html(html_content)
            
            # Extract date (DD-MM-YYYY)
            date_match = re.search(r'\b(\d{2})-(\d{2})-(\d{4})\b', title)
            draw_date = ""
            if date_match:
                draw_date = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
                
            # Extract draw code (e.g., SS-527)
            code_match = re.search(r'\b([A-Za-z]{2,3})\s*[-.]?\s*(\d{2,4})\b', title)
            draw_code = ""
            if code_match:
                prefix = code_match.group(1).upper()
                if prefix not in ["PM", "AM", "RS", "NO"]:
                    draw_code = f"{prefix}-{code_match.group(2)}"
                    
            # Extract lottery name
            lottery_name = "Kerala Lottery"
            for name in LOTTERY_NAMES:
                if name.lower() in title.lower():
                    lottery_name = name
                    break
                    
            parsed_draws.append({
                "lottery": lottery_name,
                "code": draw_code,
                "date": draw_date,
                "firstPrize": first_prize
            })
            
        return parsed_draws
    except Exception as e:
        print(f"[Scraper] Error fetching or parsing feed: {e}")
        return []

def load_result():
    """Load current result JSON file."""
    if os.path.exists(RESULT_FILE):
        try:
            with open(RESULT_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "firstPrize": "Waiting for Live Result...",
        "updated": "Waiting...",
        "lottery": "Today's Draw",
        "date": "",
        "history": []
    }

def save_result(data):
    """Save results dictionary to JSON file."""
    os.makedirs(os.path.dirname(RESULT_FILE), exist_ok=True)
    with open(RESULT_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def run_scraper_cycle():
    """
    Fetches latest entries, extracts the most recent 7 completed draws,
    and saves them as a JSON list.
    """
    parsed_draws = get_feed_data()
    if not parsed_draws:
        print("[Scraper] No draw data retrieved from feed.")
        return
        
    # Filter only completed draws (where firstPrize is found)
    completed_draws = [d for d in parsed_draws if d.get("firstPrize")]
    
    # Keep only the latest 7 results
    latest_seven = completed_draws[:7]
    
    save_result(latest_seven)
    print(f"[Scraper] Result updated in JSON. {len(latest_seven)} records saved.")

if __name__ == "__main__":
    run_scraper_cycle()
