import streamlit as st
import pandas as pd

st.set_page_config(page_title="Home Care Risk Assessment", layout="wide")

st.title("Home Care Client Risk Assessment")

# Input fields
age = st.selectbox("Age", list(range(18, 101)), index=50, help="Select the client’s age")
height = st.selectbox("Height (inches)", list(range(50, 85)), index=65, help="Select the client’s height in inches")
weight = st.selectbox("Weight (lbs)", list(range(80, 301)), index=140, help="Select the client’s weight in pounds")
seizures = st.selectbox("Seizures", ["No", "Yes"])
medications = st.selectbox("Medications", ["No", "Yes"])
adult_present = st.selectbox("Adult present during provider shift", ["No", "Yes"])
mobility = st.selectbox("Mobility score (1=low, 10=high)", list(range(1, 11)), index=5)

# New text area for extra medical information
additional_info = st.text_area(
    "Additional Medical Information",
    placeholder="Any additional medical information...",
    help="Optional details about the client's medical history, behaviors, equipment, or care needs."
)

# Initialize risk score
score = 0

# Age points
if age >= 80:
    score += 15
elif age >= 70:
    score += 10
elif age >= 60:
    score += 5

# Height points
if height < 60 or height > 70:
    score += 5

# Weight points
if weight < 100 or weight > 200:
    score += 5

# Seizures points
if seizures == "Yes":
    score += 10

# Medications points
if medications == "Yes":
    score += 5

# Adult present points
if adult_present == "Yes":
    score -= 5

# Mobility points
if mobility <= 3:
    score += 10
elif mobility <= 6:
    score += 5

# Show risk score
st.subheader(f"Total Risk Score: {score}")

# Display data in a table
data = {
    "Age": [age],
    "Height": [height],
    "Weight": [weight],
    "Seizures": [seizures],
    "Medications": [medications],
    "AdultPresent": [adult_present],
    "MobilityScore": [mobility],
    "RiskScore": [score],
    "AdditionalInfo": [additional_info if additional_info else ""]
}

df = pd.DataFrame(data)
st.subheader("Client Data Summary")
st.table(df)
