import streamlit as st
import pandas as pd

# ---------------------------
# Page config & simple CSS
# ---------------------------
st.set_page_config(
    page_title="Home Care Risk Assessment",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Soft "Home Care Comfort" theme via inline CSS
st.markdown(
    """
    <style>
    :root {
        --bg: #fbfbfb;
        --card: #ffffff;
        --accent: #3fb3ae;       /* soft teal */
        --accent-2: #f6cfa3;     /* warm neutral */
        --muted: #667085;
        --rounded: 14px;
    }
    /* page background */
    .reportview-container, .main {
        background-color: var(--bg);
    }
    /* card containers */
    .card {
        background: var(--card);
        border-radius: var(--rounded);
        padding: 18px;
        box-shadow: 0 6px 18px rgba(24,39,75,0.06);
        margin-bottom: 16px;
    }
    /* section headers */
    .section-title {
        font-size:18px;
        font-weight:600;
        color:#0f1724;
        margin-bottom:6px;
    }
    .muted {
        color: var(--muted);
        font-size:13px;
        margin-bottom:12px;
    }
    /* risk badge */
    .badge {
        display:inline-block;
        padding:8px 14px;
        border-radius:999px;
        font-weight:700;
        color:white;
    }
    .high { background:#ef4444; }       /* red */
    .medium { background:#f59e0b; }     /* amber */
    .low { background:#10b981; }        /* green */
    /* small helper text */
    .help { font-size:12px; color:var(--muted); }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Header
# ---------------------------
st.markdown("<div style='display:flex; align-items:center; gap:16px;'>"
            "<div style='font-size:30px'>🏡</div>"
            "<div><h1 style='margin:0 0 6px 0;'>Home Care Risk Assessment</h1>"
            "<div class='muted'>Friendly, easy intake — enter client details and get an instant, explainable risk score.</div></div>"
            "</div>",
            unsafe_allow_html=True)

# ---------------------------
# Inputs (card container)
# ---------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)

# Demographics row
st.markdown("<div class='section-title'>Client Demographics</div>", unsafe_allow_html=True)
st.markdown("<div class='muted'>Quickly select the client’s basic info.</div>", unsafe_allow_html=True)

age_options = list(range(18, 101))
weight_options = list(range(80, 301))
height_options = list(range(50, 85))
mobility_options = list(range(1, 6))

col1, col2, col3 = st.columns(3)
with col1:
    age = st.selectbox("Age", age_options, index=age_options.index(70))
with col2:
    weight = st.selectbox("Weight (lbs)", weight_options, index=weight_options.index(150))
with col3:
    height_values = height_options
    height = st.selectbox("Height (in)", height_values, index=height_values.index(65))

st.markdown("<hr style='margin:12px 0'>", unsafe_allow_html=True)

# Medical info row
st.markdown("<div class='section-title'>Medical & Care Info</div>", unsafe_allow_html=True)
st.markdown("<div class='muted'>Yes/No questions and mobility — choose the best option.</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    seizures = st.radio("Seizures?", ("No", "Yes"), index=0, horizontal=True)
with col2:
    medications = st.radio("Medication?", ("No", "Yes"), index=0, horizontal=True)
with col3:
    adult_present = st.radio("Adult present during provider shift?", ("No", "Yes"), index=1, horizontal=True)

st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
mobility_score = st.selectbox("Mobility score (1 = best, 5 = worst)", mobility_options, index=mobility_options.index(3))

st.markdown("</div>", unsafe_allow_html=True)  # close card

# ---------------------------
# Additional information (card)
# ---------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Additional Medical Information</div>", unsafe_allow_html=True)
st.markdown("<div class='muted'>Optional: any notes, equipment, behaviors, or recent incidents.</div>", unsafe_allow_html=True)

additional_info = st.text_area(
    "",  # no visible label (we used header above)
    placeholder="Any additional medical information...",
    height=120,
)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Risk calculation (soft card)
# ---------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
# Convert yes/no to numeric for scoring
seizures_calc = 1 if seizures == "Yes" else 0
medications_calc = 1 if medications == "Yes" else 0
adult_present_calc = 1 if adult_present == "Yes" else 0

# Weighted scoring (kept simple & adjustable)
risk_score = (
    age * 0.2
    + weight * 0.05
    + height * 0.05
    + seizures_calc * 15
    + medications_calc * 10
    - adult_present_calc * 5
    + mobility_score * 5
)

# Determine level
if risk_score > 50:
    level = "High Risk"
    cls = "high"
elif risk_score > 30:
    level = "Medium Risk"
    cls = "medium"
else:
    level = "Low Risk"
    cls = "low"

# Display badge + metric side-by-side
col1, col2 = st.columns([2, 3])
with col1:
    st.markdown(f"<div style='display:flex; align-items:center; gap:12px;'>"
                f"<div class='badge {cls}' style='font-size:16px'>{level}</div>"
                f"<div style='font-size:14px; color:var(--muted)'>Risk Score</div></div>",
                unsafe_allow_html=True)
with col2:
    st.metric(label="Calculated Risk Score", value=f"{risk_score:.1f}")

st.markdown("<div class='muted' style='margin-top:8px'>Tip: Use this score to prioritize visits and resources — higher = more attention needed.</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)  # close card

# ---------------------------
# Output table (card)
# ---------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Client Summary</div>", unsafe_allow_html=True)
st.markdown("<div class='muted'>A compact view of the entered data. 'Yes' / 'No' shown for clarity.</div>", unsafe_allow_html=True)

client_display = {
    "ClientID": [1],
    "Age": [age],
    "Height": [height],
    "Weight": [weight],
    "Seizures": [seizures],       # show Yes/No
    "Medication": [medications],  # show Yes/No
    "AdultPresent": [adult_present],
    "MobilityScore": [mobility_score],
    "RiskScore": [round(risk_score, 1)],
    "RiskLevel": [level],
    "Notes": [additional_info if additional_info else ""]
}

df = pd.DataFrame(client_display)

# st.dataframe allows horizontal scrolling if needed
st.dataframe(df, width=920, height=180)

st.markdown("</div>", unsafe_allow_html=True)  # close card

# ---------------------------
# Small footer
# ---------------------------
st.markdown("<div style='text-align:center; margin-top:10px; color:#9aa4ad; font-size:12px;'>"
            "Built with care • Keep client data secure</div>",
            unsafe_allow_html=True)
