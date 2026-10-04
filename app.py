import streamlit as st
from scam_detector import analyze_message, explain

st.title("Teen Scam Detector 🚨")

msg = st.text_area("Paste a message or link")

if st.button("Scan"):
    result = analyze_message(msg)
    st.write("Result:", result.label)
    st.write("Risk Score:", result.score)
    for r in result.reasons:
        st.write("-", r)
    for e in explain(result):
        st.write("💡", e)
