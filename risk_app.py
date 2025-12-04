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
age = st.selectbox("Age", list(range(
