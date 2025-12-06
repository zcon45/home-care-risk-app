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

input[type=number]::-webkit-inner-spin_button,
input[type=number]::-webkit-outer-spin_button{
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

if "app_stage" not in st.session_state:
    st.session_state.app_stage = "industry_select"   # industry_select, assessment_select, assessment_run

if "industry" not in st.session_state:
    st.session_state.industry = None

if "assessment" not in st.session_state:
    st.session_state.assessment = None

# Home care assessment state
if "step" not in st.session_state:
    st.session_state.step = 1

if "med_list" not in st.session_state:
    st.session_state.med_list = []

# Business assessment state
if "biz_step" not in st.session_state:
    st.session_state.biz_step = 1

if "biz_assessment" not in st.session_state:
    st.session_state.biz_assessment = None

if "biz_answers" not in st.session_state:
    st.session_state.biz_answers = {}

data = st.session_state

# Steps for Home Care assessment
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
    st.session_state.biz_step = 1

def go_to_assessment_select():
    st.session_state.app_stage = "assessment_select"
    st.session_state.assessment = None
    st.session_state.step = 1
    st.session_state.biz_step = 1

def start_home_care_assessment():
    st.session_state.assessment = "home_care_risk"
    st.session_state.app_stage = "assessment_run"
    st.session_state.step = 1
    st.session_state.med_list = []

def start_business_assessment():
    st.session_state.assessment = "business_ai_risk"
    st.session_state.app_stage = "assessment_run"
    st.session_state.biz_step = 1
    st.session_state.biz_assessment = None
    st.session_state.biz_answers = {}

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

def reset_all():
    st.session_state.clear()
    st.session_state.app_stage = "industry_select"
    st.session_state.step = 1
    st.session_state.med_list = []
    st.session_state.biz_step = 1
    st.session_state.biz_assessment = None
    st.session_state.biz_answers = {}

# ---------------------------------------------------
# BUSINESS "AI-STYLE" ASSESSMENT GENERATOR
# ---------------------------------------------------

def generate_business_assessment_structure(description, sector, counterpart):
    """
    Simple rule-based generator that creates a structured
    business risk assessment from the user's description.
    This is written so you can later swap in a real AI model.
    """
    base_sections = []

    # Counterparty & Relationship
    base_sections.append({
        "name": "Counterparty & Relationship",
        "description": "Understand who you are working with and how critical they are to your business.",
        "questions": [
            {
                "id": "counterparty_country",
                "text": "Which countries does this counterparty operate in or ship from?",
                "type": "text",
                "weight": 2,
                "scoring_map": None,
            },
            {
                "id": "relationship_type",
                "text": "What best describes this counterparty relationship?",
                "type": "select",
                "options": ["Supplier", "Customer", "Partner", "Investor", "Other"],
                "weight": 2,
                "scoring_map": {
                    "Supplier": 2,
                    "Customer": 2,
                    "Partner": 3,
                    "Investor": 3,
                    "Other": 2,
                },
            },
            {
                "id": "dependency_level",
                "text": "How dependent is your business on this counterparty for revenue or supply?",
                "type": "select",
                "options": ["Low", "Medium", "High", "Critical"],
                "weight": 3,
                "scoring_map": {"Low": 1, "Medium": 2, "High": 3, "Critical": 4},
            },
        ],
    })

    # Country & Regulatory Risk
    base_sections.append({
        "name": "Country & Regulatory Risk",
        "description": "Identify exposure to tariffs, sanctions, and regulatory instability.",
        "questions": [
            {
                "id": "tariff_exposure",
                "text": "Are your products or services impacted by tariffs or trade duties?",
                "type": "select",
                "options": ["No", "Minor impact", "Moderate impact", "Significant impact"],
                "weight": 3,
                "scoring_map": {
                    "No": 1,
                    "Minor impact": 2,
                    "Moderate impact": 3,
                    "Significant impact": 4,
                },
            },
            {
                "id": "sanctions_risk",
                "text": "Are any countries involved currently subject to sanctions or export controls?",
                "type": "select",
                "options": ["No known sanctions", "Possibly", "Yes"],
                "weight": 4,
                "scoring_map": {
                    "No known sanctions": 1,
                    "Possibly": 3,
                    "Yes": 4,
                },
            },
            {
                "id": "regulatory_complexity",
                "text": "How complex are the regulations that apply to this transaction or product?",
                "type": "select",
                "options": ["Low", "Moderate", "High", "Very high"],
                "weight": 3,
                "scoring_map": {
                    "Low": 1,
                    "Moderate": 2,
                    "High": 3,
                    "Very high": 4,
                },
            },
        ],
    })

    # Operational & Supply Chain
    base_sections.append({
        "name": "Operational & Supply Chain Risk",
        "description": "Evaluate logistics, reliability, and continuity of supply or service.",
        "questions": [
            {
                "id": "lead_time",
                "text": "What is the typical lead time for deliveries or project milestones?",
                "type": "select",
                "options": ["Same week", "1–4 weeks", "1–3 months", "More than 3 months"],
                "weight": 2,
                "scoring_map": {
                    "Same week": 1,
                    "1–4 weeks": 2,
                    "1–3 months": 3,
                    "More than 3 months": 4,
                },
            },
            {
                "id": "contingency_plans",
                "text": "Do you have backup suppliers, routes, or contingency plans in place?",
                "type": "select",
                "options": ["Yes – strong backups", "Some backups", "Minimal backups", "No backups"],
                "weight": 3,
                "scoring_map": {
                    "Yes – strong backups": 1,
                    "Some backups": 2,
                    "Minimal backups": 3,
                    "No backups": 4,
                },
            },
        ],
    })

    # Financial & Reputation
    base_sections.append({
        "name": "Financial & Reputation Risk",
        "description": "Assess financial stability and potential brand or reputation impact.",
        "questions": [
            {
                "id": "financial_health",
                "text": "How confident are you in the counterparty’s financial health?",
                "type": "select",
                "options": ["Very confident", "Somewhat confident", "Unsure", "Concerned"],
                "weight": 3,
                "scoring_map": {
                    "Very confident": 1,
                    "Somewhat confident": 2,
                    "Unsure": 3,
                    "Concerned": 4,
                },
            },
            {
                "id": "reputation_risk",
                "text": "Could working with this counterparty negatively impact your brand or public image?",
                "type": "select",
                "options": ["Very unlikely", "Unlikely", "Possible", "Likely"],
                "weight": 3,
                "scoring_map": {
                    "Very unlikely": 1,
                    "Unlikely": 2,
                    "Possible": 3,
                    "Likely": 4,
                },
            },
        ],
    })

    # Notes
    base_sections.append({
        "name": "Notes & Context",
        "description": "Capture any additional details that could affect risk.",
        "questions": [
            {
                "id": "extra_context",
                "text": "Any additional details about this deal, partner, or context?",
                "type": "text_long",
                "weight": 0,
                "scoring_map": None,
            }
        ],
    })

    return {
        "assessment_name": "AI-Style Business Risk Assessment",
        "sector": sector,
        "counterpart": counterpart,
        "description": description,
        "sections": base_sections,
    }

# ---------------------------------------------------
# BUSINESS RISK ASSESSMENT FLOW
# ---------------------------------------------------

def run_business_risk_assessment():
    data = st.session_state
    if "biz_step" not in data:
        data.biz_step = 1

    st.markdown(f"### Business Risk Assessment (AI-style) — Step {data.biz_step} of 3")
    st.progress(data.biz_step/3)

    # STEP 1 – Scenario intake
    if data.biz_step == 1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        data.biz_name = st.text_input("Business name", value=data.get("biz_name",""))
        sectors = ["Fashion / Apparel","Manufacturing","Technology / Software","Retail / E-commerce",
                   "Logistics / Transport","Other"]
        data.biz_sector = st.selectbox(
            "Primary sector",
            sectors,
            index= sectors.index(data.get("biz_sector","Fashion / Apparel"))
            if data.get("biz_sector") in sectors else 0
        )
        counterparts = ["Supplier","Customer","Partner","Investor","Other"]
        data.biz_counterpart = st.selectbox(
            "Counterparty type",
            counterparts,
            index= counterparts.index(data.get("biz_counterpart","Supplier"))
            if data.get("biz_counterpart") in counterparts else 0
        )
        data.biz_scenario = st.text_area(
            "Briefly describe the situation or deal you want to assess",
            value=data.get("biz_scenario",""),
            height=150,
            help="Example: We are a fashion brand buying fabric from a new supplier in another country."
        )

        colA,colB = st.columns(2)
        with colA:
            st.button("← Back to assessments", on_click=go_to_assessment_select, key="biz_back1")
        with colB:
            disabled = not data.biz_scenario.strip()
            if st.button("Generate Assessment →", disabled=disabled, key="biz_next1"):
                data.biz_assessment = generate_business_assessment_structure(
                    data.biz_scenario,
                    data.biz_sector,
                    data.biz_counterpart
                )
                data.biz_step = 2
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # STEP 2 – Answer dynamically generated questions
    elif data.biz_step == 2:
        if not data.biz_assessment:
            st.warning("No assessment generated yet. Please go back and describe your situation.")
            if st.button("← Back", on_click=go_to_assessment_select, key="biz_back_noassess"):
                return

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("#### Answer the questions below to assess your risk.")

        answers = data.biz_answers

        for section in data.biz_assessment["sections"]:
            st.markdown(f"**{section['name']}**")
            st.caption(section["description"])
            for q in section["questions"]:
                qid = q["id"]
                qtype = q["type"]
                default_val = answers.get(qid,"")
                if qtype == "text":
                    val = st.text_input(q["text"], value=default_val, key=f"biz_{qid}")
                elif qtype == "text_long":
                    val = st.text_area(q["text"], value=default_val, key=f"biz_{qid}")
                elif qtype == "select":
                    options = q["options"]
                    idx = options.index(default_val) if default_val in options else 0
                    val = st.selectbox(q["text"], options, index=idx, key=f"biz_{qid}")
                else:
                    val = st.text_input(q["text"], value=default_val, key=f"biz_{qid}")
                answers[qid] = val
                st.write("")
            st.markdown("---")

        colA,colB = st.columns(2)
        with colA:
            if st.button("← Back", key="biz_back2"):
                data.biz_step = 1
                st.rerun()
        with colB:
            if st.button("Calculate Risk →", key="biz_next2"):
                data.biz_answers = answers
                data.biz_step = 3
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # STEP 3 – Risk calculation & summary
    elif data.biz_step == 3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Business Risk Results")

        assess = data.biz_assessment
        answers = data.biz_answers

        total_score = 0
        max_score = 0

        for section in assess["sections"]:
            for q in section["questions"]:
                if not q["scoring_map"]:
                    continue
                ans = answers.get(q["id"])
                if ans not in q["scoring_map"]:
                    continue
                w = q["weight"]
                s_val = q["scoring_map"][ans]
                max_s = max(q["scoring_map"].values())
                total_score += w * s_val
                max_score += w * max_s

        if max_score > 0:
            risk_pct = (total_score / max_score) * 100.0
        else:
            risk_pct = 0.0

        if risk_pct >= 66:
            level, cls = "High Risk","high"
        elif risk_pct >= 40:
            level, cls = "Medium Risk","medium"
        else:
            level, cls = "Low Risk","low"

        st.markdown(f"<span class='badge {cls}'>{level}</span>", unsafe_allow_html=True)
        st.metric("Overall Business Risk Score", f"{risk_pct:.1f}%")

        st.subheader("Summary")
        st.write(f"**Business Name:** {data.get('biz_name','')}")
        st.write(f"**Sector:** {assess.get('sector','')}")
        st.write(f"**Counterparty Type:** {assess.get('counterpart','')}")
        st.write("**Scenario Description:**")
        st.write(assess.get("description",""))

        st.subheader("Key Risk Areas")
        for section in assess["sections"]:
            st.markdown(f"**{section['name']}**")
            for q in section["questions"]:
                ans = answers.get(q["id"],"(no answer)")
                st.write(f"- {q['text']}")
                st.write(f"  → **Your answer:** {ans}")
            st.write("")

        colA,colB = st.columns(2)
        with colA:
            if st.button("← Back", key="biz_back3"):
                data.biz_step = 2
                st.rerun()
        with colB:
            if st.button("Start Over", key="biz_reset"):
                reset_all()
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# HOME CARE RISK ASSESSMENT FLOW
# ---------------------------------------------------

def run_home_care_risk_assessment():
    data = st.session_state

    st.markdown(f"### Home Care Risk Assessment — Step {data.step} of {TOTAL_STEPS} · {STEPS[data.step]}")
    st.progress(data.step / TOTAL_STEPS)

    # STEP 1 – Client Info
    if data.step == 1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        data.name = st.text_input("Client Name (required)", value=data.get("name",""))
        data.client_id = st.text_input("Client ID (optional)", value=data.get("client_id",""))

        colA, colB = st.columns(2)
        with colA:
            st.button("← Back to assessments", on_click=go_to_assessment_select, key="hc_back_assess")
        with colB:
            st.button("Next →", on_click=next_step, disabled=(not data.name.strip()), key="next1")

        st.markdown("</div>", unsafe_allow_html=True)

    # STEP 2 – Demographics
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

    # STEP 3 – Seizures
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

    # STEP 4 – Medications
    elif data.step == 4:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        data.medications = st.radio(
            "Does the client take medication?",
            ["No","Yes"],
            horizontal=True,
            index=0 if data.get("medications","No")=="No" else 1
        )

        if data.medications == "Yes":
            with st.expander("Add Medication"):
                m_name = st.text_input("Medication Name", key="new_med_name")
                m_dose = st.text_input("Dosage", key="new_med_dose")
                m_freq = st.text_input("Frequency", key="new_med_freq")

                can_add = all([m_name.strip(), m_dose.strip(), m_freq.strip()])

                if st.button("Add Medication", disabled=not can_add, key="add_med"):
                    data.med_list.append(
                        {"name": m_name.strip(), "dosage": m_dose.strip(), "frequency": m_freq.strip()}
                    )
                    st.session_state.update({
    "new_med_name": "",
    "new_med_dose": "",
    "new_med_freq": ""
})
st.rerun()


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
                        st.rerun()

            meds_ok = True if data.med_list else False
        else:
            meds_ok = True

        colA, colB = st.columns(2)
        with colA:
            st.button("← Back", on_click=prev_step, key="back4")
        with colB:
            st.button("Next →", on_click=next_step, disabled=not meds_ok, key="next4")

        st.markdown("</div>", unsafe_allow_html=True)

    # STEP 5 – Mobility & Adults
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

    # STEP 6 – Review & Score
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

        st.write(f"**Client Name:** {data.name}")
        st.write(f"**Client ID:** {data.client_id}")
        st.write(f"**Age:** {age}")
        st.write(f"**Height:** {height} inches")
        st.write(f"**Weight:** {weight} lbs")
        st.write(f"**History of Seizures:** {data.seizures}")
        if data.seizures == "Yes":
            st.write(f"**Seizure Type:** {data.seizure_type}")
        st.write(f"**Takes Medication:** {data.medications}")
        if data.medications == "Yes":
            if data.med_list:
                for idx_m, med in enumerate(data.med_list, start=1):
                    st.write(f"**Medication {idx_m}:**")
                    st.write(f" • Name: {med['name']}")
                    st.write(f" • Dosage: {med['dosage']}")
                    st.write(f" • Frequency: {med['frequency']}")
            else:
                st.write("No medications entered.")
        st.write(f"**Mobility Level:** {data.get('mobility_label','')}")
        st.write(f"**Adult Present During Care:** {data.adult_present}")
        if data.adult_present == "Yes":
            st.write(f"**Adult #1:** {data.adult1} ({data.rel1})")
            if data.adult2.strip():
                st.write(f"**Adult #2:** {data.adult2} ({data.rel2})")
        st.write(f"**Additional Notes:** {data.get('notes','')}")

        colA, colB = st.columns(2)
        with colA:
            st.button("← Back", on_click=prev_step, key="back6")
        with colB:
            st.button("Start Over", on_click=reset_all, key="reset6")

        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# TOP LEVEL ROUTER
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
        ("Business", "🏢"),
    ]

    rows = [industries[:3], industries[3:6], industries[6:]]
    for row in rows:
        if not row:
            continue
        cols = st.columns(len(row))
        for (label, icon), col in zip(row, cols):
            with col:
                if st.button(f"{icon} {label}", key=f"industry_{label}"):
                    st.session_state.industry = label
                    st.session_state.app_stage = "assessment_select"
                    st.session_state.assessment = None
                    st.session_state.step = 1
                    st.session_state.biz_step = 1

    st.markdown("</div>", unsafe_allow_html=True)

elif data.app_stage == "assessment_select":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"## {data.industry} — Assessments")

    if data.industry == "Home Care":
        st.markdown("Select an assessment to begin:")

        if st.button("🏡 Home Care Risk Assessment", key="hc_risk_assess"):
            start_home_care_assessment()

        st.caption("More Home Care assessments coming soon.")

    elif data.industry == "Business":
        st.markdown("Select an assessment to begin:")

        if st.button("📊 AI Business Risk Assessment", key="biz_risk_assess"):
            start_business_assessment()

        st.caption("This assessment dynamically adapts to your business scenario.")

    else:
        st.markdown("Assessments for this industry are not configured yet.")
        st.caption("Currently, Home Care and Business assessments are active.")

    st.button("← Back to industries", on_click=go_to_industries, key="back_to_industries")

    st.markdown("</div>", unsafe_allow_html=True)

elif data.app_stage == "assessment_run":
    if data.assessment == "home_care_risk":
        run_home_care_risk_assessment()
    elif data.assessment == "business_ai_risk":
        run_business_risk_assessment()
    else:
        st.write("Selected assessment is not available yet.")

