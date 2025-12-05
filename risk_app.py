import streamlit as st

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Home Care Comfort",
    layout="centered"
)

# ---------------------------------------------------
# STYLES
# ---------------------------------------------------

st.markdown("""
<style>
body{ background:#f4fbfd; }

.card{
    background:#fff;
    border-radius:12px;
    padding:22px;
    box-shadow:0px 4px 12px rgba(0,0,0,.05);
    margin-bottom:18px;
}
.badge{
    padding:7px 16px;
    border-radius:999px;
    color:white;
    font-weight:700;
}
.high{ background:#e53e3e; }
.medium{ background:#dd6b20; }
.low{ background:#10b981; }

input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button{
    -webkit-appearance:none;
    margin:0;
}
input[type=number]{
    -moz-appearance:textfield;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SESSION STATE INIT
# ---------------------------------------------------

if "step" not in st.session_state:
    st.session_state.step = 1

if "med_list" not in st.session_state:
    st.session_state.med_list = []

data = st.session_state

STEPS = {
    1:"Client Info",
    2:"Demographics",
    3:"Medical History",
    4:"Medications",
    5:"Mobility & Safety",
    6:"Review"
}

TOTAL_STEPS = len(STEPS)

# ---------------------------------------------------
# NAV FUNCTIONS
# ---------------------------------------------------

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

def reset_all():
    st.session_state.clear()
    st.session_state.step = 1
    st.session_state.med_list = []

# ---------------------------------------------------
# HEADER / PROGRESS
# ---------------------------------------------------

st.markdown(f"### Step {data.step} of {TOTAL_STEPS} — {STEPS[data.step]}")
st.progress(data.step / TOTAL_STEPS)

# ---------------------------------------------------
# STEP 1 — CLIENT INFO
# ---------------------------------------------------

if data.step == 1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.name = st.text_input("Client Name (required)")
    data.client_id = st.text_input("Client ID (optional)")

    st.button(
        "Next →",
        on_click=next_step,
        disabled=(not data.name.strip())
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# STEP 2 — DEMOGRAPHICS
# ---------------------------------------------------

elif data.step == 2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.age = st.text_input("Age")
    data.weight = st.text_input("Weight (lbs)")

    st.markdown("**Height**")
    col1, col2 = st.columns(2)
    with col1:
        data.height_feet = st.text_input("Feet")
    with col2:
        data.height_inches = st.text_input("Inches (0–11)")

    def demo_valid():
        try:
            int(data.age)
            float(data.weight)
            ft = int(data.height_feet)
            inch = int(data.height_inches)
            return ft >= 0 and 0 <= inch <= 11
        except:
            return False

    colA,colB = st.columns(2)
    with colA:
        st.button("← Back", on_click=prev_step)
    with colB:
        st.button("Next →", on_click=next_step, disabled=not demo_valid())

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# STEP 3 — SEIZURES
# ---------------------------------------------------

elif data.step == 3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.seizures = st.radio("History of Seizures?", ["No","Yes"],horizontal=True)

    seizure_ok = True

    if data.seizures == "Yes":
        seizure_types = [
            "Select seizure type...",
            "Generalized — Tonic-clonic",
            "Generalized — Atonic",
            "Generalized — Tonic only",
            "Clonic / Myoclonic",
            "Focal",
            "Absence"
        ]
        data.seizure_type = st.selectbox("Seizure Type", seizure_types)
        seizure_ok = data.seizure_type != seizure_types[0]

    colA,colB = st.columns(2)
    with colA:
        st.button("← Back", on_click=prev_step)
    with colB:
        st.button("Next →", on_click=next_step, disabled=not seizure_ok)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# STEP 4 — MEDICATIONS
# ---------------------------------------------------

elif data.step == 4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    data.medications = st.radio("Does the client take medication?", ["No","Yes"], horizontal=True)

    if data.medications == "Yes":

        # Add medication entry
        with st.expander("Add Medication"):
            m_name = st.text_input("Medication Name")
            m_dosage = st.text_input("Dosage")
            m_freq = st.text_input("Frequency")

            can_add = all([m_name.strip(), m_dosage.strip(), m_freq.strip()])

            if st.button("Add Medication", disabled=not can_add):
                data.med_list.append({
                    "name":m_name,
                    "dosage":m_dosage,
                    "frequency":m_freq
                })

        # Display medications cleanly
        st.markdown("### Current Medications")
        for i,med in enumerate(data.med_list):
            cols = st.columns([3,2,2,1])

            cols[0].text_input("Medication", value=med["name"], key=f"name_{i}")
            cols[1].text_input("Dosage", value=med["dosage"], key=f"dose_{i}")
            cols[2].text_input("Frequency", value=med["frequency"], key=f"freq_{i}")

            if cols[3].button("🗑️", key=f"del_{i}"):
                data.med_list.pop(i)
                st.experimental_rerun()

        meds_ok = len(data.med_list) > 0

    else:
        meds_ok = True

    colA,colB = st.columns(2)
    with colA:
        st.button("← Back", on_click=prev_step)
    with colB:
        st.button("Next →", on_click=next_step, disabled=not meds_ok)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# STEP 5 — MOBILITY & ADULTS
# ---------------------------------------------------

elif data.step == 5:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    mobility_map = {
        "Walks independently (no assistance)":1,
        "Needs occasional supervision":2,
        "Uses mobility aid":3,
        "Requires hands-on assist":4,
        "Non-mobile / bedridden":5
    }

    choice = st.selectbox("Mobility Level", list(mobility_map.keys()))
    data.mobility = mobility_map[choice]

    data.adult_present = st.radio("Will an adult be present during care?",["No","Yes"],horizontal=True)

    adults_ok = True

    if data.adult_present == "Yes":
        col1,col2 = st.columns(2)
        with col1:
            data.adult1 = st.text_input("Adult #1 Name")
        with col2:
            data.rel1 = st.text_input("Relationship (required)")

        col3,col4 = st.columns(2)
        with col3:
            data.adult2 = st.text_input("Adult #2 Name")
        with col4:
            data.rel2 = st.text_input("Relationship")

        adults_ok = bool(data.adult1.strip() and data.rel1.strip())

        if data.adult2.strip() and not data.rel2.strip():
            adults_ok = False

    colA,colB = st.columns(2)
    with colA:
        st.button("← Back", on_click=prev_step)
    with colB:
        st.button("Next →", on_click=next_step, disabled=not adults_ok)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# STEP 6 — REVIEW & SCORE
# ---------------------------------------------------

elif data.step == 6:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    age = int(data.age)
    weight = float(data.weight)
    height = int(data.height_feet)*12 + int(data.height_inches)

    score = age*.2 + weight*.05 + height*.05 + data.mobility*5

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
        level, cls = "High Risk","high"
    elif score > 45:
        level, cls = "Medium Risk","medium"
    else:
        level, cls = "Low Risk","low"

    # RESULT DISPLAY
    st.markdown(f"<span class='badge {cls}'>{level}</span>",unsafe_allow_html=True)
    st.metric("Risk Score",round(score,1))

    st.subheader("Client Summary")

    st.write(f"**Client Name:** {data.name}")
    st.write(f"**Client ID:** {data.client_id}")
    st.write(f"**Age:** {age}")
    st.write(f"**Height:** {height} inches")
    st.write(f"**Weight:** {weight}")
    st.write(f"**Seizures:** {data.seizures}")
    if data.seizures == "Yes":
        st.write(f"**Seizure Type:** {data.seizure_type}")

    st.write(f"**Takes Medication:** {data.medications}")

    if data.medications == "Yes":
        for idx,med in enumerate(data.med_list, start=1):
            st.write(f"**Medication {idx}:**")
            st.write(f"  - Name: {med['name']}")
            st.write(f"  - Dosage: {med['dosage']}")
            st.write(f"  - Frequency: {med['frequency']}")

    st.write(f"**Mobility Level:** {choice}")
    st.write(f"**Adult Present:** {data.adult_present}")

    if data.adult_present == "Yes":
        st.write(f"**Adult #1:** {data.adult1} ({data.rel1})")
        if data.adult2.strip():
            st.write(f"**Adult #2:** {data.adult2} ({data.rel2})")

    st.button("← Back", on_click=prev_step)
    st.button("Start Over", on_click=reset_all)

    st.markdown("</div>", unsafe_allow_html=True)
