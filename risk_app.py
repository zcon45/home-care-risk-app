import streamlit as st
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="Home Care Risk Assessment", layout="centered")
st.title("🏥 Home Care Risk Assessment")
st.markdown("Fill in the client details below to calculate the risk score.")

# --- Dropdown options ---
age_options = list(range(1, 110))      # 18–100
weight_options = list(range(10, 400))   # 80–300 lbs
height_options = list(range(6, 100))    # 50–84 inches
mobility_options = list(range(1, 6))    # 1–5

# --- Client Demographics in columns ---
st.subheader("Client Demographics")
col1, col2, col3 = st.columns(3)
with col1:
    age = st.selectbox("Age", age_options, index=age_options.index(70), help="Select the client’s age")
with col2:
    weight = st.selectbox("Weight (lbs)", weight_options, index=weight_options.index(150), help="Select the client’s weight in pounds")
with col3:
    height = st.selectbox("Height (inches)", height_options, index=height_options.index(65), help="Select the client’s height in inches")

# --- Medical Information in columns ---
st.subheader("Medical Information")
col1, col2, col3 = st.columns(3)
with col1:
    seizures = st.radio("Seizures?", ("No", "Yes"), help="Select Yes if the client has a history of seizures", horizontal=True)
with col2:
    medications = st.radio("Medication?", ("No", "Yes"), help="Select Yes if the client takes medications", horizontal=True)
with col3:
    adult_present = st.radio("AdultPresent?", ("No", "Yes"), help="Select Yes if an adult is present during shifts", horizontal=True)

# --- Mobility Score ---
mobility_score = st.selectbox("MobilityScore (1 = best, 5 = worst)", mobility_options, index=mobility_options.index(3), help="Rate mobility from 1 (best) to 5 (worst)")

# --- Convert Yes/No to 1/0 for calculation ---
seizures_calc = 1 if seizures == "Yes" else 0
medications_calc = 1 if medications == "Yes" else 0
adult_present_calc = 1 if adult_present == "Yes" else 0

# --- Risk Calculation ---
risk_score = (
    age * 0.2 + weight * 0.05 + height * 0.05 +
    seizures_calc * 15 + medications_calc * 10 - adult_present_calc * 5 + mobility_score * 5
)

# --- Determine Risk Level ---
if risk_score > 50:
    risk_level = "High Risk"
    risk_color = "red"
elif risk_score > 30:
    risk_level = "Medium Risk"
    risk_color = "orange"
else:
    risk_level = "Low Risk"
    risk_color = "green"

# --- Display Results ---
st.subheader("📝 Risk Assessment Results")
st.markdown(f"<h2 style='color:{risk_color};'>{risk_level}</h2>", unsafe_allow_html=True)
st.metric(label="Calculated Risk Score", value=f"{risk_score:.1f}")

# --- Display Client Data Table with Yes/No for binary fields ---
client_data = {
    "ClientID": [1],
    "Age": [age],
    "Weight": [weight],
    "Height": [height],
    "Seizures": [seizures],         # Display Yes/No
    "Medication": [medications],    # Display Yes/No
    "AdultPresent": [adult_present],# Display Yes/No
    "MobilityScore": [mobility_score],
    "RiskScore": [risk_score],
    "RiskLevel": [risk_level]
}

df = pd.DataFrame(client_data)

# Use st.dataframe for better formatting and horizontal scrolling
st.dataframe(df, width=900)

