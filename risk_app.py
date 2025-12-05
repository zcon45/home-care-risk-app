import streamlit as st

# -------------------------------------
# Page Setup
# -------------------------------------
st.set_page_config(
    page_title="Home Care Comfort",
    layout="centered"
)

# -------------------------------------
# Styling
# -------------------------------------
st.markdown("""
<style>
body { background-color:#f4fbfd; }
.card {
    background:#fff;
    padding:20px;
    border-radius:12px;
    box-shadow:0 4px 12px rgba(0,0,0,0.05);
    margin-bottom:20px;
}
.section-title {
    font-size:20px;
    font-weight:600;
}
.helper {
    color:#6b7280;
    font-size:13px;
}
.badge {
    padding:7px 14px;
    border-radius:999px;
    color:white;
    font-weight:600;
}
.high { background:#e53e3e; }
.medium { background:#dd6b20; }
.low { background:#10b981; }
progress {
    width:100%;
    height:20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------
# Session State Setup
# -------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 1

# -------------------------------------
# Progress UI
# -------------------------------------
steps = {
    1:"Client Info",
    2:"Demographics",
    3:"Medical",
    4:"Medications",
    5:"Safety",
    6:"Review"
}

st.markdown(
    f"### Step {st.session_state.step} of {len(steps)} — {steps[st.session_state.step]}"
)

st.progress(st.session_state.step/len(steps))

# -------------------------------------
# Data Storage
# -------------------------------------
data = st.session_state

# -------------------------------------
# STEP 1 — Client info
# -------------------------------------
if st.session_state.step == 1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.name = st.text_input("Client Name")
    data.client_id = st.text_input("Client ID Number")

    st.markdown("<p class='helper'>This helps us keep records organized.</p>", unsafe_allow_html=True)

    if st.button("Next →"):
        st.session_state.step += 1

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------
# STEP 2 — Demographics
# -------------------------------------
elif st.session_state.step == 2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.age = st.selectbox("Age", list(range(18,101)))
    st.caption("Used to assess general health risk.")

    data.height = st.selectbox("Height (inches)", list(range(50,85)))
    data.weight = st.selectbox("Weight (lbs)", list(range(80,301)))

    col1,col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            st.session_state.step -= 1

    with col2:
        if st.button("Next →"):
            st.session_state.step += 1

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------
# STEP 3 — Medical
# -------------------------------------
elif st.session_state.step == 3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.seizures = st.radio("History of seizures?", ["No","Yes"], horizontal=True)

    data.seizure_type = ""
    if data.seizures == "Yes":
        data.seizure_type = st.selectbox(
            "Seizure type",
            [
                "Generalized—Tonic-clonic",
                "Generalized—Atonic",
                "Generalized—Tonic only",
                "Clonic/Myoclonic",
                "Focal",
                "Absence"
            ]
        )

    col1,col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            st.session_state.step -= 1
    with col2:
        if st.button("Next →"):
            if data.seizures=="Yes" and not data.seizure_type:
                st.warning("Please select a seizure type.")
            else:
                st.session_state.step += 1

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------
# STEP 4 — Medications
# -------------------------------------
elif st.session_state.step == 4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.medications = st.radio("Does the client take medication?",["No","Yes"],horizontal=True)

    data.med_reason = data.med_details = ""

    if data.medications == "Yes":
        data.med_reason = st.selectbox(
            "Primary medication reason",
            ["ADHD","Heart","Blood Pressure","Seizure Meds","Diabetes","Other"]
        )

        data.med_details = st.text_input(
            "Medication names & dosage",
            placeholder="Example: Keppra 500mg twice daily"
        )

    col1,col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            st.session_state.step -= 1

    with col2:
        if st.button("Next →"):
            st.session_state.step += 1

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------
# STEP 5 — Safety
# -------------------------------------
elif st.session_state.step == 5:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.adult_present = st.radio("Will an adult be present during care?",["No","Yes"],horizontal=True)

    data.adult1=data.adult2=""
    if data.adult_present=="Yes":
        data.adult1 = st.text_input("Adult #1 name")
        data.adult2 = st.text_input("Adult #2 name")

    data.mobility = st.selectbox("Mobility score (1 best – 5 worst)",list(range(1,6)))
    st.caption("Lower mobility increases fall & safety risk.")

    data.notes = st.text_area("Additional medical notes")

    col1,col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            st.session_state.step -= 1

    with col2:
        if st.button("Next →"):
            st.session_state.step += 1

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------
# STEP 6 — REVIEW
# -------------------------------------
elif st.session_state.step == 6:
    
    # ----- SCORING -----
    score = 0
    score += data.age * 0.2
    score += data.weight * 0.05
    score += data.height * 0.05
    score += data.mobility * 5
    
    seizure_weights = {
        "Generalized—Tonic-clonic":20,
        "Generalized—Atonic":15,
        "Generalized—Tonic only":12,
        "Clonic/Myoclonic":10,
        "Focal":8,
        "Absence":5
    }

    if data.seizures=="Yes":
        score += 10
        score += seizure_weights.get(data.seizure_type,0)

    if data.medications=="Yes":
        score += 10

    if data.adult_present=="Yes":
        score -= 5
    
    # ----- LEVEL -----
    if score > 70:
        level, cls = "High Risk", "high"
        text = "Client requires close monitoring and potential 1:1 supervision."
    elif score > 45:
        level, cls = "Medium Risk","medium"
        text = "Client suitable for home care with moderate safety oversight."
    else:
        level, cls = "Low Risk","low"
        text = "Client appropriate for standard home care services."

    # ----- OUTPUT -----
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown(f"<span class='badge {cls}'>{level}</span>", unsafe_allow_html=True)
    st.metric("Risk Score",round(score,1))
    st.write(text)

    st.divider()

    st.subheader("Client Summary")

    for key,val in data.items():
        st.markdown(f"**{key.replace('_',' ').title()}**: {val}")

    if st.button("← Edit"):
        st.session_state.step = 1

    st.markdown("</div>", unsafe_allow_html=True)
