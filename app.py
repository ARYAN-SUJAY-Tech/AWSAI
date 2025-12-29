import streamlit as st
from database import init_db, authenticate_user, create_user, save_history, get_history
from classifier import classify_issue
from prompts import build_prompt
from ai_clients import call_chatgpt
from doc_recommender import get_docs_for_hypotheses
from prompts import parse_aws_error, extract_error_block
# -----------------------------------------------------
# APP CONFIG
# -----------------------------------------------------
st.set_page_config(page_title="AWSAI Assistant", layout="centered")

init_db()

# -----------------------------------------------------
# SESSION STATE
# -----------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "user" not in st.session_state:
    st.session_state.user = None

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# -----------------------------------------------------
# THEME HANDLER
# -----------------------------------------------------
def apply_theme():
    if st.session_state.theme == "dark":
        bg = "linear-gradient(135deg, #0f172a, #334155, #f8fafc)"
        text = "#f8fafc"
    else:
        bg = "linear-gradient(135deg, #f8fafc, #A3AABE)"
        text = "#111827"

    st.markdown(f"""
    <style>
    html, body, [data-testid="stAppViewContainer"] {{
        background: {bg};
        color: {text};
    }}
    h1, h2, h3, p {{ color: {text}; }}
    textarea {{
        background-color: #ffffff;
        color: #111827;
        border-radius: 10px;
    }}
    button {{
        background: linear-gradient(90deg, #2563eb, #1e40af);
        color: white;
        border-radius: 10px;
        font-weight: 600;
    }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

if "last_input" not in st.session_state:
    st.session_state.last_input = ""

if "last_output" not in st.session_state:
    st.session_state.last_output = ""


# -----------------------------------------------------
# THEME TOGGLE
# -----------------------------------------------------
col1, col2 = st.columns([10, 1])
with col2:
    if st.button("🌙" if st.session_state.theme == "dark" else "☀️"):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()

# -----------------------------------------------------
# LANDING PAGE
# -----------------------------------------------------
if st.session_state.page == "landing":
    st.markdown("""
    <div style="text-align:center; margin-top:80px;">
        <h1>☁️ AWSAI - AI Misconfiguration Assistant</h1>
        <p>Diagnose AWS errors instantly with AI-powered explanations, security insights, and step-by-step solutions — built for developers, students, and cloud engineers.
</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Get Started"):
        st.session_state.page = "auth"
        st.rerun()

# -----------------------------------------------------
# AUTH PAGE
# -----------------------------------------------------
elif st.session_state.page == "auth":
    if st.button("< Home"):
        st.session_state.page = "landing"
        st.rerun()
        
    st.markdown("## 🔐 Authentication")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate_user(email, password):
                st.session_state.user = email
                st.session_state.page = "app"
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_email = st.text_input("New Email")
        new_password = st.text_input("New Password", type="password")

        if st.button("Create Account"):
            if create_user(new_email, new_password):
                st.success("Account created! Please login.")
            else:
                st.error("User already exists.")

# -----------------------------------------------------
# MAIN APPLICATION
# -----------------------------------------------------
elif st.session_state.page == "app":

    with st.sidebar:
        st.markdown(f"### 👤USER:\t{st.session_state.user}")
        if st.button("Logout"):
            st.session_state.page = "landing"
            st.session_state.user = None
            st.rerun()

        st.markdown("### 🕘 Previous Queries")
        for h in get_history(st.session_state.user):
            st.markdown(
             f"<p style='color:white;'>• {h}</p>",
             unsafe_allow_html=True
            )
    st.title("☁️ AWSAI - AI Misconfiguration Assistant")

    user_input = st.text_area("Paste AWS error here")

    if st.button("Analyze"):
        if not user_input.strip():
            st.warning("Please enter an AWS error.")
        else:
            if st.session_state.last_input != user_input:
                st.session_state.last_input = user_input
                with st.spinner("Analyzing AWS error..."):
                    issue = classify_issue(user_input)
                    result = call_chatgpt(build_prompt(user_input, issue))
                st.session_state.last_output = result
                save_history(st.session_state.user, issue)

            st.markdown("### 🔍 Analysis")
            st.markdown(st.session_state.last_output)




            st.markdown(result)
            st.markdown("### 📚 Recommended Documentation")

            structured_input = parse_aws_error(extract_error_block(user_input))
            print(structured_input)
            docs = get_docs_for_hypotheses(structured_input)
            for d in docs:
                st.markdown(f"#### {d['hypothesis']} (Confidence: {d['confidence']})")
                print(f"{d['hypothesis']} (Confidence: {d['confidence']})")
                for doc in d["docs"]:
                    st.markdown(f"- [{doc['title']}]({doc['url']}) - {doc['reason']}")
                    print(f"- [{doc['title']}]({doc['url']}) - {doc['reason']}")
