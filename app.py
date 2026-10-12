import streamlit as st

from auth import log_in, sign_up
from database import (
    init_db, save_scan, get_history,
    toggle_bookmark, delete_scan, delete_all_scans,
)
from scam_detector import analyze_message, explain, LABELS

init_db()

st.title("Teen Scam Detector 🚨")


def show_login_screen():
    st.subheader("Welcome")
    login_tab, signup_tab = st.tabs(["Log in", "Create account"])

    with login_tab:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Log in"):
            user = log_in(username, password)
            if user is None:
                st.error("Wrong username or password.")
            else:
                st.session_state["user"] = {"id": user["id"], "username": user["username"]}
                st.rerun()

    with signup_tab:
        new_user = st.text_input("Choose a username", key="signup_user")
        new_pass = st.text_input(
            "Choose a password (8+ characters)", type="password", key="signup_pass"
        )
        if st.button("Create account"):
            ok, message = sign_up(new_user, new_pass)
            if ok:
                st.success(message + " You can log in now.")
            else:
                st.error(message)


def show_scanner(user):
    st.write(f"Logged in as **{user['username']}**")
    if st.button("Log out"):
        st.session_state.pop("user", None)
        st.rerun()

    msg = st.text_area("Paste a message or link")

    if st.button("Scan"):
        if not msg.strip():
            st.warning("Please paste a message first.")
        else:
            result = analyze_message(msg)
            save_scan(user["id"], msg, result)
            st.write("Result:", result.label)
            st.write("Risk Score:", result.score)
            for r in result.reasons:
                st.write("-", r)
            for e in explain(result):
                st.write("💡", e)

    st.subheader("Your scan history")
    history = get_history(user["id"])

    if not history:
        st.write("No scans yet.")

    for h in history:
        col_info, col_star, col_del = st.columns([6, 1, 1])
        col_info.text(f"{LABELS[h['level']]} (score {h['score']}): {h['message']}")
        star = "⭐" if h["bookmarked"] else "☆"
        if col_star.button(star, key=f"star_{h['id']}"):
            toggle_bookmark(user["id"], h["id"])
            st.rerun()
        if col_del.button("🗑️", key=f"del_{h['id']}"):
            delete_scan(user["id"], h["id"])
            st.rerun()

    if history and st.button("Delete all history"):
        delete_all_scans(user["id"])
        st.rerun()


user = st.session_state.get("user")
if user is None:
    show_login_screen()
else:
    show_scanner(user)
