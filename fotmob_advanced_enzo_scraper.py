import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

PLAYER_ID = "1137705"  # Enzo Fernandez
PROFILE_URL = f"https://www.fotmob.com/players/{PLAYER_ID}"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
]

def random_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9"
    }

def fetch_profile_page():
    resp = requests.get(PROFILE_URL, headers=random_headers())
    resp.raise_for_status()
    return resp.text

def parse_matches(html):
    soup = BeautifulSoup(html, "html.parser")
    matches = []
    # The selector logic below is a starting point. You may need to update it
    # by inspecting FotMob structure for the current season.
    for match_row in soup.select('a[href*="/matches/"]'):
        date = match_row.select_one('span')
        date = date.text.strip() if date else ""
        comp = ""  # Competition info may be elsewhere, left blank for now
        opponent = ""
        score = ""
        # Try to extract opponent and score from match_row.text or sub-elements
        text = match_row.text.strip()
        if "vs" in text:
            parts = text.split("vs", 1)
            opponent = parts[1].split()[0] if len(parts) > 1 else ""
        # Detect Player of the Match indicator (may need adjustment!)
        motm = False
        if match_row.select_one('svg[data-testid="StarIcon"]') or "Player of the Match" in text or "MOTM" in text:
            motm = True
        matches.append({
            "date": date,
            "competition": comp,
            "opponent": opponent,
            "score": score,
            "player_of_the_match": motm
        })
    return matches

def main():
    print("Fetching Enzo Fernandez FotMob match data (HTML scraping method)...")
    html = fetch_profile_page()
    matches = parse_matches(html)
    motm_matches = [m for m in matches if m['player_of_the_match']]
    print(f"\nFound {len(motm_matches)} 'Player of the Match' awards:")
    for match in motm_matches:
        print(f"{match['date']} | {match['competition']} | vs {match['opponent']} | {match['score']}")
    df = pd.DataFrame(matches)
    df.to_csv("enzo_fernandez_matches_2025_2026.csv", index=False)
    print("Exported to enzo_fernandez_matches_2025_2026.csv")

if __name__ == "__main__":
    main()
