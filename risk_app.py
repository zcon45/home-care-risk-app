import streamlit as st

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Home Care Comfort",
    layout="centered",
)

# =========================================
# STYLING
# =========================================

st.markdown("""
<style>
body {
    background-color:#f4fbfd;
}
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
input[type=number] {
    -moz-appearance:textfield;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# SESSION STATE INITIALIZATION
# =========================================

if "step" not in st.session_state:
    st.session_state.step = 1

data = st.session_state

steps = {
    1: "Client Information",
    2: "Demographics",
    3: "Medical History",
    4: "Medications",
    5: "Mobility & Safety",
    6: "Review"
}

# =========================================
# CALLBACK HANDLERS
# =========================================

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

def reset_all():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.session_state.step = 1

# =========================================
# HEADER + PROGRESS
# =========================================

st.markdown(f"### Step {data.step} of {len(steps)} — {steps[data.step]}")
st.progress(data.step / len(steps))


# =========================================
# STEP 1 — CLIENT INFO
# =========================================

if data.step == 1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.name = st.text_input("Client Name (required)")
    data.client_id = st.text_input("Client ID (optional)")

    if not data.name.strip():
        st.warning("Client name is required before continuing.")

    st.button(
        "Next →",
        on_click=next_step,
        disabled=not data.name.strip(),
        key="next1"
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# STEP 2 — DEMOGRAPHICS
# =========================================

elif data.step == 2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.age = st.text_input("Age")
    data.weight = st.text_input("Weight (lbs)")

    st.markdown("### Height")
    col1, col2 = st.columns(2)
    with col1:
        data.height_feet = st.text_input("Feet")
    with col2:
        data.height_inches = st.text_input("Inches (0–11)")

    def valid_demographics():
        try:
            age = int(data.age)
            weight = float(data.weight)
            ft = int(data.height_feet)
            inch = int(data.height_inches)
            return age > 0 and weight > 0 and ft >= 0 and 0 <= inch <= 11
        except:
            return False

    col_back, col_next = st.columns(2)
    with col_back:
        st.button("← Back", on_click=prev_step, key="back2")

    with col_next:
        st.button("Next →", on_click=next_step, disabled=not valid_demographics(), key="next2")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# STEP 3 — SEIZURES
# =========================================

elif data.step == 3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.seizures = st.radio("History of seizures?", ["No", "Yes"], horizontal=True)

    if data.seizures == "Yes":
        seizure_options = [
            "Select seizure type...",
            "Generalized — Tonic-clonic",
            "Generalized — Atonic",
            "Generalized — Tonic only",
            "Clonic / Myoclonic",
            "Focal",
            "Absence"
        ]

        data.seizure_type = st.selectbox("Seizure Type", seizure_options)

        seizure_ok = data.seizure_type != "Select seizure type..."
    else:
        data.seizure_type = ""
        seizure_ok = True

    col_back, col_next = st.columns(2)
    with col_back:
        st.button("← Back", on_click=prev_step, key="back3")

    with col_next:
        st.button("Next →", on_click=next_step, disabled=not seizure_ok, key="next3")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# STEP 4 — MEDICATIONS
# =========================================

elif data.step == 4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.medications = st.radio("Does the client take medication?", ["No", "Yes"], horizontal=True)

    if data.medications == "Yes":
        data.med_reason = st.selectbox(
            "Medication reason",
            ["ADHD", "Heart", "Blood Pressure", "Seizure Medications", "Diabetes", "Other"]
        )

        data.med_details = st.text_input("Medication & dosage")

    col_back, col_next = st.columns(2)
    with col_back:
        st.button("← Back", on_click=prev_step, key="back4")
    with col_next:
        st.button("Next →", on_click=next_step, key="next4")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# STEP 5 — MOBILITY & SAFETY
# =========================================

elif data.step == 5:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    mobility_map = {
        "Walks independently (no assistance needed)": 1,
        "Needs occasional supervision or help": 2,
        "Uses mobility aid (walker/cane/brace)": 3,
        "Requires hands-on assistance": 4,
        "Non-mobile / bedridden": 5
    }

    data.mobility_label = st.selectbox("Mobility", list(mobility_map.keys()))
    data.mobility = mobility_map[data.mobility_label]

    data.adult_present = st.radio("Will adult be present?", ["No","Yes"], horizontal=True)

    if data.adult_present == "Yes":
        data.adult1 = st.text_input("Adult #1 Name")
        data.adult2 = st.text_input("Adult #2 Name")

    data.notes = st.text_area("Additional notes")

    col_back, col_next = st.columns(2)
    with col_back:
        st.button("← Back", on_click=prev_step, key="back5")
    with col_next:
        st.button("Next →", on_click=next_step, key="next5")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# STEP 6 — REVIEW
# =========================================

elif data.step == 6:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    age = int(data.age)
    weight = float(data.weight)
    height = int(data.height_feet)*12 + int(data.height_inches)
    score = age*0.2 + weight*0.05 + height*0.05 + data.mobility*5

    seizure_scores = {
        "Generalized — Tonic-clonic":20,
        "Generalized — Atonic":15,
        "Generalized — Tonic only":12,
        "Clonic / Myoclonic":10,
        "Focal":8,
        "Absence":5
    }

    if data.seizures == "Yes":
        score += 10 + seizure_scores.get(data.seizure_type,0)

    if data.medications == "Yes":
        score += 10

    if data.adult_present == "Yes":
        score -= 5

    if score > 70:
        level, cls, msg = "High Risk","high","Close monitoring recommended."
    elif score > 45:
        level, cls, msg = "Medium Risk","medium","Moderate oversight recommended."
    else:
        level, cls, msg = "Low Risk","low","Standard home care appropriate."

    st.markdown(f"<span class='badge {cls}'>{level}</span>", unsafe_allow_html=True)
    st.metric("Risk Score", round(score,1))
    st.write(msg)

    st.subheader("Client Summary")
    for k,v in data.items():
        if k != "step":
            st.write(f"**{k.replace('_',' ').title()}**: {v}")

    st.button("← Back", on_click=prev_step, key="back6")
    st.button("Start Over", on_click=reset_all, key="reset")

    st.markdown("</div>", unsafe_allow_html=True)
