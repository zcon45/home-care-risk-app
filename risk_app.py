import streamlit as st

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Home Care Comfort Portal",
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

.industry-card {
    background:#ffffff;
    padding:18px;
    border-radius:12px;
    box-shadow:0px 4px 10px rgba(0,0,0,.04);
    text-align:center;
    cursor:pointer;
    border:1px solid #e2e8f0;
}
.industry-title {
    font-size:16px;
    font-weight:600;
    margin-top:8px;
}

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
# GLOBAL SESSION STATE INIT
# ---------------------------------------------------

if "app_stage" not in st.session_state:
    st.session_state.app_stage = "industry_select"   # industry_select, assessment_select, assessment_run

if "industry" not in st.session_state:
    st.session_state.industry = None

if "assessment" not in st.session_state:
    st.session_state.assessment = None

if "step" not in st.session_state:
    st.session_state.step = 1

if "med_list" not in st.session_state:
    st.session_state.med_list = []

data = st.session_state

# Steps only apply inside the Home Care Risk Assessment
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
# NAV HELPERS
# ---------------------------------------------------

def go_to_industries():
    st.session_state.app_stage = "industry_select"
    st.session_state.industry = None
    st.session_state.assessment = None
    st.session_state.step = 1

def go_to_assessment_select():
    st.session_state.app_stage = "assessment_select"
    st.session_state.assessment = None
    st.session_state.step = 1

def start_home_care_assessment():
    st.session_state.assessment = "home_care_risk"
    st.session_state.app_stage = "assessment_run"
    st.session_state.step = 1
    st.session_state.med_list = []

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

def reset_all():
    st.session_state.clear()
    st.session_state.app_stage = "industry_select"
    st.session_state.step = 1
    st.session_state.med_list = []

# ---------------------------------------------------
# HOME CARE RISK ASSESSMENT LOGIC (EXISTING APP)
# ---------------------------------------------------

