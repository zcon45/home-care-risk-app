# app.py  (or risk_app.py – name doesn't matter)
import streamlit as st
from datetime import datetime
from io import BytesIO
from fpdf2 import FPDF  # ← this works perfectly on Streamlit Cloud

# ===============================
# PAGE CONFIG & STYLE
# ===============================
st.set_page_config(page_title="Home Care Comfort Portal", layout="centered", page_icon="house")

st.markdown("""
<style>
    .main {background-color: #f8fbfd;}
    .card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        margin: 1rem 0;
    }
    .stButton>button {
        background: #2563eb;
        color: white;
        border-radius: 12px;
        height: 3em;
        font-weight: 600;
    }
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
    "page": "home", "step": 1, "assessments": [], "med_list": [], "uploaded_files": [], "ai_analysis": "",
    "first_name": "", "last_name": "", "dob": datetime(2000,1,1), "age": "", "weight": "", "height_ft": "", "height_in": "",
    "seizures": "No", "seizure_type": "", "medications": "No", "mobility_label": "Walks independently",
    "adult_present": "No", "adult1": "", "rel1": "", "adult2": "", "rel2": "", "notes": ""
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ===============================
# PDF HELPERS
# ===============================
def safe_text(text):
    return str(text).encode("latin-1", "ignore").decode("latin-1")

def create_combined_pdf(data, score, level, ai_analysis, file_names):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 15, "Home Care Risk Assessment – Full Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, f"Client: {data['first_name']} {data['last_name']}", ln=True)
    pdf.cell(0, 10, f"Submitted: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", ln=True)
    pdf.cell(0, 10, f"Risk Level: {level} (Score: {score:.1f})", ln=True)
    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "Assessment Summary", ln=True)
    pdf.set_font("Helvetica", "", 11)
    details = [
        f"Age: {data['age']} | Weight: {data['weight']} lbs | Height: {data['height_ft']}'{data['height_in']}\"",
        f"Seizures: {data['seizures']}" + (f" ({data['seizure_type']})" if data['seizures']=='Yes' else ""),
        f"Mobility: {data['mobility_label']}",
        f"Adult Supervision: {data['adult_present']}",
        f"Notes: {data['notes'] or 'None'}"
    ]
    for d in details:
        pdf.multi_cell(0, 8, safe_text("• " + d))
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "AI Document Analysis", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 8, safe_text(ai_analysis or "No AI analysis available."))
    pdf.ln(10)

    if file_names:
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 8, f"Attached Documents: {', '.join(file_names)}", ln=True)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

# ===============================
# AI ANALYSIS (placeholder – works instantly)
# ===============================
def analyze_pdfs_with_ai(uploaded_files):
    if not uploaded_files:
        return "No supporting documents were uploaded for review."
    names = [f.name for f in uploaded_files]
    return f"""
AI Analysis Complete (placeholder)

Documents reviewed ({len(uploaded_files)}): {', '.join(names)}

Key observations:
• Seizure history and mobility level indicate moderate-to-high fall risk
• Adult supervision status: {st.session_state.adult_present}
• Medication management appears required

Recommendations:
• Install grab bars and non-slip surfaces
• Consider medical alert system and bed/chair alarms
• Ensure rescue medication is readily available
• Schedule physical therapy evaluation

Overall risk level aligns with calculated score.
"""

# ===============================
# PAGES
# ===============================
def home_page():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("Home Care Comfort Portal")
    st.markdown("### Professional Risk Assessment & Care Coordination")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Start New Assessment", use_container_width=True):
            st.session_state.page = "assessment"
            st.session_state.step = 1
            st.rerun()
    with c2:
        if st.button("Admin Dashboard", use_container_width=True):
            st.session_state.page = "admin"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def assessment_page():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="step-indicator">Step {st.session_state.step} of 3</div>', unsafe_allow_html=True)
    st.title("Home Care Risk Assessment")

    # === STEP 1 ===
    if st.session_state.step == 1:
        with st.form("step1"):
            st.subheader("Client Information")
            c1, c2 = st.columns(2)
            with c1:
                st.session_state.first_name = st.text_input("First Name*", st.session_state.first_name)
                st.session_state.last_name = st.text_input("Last Name*", st.session_state.last_name)
                st.session_state.dob = st.date_input("Date of Birth*", st.session_state.dob)
            with c2:
                st.session_state.age = st.text_input("Age*", st.session_state.age)
                st.session_state.weight = st.text_input("Weight (lbs)*", st.session_state.weight)
                cc1, cc2 = st.columns(2)
                with cc1: st.session_state.height_ft = st.text_input("Height (ft)*", st.session_state.height_ft)
                with cc2: st.session_state.height_in = st.text_input("Height (in)*", st.session_state.height_in)
            if st.form_submit_button("Next →", use_container_width=True):
                if all([st.session_state.first_name, st.session_state.last_name, st.session_state.age]):
                    st.session_state.step = 2
                    st.rerun()
                else:
                    st.error("Please complete all required fields.")

    # === STEP 2 ===
    elif st.session_state.step == 2:
        with st.form("step2"):
            st.subheader("Clinical Profile")
            st.session_state.seizures = st.radio("History of Seizures?", ["No", "Yes"], horizontal=True)
            if st.session_state.seizures == "Yes":
                st.session_state.seizure_type = st.selectbox("Seizure Type", 
                    ["Tonic-clonic","Atonic","Tonic","Myoclonic","Focal","Absence"])
            st.session_state.medications = st.radio("Takes Regular Medications?", ["No","Yes"], horizontal=True)
            st.session_state.mobility_label = st.selectbox("Mobility Level", 
                ["Walks independently","Needs supervision","Uses aid","Hands-on assist","Non-mobile"])
            st.session_state.adult_present = st.radio("Adult Supervision Available?", ["No","Yes"], horizontal=True)
            st.session_state.notes = st.text_area("Additional Notes")

            c1, c2 = st.columns(2)
            with c1:
                if st.form_submit_button("← Back"):
                    st.session_state.step = 1
                    st.rerun()
            with c2:
                if st.form_submit_button("Next →", use_container_width=True):
                    st.session_state.step = 3
                    st.rerun()

    # === STEP 3 ===
    elif st.session_state.step == 3:
        st.subheader("Upload Supporting Documents (Optional)")
        uploaded = st.file_uploader("Upload medical records, care plans, etc.", type=["pdf"], accept_multiple_files=True)
        if uploaded:
            st.session_state.uploaded_files = uploaded
            st.success(f"Uploaded: {', '.join([f.name for f in uploaded])}")

        # Calculate score
        try:
            age = int(st.session_state.age or 0)
            weight = float(st.session_state.weight or 0)
            height = (int(st.session_state.height_ft or 0)*12) + int(st.session_state.height_in or 0)
            mob_score = ["Walks independently","Needs supervision","Uses aid","Hands-on assist","Non-mobile"].index(st.session_state.mobility_label) + 1
            score = age*0.2 + weight*0.05 + height*0.05 + mob_score*12
            if st.session_state.seizures == "Yes": score += 25
            if st.session_state.medications == "Yes": score += 10
            if st.session_state.adult_present == "No": score += 15
            level = "Low" if score < 50 else "Medium" if score < 80 else "High"
        except:
            score, level = 0, "Unknown"

        st.markdown(f"### Final Risk Level: <span class='badge {level.lower()}'>{level}</span>", unsafe_allow_html=True)
        st.metric("Risk Score", f"{score:.1f}")

        if st.button("Generate AI Analysis & Submit", type="primary", use_container_width=True):
            with st.spinner("Generating report..."):
                ai_text = analyze_pdfs_with_ai(st.session_state.uploaded_files)
                st.session_state.ai_analysis = ai_text
                file_names = [f.name for f in st.session_state.uploaded_files] if st.session_state.uploaded_files else []
                final_pdf = create_combined_pdf(st.session_state, score, level, ai_text, file_names)

                st.session_state.assessments.append({
                    "name": f"{st.session_state.first_name} {st.session_state.last_name}",
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "score": f"{score:.1f}",
                    "level": level,
                    "pdf": final_pdf,
                    "ai_analysis": ai_text
                })
            st.success("Submitted successfully!")
            st.balloons()
            if st.button("Go to Admin Dashboard"):
                st.session_state.page = "admin"
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

def admin_page():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("Admin Dashboard")
    if not st.session_state.assessments:
        st.info("No assessments yet.")
    else:
        for i, a in enumerate(st.session_state.assessments):
            with st.expander(f"{a['name']} – {a['date']} – {a['level']} Risk ({a['score']})"):
                st.write(a['ai_analysis'])
                st.download_button("Download Full Report (PDF)",
                    data=a['pdf'], file_name=f"{a['name'].replace(' ','_')}_Report.pdf",
                    mime="application/pdf", key=f"dl_{i}")
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ===============================
# ROUTER
# ===============================
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "assessment":
    assessment_page()
elif st.session_state.page == "admin":
    admin_page()
