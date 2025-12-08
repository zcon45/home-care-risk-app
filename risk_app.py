# risk_app.py   ← or app.py – name doesn't matter
import streamlit as st
from datetime import datetime
from io import BytesIO
from fpdf2 import FPDF          # ← this is correct

# ===============================
# CONFIG & STYLE
# ===============================
st.set_page_config(page_title="Home Care Comfort Portal", layout="centered", page_icon="house")

st.markdown("""
<style>
    .main {background-color: #f8fbfd;}
    .card {background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 8px 25px rgba(0,0,0,0.08); margin: 1rem 0;}
    .stButton>button {background: #2563eb; color: white; border-radius: 12px; height: 3em; font-weight: 600;}
    .badge {padding: 8px 20px; border-radius: 50px; font-weight: bold; display: inline-block;}
    .low {background:#10b981; color:white;}
    .medium {background:#f59e0b; color:white;}
    .high {background:#ef4444; color:white;}
    h1,h2,h3 {color:#1e293b;}
    .step-indicator {font-size:1.1rem; color:#64748b; margin-bottom:1.5rem;}
</style>
""", unsafe_allow_html=True)

# ===============================
# SESSION STATE
# ===============================
defaults = {
    "page": "home", "step": 1, "assessments": [], "uploaded_files": [], "ai_analysis": "",
    "first_name": "", "last_name": "", "dob": datetime(2000,1,1), "age": "", "weight": "", "height_ft": "", "height_in": "",
    "seizures": "No", "seizure_type": "", "medications": "No", "mobility_label": "Walks independently",
    "adult_present": "No", "notes": ""
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ===============================
# PDF & AI
# ===============================
def safe_text(text):
    return str(text).encode("latin-1", "ignore").decode("latin-1")

def create_pdf(data, score, level, ai_text, files):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 15, "Home Care Risk Assessment – Full Report", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, f"Client: {data['first_name']} {data['last_name']}", ln=True)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%B %d, %Y %I:%M %p')}", ln=True)
    pdf.cell(0, 10, f"Risk Level: {level} (Score: {score:.1f})", ln=True)
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "AI Analysis & Recommendations", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 8, safe_text(ai_text or "No additional analysis."))
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

def fake_ai_analysis(files):
    names = ", ".join([f.name for f in files]) if files else "None"
    return f"""AI Analysis Complete

Documents uploaded: {names}

Summary & Recommendations:
• Client has {'a history of seizures' if st.session_state.seizures=='Yes' else 'no seizure history'}
• Mobility level: {st.session_state.mobility_label}
• Adult supervision: {st.session_state.adult_present}
• Install grab bars and non-slip mats
• Consider medical alert pendant
• Keep rescue medication accessible
Overall risk matches calculated score."""

# ===============================
# PAGES
# ===============================
def home():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("Home Care Comfort Portal")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Start Assessment", use_container_width=True):
            st.session_state.page = "assessment"; st.session_state.step = 1; st.rerun()
    with c2:
        if st.button("Admin Dashboard", use_container_width=True):
            st.session_state.page = "admin"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def assessment():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="step-indicator">Step {st.session_state.step} of 3</div>', unsafe_allow_html=True)
    st.title("Home Care Risk Assessment")

    if st.session_state.step == 1:
        with st.form("step1"):
            st.subheader("Client Information")
            c1, c2 = st.columns(2)
            with c1:
                st.session_state.first_name = st.text_input("First Name*", st.session_state.first_name)
                st.session_state.last_name = st.text_input("Last Name*", st.session_state.last_name)
            with c2:
                st.session_state.age = st.text_input("Age*", st.session_state.age)
                st.session_state.weight = st.text_input("Weight (lbs)*", st.session_state.weight)
            cc1, cc2 = st.columns(2)
            with cc1: st.session_state.height_ft = st.text_input("Height (ft)*", st.session_state.height_ft)
            with cc2: st.session_state.height_in = st.text_input("Height (in)*", st.session_state.height_in)
            if st.form_submit_button("Next →", use_container_width=True):
                if st.session_state.first_name and st.session_state.last_name and st.session_state.age:
                    st.session_state.step = 2; st.rerun()
                else:
                    st.error("Fill all required fields")

    elif st.session_state.step == 2:
        with st.form("step2"):
            st.session_state.seizures = st.radio("Seizures?", ["No","Yes"], horizontal=True)
            if st.session_state.seizures == "Yes":
                st.session_state.seizure_type = st.selectbox("Type", ["Tonic-clonic","Atonic","Tonic","Myoclonic","Focal","Absence"])
            st.session_state.medications = st.radio("Medications?", ["No","Yes"], horizontal=True)
            st.session_state.mobility_label = st.selectbox("Mobility", ["Walks independently","Needs supervision","Uses aid","Hands-on assist","Non-mobile"])
            st.session_state.adult_present = st.radio("Adult supervision?", ["Yes","No"], horizontal=True)
            st.session_state.notes = st.text_area("Notes")
            c1, c2 = st.columns(2)
            with c1: st.form_submit_button("← Back", on_click=lambda: st.session_state.update(step=1) or st.rerun())
            with c2: 
                if st.form_submit_button("Next →", use_container_width=True):
                    st.session_state.step = 3; st.rerun()

    elif st.session_state.step == 3:
        st.subheader("Upload Documents (optional)")
        uploaded = st.file_uploader("PDFs only", type="pdf", accept_multiple_files=True)
        if uploaded: st.session_state.uploaded_files = uploaded; st.success("Uploaded!")

        # Simple score
        try:
            score = int(st.session_state.age or 0)*0.3 + \
                    ["Walks independently","Needs supervision","Uses aid","Hands-on assist","Non-mobile"].index(st.session_state.mobility_label)*10 + \
                    (30 if st.session_state.seizures=="Yes" else 0) + \
                    (15 if st.session_state.adult_present=="No" else 0)
            level = "Low" if score < 50 else "Medium" if score < 90 else "High"
        except:
            score, level = 0, "Unknown"

        st.markdown(f"### Risk Level: <span class='badge {level.lower()}'>{level}</span>", unsafe_allow_html=True)

        if st.button("Generate AI Report & Submit", type="primary", use_container_width=True):
            ai = fake_ai_analysis(st.session_state.uploaded_files)
            pdf = create_pdf(st.session_state, score, level, ai, st.session_state.uploaded_files)
            st.session_state.assessments.append({
                "name": f"{st.session_state.first_name} {st.session_state.last_name}",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "score": score, "level": level, "pdf": pdf, "ai": ai
            })
            st.success("Submitted!"); st.balloons()
            if st.button("Go to Admin"): st.session_state.page = "admin"; st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

def admin():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("Admin Dashboard")
    if not st.session_state.assessments:
        st.info("No submissions yet")
    for i, a in enumerate(st.session_state.assessments):
        with st.expander(f"{a['name']} – {a['date']} – {a['level']} Risk"):
            st.write(a['ai'])
            st.download_button("Download Full PDF Report", a['pdf'],
                file_name=f"{a['name'].replace(' ','_')}_Report.pdf",
                mime="application/pdf", key=i)
    if st.button("← Home"): st.session_state.page = "home"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ===============================
# ROUTER
# ===============================
if st.session_state.page == "home":
    home()
elif st.session_state.page == "assessment":
    assessment()
elif st.session_state.page == "admin":
    admin()
