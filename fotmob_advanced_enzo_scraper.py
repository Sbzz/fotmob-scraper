import requests
from bs4 import BeautifulSoup
import random
import time
import pandas as pd

PLAYER_ID = "1137705"  # Enzo Fernandez
BASE_PROFILE_URL = f"https://www.fotmob.com/players/{PLAYER_ID}"
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
    resp = requests.get(BASE_PROFILE_URL, headers=random_headers())
    resp.raise_for_status()
    return resp.text

def parse_matches(html):
    soup = BeautifulSoup(html, "html.parser")
    # Inspect the FotMob page for the correct selectors!
    matches = []
    # Example: You may need to update the following selectors.
    for match_row in soup.select('a[href*="/matches/"]'):
        # Extract match details
        date = match_row.select_one('span[class*="MatchDate"]').text.strip() if match_row.select_one('span[class*="MatchDate"]') else ""
        comp = match_row.select_one('span[class*="MatchLeagueName"]').text.strip() if match_row.select_one('span[class*="MatchLeagueName"]') else ""
        opponent = match_row.select_one('span[class*="MatchOpponentName"]').text.strip() if match_row.select_one('span[class*="MatchOpponentName"]') else ""
        score = match_row.select_one('span[class*="MatchScore"]').text.strip() if match_row.select_one('span[class*="MatchScore"]') else ""
        # Detect Player of the Match: look for star icon or MOTM label
        motm = False
        if match_row.select_one('svg[data-testid="StarIcon"]') or "Player of the Match" in match_row.text or "MOTM" in match_row.text:
            motm = True
        matches.append({
            "date": date,
            "competition": comp,
            "opponent": opponent,
            "score": score,
            "player_of_the_match": motm
        })
    return matches

def filter_current_season(matches, season_str="2025/2026"):
    # Optionally, you can refine this function based on how FotMob formats dates/seasons
    return [m for m in matches if season_str in m.get("competition", "") or season_str in m.get("date", "")]

def main():
    print("Fetching Enzo Fernandez FotMob match data...")
    html = fetch_profile_page()
    matches = parse_matches(html)
    # Optionally, filter for the current season
    # matches = filter_current_season(matches)
    motm_matches = [m for m in matches if m['player_of_the_match']]
    print(f"\nFound {len(motm_matches)} 'Player of the Match' awards:")
    for match in motm_matches:
        print(f"{match['date']} | {match['competition']} | vs {match['opponent']} | {match['score']}")
    # Export to CSV (optional)
    export = input("Export full match data to CSV? (y/n): ")
    if export.lower().startswith('y'):
        df = pd.DataFrame(matches)
        df.to_csv("enzo_fernandez_matches_2025_2026.csv", index=False)
        print("Exported to enzo_fernandez_matches_2025_2026.csv")

if __name__ == "__main__":
    main()
