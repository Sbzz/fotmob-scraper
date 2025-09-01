import requests
import pandas as pd

PLAYER_ID = "1137705"
API_URL = f"https://www.fotmob.com/api/playerData?id={PLAYER_ID}"

def main():
    print("Fetching Enzo Fernandez FotMob match data (API method)...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Referer": "https://www.fotmob.com/",
        "Accept": "application/json",
    }
    resp = requests.get(API_URL, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    matches = []
    for season in data.get("seasons", []):
        for match in season.get("matches", []):
            motm = match.get("isPlayerOfTheMatch", False)
            matches.append({
                "date": match.get("matchTimeUTC", ""),
                "competition": match.get("leagueName", ""),
                "opponent": match.get("opponent", ""),
                "score": match.get("scoreStr", ""),
                "player_of_the_match": motm
            })
    motm_matches = [m for m in matches if m['player_of_the_match']]
    print(f"\nFound {len(motm_matches)} 'Player of the Match' awards:")
    for match in motm_matches:
        print(f"{match['date']} | {match['competition']} | vs {match['opponent']} | {match['score']}")
    df = pd.DataFrame(matches)
    df.to_csv("enzo_fernandez_matches_2025_2026.csv", index=False)
    print("Exported to enzo_fernandez_matches_2025_2026.csv")

if __name__ == "__main__":
    main()
