# fotmob-scraper
Fotmob scraper test
````markdown name=README.md
# FotMob Advanced Enzo Fernandez Scraper

A Python script to scrape Enzo Fernandez's match data from FotMob, including "Player of the Match" awards, and export the results to a CSV file.  
This script is designed for environments like Render, GitHub Actions, or any other non-interactive Python runtime.

## Features

- Fetches Enzo Fernandez's match data from FotMob
- Detects and marks "Player of the Match" awards
- Outputs all matches and exports to `enzo_fernandez_matches_2025_2026.csv`
- Built for non-interactive/cloud environments (no `input()` prompts)

## Usage

### 1. Clone or Download

Clone this repository to your environment:

```bash
git clone https://github.com/yourusername/fotmob-scraper.git
cd fotmob-scraper
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Run the Script

```bash
python fotmob_advanced_enzo_scraper.py
```

- The script will print the number of "Player of the Match" awards found and export the full match data to `enzo_fernandez_matches_2025_2026.csv`.

### 4. Deploying on Render or Cloud

- Deploy as a background worker or cron job.
- No manual input required.

## Notes

- If FotMob updates their HTML structure, you may need to update the CSS selectors in `fotmob_advanced_enzo_scraper.py`.
- Files written by the script may not persist in some cloud platforms unless uploaded to external storage (S3, etc.).

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies.

## Disclaimer

This script is for educational and personal use only.  
Web scraping may violate FotMob's terms of service. Use responsibly.

````
