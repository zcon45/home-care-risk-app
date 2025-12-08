import streamlit as st
from datetime import datetime
from io import BytesIO
from fpdf import FPDF

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
if "page" not in st.session_state:
    st.session_state.page = "home"
if "assessments" not in st.session_state:
    st.session_state.assessments = []

# ===============================
# PDF FUNCTION
# ===============================
def create_pdf(name, score, level):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 15, "Home Care Risk Assessment", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 14)
    pdf.cell(0, 10, f"Client: {name}", ln=True)
    pdf.cell(0, 10, f"Risk Level: {level}   |   Score: {score:.1f}", ln=True)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", ln=True)
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
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Start New Assessment", use_container_width=True):
            st.session_state.page = "assessment"
            st.rerun()
    with c2:
        if st.button("Admin Dashboard", use_container_width=True):
            st.session_state.page = "admin"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

def assessment():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.title("Client Risk Assessment")

    with st.form("main_form"):
        st.text_input("First Name*", key="first_name")
        st.text_input("Last Name*", key="last_name")
        st.text_input("Age*", key="age")
        st.text_input("Weight (lbs)", key="weight", placeholder="e.g. 150")
        st.selectbox("Mobility Level*", [
            "Walks independently", "Needs supervision", "Uses aid",
            "Hands-on assist", "Non-mobile"
        ], key="mobility")
        st.radio("History of Seizures?", ["No", "Yes"], horizontal=True, key="seizures")
        st.radio("Adult Present 24/7?", ["Yes", "No"], horizontal=True, key="adult_present")
        st.text_area("Additional Notes", key="notes")

        # Simple risk score
        try:
            score = (int(st.session_state.age) * 0.4) + \
                    (["Walks independently","Needs supervision","Uses aid","Hands-on assist","Non-mobile"].index(st.session_state.mobility) * 15) + \
                    (50 if st.session_state.seizures == "Yes" else 0) + \
                    (40 if st.session_state.adult_present == "No" else 0)
            level = "Low" if score < 80 else "Medium" if score < 140 else "High"
        except:
            score, level = 0, "Unknown"

        st.markdown(f"### Risk Level: <span class='badge {level.lower()}'>{level}</span>", unsafe_allow_html=True)
        st.metric("Total Risk Score", f"{score:.1f}")

        submitted = st.form_submit_button("Submit to Admin", type="primary", use_container_width=True)
        if submitted:
            name = f"{st.session_state.first_name} {st.session_state.last_name}"
            pdf = create_pdf(name, score, level)
            st.session_state.assessments.append({
                "name": name,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "level": level,
                "score": score,
                "pdf": pdf
            })
            st.success("Assessment submitted successfully!")
            st.balloons()

    st.markdown("</div>", unsafe_allow_html=True)

def admin():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.title("Admin Dashboard")
    if not st.session_state.assessments:
        st.info("No assessments submitted yet.")
    else:
        for i, a in enumerate(st.session_state.assessments):
            with st.expander(f"{a['name']} — {a['date']} — {a['level']} Risk ({a['score']:.1f})"):
                st.download_button(
                    "Download PDF Report",
                    data=a["pdf"],
                    file_name=f"{a['name'].replace(' ', '_')}_Report.pdf",
                    mime="application/pdf",
                    key=i
                )
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# ROUTER
# ===============================
if st.session_state.page == "home":
    home()
elif st.session_state.page == "assessment":
    assessment()
elif st.session_state.page == "admin":
    admin()
