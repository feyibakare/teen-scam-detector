# Teen Scam Detector

A Python web app that checks messages for common scam warning signs and explains the risk in simple language for teens. Users can create an account, save their scans, and see stats about what they have checked.

## Features

- **Scan a message or link** and get a risk level (Likely Safe, Possible Scam, High Risk Scam), a score, and the reasons behind it
- **Teen-friendly tips** that explain why each warning sign is dangerous
- **User accounts** with sign up and log in
- **Private scan history** where users can bookmark scans, delete one, or delete everything
- **Dashboard** showing total scans, scans by risk level, scans over the last 7 days, and the most common warning signs
- **Automated tests** with pytest

## How detection works

The detector is rule based. It adds up points for:

- Suspicious words and phrases, like "urgent", "you won", "verify", and "pay immediately". Stronger phrases are worth more points.
- Links, with extra points for shortened links (like bit.ly) because they hide where they go

Keywords are matched as whole words, so "free" is flagged but "freezing" is not. The total score decides the level: 3 or more is High Risk, 2 is Possible Scam, and anything lower is Likely Safe.

## Tech stack

Python, Streamlit, SQLite, pandas, pytest

## Getting started

1. Clone the repo and open the folder
2. Install the requirements:
```
   pip install -r requirements.txt
```
3. Run the app:
```
   python -m streamlit run app.py
```
4. Run the tests:
```
   python -m pytest
```

The database file (`scans.db`) is created automatically the first time you run the app.

## Project structure

```
app.py                  Streamlit interface (login, scanner, history, dashboard)
scam_detector.py        Detection rules and scoring
database.py             SQLite tables and queries
auth.py                 Sign up, log in, password hashing
test_scam_detector.py   Tests for the detector
test_database.py        Tests for the database and per-user access
```

## Security and privacy decisions

- Passwords are never stored. Each one is hashed with scrypt and a random salt, and checked with a constant-time comparison.
- Login gives the same error for a wrong username and a wrong password, so it doesn't reveal which usernames exist.
- All database queries use parameters (`?`), which protects against SQL injection.
- Every query on scans includes the logged-in user's id, so one user cannot see, bookmark, or delete another user's scans. Tests check this.
- Saved messages are shown as plain text so a scam link in your history is never clickable.
- Users can delete their scans at any time, and the database file is kept out of Git.

## Known limitations

- It uses keyword rules, so new scams or cleverly worded ones can slip through, and some harmless messages may get flagged.
- It only reads text. It can't check who really sent a message.
- There is no limit on login attempts, no password reset, and sessions end when the page is refreshed.
- Saved messages are stored unencrypted in a local SQLite file. This is a learning project and is not ready for real users. A deployed version would need HTTPS and a hosted database.
