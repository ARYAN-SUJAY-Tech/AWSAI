import streamlit as st
from database import create_user, authenticate_user
import sqlite3

DB_NAME = "users.db"


def reset_password(email, new_password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "UPDATE users SET password=? WHERE email=?",
        (new_password, email)
    )
    conn.commit()
    conn.close()


def auth_page():
    st.subheader("🔐 Authentication")

    option = st.radio("Choose an option", ["Login", "Sign Up", "Forgot Password"])

    # ---------------- LOGIN ----------------
    if option == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = authenticate_user(email, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid email or password")

    # ---------------- SIGN UP ----------------
    elif option == "Sign Up":
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Create Account"):
            if create_user(username, email, password):
                st.success("Account created successfully! Please log in.")
            else:
                st.error("User already exists.")

    # ---------------- FORGOT PASSWORD ----------------
    else:
        email = st.text_input("Registered Email")
        new_password = st.text_input("New Password", type="password")

        if st.button("Reset Password"):
            reset_password(email, new_password)
            st.success("Password updated successfully. Please login.")
