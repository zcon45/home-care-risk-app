import streamlit as st
import pandas as pd

# --- Page config ---
st.set_page_config(
    page_title="Home Care Comfort",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Custom CSS for modern look ---
st.markdown("""
<style>
:root {
    --bg: #e6f7fb;         /* light blue */
    --card: #ffffff;
    --accent: #3fb3ae;
    --muted: #4a5568;
    --rounded: 12px;
}
body, .reportview-container, .main {
    background-color: var(--bg);
    font-family: 'Segoe UI', sans-serif;
}
.card {
    background: var(--card);
    border-radius: var(--rounded);
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
.section-title {
    font-size: 20px;
    font-weight: 600;
    color: #0f1724;
    margin-bottom: 10px;
}
.muted {
    color: var(--muted);
    font-size: 14px;
    margin-bottom: 15px;
}
.badge {
    display:inline-block;
    padding: 6px 14px;
    border-radius: 999px;
    font-weight:700;
    color:white;
}
.high { background:#e53e3e; }
.medium { background:#dd6b20; }
.low { background:#10b981; }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div style='display:flex; align-items:center; gap:12px;'>
    <div style='font-size:32px'>🏡</div>
    <div>
        <h1 style='margin:0 0 4px 0;'>Home Care Comfort</h1>
        <div class='muted'>Friendly risk assessment for home care clients.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Client Demographics Card ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Client Demographics</div>", unsafe_allow_html=True)

ages = list(range(18, 101))
weights = list(range(80, 301))
heights = list(range(50, 85))

age = st.selectbox("Age", ages, index=ages.index(70))
weight = st.selectbox("Weight (lbs)", weights, index=weights.index(150))
height = st.selectbox("Height (inches)", heights, index=heights.index(65))

st.markdown("</div>", unsafe_allow_html=True)

# --- Medical & Care Info Card ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Medical & Care Information</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    has_seizures = st.radio("History of Seizures?", ["No", "Yes"], index=0, horizontal=True)
with col2:
    medications = st.radio("Medication?", ["No", "Yes"], index=0, horizontal=True)

adult_present = st.radio("Adult present during provider shift?", ["No", "Yes"], index=1, horizontal=True)
mobility = st.selectbox("Mobility score (1 = best, 5 = worst)", list(range(1, 6)), index=2)

# --- Seizure type dropdown if seizures exist ---
seizure_type = None
if has_seizures == "Yes":
    seizure_type = st.selectbox(
        "Seizure Type (if applicable)",
        options=[
            "Generalized — Tonic-clonic",
            "Generalized — Atonic (drop attacks)",
            "Generalized — Tonic only",
            "Generalized — Clonic / Myoclonic",
            "Focal (aware or impaired awareness)",
            "Generalized — Absence"
        ],
        help="Select the seizure type for more precise risk scoring."
    )
st.markdown("</div>", unsafe_allow_html=True)

# --- Additional Notes Card ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Additional Medical Information</div>", unsafe_allow_html=True)
additional_info = st.text_area("", placeholder="Any additional medical information...", height=100)
st.markdown("</div>", unsafe_allow_html=True)

# --- Risk Calculation ---
score = 0
score += age * 0.2
score += weight * 0.05
score += height * 0.05

if has_seizures == "Yes":
    score += 10
    if seizure_type == "Generalized — Tonic-clonic": score += 20
    elif seizure_type == "Generalized — Atonic (drop attacks)": score += 15
    elif seizure_type == "Generalized — Tonic only": score += 12
    elif seizure_type == "Generalized — Clonic / Myoclonic": score += 10
    elif seizure_type == "Focal (aware or impaired awareness)": score += 8
    elif seizure_type == "Generalized — Absence": score += 5

if medications == "Yes": score += 10
if adult_present == "Yes": score -= 5
score += mobility * 5

# --- Determine Risk Level ---
if score > 70: level, cls = "High Risk", "high"
elif score > 45: level, cls = "Medium Risk", "medium"
else: level, cls = "Low Risk", "low"

# --- Display Risk Badge ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
col1, col2 = st.columns([2, 3])
with col1:
    st.markdown(f"<div class='badge {cls}' style='font-size:16px'>{level}</div>", unsafe_allow_html=True)
    st.markdown("<div class='muted'>Risk Level</div>", unsafe_allow_html=True)
with col2:
    st.metric("Risk Score", f"{score:.1f}")
st.markdown("</div>", unsafe_allow_html=True)

# --- Client Summary Table ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Client Summary</div>", unsafe_allow_html=True)

data = {
    "Age": age,
    "Height": height,
    "Weight": weight,
    "Seizures": has_seizures,
    "SeizureType": seizure_type if seizure_type else "",
    "Medication": medications,
    "AdultPresent": adult_present,
    "Mobility": mobility,
    "RiskScore": round(score,1),
    "RiskLevel": level,
    "Notes": additional_info if additional_info else ""
}

df = pd.DataFrame([data])
st.dataframe(df, width=900, height=200)
st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div style='text-align:center; margin-top:12px; color:#718096; font-size:12px;'>
Home Care Comfort — Confidential
</div>
""", unsafe_allow_html=True)
