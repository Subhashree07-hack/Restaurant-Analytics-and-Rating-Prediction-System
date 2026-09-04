import streamlit as st
import json
import os
import hashlib

USER_FILE = "users.json"


# -------------------------
# PASSWORD HASH FUNCTION
# -------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# -------------------------
# LOAD USERS
# -------------------------
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}


# -------------------------
# SAVE USERS
# -------------------------
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)


# -------------------------
# LOGIN PAGE
# -------------------------
def login_page():

    st.markdown("""
    <style>
    .login-box {
        width: 400px;
        margin: auto;
        margin-top: 100px;
        padding: 30px;
        background: #111827;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0px 0px 20px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    st.title("🏦 Loan AI Login")

    users = load_users()

    mode = st.radio("Select", ["Login", "Sign Up"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")


    # -------------------------
    # SIGN UP
    # -------------------------
    if mode == "Sign Up":
        if st.button("Create Account"):

            if username in users:
                st.error("User already exists ❌")
            else:
                users[username] = hash_password(password)
                save_users(users)
                st.success("Account created ✅")


    # -------------------------
    # LOGIN
    # -------------------------
    if mode == "Login":
        if st.button("Login"):

            if username in users and users[username] == hash_password(password):

                st.session_state["logged_in"] = True
                st.session_state["user"] = username

                st.success("Login successful ✅")
                st.rerun()

            else:
                st.error("Invalid credentials ❌")

    st.markdown("</div>", unsafe_allow_html=True)


# -------------------------
# CHECK LOGIN
# -------------------------
def login():
    return st.session_state.get("logged_in", False)