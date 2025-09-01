import requests
import pandas as pd

PLAYER_ID = "1137705"  # Enzo Fernandez
API_URL = f"https://www.fotmob.com/api/playerData?id={PLAYER_ID}"

def main():
    print("Fetching Enzo Fernandez FotMob match data (API method)...")
    resp = requests.get(API_URL)
    resp.raise_for_status()
    data = resp.json()
    matches = []
    # Try to extract all seasons and matches
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