def run_home_care_risk_assessment():
    data = st.session_state

    # Header + Progress
    st.markdown(f"### Home Care Risk Assessment — Step {data.step} of {TOTAL_STEPS} · {STEPS[data.step]}")
    st.progress(data.step / TOTAL_STEPS)

    # ===== STEP 1 — CLIENT INFO =====
    if data.step == 1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        data.name = st.text_input("Client Name (required)", value=data.get("name",""))
        data.client_id = st.text_input("Client ID (optional)", value=data.get("client_id",""))

        colA, colB = st.columns(2)
        with colA:
            st.button("← Back to assessments", on_click=go_to_assessment_select, key="back_assess_list")
        with colB:
            st.button("Next →", on_click=next_step, disabled=(not data.name.strip()), key="next1")

        st.markdown("</div>", unsafe_allow_html=True)

    # ===== STEP 2 — DEMOGRAPHICS =====
    elif data.step == 2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        data.age = st.text_input("Age", value=data.get("age",""))
        data.weight = st.text_input("Weight (lbs)", value=data.get("weight",""))

        st.markdown("**Height**")
        col1, col2 = st.columns(2)
        with col1:
            data.height_feet = st.text_input("Feet", value=data.get("height_feet",""))
        with col2:
            data.height_inches = st.text_input("Inches (0–11)", value=data.get("height_inches",""))

        def demo_valid():
            try:
                age = int(data.age)
                weight = float(data.weight)
                ft = int(data.height_feet)
                inch = int(data.height_inches)
                return age > 0 and weight > 0 and ft >= 0 and 0 <= inch <= 11
            except:
                return False

        colA, colB = st.columns(2)
        with colA:
            st.button("← Back", on_click=prev_step, key="back2")
        with colB:
            st.button("Next →", on_click=next_step, disabled=not demo_valid(), key="next2")

        st.markdown("</div>", unsafe_allow_html=True)

    # ===== STEP 3 — SEIZURES =====
    elif data.step == 3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        data.seizures = st.radio(
            "History of Seizures?",
            ["No","Yes"],
            horizontal=True,
            index=0 if data.get("seizures","No")=="No" else 1
        )

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
            current = data.get("seizure_type","Select seizure type...")
            if current not in seizure_types:
                current = "Select seizure type..."
            idx = seizure_types.index(current)
            sel = st.selectbox("Seizure Type", seizure_types, index=idx)
            data.seizure_type = sel
            seizure_ok = sel != "Select seizure type..."

        colA, colB = st.columns(2)
        with colA:
            st.button("← Back", on_click=prev_step, key="back3")
        with colB:
            st.button("Next →", on_click=next_step, disabled=not seizure_ok, key="next3")

        st.markdown("</div>", unsafe_allow_html=True)

    # ===== STEP 4 — MEDICATIONS =====
    elif data.step == 4:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        data.medications = st.radio(
            "Does the client take medication?",
            ["No","Yes"],
            horizontal=True,
            index=0 if data.get("medications","No")=="No" else 1
        )

        if data.medications == "Yes":
            # Add medication
            with st.expander("Add Medication"):
                m_name = st.text_input("Medication Name", key="new_med_name")
                m_dose = st.text_input("Dosage", key="new_med_dose")
                m_freq = st.text_input("Frequency", key="new_med_freq")

                can_add = all([m_name.strip(), m_dose.strip(), m_freq.strip()])

                if st.button("Add Medication", disabled=not can_add, key="add_med"):
                    data.med_list.append(
                        {"name": m_name.strip(), "dosage": m_dose.strip(), "frequency": m_freq.strip()}
                    )
                    st.session_state.new_med_name = ""
                    st.session_state.new_med_dose = ""
                    st.session_state.new_med_freq = ""
                    st.experimental_rerun()

            st.markdown("### Current Medications")
            if not data.med_list:
                st.caption("No medications added yet.")
            else:
                for i, med in enumerate(data.med_list):
                    cols = st.columns([3, 2, 2, 1])

                    name_key = f"med_name_{i}"
                    dose_key = f"med_dose_{i}"
                    freq_key = f"med_freq_{i}"

                    if name_key not in st.session_state:
                        st.session_state[name_key] = med["name"]
                    if dose_key not in st.session_state:
                        st.session_state[dose_key] = med["dosage"]
                    if freq_key not in st.session_state:
                        st.session_state[freq_key] = med["frequency"]

                    cols[0].text_input("Medication", key=name_key)
                    cols[1].text_input("Dosage", key=dose_key)
                    cols[2].text_input("Frequency", key=freq_key)

                    data.med_list[i]["name"] = st.session_state[name_key]
                    data.med_list[i]["dosage"] = st.session_state[dose_key]
                    data.med_list[i]["frequency"] = st.session_state[freq_key]

                    if cols[3].button("🗑️", key=f"del_med_{i}"):
                        data.med_list.pop(i)
                        st.experimental_rerun()

            meds_ok = True if data.med_list else False
        else:
            meds_ok = True

        colA, colB = st.columns(2)
        with colA:
            st.button("← Back", on_click=prev_step, key="back4")
        with colB:
            st.button("Next →", on_click=next_step, disabled=not meds_ok, key="next4")

        st.markdown("</div>", unsafe_allow_html=True)

    # ===== STEP 5 — MOBILITY & ADULTS =====
    elif data.step == 5:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        mobility_map = {
            "Walks independently (no assistance)": 1,
            "Needs occasional supervision": 2,
            "Uses mobility aid": 3,
            "Requires hands-on assist": 4,
            "Non-mobile / bedridden": 5,
        }

        default_label = data.get("mobility_label", "Walks independently (no assistance)")
        if default_label not in mobility_map:
            default_label = "Walks independently (no assistance)"

        labels = list(mobility_map.keys())
        idx = labels.index(default_label)

        mobility_label = st.selectbox("Mobility Level", labels, index=idx)
        data.mobility_label = mobility_label
        data.mobility = mobility_map[mobility_label]

        data.adult_present = st.radio(
            "Will an adult be present during care?",
            ["No","Yes"],
            horizontal=True,
            index=0 if data.get("adult_present","No")=="No" else 1
        )

        adults_ok = True

        data.adult1 = data.get("adult1","")
        data.rel1 = data.get("rel1","")
        data.adult2 = data.get("adult2","")
        data.rel2 = data.get("rel2","")

        if data.adult_present == "Yes":
            col1,col2 = st.columns(2)
            with col1:
                data.adult1 = st.text_input("Adult #1 Name", value=data.adult1)
            with col2:
                data.rel1 = st.text_input("Relationship (required)", value=data.rel1)

            col3,col4 = st.columns(2)
            with col3:
                data.adult2 = st.text_input("Adult #2 Name", value=data.adult2)
            with col4:
                data.rel2 = st.text_input("Relationship", value=data.rel2)

            adults_ok = bool(data.adult1.strip() and data.rel1.strip())

            if data.adult2.strip() and not data.rel2.strip():
                adults_ok = False

        data.notes = st.text_area("Additional medical notes", value=data.get("notes",""))

        colA, colB = st.columns(2)
        with colA:
            st.button("← Back", on_click=prev_step, key="back5")
        with colB:
            st.button("Next →", on_click=next_step, disabled=not adults_ok, key="next5")

        st.markdown("</div>", unsafe_allow_html=True)

    # ===== STEP 6 — REVIEW & SCORE =====
    elif data.step == 6:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        age = int(data.age)
        weight = float(data.weight)
        height = int(data.height_feet) * 12 + int(data.height_inches)
        mobility_val = data.mobility

        score = age * 0.2 + weight * 0.05 + height * 0.05 + mobility_val * 5

        seizure_scores = {
            "Generalized — Tonic-clonic": 20,
            "Generalized — Atonic": 15,
            "Generalized — Tonic only": 12,
            "Clonic / Myoclonic": 10,
            "Focal": 8,
            "Absence": 5
        }

        if data.seizures == "Yes":
            score += 10 + seizure_scores.get(data.seizure_type, 0)

        if data.medications == "Yes":
            score += 10

        if data.adult_present == "Yes":
            score -= 5

        if score > 70:
            level, cls = "High Risk", "high"
        elif score > 45:
            level, cls = "Medium Risk", "medium"
        else:
            level, cls = "Low Risk", "low"

        st.markdown(f"<span class='badge {cls}'>{level}</span>", unsafe_allow_html=True)
        st.metric("Risk Score", round(score, 1))

        st.subheader("Client Summary")

        # 1. Client Identification
        st.write(f"**Client Name:** {data.name}")
        st.write(f"**Client ID:** {data.client_id}")

        # 2. Demographics
        st.write(f"**Age:** {age}")
        st.write(f"**Height:** {height} inches")
        st.write(f"**Weight:** {weight} lbs")

        # 3. Medical History
        st.write(f"**History of Seizures:** {data.seizures}")
        if data.seizures == "Yes":
            st.write(f"**Seizure Type:** {data.seizure_type}")

        # 4. Medications
        st.write(f"**Takes Medication:** {data.medications}")
        if data.medications == "Yes":
            if data.med_list:
                for idx, med in enumerate(data.med_list, start=1):
                    st.write(f"**Medication {idx}:**")
                    st.write(f" • Name: {med['name']}")
                    st.write(f" • Dosage: {med['dosage']}")
                    st.write(f" • Frequency: {med['frequency']}")
            else:
                st.write("No medications entered.")

        # 5. Safety & Mobility
        st.write(f"**Mobility Level:** {data.get('mobility_label','')}")
        st.write(f"**Adult Present During Care:** {data.adult_present}")
        if data.adult_present == "Yes":
            st.write(f"**Adult #1:** {data.adult1} ({data.rel1})")
            if data.adult2.strip():
                st.write(f"**Adult #2:** {data.adult2} ({data.rel2})")

        # 6. Additional Notes
        st.write(f"**Additional Notes:** {data.get('notes','')}")

        colA, colB = st.columns(2)
        with colA:
            st.button("← Back", on_click=prev_step, key="back6")
        with colB:
            st.button("Start Over", on_click=reset_all, key="reset6")

        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# TOP-LEVEL ROUTER: INDUSTRIES → ASSESSMENTS → APP
