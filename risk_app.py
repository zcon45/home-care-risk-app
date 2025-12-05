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

/* hide number input spinners in most browsers */
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

# -----------------------------
# Session State
# -----------------------------
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

# -----------------------------
# Header / Progress
# -----------------------------
st.markdown(f"### Step {data.step} of {len(steps)} — {steps[data.step]}")
st.progress(data.step / len(steps))

# Helper to safely get numeric values later
def get_int(val, default=0):
    try:
        return int(val)
    except Exception:
        return default

def get_float(val, default=0.0):
    try:
        return float(val)
    except Exception:
        return default

# =======================================================
# STEP 1 — CLIENT INFO (NAME REQUIRED)
# =======================================================
if data.step == 1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.name = st.text_input("Client Name (required)", value=data.get("name", ""))
    data.client_id = st.text_input("Client ID (optional)", value=data.get("client_id", ""))

    if st.button("Next →", key="next1"):
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

    data.age = st.text_input("Age", value=data.get("age", ""))
    data.weight = st.text_input("Weight (lbs)", value=data.get("weight", ""))

    st.markdown("### Height")
    col1, col2 = st.columns(2)
    with col1:
        data.height_feet = st.text_input("Feet", value=data.get("height_feet", ""))
    with col2:
        data.height_inches = st.text_input("Inches", value=data.get("height_inches", ""))

    col_back, col_next = st.columns(2)

    with col_back:
        if st.button("← Back", key="back2"):
            data.step = 1

    with col_next:
        if st.button("Next →", key="next2"):
            try:
                age_val = int(data.age)
                weight_val = float(data.weight)
                feet_val = int(data.height_feet)
                inches_val = int(data.height_inches)

                if age_val <= 0 or weight_val <= 0:
                    st.warning("Age and weight must be valid positive numbers.")
                elif feet_val < 0 or inches_val < 0 or inches_val > 11:
                    st.warning("Height must be valid and inches between 0 and 11.")
                else:
                    data.age_val = age_val
                    data.weight_val = weight_val
                    data.height_val = feet_val * 12 + inches_val
                    data.step = 3
            except Exception:
                st.warning("Please complete age, weight, feet, and inches with valid numbers before continuing.")

    st.markdown("</div>", unsafe_allow_html=True)

# =======================================================
# STEP 3 — MEDICAL HISTORY (SEIZURES)
# =======================================================
elif data.step == 3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.seizures = st.radio(
        "History of seizures?",
        ["No", "Yes"],
        horizontal=True,
        index=0 if data.get("seizures", "No") == "No" else 1
    )

    data.seizure_type = data.get("seizure_type", "")

    if data.seizures == "Yes":
        seizure_options = [
            "Select seizure type...",
            "Generalized — Tonic-clonic",
            "Generalized — Atonic",
            "Generalized — Tonic only",
            "Clonic / Myoclonic",
            "Focal",
            "Absence",
        ]
        # choose index based on saved value if exists
        if data.seizure_type in seizure_options:
            default_idx = seizure_options.index(data.seizure_type)
        else:
            default_idx = 0

        selection = st.selectbox(
            "Seizure type",
            seizure_options,
            index=default_idx,
            help="Choose the closest matching seizure type."
        )

        # Do not store placeholder as a valid type
        data.seizure_type = "" if selection == "Select seizure type..." else selection

    col_back, col_next = st.columns(2)

    with col_back:
        if st.button("← Back", key="back3"):
            data.step = 2

    with col_next:
        if st.button("Next →", key="next3"):
            if data.seizures == "Yes" and not data.seizure_type:
                st.warning("Please select a seizure type before continuing.")
            else:
                data.step = 4

    st.markdown("</div>", unsafe_allow_html=True)

# =======================================================
# STEP 4 — MEDICATIONS
# =======================================================
elif data.step == 4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.medications = st.radio(
        "Does the client take medication?",
        ["No", "Yes"],
        horizontal=True,
        index=0 if data.get("medications", "No") == "No" else 1
    )

    data.med_reason = data.get("med_reason", "")
    data.med_details = data.get("med_details", "")

    if data.medications == "Yes":
        data.med_reason = st.selectbox(
            "Medication reason",
            ["ADHD", "Heart", "Blood Pressure", "Seizure Medications", "Diabetes", "Other"],
            index=(["ADHD", "Heart", "Blood Pressure", "Seizure Medications", "Diabetes", "Other"].index(data.med_reason)
                   if data.med_reason in ["ADHD", "Heart", "Blood Pressure", "Seizure Medications", "Diabetes", "Other"]
                   else 0)
        )
        data.med_details = st.text_input(
            "Medication & dosage",
            value=data.med_details,
            placeholder="Example: Keppra 500mg twice daily"
        )

    col_back, col_next = st.columns(2)

    with col_back:
        if st.button("← Back", key="back4"):
            data.step = 3

    with col_next:
        if st.button("Next →", key="next4"):
            data.step = 5

    st.markdown("</div>", unsafe_allow_html=True)

