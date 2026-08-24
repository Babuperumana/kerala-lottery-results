import os
import re
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timezone, timedelta

# Define paths relative to this script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULT_FILE = os.path.join(BASE_DIR, 'result.json')

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
    Parse the 1st prize and all other prizes from the post body HTML.
    Returns a tuple of (first_prize, all_prizes_dict).
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style tags to clear garbage strings
    for s in soup(["script", "style"]):
        s.decompose()
        
    all_elements = [el.strip() for el in soup.find_all(string=True) if el.strip()]
    
    prizes = {}
    current_prize_name = None
    
    prize_keywords = [
        "1st Prize", "2nd Prize", "3rd Prize", "4th Prize", "5th Prize", 
        "6th Prize", "7th Prize", "8th Prize", "9th Prize", "Consolation Prize"
    ]
    
    for i, el in enumerate(all_elements):
        found_header = False
        for kw in prize_keywords:
            if kw.lower() in el.lower() and len(el) < 60 and "repeated" not in el.lower() and "structure" not in el.lower():
                if kw not in prizes:
                    current_prize_name = kw
                    
                    details_str = el.strip()
                    lookahead = 1
                    while i + lookahead < len(all_elements) and lookahead <= 3:
                        next_el = all_elements[i + lookahead].strip()
                        if next_el == "₹" or next_el == ":" or "Rs" in next_el or "/-" in next_el or "Lakhs" in next_el or "Crore" in next_el or re.match(r'^[\d,]+/-', next_el):
                            details_str += " " + next_el
                            lookahead += 1
                        else:
                            break
                            
                    prizes[current_prize_name] = {
                        "details": details_str,
                        "numbers": []
                    }
                    found_header = True
                else:
                    # We already parsed this prize, so ignore this duplicate header
                    current_prize_name = None
                    found_header = True
                break
                
        if found_header:
            continue
            
        if current_prize_name:
            # If we hit footer text, stop parsing prizes completely
            footer_keywords = ['prize structure', 'repeated numbers', 'next ', 'kerala lottery result', 'date:', 'draw results']
            if any(w in el.lower() for w in footer_keywords):
                current_prize_name = None
                continue
                
            if el.startswith("(") and el.endswith(")"):
                continue
            
            # Ignore generic text lines that might contain numbers (like dates, agent info)
            ignore_words = ['result', 'agent', 'agency', 'draw']
            if any(w in el.lower() for w in ignore_words):
                continue
                
            # Explicitly skip if element is a standalone date
            if re.match(r'^\d{2}[-/.]\d{2}[-/.]\d{4}$', el.strip()):
                continue
                
            if current_prize_name in ["1st Prize", "2nd Prize", "3rd Prize", "Consolation Prize"]:
                matches = re.findall(r'[A-Za-z]{2}\s?\d{6}', el)
            else:
                matches = re.findall(r'\b\d{4}\b', el)
                
            if matches:
                prizes[current_prize_name]["numbers"].extend(matches)
                
    return prizes

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
                
            # Extract all prizes
            all_prizes = parse_result_from_html(html_content)
            
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
                "prizes": all_prizes
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
        
    # Filter only completed draws (where 1st Prize is found)
    completed_draws = [d for d in parsed_draws if d.get("prizes") and "1st Prize" in d["prizes"] and d["prizes"]["1st Prize"]["numbers"]]
    
    # Keep only the latest 7 results
    latest_seven = completed_draws[:7]
    
    save_result(latest_seven)
    print(f"[Scraper] Result updated in JSON. {len(latest_seven)} records saved.")

if __name__ == "__main__":
    run_scraper_cycle()
