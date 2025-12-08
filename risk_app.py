import streamlit as st

# Page Config
st.set_page_config(
    page_title="Home Care Comfort Portal",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Professional CSS
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);}
    .portal-card {
        background: white; padding: 3.5rem; border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center;
        max-width: 800px; margin: 3rem auto;
    }
    .portal-title {font-size: 3rem; color: #2c3e50; font-weight: 700; margin-bottom: 0.5rem;}
    .portal-subtitle {font-size: 1.25rem; color: #7f8c8d; margin-bottom: 3rem;}
    .client-btn {background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);}
    .admin-btn {background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);}
    .access-btn {
        color: white !important; border: none; padding: 1.3rem;
        border-radius: 50px; font-size: 1.25rem; font-weight: 600;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2); transition: all 0.3s;
    }
    .access-btn:hover {transform: translateY(-4px); box-shadow: 0 10px 30px rgba(0,0,0,0.3);}
    .footer-text {margin-top: 3rem; color: #bdc3c7; font-size: 0.95rem;}
    .assessment-card {background: white; padding: 2.5rem; border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); max-width: 700px; margin: 2rem auto;}
    .step-header {font-size: 1.1rem; color: #636e72; margin-bottom: 1.5rem; text-align: center;}
    .next-btn {background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);}
</style>
""", unsafe_allow_html=True)

# Session State
if "page" not in st.session_state:
    st.session_state.page = "home"
if "step" not in st.session_state:
    st.session_state.step = 1
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

# HOME PAGE
def home():
    st.markdown('<div class="portal-card">', unsafe_allow_html=True)
    st.markdown('<h1 class="portal-title">🏠 Home Care Comfort Portal</h1>', unsafe_allow_html=True)
    st.markdown('<p class="portal-subtitle">Secure, professional assessment and coordination for home care services.</p>', unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        if st.button("👤 Client Assessment", key="client", use_container_width=True):
            st.session_state.page = "assessment"
            st.session_state.step = 1
            st.rerun()
    with c2:
        if st.button("🛡️ Admin Dashboard", key="admin", use_container_width=True):
            st.session_state.page = "admin"
            st.rerun()

    st.markdown("""
    <script>
        const buttons = document.querySelectorAll('[data-testid="stButton"] button');
        if (buttons[0]) buttons[0].classList.add('access-btn', 'client-btn');
        if (buttons[1]) buttons[1].classList.add('access-btn', 'admin-btn');
    </script>
    """, unsafe_allow_html=True)

    st.markdown('<p class="footer-text">Powered by Streamlit • Confidential & Secure</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ASSESSMENT
def assessment():
    st.markdown('<div class="assessment-card">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#2c3e50;'>Client Risk Assessment</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#636e72; margin-bottom:2rem;'>Please complete all three steps</p>", unsafe_allow_html=True)
    
    # Progress bar
    progress = {"1": 0.33, "2": 0.66, "3": 1.0}
    st.progress(progress[str(st.session_state.step)])

    if st.session_state.step == 1:
        st.markdown("<div class='step-header'>Step 1 of 3 • Client Identification</div>", unsafe_allow_html=True)
        with st.form("step1"):
            data["first_name"] = st.text_input("First Name*", value=data["first_name"])
            data["last_name"] = st.text_input("Last Name*", value=data["last_name"])
            data["client_id"] = st.text_input("Client ID*", value=data["client_id"])
            if st.form_submit_button("Next →", use_container_width=True):
                if data["first_name"] and data["last_name"] and data["client_id"]:
                    st.session_state.step = 2
                    st.rerun()
                else:
                    st.error("Please fill in all required fields")

    elif st.session_state.step == 2:
        st.markdown("<div class='step-header'>Step 2 of 3 • Physical Profile</div>", unsafe_allow_html=True)
        with st.form("step2"):
            data["age"] = st.text_input("Age*", value=data["age"], placeholder="e.g. 74")
            col1, col2 = st.columns(2)
            with col1:
                data["height"] = st.text_input("Height*", value=data["height"], placeholder="e.g. 5'7\"")
            with col2:
                data["weight"] = st.text_input("Weight (lbs)*", value=data["weight"], placeholder="e.g. 165")
            
            colb, coln = st.columns(2)
            with colb:
                if st.form_submit_button("← Back"):
                    st.session_state.step = 1
                    st.rerun()
            with coln:
                if st.form_submit_button("Next →", use_container_width=True):
                    if data["age"] and data["height"] and data["weight"]:
                        st.session_state.step = 3
                        st.rerun()
                    else:
                        st.error("Please complete all fields")

    elif st.session_state.step == 3:
        st.markdown("<div class='step-header'>Step 3 of 3 • Medical Profile</div>", unsafe_allow_html=True)
        with st.form("step3"):
            st.markdown("#### Medical History", unsafe_allow_html=True)
            
            data["diagnoses"] = st.radio("Any medical diagnoses?", ["No", "Yes"], horizontal=True)
            if data["diagnoses"] == "Yes":
                data["diagnoses_details"] = st.text_area("Please list all diagnoses", value=data["diagnoses_details"], height=100)

            data["seizures"] = st.radio("History of seizures?", ["No", "Yes"], horizontal=True)
            if data["seizures"] == "Yes":
                data["seizure_details"] = st.text_area("Please describe seizure type and frequency", value=data["seizure_details"], height=100)

            data["medications"] = st.radio("Currently taking medications?", ["No", "Yes"], horizontal=True)
            if data["medications"] == "Yes":
                data["medication_details"] = st.text_area("Please list medications and dosages", value=data["medication_details"], height=120)

            data["assist_medical"] = st.radio("Will provider be expected to assist with any medical needs?", ["No", "Yes"], horizontal=True)

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

# THANK YOU PAGE
def thank_you():
    st.markdown('<div class="assessment-card">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#2c3e50;'>Thank You!</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1.2rem;'>Your assessment has been submitted successfully.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>A care coordinator will review your information shortly.</p>", unsafe_allow_html=True)
    if st.button("← Return to Home", use_container_width=True):
        st.session_state.page = "home"
        st.session_state.step = 1
        for key in data:
            data[key] = "" if "_details" not in key else data[key]
        data.update({"diagnoses":"No","seizures":"No","medications":"No","assist_medical":"No"})
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ADMIN PAGE
def admin():
    st.markdown('<div class="assessment-card">', unsafe_allow_html=True)
    st.title("Admin Dashboard")
    st.info("Submitted assessments will appear here in the next update.")
    if st.button("← Back to Home"):
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
