import streamlit as st
from PyPDF2 import PdfReader
from app.langgraph_flow.graph import build_langgraph
from app.utils.generate_pdf import generate_pdf
import unicodedata
from app.auth.auth_config import USER_DB

# Initialize session state
# if "authenticated" not in st.session_state:
#     st.session_state.authenticated = False
#     st.session_state.user_role = None
#     st.session_state.username = None


# def login(username, password):
#     user = USER_DB.get(username)
#     if user and user["password"] == password:
#         st.session_state.authenticated = True
#         st.session_state.user_role = user["role"]
#         st.session_state.username = username
#         return True
#     return False

# if not st.session_state.authenticated:
#     st.title("🔒 AI Pitch Assistant Login")

#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     if st.button("Login"):
#         if login(username, password):
#             st.success(f"Welcome {username} ({st.session_state.user_role})!")
#             st.experimental_user()
#         else:
#             st.error("Invalid credentials.")
#     st.stop()



# def logout():
#     st.session_state.authenticated = False
#     st.session_state.user_role = None
#     st.session_state.username = None

# Load LangGraph
graph = build_langgraph()

def normalize_text(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


# --- UI HEADER ---
st.set_page_config(page_title="AI Pitch Assistant", layout="wide")
st.title("🎓 AI Pitch Assistant for Campus Recruitment")

# --- Resume Upload Section ---
st.header("1️⃣ Upload Resume")

uploaded_file = st.file_uploader("Upload student's resume (PDF or text)", type=["pdf", "txt"])

resume_text = ""
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        resume_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    else:
        resume_text = uploaded_file.read().decode("utf-8")

    st.success("Resume uploaded successfully.")

# --- LangGraph Execution ---
if resume_text:
    st.header("2️⃣ Run Pitch Generation Pipeline")

    if st.button("🚀 Generate Pitch"):
        with st.spinner("Analyzing resume and generating pitch..."):
            result = graph.invoke({
                "resume_text": resume_text,
                "metadata": {}
            })

        st.success("Pitch generation complete!")

        # --- Display Results ---
        st.subheader("📌 Profile Insights")
        st.markdown(result["profile_insights"])

        st.subheader("📚 Recruiter Context")
        st.markdown(result["recruiter_context"])

        st.subheader("🎤 Final Elevator Pitch")
        st.markdown(result["final_pitch"])

        # Export section
        clean_text = normalize_text(result["final_pitch"])
        
        pdf_file = generate_pdf(clean_text)
        st.download_button(
            label="📥 Download Pitch as .pdf",
            data=pdf_file,
            file_name="elevator_pitch.pdf",
            mime="application/pdf"
        )

        # --- Review/Approval ---
        st.header("3️⃣ Placement Coordinator Approval")
        if st.checkbox("✅ Approve pitch for student profile"):
            st.success("Pitch approved and ready to be shared with recruiters.")
        else:
            st.info("Awaiting coordinator approval.")

else:
    st.info("Please upload a resume to begin.")
