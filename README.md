# Teen Scam Detector
A Python web app that checks a text message for common scam warning signs and explains the risk in simple language for teens.

## What it does
- You paste a message or link and click Scan
- The app gives a risk level (Likely Safe, Possible Scam, or High Risk Scam), a score, and the reasons behind it
- It adds short tips explaining why each warning sign is dangerous

## How it works
The detector is rule based. It looks for:
- Suspicious keywords and phrases such as "urgent", "you won", "verify", and "gift card"
- Links, with extra weight for shortened links (like bit.ly) that hide where they go

Each warning sign adds points to a score, and the score decides the risk level.

## Run it
1. Install Python 3 and then run: `pip install streamlit pytest`
2. Start the app: `python -m streamlit run app.py`
3. Run the tests: `python -m pytest`

## Project files
- `scam_detector.py`: the detection logic
- `app.py`: the Streamlit web interface
- `test_scam_detector.py`: automated tests
- `fake_scams.txt`: sample scam messages
- `old_versions/`: earlier desktop and simulator versions

## Limitations
- It uses keyword rules, so new or cleverly worded scams can slip through
- It can flag harmless messages that happen to contain suspicious words
- It only reads text, not images
