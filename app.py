import streamlit as st
from scam_detector import analyze_message, explain, LABELS
from database import (
    init_db, save_scan, get_history,
    toggle_bookmark, delete_scan, delete_all_scans,
)

st.title("Teen Scam Detector 🚨")

msg = st.text_area("Paste a message or link")

if st.button("Scan"):
    result = analyze_message(msg)
    save_scan(msg, result)
    st.write("Result:", result.label)
    st.write("Risk Score:", result.score)
    for r in result.reasons:
        st.write("-", r)
    for e in explain(result):
        st.write("💡", e)

st.subheader("Scan history")
history = get_history()

if not history:
    st.write("No scans yet.")

for h in history:
    col_info, col_star, col_del = st.columns([6, 1, 1])
    star = "⭐" if h["bookmarked"] else "☆"
    col_info.write(f"{LABELS[h['level']]} (score {h['score']}): {h['message'][:60]}")
    if col_star.button(star, key=f"star_{h['id']}"):
        toggle_bookmark(h["id"])
        st.rerun()
    if col_del.button("🗑️", key=f"del_{h['id']}"):
        delete_scan(h["id"])
        st.rerun()

if history and st.button("Delete all history"):
    delete_all_scans()
    st.rerun()
