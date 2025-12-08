# app.py - Home Care Comfort Portal (Updated with Client Assessment Flow)
import streamlit as st

# Page Config
st.set_page_config(
    page_title="Home Care Comfort Portal",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Professional Look
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
    }
    .portal-card {
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        text-align: center;
        max-width: 800px;
        margin: 0 auto;
    }
    .assessment-card {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        max-width: 700px;
        margin: 0 auto;
    }
    .portal-title, .assessment-title {
        font-size: 2.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    .portal-subtitle, .assessment-subtitle {
        font-size: 1.2rem;
        color: #7f8c8d;
        margin-bottom: 2rem;
    }
    .access-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 600;
        width: 100%;
        margin: 1rem 0;
        transition: transform 0.2s;
    }
    .access-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    .admin-button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .client-button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    .next-button {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 600;
        width: 100%;
        margin-top: 2rem;
        transition: transform 0.2s;
    }
    .next-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    .stButton > button {
        background: none;
        border: none;
        padding: 0;
        margin: 0;
    }
    .form-section {
        margin-bottom: 1.5rem;
    }
    .step-indicator {
        font-size: 1rem;
        color: #7f8c8d;
        margin-bottom: 1rem;
        text-align: left;
    }
</style>
""", unsafe_allow_html=True)

# Session State for Navigation and Data
if "page" not in st.session_state:
    st.session_state.page = "home"
if "assessment_step" not in st.session_state:
    st.session_state.assessment_step = 1
if "client_data" not in st.session_state:
    st.session_state.client_data = {
        "first_name": "",
        "last_name": "",
        "client_id": "",
        "age": "",
        "height": "",
        "weight": "",
        "diagnoses": "No",
        "diagnoses_details": "",
        "seizures": "No",
        "seizure_types": "",
        "medications": "No",
        "medications_details": "",
        "assist_medical": "No"
    }

# Home Page
def home_page():
    st.markdown("""
    <div class="portal-card">
        <h1 class="portal-title">🏠 Home Care Comfort Portal</h1>
        <p class="portal-subtitle">Secure, professional assessment and coordination for home care services.</p>
        
        <div style="display: flex; flex-direction: column; gap: 1rem; max-width: 400px; margin: 0 auto;">
            <button class="access-button client-button" onclick="this.blur();">👤 Client Assessment</button>
            <button class="access-button admin-button" onclick="this.blur();">🛡️ Admin Dashboard</button>
        </div>
        
        <p style="margin-top: 2rem; color: #bdc3c7; font-size: 0.9rem;">
            Powered by Streamlit | Confidential & Secure
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Handle button clicks (using Streamlit buttons hidden under CSS)
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Client Assessment Button", key="client_btn"):
            st.session_state.page = "assessment"
            st.session_state.assessment_step = 1
            st.rerun()
    with col2:
        if st.button("Admin Dashboard Button", key="admin_btn"):
            st.session_state.page = "admin"
            st.rerun()

# Client Assessment Pages
def assessment_page():
    data = st.session_state.client_data
    st.markdown("<div class='assessment-card'>", unsafe_allow_html=True)
    st.markdown("<h1 class='assessment-title'>Client Risk Assessment</h1>", unsafe_allow_html=True)
    st.markdown("<p class='assessment-subtitle'>Please provide accurate information for a comprehensive evaluation.</p>", unsafe_allow_html=True)

    if st.session_state.assessment_step == 1:
        st.markdown("<div class='step-indicator'>Step 1 of 3: Basic Identification</div>", unsafe_allow_html=True)
        with st.form("step1_form"):
            st.markdown("<div class='form-section'>", unsafe_allow_html=True)
            data["first_name"] = st.text_input("First Name*", value=data["first_name"])
            data["last_name"] = st.text_input("Last Name*", value=data["last_name"])
            data["client_id"] = st.text_input("Client ID*", value=data["client_id"])
            st.markdown("</div>", unsafe_allow_html=True)
            
            if st.form_submit_button("Next →", type="primary"):
                if data["first_name"] and data["last_name"] and data["client_id"]:
                    st.session_state.assessment_step = 2
                    st.rerun()
                else:
                    st.error("Please fill all required fields.")

    elif st.session_state.assessment_step == 2:
        st.markdown("<div class='step-indicator'>Step 2 of 3: Physical Profile</div>", unsafe_allow_html=True)
        with st.form("step2_form"):
            st.markdown("<div class='form-section'>", unsafe_allow_html=True)
            data["age"] = st.text_input("Age*", value=data["age"])
            cols = st.columns(2)
            with cols[0]:
                data["height"] = st.text_input("Height (e.g., 5'10\")*", value=data["height"])
            with cols[1]:
                data["weight"] = st.text_input("Weight (lbs)*", value=data["weight"])
            st.markdown("</div>", unsafe_allow_html=True)
            
            col_back, col_next = st.columns(2)
            with col_back:
                if st.form_submit_button("← Back"):
                    st.session_state.assessment_step = 1
                    st.rerun()
            with col_next:
                if st.form_submit_button("Next →", type="primary"):
                    if data["age"] and data["height"] and data["weight"]:
                        st.session_state.assessment_step = 3
                        st.rerun()
                    else:
                        st.error("Please fill all required fields.")

    elif st.session_state.assessment_step == 3:
        st.markdown("<div class='step-indicator'>Step 3 of 3: Medical Profile</div>", unsafe_allow_html=True)
        with st.form("step3_form"):
            st.markdown("<div class='form-section'>", unsafe_allow_html=True)
            data["diagnoses"] = st.radio("Any Diagnoses?", ["No", "Yes"], horizontal=True)
            if data["diagnoses"] == "Yes":
                data["diagnoses_details"] = st.text_area("Please specify diagnoses", value=data["diagnoses_details"])
            
            data["seizures"] = st.radio("Seizure History?", ["No", "Yes"], horizontal=True)
            if data["seizures"] == "Yes":
                data["seizure_types"] = st.text_area("Please specify seizure types", value=data["seizure_types"])
            
            data["medications"] = st.radio("Medication History?", ["No", "Yes"], horizontal=True)
            if data["medications"] == "Yes":
                data["medications_details"] = st.text_area("Please specify medications", value=data["medications_details"])
            
            data["assist_medical"] = st.radio("Provider Expected to Assist with Medical Needs?", ["No", "Yes"], horizontal=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            col_back, col_submit = st.columns(2)
            with col_back:
                if st.form_submit_button("← Back"):
                    st.session_state.assessment_step = 2
                    st.rerun()
            with col_submit:
                if st.form_submit_button("Submit Assessment", type="primary"):
                    # Here we'll handle submission - for now, just navigate to a confirmation
                    st.session_state.page = "home"  # Or to admin, etc. - we'll add later
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# Admin Page (Placeholder for now)
def admin_page():
    st.markdown("<div class='assessment-card'>", unsafe_allow_html=True)
    st.markdown("<h1 class='assessment-title'>Admin Dashboard</h1>", unsafe_allow_html=True)
    st.info("Admin features coming soon. Assessments will be listed here.")
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Router
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "assessment":
    assessment_page()
elif st.session_state.page == "admin":
    admin_page()