# ---------------------------------------------------

if data.app_stage == "industry_select":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## Select an Industry")
    st.markdown("Choose the industry to see available assessments.")

    industries = [
        ("Healthcare", "🩺"),
        ("Home Care", "🏡"),
        ("Behavioral Health", "🧠"),
        ("Education", "📚"),
        ("Child Services", "👶"),
        ("Housing", "🏠"),
    ]

    rows = [industries[:3], industries[3:]]
    for row in rows:
        cols = st.columns(len(row))
        for (label, icon), col in zip(row, cols):
            with col:
                if st.button(f"{icon} {label}", key=f"industry_{label}"):
                    st.session_state.industry = label
                    st.session_state.app_stage = "assessment_select"
                    st.session_state.assessment = None
                    st.session_state.step = 1
    st.markdown("</div>", unsafe_allow_html=True)

elif data.app_stage == "assessment_select":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"## {data.industry} — Assessments")

    if data.industry == "Home Care":
        st.markdown("Select an assessment to begin:")

        if st.button("🏡 Home Care Risk Assessment", key="hc_risk_assess"):
            start_home_care_assessment()

        st.caption("More Home Care assessments coming soon.")
    else:
        st.markdown("Assessments for this industry are not configured yet.")
        st.caption("Only the Home Care Risk Assessment is active right now.")

    st.button("← Back to industries", on_click=go_to_industries, key="back_to_industries")

    st.markdown("</div>", unsafe_allow_html=True)

elif data.app_stage == "assessment_run":
    if data.assessment == "home_care_risk":
        run_home_care_risk_assessment()
    else:
        st.write("Selected assessment is not available yet.")
