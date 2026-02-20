import streamlit as st
from scam_detector import analyze_message

st.title("Teen Scam Detector 🚨")

msg = st.text_input("Paste a message or link")

if st.button("Scan"):
    risk, score, reasons = analyze_message(msg)
    st.write("Result:", risk)
    st.write("Risk Score:", score)
    for r in reasons:
        st.write("-", r)