# =======================================================
# STEP 5 — MOBILITY & SAFETY
# =======================================================
elif data.step == 5:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    mobility_map = {
        "Walks independently (no assistance needed)": 1,
        "Needs occasional supervision or help": 2,
        "Uses mobility aid (walker/cane/brace)": 3,
        "Requires hands-on assistance": 4,
        "Non-mobile / bedridden": 5
    }
    mobility_labels = list(mobility_map.keys())

    current_label = data.get("mobility_label", mobility_labels[0])
    if current_label not in mobility_labels:
        current_label = mobility_labels[0]

    mobility_choice = st.selectbox(
        "Mobility level",
        mobility_labels,
        index=mobility_labels.index(current_label)
    )
    data.mobility_label = mobility_choice
    data.mobility = mobility_map[mobility_choice]

    data.adult_present = st.radio(
        "Will an adult be present during care?",
        ["No", "Yes"],
        horizontal=True,
        index=0 if data.get("adult_present", "Yes") == "No" else 1
    )

    data.adult1 = st.text_input("Adult #1 Name", value=data.get("adult1", "")) if data.adult_present == "Yes" else ""
    data.adult2 = st.text_input("Adult #2 Name", value=data.get("adult2", "")) if data.adult_present == "Yes" else ""

    data.notes = st.text_area("Additional medical notes", value=data.get("notes", ""))

    col_back, col_next = st.columns(2)

    with col_back:
        if st.button("← Back", key="back5"):
            data.step = 4

    with col_next:
        if st.button("Next →", key="next5"):
            data.step = 6

    st.markdown("</div>", unsafe_allow_html=True)

# =======================================================
# STEP 6 — REVIEW & SCORING
# =======================================================
elif data.step == 6:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    age_val = data.get("age_val", get_int(data.get("age", 0)))
    weight_val = data.get("weight_val", get_float(data.get("weight", 0)))
    height_val = data.get("height_val", 0)
    mobility_val = data.get("mobility", 3)

    score = 0
    score += age_val * 0.2
    score += weight_val * 0.05
    score += height_val * 0.05
    score += mobility_val * 5

    seizure_scores = {
        "Generalized — Tonic-clonic": 20,
        "Generalized — Atonic": 15,
        "Generalized — Tonic only": 12,
        "Clonic / Myoclonic": 10,
        "Focal": 8,
        "Absence": 5
    }

    if data.get("seizures") == "Yes":
        score += 10
        score += seizure_scores.get(data.get("seizure_type", ""), 0)

    if data.get("medications") == "Yes":
        score += 10

    if data.get("adult_present") == "Yes":
        score -= 5

    if score > 70:
        level, cls, msg = "High Risk", "high", "Close monitoring and supervision recommended."
    elif score > 45:
        level, cls, msg = "Medium Risk", "medium", "Moderate oversight appropriate."
    else:
        level, cls, msg = "Low Risk", "low", "Appropriate for standard home care services."

    st.markdown(f"<span class='badge {cls}'>{level}</span>", unsafe_allow_html=True)
    st.metric("Risk Score", round(score, 1))
    st.write(msg)

    st.subheader("Client Summary")
    st.write(f"**Client Name:** {data.get('name','')}")
    st.write(f"**Client ID:** {data.get('client_id','')}")
    st.write(f"**Age:** {age_val}")
    st.write(f"**Weight (lbs):** {weight_val}")
    st.write(f"**Height (in):** {height_val}")
    st.write(f"**Seizures:** {data.get('seizures','')}")
    st.write(f"**Seizure Type:** {data.get('seizure_type','')}")
    st.write(f"**Medications:** {data.get('medications','')}")
    st.write(f"**Medication Reason:** {data.get('med_reason','')}")
    st.write(f"**Medication Details:** {data.get('med_details','')}")
    st.write(f"**Mobility Level:** {data.get('mobility_label','')}")
    st.write(f"**Adult Present:** {data.get('adult_present','')}")
    st.write(f"**Adults:** {data.get('adult1','')} {data.get('adult2','')}")
    st.write(f"**Additional Notes:** {data.get('notes','')}")

    col_back, col_reset = st.columns(2)
    with col_back:
        if st.button("← Back", key="back6"):
            data.step = 5
    with col_reset:
        if st.button("Start Over", key="reset6"):
            for k in list(data.keys()):
                del st.session_state[k]
            st.session_state.step = 1

    st.markdown("</div>", unsafe_allow_html=True)
