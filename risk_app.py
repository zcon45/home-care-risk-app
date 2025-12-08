"""Streamlit Home Care Comfort Portal.

Enterprise-grade medical and behavioral assessment experience for a home care
provider. The app emphasizes resiliency, clarity, and a polished visual design
while remaining fully backward compatible with previously collected
assessments.
"""

from __future__ import annotations

import re␊
from datetime import datetime␊
from typing import Dict, List, Tuple␊
␊
import streamlit as st␊


# ----------------------------------------------------------------------------
# Page configuration
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Home Care Comfort Portal",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ----------------------------------------------------------------------------
# Global styles (cards, typography, animations)
# ----------------------------------------------------------------------------
st.markdown(
    """
<style>
    /* Layout & background */
    .main {background: radial-gradient(circle at 20% 20%, #eef2ff 0, #f7f9fc 38%, #ffffff 100%);}    
    section[data-testid="stSidebar"] {background: #0f172a; color: #f8fafc;}

    /* Top card */
    .hero-card, .assessment-card {    
@@ -245,65 +245,62 @@ def calculate_risk(assessment: Dict[str, str]) -> Tuple[float, str, List[str]]:

    adl = assessment.get("behavior_daily")
    if adl and adl != "Independent":
        score += 20
        breakdown.append("ADL support required: +20")

    if assessment.get("behavior_mental") == "Yes":
        score += 22
        breakdown.append("Mental health history: +22")

    # Categorize risk
    if score < 60:
        level = "Low"
    elif score < 105:
        level = "Medium"
    else:
        level = "High"

    return score, level, breakdown


def logo_header() -> None:
    """Render the top hero with logo placeholder and CTA buttons."""

    st.markdown("<div class='hero-card'>", unsafe_allow_html=True)
    st.markdown("<div class='eyebrow'>Home Care Comfort</div>", unsafe_allow_html=True)
    st.markdown(
        "<h1>Medical & Behavioral Assessment</h1><p class='muted'>A concierge-grade intake experience built for safety, accuracy, and efficiency.</p>",
        unsafe_allow_html=True,
    )

    with st.container():
        col_logo, col_cta = st.columns([1, 2], gap="large")
        with col_logo:
            st.image("assets/logo.png", use_column_width=True)
        with col_cta:
            c1, c2 = st.columns(2, gap="medium")
            with c1:
                if st.button("Client Assessment", key="btn_client", use_container_width=True):
                    st.session_state.page = "assessment"
                    st.session_state.step = 1
                    st.rerun()
            with c2:
                if st.button("Admin Dashboard", key="btn_admin", use_container_width=True):
                    st.session_state.page = "admin"
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Style the CTA buttons after initial render
    st.markdown(
        """
        <script>
            const buttons = document.querySelectorAll('[data-testid="stButton"]');
            if (buttons[0]) buttons[0].classList.add('primary-btn');
            if (buttons[1]) buttons[1].classList.add('secondary-btn');
        </script>
        """,
        unsafe_allow_html=True,
    )


