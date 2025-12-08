# app.py - Home Care Comfort Portal (Professional Upgrade)
import streamlit as st

# Page Config
st.set_page_config(
    page_title="Home Care Comfort Portal",
    page_icon="house",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Professional CSS - Refined & Elegant
st.markdown("""
<style>
    .main {
        background: #f8fafc;
        font-family: 'Segoe UI', sans-serif;
    }
    .header-card {
        background: white;
        padding: 4rem 2rem;
        border-radius: 24px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.08);
        text-align: center;
        max-width: 900px;
        margin: 3rem auto;
        border: 1px solid #e2e8f0;
    }
    .portal-title {
        font-size: 3.2rem;
        color: #1e293b;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    .portal-subtitle {
        font-size: 1.3rem;
        color: #64748b;
        max-width: 700px;
        margin: 0 auto 3rem auto;
        line-height: 1.6;
    }
    .btn-primary {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 1.1rem 2.5rem;
        border-radius: 16px;
        font-size: 1.15rem;
        font-weight: 600;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
        transition: all 0.3s;
        width: 100%;
    }
    .btn-primary:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(59, 130, 246, 0.4);
    }
    .btn-secondary {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
    }
    .btn-secondary:hover {
        box-shadow: 0 12px 30px rgba(139, 92, 246, 0.4);
    }
    .assessment-card {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        max-width: 750px;
        margin: 2rem auto;
        border: 1px solid #e2e8f0;
    }
    .step-header {
        font-size: 1.1rem;
        color: #64748b;
        font-weight: 500;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .section-title {
        font-size: 1.4rem;
        color: #1e293b;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e0e7ff;
    }
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: 4rem;
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Session State
if "page" not in st.session_state:
    st.session_state.page = "home"
if "step" not in st.session_state:
    st.session_state.step = 1

# Client Data
if "data" not in st.session_state:
    st.session_state.data = {
        "first_name": "", "last_name": "", "client_id": "",
        "age": "", "height": "", "weight": "",
        "diagnoses": "No", "diagnoses_details": "",
        "seizures": "No", "seizure_details": "",
        "medications": "No", "medication_details": "",
        "assist_medical": "No"
    }

data = st.session_state.data

# HOME PAGE - Professional Redesign
def home():
    st.markdown('<div class="header-card">', unsafe_allow_html=True)
    st.markdown('<h1 class="portal-title">Home Care Comfort Portal</h1>', unsafe_allow_html=True)
    st.markdown('<p class="portal-subtitle">A secure, confidential platform for assessing care needs and coordinating professional home care services with compassion and precision.</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        if st.button("Client Assessment", use_container_width=True):
            st.session_state.page = "assessment"
            st.session_state.step = 1
            st.rerun()
    
    with col2:
        if st.button("Admin Dashboard", use_container_width=True):
            st.session_state.page = "admin"
            st.rerun()

    # Apply professional button styling
    st.markdown("""
    <script>
        const buttons = document.querySelectorAll('[data-testid="stButton"] button');
        buttons[0].classList.add('btn-primary');
        buttons[1].classList.add('btn-primary', 'btn-secondary');
    </script>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="footer">© 2025 Home Care Comfort Portal • Confidential & HIPAA-Compliant</div>', unsafe_allow_html=True)

# ASSESSMENT
def assessment():
    st.markdown('<div class="assessment-card">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#1e293b; margin-bottom:0.5rem;'>Client Risk Assessment</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#64748b;'>Please complete all steps accurately</p>", unsafe_allow_html=True)

    if st.session_state.step == 1:
        st.markdown("<div class='step-header'>Step 1 of 3 — Client Identification</div>", unsafe_allow_html=True)
        with st.form("step1"):
            st.text_input("First Name*", key="data.first_name", value=data["first_name"])
            st.text_input("Last Name*", key="data.last_name", value=data["last_name"])
            st.text_input("Client ID*", key="data.client_id", value=data["client_id"])
            if st.form_submit_button("Continue →", use_container_width=True, type="primary"):
                if data["first_name"] and data["last_name"] and data["client_id"]:
                    st.session_state.step = 2
                    st.rerun()
                else:
                    st.error("All fields are required")

    elif st.session_state.step == 2:
        st.markdown("<div class='step-header'>Step 2 of 3 — Physical Profile</div>", unsafe_allow_html=True)
        with st.form("step2"):
            st.text_input("Age*", key="data.age", value=data["age"], placeholder="e.g. 78")
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Height*", key="data.height", value=data["height"], placeholder="e.g. 5'6\"")
            with col2:
                st.text_input("Weight (lbs)*", key="data.weight", value=data["weight"], placeholder="e.g. 150")
            
            colb, coln = st.columns(2)
            with colb:
                if st.form_submit_button("← Back"):
                    st.session_state.step = 1
                    st.rerun()
            with coln:
                if st.form_submit_button("Continue →", use_container_width=True, type="primary"):
                    if data["age"] and data["height"] and data["weight"]:
                        st.session_state.step = 3
                        st.rerun()
                    else:
                        st.error("Please complete all fields")

    elif st.session_state.step == 3:
        st.markdown("<div class='step-header'>Step 3 of 3 — Medical Profile</div>", unsafe_allow_html=True)
        with st.form("step3"):
            st.markdown("<div class='section-title'>Medical History</div>", unsafe_allow_html=True)

            data["diagnoses"] = st.radio("Does the client have any diagnosed medical conditions?", ["No", "Yes"], horizontal=True)
            if data["diagnoses"] == "Yes":
                with st.expander("Please specify diagnoses", expanded=True):
                    st.text_area("", key="data.diagnoses_details", value=data["diagnoses_details"], height=100)

            data["seizures"] = st.radio("Does the client have a history of seizures?", ["No", "Yes"], horizontal=True)
            if data["seizures"] == "Yes":
                with st.expander("Please describe seizure type and frequency", expanded=True):
                    st.text_area("", key="data.seizure_details", value=data["seizure_details"], height=100)

            data["medications"] = st.radio("Is the client currently taking any medications?", ["No", "Yes"], horizontal=True)
            if data["medications"] == "Yes":
                with st.expander("Please list medications (include dosage if known)", expanded=True):
                    st.text_area("", key="data.medication_details", value=data["medication_details"], height=120)

            data["assist_medical"] = st.radio("Will the care provider be expected to assist with medical tasks?", ["No", "Yes"], horizontal=True)

            colb, cols = st.columns(2)
            with colb:
                if st.form_submit_button("← Back"):
                    st.session_state.step = 2
                    st.rerun()
            with cols:
                if st.form_submit_button("Submit Assessment", type="primary", use_container_width=True):
                    st.success("Assessment submitted successfully!")
                    st.balloons()
                    st.session_state.page = "thank_you"
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Thank You Page
def thank_you():
    st.markdown('<div class="assessment-card">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#1e293b;'>Thank You</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1.3rem; color:#475569;'>Your assessment has been securely submitted.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#64748b;'>A care coordinator will review the information and contact you shortly.</p>", unsafe_allow_html=True)
    if st.button("Return to Home", use_container_width=True):
        st.session_state.page = "home"
        st.session_state.step = 1
        for key in st.session_state.data:
            st.session_state.data[key] = "" if key.endswith("_details") else ("No" if key in ["diagnoses","seizures","medications","assist_medical"] else "")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Admin Page (placeholder)
def admin():
    st.markdown('<div class="assessment-card">', unsafe_allow_html=True)
    st.title("Admin Dashboard")
    st.info("Submitted assessments will be listed here in the final version.")
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ROUTER
if st.session_state.page == "home":
    home()
elif st.session_state.page == "assessment":
    assessment()
elif st.session_state.page == "thank_you":
    thank_you()
elif st.session_state.page == "admin":
    admin()
