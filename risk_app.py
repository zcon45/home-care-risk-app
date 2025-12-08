import streamlit as st
from datetime import datetime
from io import BytesIO
from fpdf import FPDF   # ← this is the correct package

# ===============================
# CONFIG & STYLE
# ===============================
st.set_page_config(page_title="Home Care Comfort Portal", layout="centered", page_icon="house")

st.markdown("""
<style>
    .main {background:#f8fbfd;}
    .card {background:white; padding:2rem; border-radius:16px; box-shadow:0 8px 25px rgba(0,0,0,0.08); margin:1rem 0;}
    .stButton>button {background:#2563eb; color:white; border-radius:12px; height:3em; font-weight:600;}
    .badge {padding:8px 20px; border-radius:50px; font-weight:bold; display:inline-block;}
    .low {background:#10b981; color:white;}
    .medium {background:#f59e0b; color:white;}
    .high {background:#ef4444; color:white;}
</style>
""", unsafe_allow_html=True)

# ===============================
# SESSION STATE
# ===============================
if "page" not in st.session_state: st.session_state.page = "home"
if "step" not in st.session_state: st.session_state.step = 1
if "assessments" not in st.session_state: st.session_state.assessments = []

defaults = ["first_name","last_name","age","weight","height_ft","height_in","seizures","mobility_label","adult_present","notes"]
for key in defaults:
    if key not in st.session_state: st.session_state[key] = ""

# ===============================
# PDF FUNCTION
# ===============================
def make_pdf(name, score, level):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Home Care Risk Assessment", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Client: {name}", ln=True)
    pdf.cell(0, 10, f"Risk Level: {level} | Score: {score:.1f}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

# ===============================
# PAGES
# ===============================
def home():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.title("Home Care Comfort Portal")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Assessment", use_container_width=True):
            st.session_state.page = "assessment"
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Admin Dashboard", use_container_width=True):
            st.session_state.page = "admin"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

def assessment():
    st.markdown("<div class='card
