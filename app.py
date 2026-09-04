import streamlit as st
import pandas as pd
import pickle

from chatbot import get_chat_response
from utils import create_chart, generate_pdf, save_chart_image


# =========================
# LOAD ML MODEL
# =========================
model = pickle.load(
    open("model/loan_model.pkl", "rb")
)


st.set_page_config(
    page_title="Loan AI ",
    layout="wide"
)


# =========================
# LOGIN PAGE
# =========================

if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.user = ""


if not st.session_state.login:

    st.markdown(
        "<h1 style='text-align:center;'>🔐 Loan AI Login</h1>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        user = st.text_input("Username")

        pwd = st.text_input(
            "Password",
            type="password"
        )


        if st.button("Login"):

            if user and pwd:

                st.session_state.login = True
                st.session_state.user = user

                st.rerun()

            else:
                st.error("Enter username and password")


    st.stop()



# =========================
# USER
# =========================

st.sidebar.success(
    f"👤 Logged in as: {st.session_state.user}"
)


st.title("💬 Loan AI ")


# =========================
# CHAT
# =========================
# =========================
# CHAT
# =========================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_msg = st.chat_input(
    "Ask anything about loans...",
    key="loan_chat"
)

if user_msg:

    # Convert previous messages into Gemini history format
    history = []

    for role, text in st.session_state.chat_history:

        if role == "user":
            history.append(
                {
                    "role": "user",
                    "parts": [text]
                }
            )

        else:
            history.append(
                {
                    "role": "model",
                    "parts": [text]
                }
            )

    # Get AI reply
    reply = get_chat_response(user_msg, history)

    # Save messages
    st.session_state.chat_history.append(
        ("user", user_msg)
    )

    st.session_state.chat_history.append(
        ("ai", reply)
    )

# Display chat
for role, text in st.session_state.chat_history:

    if role == "user":

        st.markdown(
            f"""
            <div style="
            text-align:right;
            background:#DCF8C6;
            padding:10px;
            border-radius:10px;
            margin:5px;">
            🧑 {text}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div style="
            background:#F1F0F0;
            padding:10px;
            border-radius:10px;
            margin:5px;">
            🤖 {text}
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================
# LOAN PREDICTION
# =========================


st.divider()

st.subheader("🏦 Loan Prediction")


name = st.text_input("Name")

age = st.number_input(
    "Age",
    min_value=18,
    max_value=100
)


income = st.number_input("Income")

credit = st.number_input(
    "Credit Score"
)

loan = st.number_input(
    "Loan Amount"
)

years = st.number_input(
    "Years Employed"
)



if st.button("Check Loan Eligibility 🚀"):


    data = pd.DataFrame(
        [[income,credit,loan,years]],
        columns=[
            "income",
            "credit_score",
            "loan_amount",
            "years_employed"
        ]
    )


    pred = model.predict(data)[0]

    prob = (
        model.predict_proba(data)[0][1]
        *100
    )


    if pred:

        result="Approved"

        st.success(
            "✅ Loan Approved"
        )

    else:

        result="Rejected"

        st.error(
            "❌ Loan Rejected"
        )



    # GRAPH

    fig=create_chart(prob)

    st.plotly_chart(fig)



    # EXPLANATION

    if prob > 70:

        reason = (
        "Strong profile: "
        "High credit score and stable income."
        )

    elif prob > 40:

        reason = (
        "Medium risk: "
        "Some factors need review."
        )

    else:

        reason = f"""
AI Analysis:
The applicant has a credit score of {credit}
with income {income}. 
The model predicts {prob:.2f}% approval confidence.
"""


    st.info("🧠 AI Explanation")

    st.write(reason)



    # SAVE GRAPH

    chart_path = save_chart_image(fig)



    # PDF

    pdf_file = generate_pdf(
        name,
        age,
        income,
        credit,
        loan,
        years,
        result,
        prob,
        reason,
        chart_path
    )


    with open(pdf_file,"rb") as f:

        st.download_button(
            "📄 Download Loan Report",
            f,
            file_name=pdf_file
        )


    st.success(
        "✔ Analysis Completed"
    )