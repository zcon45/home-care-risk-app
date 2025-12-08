import streamlit as st
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="Home Care Comfort Portal",
    page_icon="house",
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
    .detail-box {
        background: #f8f9fc; padding: 1.2rem; border-radius: 12px; 
        border: 1px solid #e0e0e0; margin-top: 0.8rem; margin-bottom: 1.5rem;
    }
    .badge {
        padding: 10px 26px; border-radius: 50px; font-weight: bold; font-size: 1.1rem; display: inline-block;
    }
    .low {background:#10b981; color:white;}
    .medium {background:#f59e0b; color:white;}
    .high {background:#ef4444; color:white;}
    .risk-breakdown {background:#f1f8ff; padding:1rem; border-radius:12px; border-left:4px solid #3b82f6;}
</style>
""", unsafe_allow_html=True)

# Session State + Backward Compatibility
if "page" not in st.session_state:
    st.session_state.page = "home"
if "step" not in st.session_state:
    st.session_state.step = 1
if "data" not in st.session_state:
    st.session_state.data = {}
if "assessments" not in st.session_state:
    st.session_state.assessments = []

# Default data structure (with safe defaults)
default_data = {
    "first_name": "", "last_name": "", "client_id": "",
    "age": "", "height": "", "weight": "",
    "diagnoses": "No", "diagnoses_details": "",
    "seizures": "No", "seizure_details": "",
    "medications": "No", "medication_details": "",
    "assist_medical": "No",
    "behavior_mood": "Stable", "behavior_sleep": "Good",
    "behavior_social": "Active", "behavior_daily": "Independent",
    "behavior_mental": "No", "behavior_mental_details": ""
}

# Ensure current data has all keys
for key, value in default_data.items():
    if key not in st.session_state.data:
        st.session_state.data[key] = value

data = st.session_state.data

# HOME PAGE
def home():
    st.markdown('<div class="portal-card">', unsafe_allow_html=True)
    st.markdown('<h1 class="portal-title">Home Care Comfort Portal</h1>', unsafe_allow_html=True)
    st.markdown('<p class="portal-subtitle">Comprehensive Medical & Behavioral Assessment</p>', unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        if st.button("Client Assessment", key="client", use_container_width=True):
            st.session_state.page = "assessment"
            st.session_state.step = 1
            st.rerun()
    with c2:
        if st.button("Admin Dashboard", key="admin", use_container_width=True):
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
    st.markdown("<h2 style='text-align:center; color:#2c3e50;'>Client Assessment</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#636e72; margin-bottom:2rem;'>4 quick steps • Takes ~5 minutes</p>", unsafe_allow_html=True)
    
    progress = {"1": 0.25, "2": 0.5, "3": 0.75, "4": 1.0}
    st.progress(progress[str(st.session_state.step)])

    if st.session_state.step == 1:
        st.markdown("<div class='step-header'>Step 1 of 4 • Client Identification</div>", unsafe_allow_html=True)
        with st.form("step1"):
            data["first_name"] = st.text_input("First Name*", value=data["first_name"])
            data["last_name"] = st.text_input("Last Name*", value=data["last_name"])
            data["client_id"] = st.text_input("Client ID*", value=data["client_id"])
            if st.form_submit_button("Next", use_container_width=True):
                if all([data["first_name"], data["last_name"], data["client_id"]]):
                    st.session_state.step = 2
                    st.rerun()
                else:
                    st.error("All fields required")

    elif st.session_state.step == 2:
        st.markdown("<div class='step-header'>Step 2 of 4 • Physical Profile</div>", unsafe_allow_html=True)
        with st.form("step2"):
            data["age"] = st.text_input("Age*", value=data["age"], placeholder="e.g. 74")
            c1, c2 = st.columns(2)
            with c1:
                data["height"] = st.text_input("Height*", value=data["height"], placeholder="e.g. 5'7\"")
            with c2:
                data["weight"] = st.text_input("Weight (lbs)*", value=data["weight"], placeholder="e.g. 165")
            cback, cnext = st.columns(2)
            with cback:
                if st.form_submit_button("Back"):
                    st.session_state.step = 1
                    st.rerun()
            with cnext:
                if st.form_submit_button("Next", use_container_width=True):
                    if data["age"] and data["height"] and data["weight"]:
                        st.session_state.step = 3
                        st.rerun()
                    else:
                        st.error("All fields required")

    elif st.session_state.step == 3:
        st.markdown("<div class='step-header'>Step 3 of 4 • Medical History</div>", unsafe_allow_html=True)
        with st.form("step3"):
            st.markdown("#### Medical Conditions")
            c1, c2 = st.columns([3,2])
            with c1:
                data["diagnoses"] = st.radio("Any diagnosed conditions?", ["No", "Yes"], horizontal=True, key="diag_radio")
            if data["diagnoses"] == "Yes":
                with c2:
                    data["diagnoses_details"] = st.text_area("Details", value=data["diagnoses_details"], height=80, label_visibility="collapsed", key="diag_detail")

            c1, c2 = st.columns([3,2])
            with c1:
                data["seizures"] = st.radio("History of seizures?", ["No", "Yes"], horizontal=True, key="seiz_radio")
            if data["seizures"] == "Yes":
                with c2:
                    data["seizure_details"] = st.text_area("Details", value=data["seizure_details"], height=80, label_visibility="collapsed", key="seiz_detail")

            c1, c2 = st.columns([3,2])
            with c1:
                data["medications"] = st.radio("Taking medications?", ["No", "Yes"], horizontal=True, key="med_radio")
            if data["medications"] == "Yes":
                with c2:
                    data["medication_details"] = st.text_area("Details", value=data["medication_details"], height=80, label_visibility="collapsed", key="med_detail")

            data["assist_medical"] = st.radio("Will caregiver assist with medical tasks?", ["No", "Yes"], horizontal=True, key="assist_radio")

            cback, cnext = st.columns(2)
            with cback:
                if st.form_submit_button("Back"):
                    st.session_state.step = 2
                    st.rerun()
            with cnext:
                if st.form_submit_button("Next", use_container_width=True):
                    st.session_state.step = 4
                    st.rerun()

    elif st.session_state.step == 4:
        st.markdown("<div class='step-header'>Step 4 of 4 • Behavioral Profile</div>", unsafe_allow_html=True)
        with st.form("step4"):
            st.markdown("#### Daily Functioning & Behavior")
            data["behavior_mood"] = st.selectbox("Mood over past month?", ["Stable", "Occasional changes", "Frequent changes"], key="mood")
            data["behavior_sleep"] = st.selectbox("Sleep quality?", ["Good (7-9 hrs)", "Fair (5-7 hrs)", "Poor (<5 hrs)"], key="sleep")
            data["behavior_social"] = st.selectbox("Social engagement?", ["Active & positive", "Limited", "Withdrawn"], key="social")
            data["behavior_daily"] = st.selectbox("Daily activities (ADLs)?", ["Independent", "Some help needed", "Full assistance"], key="adl")
            data["behavior_mental"] = st.radio("Any mental health history?", ["No", "Yes"], horizontal=True, key="mental_radio")
            if data["behavior_mental"] == "Yes":
                data["behavior_mental_details"] = st.text_area("Details", value=data["behavior_mental_details"], height=100, key="mental_detail")

            cback, csubmit = st.columns(2)
            with cback:
                if st.form_submit_button("Back"):
                    st.session_state.step = 3
                    st.rerun()
            with csubmit:
                if st.form_submit_button("Submit Assessment", type="primary", use_container_width=True):
                    st.session_state.assessments.append(data.copy())
                    st.success("Assessment submitted successfully!")
                    st.balloons()
                    # Reset form
                    st.session_state.data = default_data.copy()
                    st.session_state.step = 1
                    st.session_state.page = "admin"
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ADMIN DASHBOARD
def admin():
    st.markdown('<div class="assessment-card">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#2c3e50;'>Admin Dashboard</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#636e72;'>All Completed Client Assessments</p>", unsafe_allow_html=True)
    
    if not st.session_state.assessments:
        st.info("No assessments submitted yet.")
    else:
        for i, ass in enumerate(reversed(st.session_state.assessments)):
            name = f"{ass.get('first_name','')} {ass.get('last_name','')}".strip()
            client_id = ass.get('client_id', 'N/A')
            
            # Safe risk calculation
            try:
                age = int(ass.get('age', 0) or 0)
                weight = float(ass.get('weight', 0) or 0)
                height_str = ass.get('height', '0')
                height_ft = height_in = 0
                if "'" in height_str:
                    parts = height_str.replace('"','').split("'")
                    height_ft = int(parts[0]) if parts[0].isdigit() else 0
                    height_in = int(parts[1]) if len(parts)>1 and parts[1].isdigit() else 0
                height_inches = height_ft*12 + height_in
                
                score = 0
                breakdown = []
                score += age * 0.2; breakdown.append(f"Age ({age}): +{age*0.2:.1f}")
                score += weight * 0.05; breakdown.append(f"Weight ({weight} lbs): +{weight*0.05:.1f}")
                score += height_inches * 0.05; breakdown.append(f"Height ({height_inches} in): +{height_inches*0.05:.1f}")
                if ass.get('diagnoses') == "Yes": score += 10; breakdown.append("Diagnoses: +10")
                if ass.get('seizures') == "Yes": score += 25; breakdown.append("Seizures: +25")
                if ass.get('medications') == "Yes": score += 10; breakdown.append("Medications: +10")
                if ass.get('assist_medical') == "Yes": score += 15; breakdown.append("Medical Assistance: +15")
                if ass.get('behavior_mood') != "Stable": score += 10; breakdown.append("Mood instability: +10")
                if ass.get('behavior_sleep') != "Good (7-9 hrs)": score += 10; breakdown.append("Poor sleep: +10")
                if ass.get('behavior_social') != "Active & positive": score += 10; breakdown.append("Social withdrawal: +10")
                if ass.get('behavior_daily') != "Independent": score += 15; breakdown.append("ADL dependence: +15")
                if ass.get('behavior_mental') == "Yes": score += 20; breakdown.append("Mental health history: +20")
                
                level = "Low" if score < 60 else "Medium" if score < 100 else "High"
            except:
                score, level, breakdown = 0, "Error", ["Calculation error"]
            
            risk_class = level.lower()
            with st.expander(f"{name} • ID: {client_id} • Risk: <span class='badge {risk_class}'>{level}</span> (Score: {score:.1f})", expanded=True):
                st.write(f"**Submitted:** {datetime.now().strftime('%b %d, %Y • %I:%M %p')}")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Age:** {ass.get('age','—')} | **Height:** {ass.get('height','—')} | **Weight:** {ass.get('weight','—')} lbs")
                    st.write(f"**Diagnoses:** {ass.get('diagnoses','—')}")
                    if ass.get('diagnoses_details'): st.write("→ " + ass.get('diagnoses_details',''))
                    st.write(f"**Seizures:** {ass.get('seizures','—')}")
                    if ass.get('seizure_details'): st.write("→ " + ass.get('seizure_details',''))
                with col2:
                    st.write(f"**Medications:** {ass.get('medications','—')}")
                    if ass.get('medication_details'): st.write("→ " + ass.get('medication_details',''))
                    st.write(f"**Medical Assistance Needed:** {ass.get('assist_medical','—')}")
                    st.write(f"**Daily Activities:** {ass.get('behavior_daily','—')}")
                    st.write(f"**Mood:** {ass.get('behavior_mood','—')} | **Sleep:** {ass.get('behavior_sleep','—')}")
                
                st.markdown("### Risk Score Breakdown", unsafe_allow_html=True)
                st.markdown("<div class='risk-breakdown'>", unsafe_allow_html=True)
                for item in breakdown:
                    st.write("• " + item)
                st.write(f"**Final Score: {score:.1f} → {level} Risk**")
                st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ROUTER
if st.session_state.page == "home":
    home()
elif st.session_state.page == "assessment":
    assessment()
elif st.session_state.page == "admin":
    admin()
