import streamlit as st

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(
    page_title="Home Care Comfort",
    layout="centered",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
body { background-color:#f4fbfd; }
.card {
    background:#ffffff;
    padding:20px;
    border-radius:12px;
    box-shadow:0px 4px 10px rgba(0,0,0,.05);
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
    padding:7px 16px;
    border-radius:999px;
    font-weight:700;
    color:white;
}
.high { background:#e53e3e; }
.medium { background:#dd6b20; }
.low { background:#10b981; }
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
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
# Header
# -----------------------------
st.markdown(f"### Step {data.step} of {len(steps)} — {steps[data.step]}")
st.progress(data.step / len(steps))

# =======================================================
# STEP 1 — CLIENT INFO (NAME REQUIRED)
# =======================================================
if data.step == 1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.name = st.text_input("Client Name (required)")
    data.client_id = st.text_input("Client ID (optional)")

    if st.button("Next →"):
        if not data.name.strip():
            st.warning("Client name must be entered to continue.")
        else:
            data.step = 2

    st.markdown("</div>", unsafe_allow_html=True)

# =======================================================
# STEP 2 — DEMOGRAPHICS
# =======================================================
elif data.step == 2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.age = st.text_input("Age")
    data.weight = st.text_input("Weight (lbs)")

    st.markdown("### Height")

    col1,col2 = st.columns(2)
    with col1:
        data.height_feet = st.text_input("Feet")
    with col2:
        data.height_inches = st.text_input("Inches")

    back, next = st.columns(2)

    with back:
        if st.button("← Back"):
            data.step = 1

    with next:
        if st.button("Next →"):
            try:
                age = int(data.age)
                weight = float(data.weight)
                feet = int(data.height_feet)
                inches = int(data.height_inches)

                if age <= 0 or weight <= 0:
                    st.warning("Age and weight must be valid positive numbers.")
                elif feet < 0 or inches < 0 or inches > 11:
                    st.warning("Height must be valid (0–11 inches).")
                else:
                    data.height = feet * 12 + inches
                    data.step = 3

            except:
                st.warning("Please enter all demographic fields before continuing.")

    st.markdown("</div>", unsafe_allow_html=True)

# =======================================================
# STEP 3 — MEDICAL HISTORY
# =======================================================
elif data.step == 3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.seizures = st.radio("History of seizures?", ["No", "Yes"], horizontal=True)

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
                "Absence",
            ]
        )

    back, next = st.columns(2)

    with back:
        if st.button("← Back"):
            data.step = 2

    with next:
        if st.button("Next →"):
            if data.seizures == "Yes" and not data.seizure_type:
                st.warning("You must select a seizure type to continue.")
            else:
                data.step = 4

    st.markdown("</div>", unsafe_allow_html=True)

# =======================================================
# STEP 4 — MEDICATIONS
# =======================================================
elif data.step == 4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.medications = st.radio("Does the client take medication?",["No","Yes"], horizontal=True)

    data.med_reason = ""
    data.med_details = ""

    if data.medications == "Yes":
        data.med_reason = st.selectbox(
            "Medication reason",
            ["ADHD","Heart","Blood Pressure","Seizure Medications","Diabetes","Other"]
        )
        data.med_details = st.text_input("Medication & dosage")

    back,next = st.columns(2)

    with back:
        if st.button("← Back"):
            data.step = 3

    with next:
        if st.button("Next →"):
            data.step = 5

    st.markdown("</div>", unsafe_allow_html=True)

# =======================================================
# STEP 5 — MOBILITY & SAFETY
# =======================================================
elif data.step == 5:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    mobility_map = {
        "Walks independently (no assistance needed)":1,
        "Needs occasional supervision or help":2,
        "Uses mobility aid (walker/cane/brace)":3,
        "Requires hands-on assistance":4,
        "Non-mobile / bedridden":5
    }

    mobility_choice = st.selectbox("Mobility level", list(mobility_map.keys()))
    data.mobility = mobility_map[mobility_choice]

    data.adult_present = st.radio("Will an adult be present during care?",["No","Yes"], horizontal=True)

    data.adult1 = ""
    data.adult2 = ""

    if data.adult_present=="Yes":
        data.adult1 = st.text_input("Adult #1 Name")
        data.adult2 = st.text_input("Adult #2 Name")

    data.notes = st.text_area("Additional medical notes")

    back,next = st.columns(2)

    with back:
        if st.button("← Back"):
            data.step = 4

    with next:
        if st.button("Next →"):
            data.step = 6

    st.markdown("</div>", unsafe_allow_html=True)

# =======================================================
# STEP 6 — REVIEW & SCORING
# =======================================================
elif data.step == 6:

    score = 0

    score += float(data.age) * 0.2
    score += float(data.weight) * 0.05
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
        level, cls, msg = "High Risk","high","Close monitoring and supervision recommended."
    elif score > 45:
        level, cls, msg = "Medium Risk","medium","Moderate oversight appropriate."
    else:
        level, cls, msg = "Low Risk","low","Appropriate for standard home care services."

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown(f"<span class='badge {cls}'>{level}</span>", unsafe_allow_html=True)
    st.metric("Risk Score", round(score,1))
    st.write(msg)

    st.subheader("Client Summary")

    for key,val in data.items():
        if key not in ["step"]:
            st.markdown(f"**{key.replace('_',' ').title()}**: {val}")

    if st.button("Start Over"):
        data.clear()
        st.session_state.step = 1

    st.markdown("</div>", unsafe_allow_html=True)

