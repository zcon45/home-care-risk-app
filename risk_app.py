import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# --- Initialize OpenAI client ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Page config ---
st.set_page_config(
    page_title="Home Care Comfort",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- CSS styling ---
st.markdown("""
<style>
.card {
    background-color: #ffffff;
    border-radius: 12px;
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
    color: #4a5568;
    font-size: 14px;
}
.badge {
    display:inline-block;
    padding: 6px 14px;
    border-radius: 999px;
    color:white;
    font-weight:700;
}
.high { background:#e53e3e; }
.medium { background:#dd6b20; }
.low { background:#10b981; }

table, th, td {
    border: 1px solid #ddd;
}
th, td {
    padding: 8px;
    word-wrap: break-word;
}
th {
    background-color: #f2f2f2;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div style='display:flex; align-items:center; gap:12px;'>
  <div style='font-size:32px'>🏡</div>
  <div>
    <h1 style='margin:0;'>Home Care Comfort</h1>
    <div class='muted'>Friendly AI-assisted home care risk assessment</div>
  </div>
</div>
""", unsafe_allow_html=True)

# --- Client Info ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Client Information</div>", unsafe_allow_html=True)

client_name = st.text_input("Client Name")
client_id = st.text_input("Client ID / Number")

st.markdown("</div>", unsafe_allow_html=True)

# --- Demographics ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Client Demographics</div>", unsafe_allow_html=True)

ages = list(range(18, 101))
weights = list(range(80, 301))
heights = list(range(50, 85))

age = st.selectbox("Age", ages)
weight = st.selectbox("Weight (lbs)", weights)
height = st.selectbox("Height (inches)", heights)

st.markdown("</div>", unsafe_allow_html=True)

# --- Medical info ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Medical & Care Information</div>", unsafe_allow_html=True)

col1, col2 = st.columns([2,3])

with col1:
    has_seizures = st.radio("History of Seizures?", ["No", "Yes"], horizontal=True)

with col2:
    seizure_type = None
    if has_seizures == "Yes":
        seizure_type = st.selectbox(
            "Seizure Type",
            [
                "Generalized — Tonic-clonic",
                "Generalized — Atonic (drop attacks)",
                "Generalized — Tonic only",
                "Generalized — Clonic / Myoclonic",
                "Focal (aware or impaired awareness)",
                "Generalized — Absence",
            ],
        )

col3, col4 = st.columns([2,3])

with col3:
    medications = st.radio("Medication?", ["No", "Yes"], horizontal=True)

with col4:
    med_reason = ""
    med_details = ""

    if medications == "Yes":
        med_reason = st.selectbox(
            "Medication Reason",
            ["ADHD", "Heart", "Blood Pressure", "Seizure Medications", "Diabetes", "Other"],
        )
        med_details = st.text_input("Medication + Dosage")

col5, col6 = st.columns([2,3])

with col5:
    adult_present = st.radio("Adult present during shift?", ["No", "Yes"], horizontal=True)

with col6:
    adult1 = adult2 = ""
    if adult_present == "Yes":
        adult1 = st.text_input("Adult #1 Name")
        adult2 = st.text_input("Adult #2 Name")

mobility = st.selectbox("Mobility Score (1 = best, 5 = worst)", list(range(1,6)))

st.markdown("</div>", unsafe_allow_html=True)

# --- Additional notes ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Additional Medical Notes</div>", unsafe_allow_html=True)
additional_info = st.text_area("", placeholder="Any additional information...")
st.markdown("</div>", unsafe_allow_html=True)

# --- Risk scoring ---
score = 0
score += age * 0.2
score += weight * 0.05
score += height * 0.05
score += mobility * 5

if has_seizures == "Yes":
    score += 10
    weights = {
        "Generalized — Tonic-clonic":20,
        "Generalized — Atonic (drop attacks)":15,
        "Generalized — Tonic only":12,
        "Generalized — Clonic / Myoclonic":10,
        "Focal (aware or impaired awareness)":8,
        "Generalized — Absence":5,
    }
    score += weights.get(seizure_type, 0)

if medications == "Yes":
    score += 10
if adult_present == "Yes":
    score -= 5

# --- Risk Level ---
if score > 70:
    level, cls = "High Risk", "high"
elif score > 45:
    level, cls = "Medium Risk", "medium"
else:
    level, cls = "Low Risk", "low"

# --- Display results ---
st.markdown("<div class='card'>", unsafe_allow_html=True)

c1, c2 = st.columns([2,3])

with c1:
    st.markdown(f"<div class='badge {cls}'>{level}</div>", unsafe_allow_html=True)
    st.markdown("<div class='muted'>Risk Level</div>", unsafe_allow_html=True)

with c2:
    st.metric("Risk Score", f"{round(score,1)}")

st.markdown("</div>", unsafe_allow_html=True)

# --- Summary ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Client Summary</div>", unsafe_allow_html=True)

summary_html = f"""
<table style='width:100%'>
<tr><th>Field</th><th>Value</th></tr>
<tr><td>Client Name</td><td>{client_name}</td></tr>
<tr><td>Client ID</td><td>{client_id}</td></tr>
<tr><td>Age</td><td>{age}</td></tr>
<tr><td>Height</td><td>{height}</td></tr>
<tr><td>Weight</td><td>{weight}</td></tr>
<tr><td>Seizures</td><td>{has_seizures}</td></tr>
<tr><td>Seizure Type</td><td>{seizure_type}</td></tr>
<tr><td>Medication</td><td>{medications}</td></tr>
<tr><td>Medication Reason</td><td>{med_reason}</td></tr>
<tr><td>Medication Details</td><td>{med_details}</td></tr>
<tr><td>Adults Present</td><td>{adult1} {adult2}</td></tr>
<tr><td>Mobility</td><td>{mobility}</td></tr>
<tr><td>Risk Level</td><td>{level}</td></tr>
<tr><td>Risk Score</td><td>{round(score,1)}</td></tr>
<tr><td>Additional Notes</td><td>{additional_info}</td></tr>
</table>
"""

st.markdown(summary_html, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- AI ASSISTANT ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>🤖 Need Help? Ask Our AI Assistant</div>", unsafe_allow_html=True)

user_question = st.text_input("Ask a general question about this form or the terms used:")

if user_question:
    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role":"system",
                        "content":"You assist users completing a healthcare risk form. Explain terms and guide them safely. Do not provide medical diagnosis or treatment advice."
                    },
                    {"role":"user","content":user_question}
                ]
            )

            ai_reply = response.choices[0].message.content
            st.success(ai_reply)

        except Exception as e:
            st.error("AI service is temporarily unavailable.")

st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div style='text-align:center; margin-top:12px; color:#718096; font-size:12px;'>
Home Care Comfort — Confidential | AI assistant does not store any personal data.
</div>
""", unsafe_allow_html=True)
