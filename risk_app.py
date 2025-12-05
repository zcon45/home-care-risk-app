import streamlit as st

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(
    page_title="Home Care Comfort",
    layout="centered"
)

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
.card {
    background:#ffffff;
    padding:20px;
    border-radius:12px;
    box-shadow:0px 4px 10px rgba(0,0,0,.05);
    margin-bottom:20px;
}
.section-title { font-size:20px; font-weight:600; }
.helper { color:#6b7280; font-size:13px; }
.badge {
    padding:7px 16px;
    border-radius:999px;
    font-weight:700;
    color:white;
}
.high { background:#e53e3e; }
.medium { background:#dd6b20; }
.low { background:#10b981; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Session State
# -----------------------------
if "step" not in st.session_state:
    st.session_state.step = 1

data = st.session_state

steps = {
    1:"Client Information",
    2:"Demographics",
    3:"Medical History",
    4:"Medications",
    5:"Mobility & Safety",
    6:"Review"
}

# -----------------------------
# Progress Indicators
# -----------------------------
st.markdown(f"### Step {data.step} of {len(steps)} — {steps[data.step]}")
st.progress(data.step / len(steps))

# =================================================
# STEP 1 — CLIENT INFORMATION
# =================================================
if data.step == 1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.name = st.text_input("Client Name (required)")
    data.client_id = st.text_input("Client ID (optional)")

    if st.button("Next →"):
        if not data.name.strip():
            st.warning("You must enter the client's name to continue.")
        else:
            data.step += 1

    st.markdown("</div>", unsafe_allow_html=True)

# =================================================
# STEP 2 — DEMOGRAPHICS
# =================================================
elif data.step == 2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.age = st.number_input("Age", min_value=0, max_value=120)
    data.weight = st.number_input("Weight (lbs)", min_value=1)

    st.markdown("### Height")
    st.caption("Enter inches OR feet + inches")

    col1, col2 = st.columns(2)
    with col1:
        data.height_inches = st.number_input("Total inches", min_value=0)
    with col2:
        data.height_feet = st.number_input("Feet", min_value=0)
        data.height_extra_inches = st.number_input("Inches", min_value=0, max_value=11)

    left,right = st.columns(2)
    with left:
        if st.button("← Back"):
            data.step -= 1
    with right:
        if st.button("Next →"):
            height_valid = (
                data.height_inches > 0
                or (data.height_feet > 0 or data.height_extra_inches > 0)
            )

            if not data.age or not data.weight or not height_valid:
                st.warning("Age, weight, and height must be completed to continue.")
            else:
                if data.height_inches > 0:
                    data.height = data.height_inches
                else:
                    data.height = data.height_feet * 12 + data.height_extra_inches

                data.step += 1

    st.markdown("</div>", unsafe_allow_html=True)

# =================================================
# STEP 3 — MEDICAL HISTORY
# =================================================
elif data.step == 3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.seizures = st.radio("History of seizures?", ["No","Yes"], horizontal=True)

    data.seizure_type = ""
    if data.seizures == "Yes":
        data.seizure_type = st.selectbox(
            "Seizure type",
            [
                "Generalized — Tonic-clonic",
                "Generalized — Atonic",
                "Generalized — Tonic only",
                "Clonic / Myoclonic",
                "Focal",
                "Absence"
            ]
        )

    left,right = st.columns(2)
    with left:
        if st.button("← Back"):
            data.step -= 1
    with right:
        if st.button("Next →"):
            if data.seizures=="Yes" and not data.seizure_type:
                st.warning("You must select a seizure type.")
            else:
                data.step += 1

    st.markdown("</div>", unsafe_allow_html=True)

# =================================================
# STEP 4 — MEDICATIONS
# =================================================
elif data.step == 4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.medications = st.radio("Does the client take medication?", ["No","Yes"], horizontal=True)

    data.med_reason = ""
    data.med_details = ""

    if data.medications == "Yes":
        data.med_reason = st.selectbox(
            "Medication reason",
            ["ADHD","Heart","Blood Pressure","Seizure Medications","Diabetes","Other"]
        )
        data.med_details = st.text_input(
            "Medication & dosage",
            placeholder="Example: Keppra 500mg twice daily"
        )

    left,right = st.columns(2)
    with left:
        if st.button("← Back"):
            data.step -= 1
    with right:
        if st.button("Next →"):
            data.step += 1

    st.markdown("</div>", unsafe_allow_html=True)

# =================================================
# STEP 5 — MOBILITY & SAFETY
# =================================================
elif data.step == 5:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    mobility_options = {
        "Walks independently with no assistance":1,
        "Needs occasional help or supervision":2,
        "Uses walker, cane, or brace":3,
        "Requires full hands-on assistance":4,
        "Non-mobile or bedridden":5
    }

    mobility_text = st.selectbox("Client mobility", list(mobility_options.keys()))
    data.mobility = mobility_options[mobility_text]

    data.adult_present = st.radio("Will an adult be present during care?",["No","Yes"], horizontal=True)

    data.adult1 = data.adult2 = ""
    if data.adult_present=="Yes":
        data.adult1 = st.text_input("Adult 1 name")
        data.adult2 = st.text_input("Adult 2 name")

    data.notes = st.text_area("Additional medical notes")

    left,right = st.columns(2)
    with left:
        if st.button("← Back"):
            data.step -= 1
    with right:
        if st.button("Next →"):
            data.step += 1

    st.markdown("</div>", unsafe_allow_html=True)

# =================================================
# STEP 6 — REVIEW & SCORE
# =================================================
elif data.step == 6:

    score = 0
    score += data.age * 0.2
    score += data.weight * 0.05
    score += data.height * 0.05
    score += data.mobility * 5

    seizure_scores = {
        "Generalized — Tonic-clonic":20,
        "Generalized — Atonic":15,
        "Generalized — Tonic only":12,
        "Clonic / Myoclonic":10,
        "Focal":8,
        "Absence":5
    }

    if data.seizures=="Yes":
        score += 10
        score += seizure_scores.get(data.seizure_type,0)

    if data.medications=="Yes":
        score += 10

    if data.adult_present=="Yes":
        score -= 5

    if score > 70:
        level,cls,msg = "High Risk","high","Close monitoring recommended."
    elif score > 45:
        level,cls,msg = "Medium Risk","medium","Moderate supervision recommended."
    else:
        level,cls,msg = "Low Risk","low","Appropriate for standard care."

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown(f"<span class='badge {cls}'>{level}</span>", unsafe_allow_html=True)
    st.metric("Risk Score",round(score,1))
    st.write(msg)

    st.subheader("Client Summary")

    for k,v in data.items():
        if k not in ["step","height_inches","height_feet","height_extra_inches"]:
            st.markdown(f"**{k.replace('_',' ').title()}**: {v}")

    if st.button("Start Over"):
        data.clear()
        st.session_state.step = 1

    st.markdown("</div>", unsafe_allow_html=True)
