"""Streamlit Home Care Comfort Portal.

Enterprise-grade medical and behavioral assessment experience for a home care
provider. The app emphasizes resiliency, clarity, and a polished visual design
while remaining fully backward compatible with previously collected
assessments.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Dict, List, Tuple

import streamlit as st


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
        background: #ffffff;
        border-radius: 24px;
        padding: 28px 34px;
        box-shadow: 0 14px 40px rgba(15, 23, 42, 0.12);
        border: 1px solid #eef2f7;
        position: relative;
        overflow: hidden;
    }
    .hero-card:before {
        content: "";
        position: absolute;
        inset: -50% auto auto -20%;
        width: 320px;
        height: 320px;
        background: radial-gradient(circle at 30% 30%, rgba(14,165,233,0.08), transparent 60%);
        z-index: 0;
    }
    .hero-card > * {position: relative; z-index: 1;}

    /* Typography */
    h1 {font-weight: 800; letter-spacing: -0.6px;}
    h2 {font-weight: 700; letter-spacing: -0.3px;}
    p, label, span {font-family: "Inter", "Segoe UI", system-ui, sans-serif;}
    .eyebrow {color: #0ea5e9; text-transform: uppercase; font-weight: 700; font-size: 0.85rem; letter-spacing: 1.2px;}
    .muted {color: #64748b;}

    /* Buttons */
    .primary-btn button {background: linear-gradient(135deg, #0284c7 0%, #0ea5e9 100%);
        color: #fff; border: none; padding: 0.9rem 1.1rem; font-weight: 700;
        border-radius: 14px; box-shadow: 0 8px 22px rgba(14,165,233,0.28);
        transition: transform 150ms ease, box-shadow 200ms ease;}
    .primary-btn button:hover {transform: translateY(-1px); box-shadow: 0 12px 26px rgba(14,165,233,0.35);}    
    .secondary-btn button {background: #0f172a; color: #fff; border-radius: 14px; padding: 0.9rem 1.1rem; font-weight: 700; border: none;}

    /* Progress */
    .stProgress > div > div {border-radius: 999px;}
    .stProgress > div > div > div {background: linear-gradient(120deg, #0ea5e9, #22d3ee);}   

    /* Detail boxes */
    .inline-detail {background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 0.85rem 1rem;}

    /* Risk badge */
    .risk-badge {display: inline-flex; align-items: center; gap: 6px; padding: 0.45rem 0.9rem;
        border-radius: 999px; font-weight: 800; letter-spacing: 0.2px; color: #0f172a;}
    .risk-low {background: #ecfdf3; color: #166534; border: 1px solid #bbf7d0;}
    .risk-medium {background: #fff7ed; color: #9a3412; border: 1px solid #fed7aa;}
    .risk-high {background: #fef2f2; color: #991b1b; border: 1px solid #fecdd3; box-shadow: 0 0 0 3px rgba(248, 113, 113, 0.14);}  

    /* Expander */
    details[open] summary {background: #0f172a !important; color: #e2e8f0 !important; border-radius: 16px 16px 0 0;}
    details summary {border-radius: 16px; padding: 0.9rem 1rem; background: #0ea5e9; color: #0f172a; font-weight: 700;}
    .risk-breakdown {background: #f8fafc; border-radius: 12px; padding: 1rem; border: 1px solid #e2e8f0;}

    /* Animated reveal for conditional fields */
    .fade-in {animation: fadeIn 220ms ease-in forwards; opacity: 0;}
    @keyframes fadeIn {from {opacity: 0; transform: translateY(-2px);} to {opacity: 1; transform: translateY(0);} }

    /* Helper text */
    .hint {color: #94a3b8; font-size: 0.9rem; margin-top: -8px; margin-bottom: 12px;}
    .logo-placeholder {border: 1px dashed #cbd5e1; border-radius: 12px; padding: 12px; text-align: center; background: #f8fafc; color: #475569;}
</style>
""",
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------------
# Defaults and helpers
# ----------------------------------------------------------------------------
DEFAULT_ASSESSMENT: Dict[str, str] = {
    "first_name": "",
    "last_name": "",
    "client_id": "",
    "age": "",
    "height": "",
    "weight": "",
    "diagnoses": "No",
    "diagnoses_details": "",
    "seizures": "No",
    "seizure_details": "",
    "medications": "No",
    "medication_details": "",
    "assist_medical": "No",
    "behavior_mood": "Stable",
    "behavior_sleep": "Good (7-9 hrs)",
    "behavior_social": "Active & positive",
    "behavior_daily": "Independent",
    "behavior_mental": "No",
    "behavior_mental_details": "",
}


def ensure_session_defaults() -> None:
    """Initialize session state with safe defaults and backward compatibility."""

    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "data" not in st.session_state:
        st.session_state.data = {}
    if "assessments" not in st.session_state:
        st.session_state.assessments: List[Dict[str, str]] = []

    # Backfill missing keys for the active draft assessment
    for key, default in DEFAULT_ASSESSMENT.items():
        st.session_state.data.setdefault(key, default)


def parse_height_to_inches(raw: str) -> Tuple[int, str]:
    """Parse height strings like 5'7" or 67 into total inches with feedback.

    Returns (inches, normalized_display).
    """

    cleaned = raw.strip()
    if not cleaned:
        return 0, ""

    # Accept patterns: 5'7", 5'7, 5 ft 7 in, 67, 170cm (converted), 5.7
    ft_in_pattern = re.compile(r"(?P<ft>\d+)[\s']*(ft)?[\s-]*(?P<inch>\d{0,2})[\s\"]*(in)?", re.IGNORECASE)
    metric_pattern = re.compile(r"(?P<cm>\d+)\s*cm", re.IGNORECASE)

    # Metric (cm)
    metric_match = metric_pattern.fullmatch(cleaned)
    if metric_match:
        cm_val = int(metric_match.group("cm"))
        inches = round(cm_val / 2.54)
        return inches, f"{cm_val} cm ({inches}\" total)"

    # Feet and inches
    ft_match = ft_in_pattern.fullmatch(cleaned.replace('\"', ""))
    if ft_match:
        feet = int(ft_match.group("ft")) if ft_match.group("ft") else 0
        inches = int(ft_match.group("inch")) if ft_match.group("inch") else 0
        total = feet * 12 + inches
        return total, f"{feet}'{inches}\""

    # Raw inches number
    if cleaned.isdigit():
        total = int(cleaned)
        return total, f"{total}\""

    return 0, ""


def calculate_risk(assessment: Dict[str, str]) -> Tuple[float, str, List[str]]:
    """Calculate a transparent risk score with weighted factors."""

    age_val = float(assessment.get("age") or 0)
    weight_val = float(assessment.get("weight") or 0)
    height_inches, height_label = parse_height_to_inches(assessment.get("height", ""))

    score = 0.0
    breakdown: List[str] = []

    # Age weighting
    age_weight = 0.35
    age_component = min(age_val, 100) * age_weight
    score += age_component
    breakdown.append(f"Age ({age_val:.0f}): +{age_component:.1f} (weighted {age_weight})")

    # Body considerations
    weight_weight = 0.12
    weight_component = min(weight_val, 400) * weight_weight / 2
    score += weight_component
    breakdown.append(f"Weight ({weight_val:.0f} lbs): +{weight_component:.1f} (mobility & lift risk)")

    height_weight = 0.08
    height_component = min(height_inches, 84) * height_weight / 2
    score += height_component
    breakdown.append(
        f"Height ({height_label or assessment.get('height','—')}): +{height_component:.1f} (transfer complexity)"
    )

    # Medical flags
    if assessment.get("diagnoses") == "Yes":
        score += 12
        breakdown.append("Diagnosed conditions: +12")
    if assessment.get("seizures") == "Yes":
        score += 28
        breakdown.append("Seizure history: +28")
    if assessment.get("medications") == "Yes":
        score += 12
        breakdown.append("Active medications: +12")
    if assessment.get("assist_medical") == "Yes":
        score += 18
        breakdown.append("Caregiver medical assistance: +18")

    # Behavioral considerations
    mood = assessment.get("behavior_mood")
    if mood and mood != "Stable":
        score += 10
        breakdown.append("Mood variability: +10")

    sleep = assessment.get("behavior_sleep")
    if sleep and sleep != "Good (7-9 hrs)":
        score += 10
        breakdown.append("Non-optimal sleep: +10")

    social = assessment.get("behavior_social")
    if social and social != "Active & positive":
        score += 8
        breakdown.append("Reduced social engagement: +8")

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
            st.markdown(
                "<div class='logo-placeholder'>Upload your logo via st.image('path/to/logo.png') in logo_header().</div>",
                unsafe_allow_html=True,
            )
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


# ----------------------------------------------------------------------------
# Assessment steps
# ----------------------------------------------------------------------------
def step_client_identification(data: Dict[str, str]) -> bool:
    with st.form("step1_form", clear_on_submit=False):
        data["first_name"] = st.text_input("First Name*", value=data.get("first_name", ""), key="first_name_input")
        data["last_name"] = st.text_input("Last Name*", value=data.get("last_name", ""), key="last_name_input")
        data["client_id"] = st.text_input("Client ID*", value=data.get("client_id", ""), key="client_id_input")
        submitted = st.form_submit_button("Next", use_container_width=True)
    if submitted:
        if all([data.get("first_name"), data.get("last_name"), data.get("client_id")]):
            return True
        st.error("Please complete all required fields.")
    return False


def step_physical_profile(data: Dict[str, str]) -> Tuple[bool, bool]:
    with st.form("step2_form", clear_on_submit=False):
        age_val = st.number_input("Age*", min_value=0, max_value=120, value=int(data.get("age") or 0), key="age_input")
        data["age"] = str(age_val)

        col_height, col_weight = st.columns(2, gap="medium")
        with col_height:
            data["height"] = st.text_input("Height*", value=data.get("height", ""), placeholder="e.g. 5'7\" or 170cm", key="height_input")
        with col_weight:
            weight_val = st.number_input("Weight (lbs)*", min_value=0, max_value=1000, value=int(float(data.get("weight") or 0)), key="weight_input")
            data["weight"] = str(weight_val)

        col_back, col_next = st.columns(2)
        back = col_back.form_submit_button("Back")
        next_step = col_next.form_submit_button("Next", use_container_width=True)

    if back:
        st.session_state.step = 1
        st.rerun()

    if next_step:
        inches, normalized = parse_height_to_inches(data.get("height", ""))
        if inches == 0:
            st.error("Please enter height in feet & inches (e.g., 5'7\"), inches, or centimeters.")
            return False, False
        data["height"] = normalized or data.get("height", "")
        if weight_val <= 0:
            st.error("Weight must be greater than 0.")
            return False, False
        return True, True

    return False, False


def step_medical_history(data: Dict[str, str]) -> Tuple[bool, bool]:
    with st.form("step3_form", clear_on_submit=False):
        st.markdown("#### Medical Conditions")

        diag_col, diag_detail_col = st.columns([3, 2], gap="small")
        with diag_col:
            data["diagnoses"] = st.radio(
                "Any diagnosed conditions?",
                ["No", "Yes"],
                horizontal=True,
                key="diagnoses_radio",
            )
        with diag_detail_col:
            if data.get("diagnoses") == "Yes":
                st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
                data["diagnoses_details"] = st.text_area(
                    "Details",
                    value=data.get("diagnoses_details", ""),
                    height=90,
                    label_visibility="collapsed",
                    key="diagnoses_details_area",
                )
                st.markdown("</div>", unsafe_allow_html=True)

        seiz_col, seiz_detail_col = st.columns([3, 2], gap="small")
        with seiz_col:
            data["seizures"] = st.radio(
                "History of seizures?",
                ["No", "Yes"],
                horizontal=True,
                key="seizures_radio",
            )
        with seiz_detail_col:
            if data.get("seizures") == "Yes":
                st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
                data["seizure_details"] = st.text_area(
                    "Details",
                    value=data.get("seizure_details", ""),
                    height=90,
                    label_visibility="collapsed",
                    key="seizure_details_area",
                )
                st.markdown("</div>", unsafe_allow_html=True)

        med_col, med_detail_col = st.columns([3, 2], gap="small")
        with med_col:
            data["medications"] = st.radio(
                "Taking medications?",
                ["No", "Yes"],
                horizontal=True,
                key="medications_radio",
            )
        with med_detail_col:
            if data.get("medications") == "Yes":
                st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
                data["medication_details"] = st.text_area(
                    "Details",
                    value=data.get("medication_details", ""),
                    height=90,
                    label_visibility="collapsed",
                    key="medication_details_area",
                )
                st.markdown("</div>", unsafe_allow_html=True)

        data["assist_medical"] = st.radio(
            "Will caregiver assist with medical tasks?",
            ["No", "Yes"],
            horizontal=True,
            key="assist_medical_radio",
        )

        col_back, col_next = st.columns(2)
        back = col_back.form_submit_button("Back")
        next_step = col_next.form_submit_button("Next", use_container_width=True)

    if back:
        st.session_state.step = 2
        st.rerun()

    if next_step:
        return True, True

    return False, False


def step_behavioral_profile(data: Dict[str, str]) -> Tuple[bool, bool]:
    with st.form("step4_form", clear_on_submit=False):
        st.markdown("#### Daily Functioning & Behavior")

        data["behavior_mood"] = st.selectbox(
            "Mood over past month?",
            ["Stable", "Occasional changes", "Frequent changes"],
            index=["Stable", "Occasional changes", "Frequent changes"].index(data.get("behavior_mood", "Stable")),
            key="behavior_mood_select",
        )
        data["behavior_sleep"] = st.selectbox(
            "Sleep quality?",
            ["Good (7-9 hrs)", "Fair (5-7 hrs)", "Poor (<5 hrs)"],
            index=["Good (7-9 hrs)", "Fair (5-7 hrs)", "Poor (<5 hrs)"].index(data.get("behavior_sleep", "Good (7-9 hrs)")),
            key="behavior_sleep_select",
        )
        data["behavior_social"] = st.selectbox(
            "Social engagement?",
            ["Active & positive", "Limited", "Withdrawn"],
            index=["Active & positive", "Limited", "Withdrawn"].index(data.get("behavior_social", "Active & positive")),
            key="behavior_social_select",
        )
        data["behavior_daily"] = st.selectbox(
            "Daily activities (ADLs)?",
            ["Independent", "Some help needed", "Full assistance"],
            index=["Independent", "Some help needed", "Full assistance"].index(data.get("behavior_daily", "Independent")),
            key="behavior_daily_select",
        )
        data["behavior_mental"] = st.radio(
            "Any mental health history?",
            ["No", "Yes"],
            horizontal=True,
            key="behavior_mental_radio",
        )
        if data.get("behavior_mental") == "Yes":
            st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
            data["behavior_mental_details"] = st.text_area(
                "Details",
                value=data.get("behavior_mental_details", ""),
                height=110,
                key="behavior_mental_details_area",
            )
            st.markdown("</div>", unsafe_allow_html=True)

        col_back, col_submit = st.columns(2)
        back = col_back.form_submit_button("Back")
        submit = col_submit.form_submit_button("Submit Assessment", type="primary", use_container_width=True)

    if back:
        st.session_state.step = 3
        st.rerun()

    if submit:
        return True, True

    return False, False


# ----------------------------------------------------------------------------
# Views
# ----------------------------------------------------------------------------
def home_view() -> None:
    logo_header()
    st.markdown("""
    <p class='muted' style='text-align:center; margin-top:14px;'>HIPAA-aligned • Protected • Built for seamless caregiver onboarding</p>
    """, unsafe_allow_html=True)


def assessment_view() -> None:
    data = st.session_state.data

    st.markdown("<div class='assessment-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Client Assessment</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p class='muted' style='text-align:center; margin-bottom:18px;'>4 streamlined steps • Estimated time: 5 minutes</p>",
        unsafe_allow_html=True,
    )

    progress = {1: 0.25, 2: 0.5, 3: 0.75, 4: 1.0}
    st.progress(progress.get(st.session_state.step, 0.25))

    if st.session_state.step == 1:
        st.markdown("<div class='step-header'>Step 1 of 4 • Client Identification</div>", unsafe_allow_html=True)
        if step_client_identification(data):
            st.session_state.step = 2
            st.rerun()

    elif st.session_state.step == 2:
        st.markdown("<div class='step-header'>Step 2 of 4 • Physical Profile</div>", unsafe_allow_html=True)
        completed, _ = step_physical_profile(data)
        if completed:
            st.session_state.step = 3
            st.rerun()

    elif st.session_state.step == 3:
        st.markdown("<div class='step-header'>Step 3 of 4 • Medical History</div>", unsafe_allow_html=True)
        completed, _ = step_medical_history(data)
        if completed:
            st.session_state.step = 4
            st.rerun()

    else:
        st.markdown("<div class='step-header'>Step 4 of 4 • Behavioral Profile</div>", unsafe_allow_html=True)
        completed, submitted = step_behavioral_profile(data)
        if completed and submitted:
            # Persist assessment with timestamp while keeping backward compatibility
            assessment_record = {**DEFAULT_ASSESSMENT, **data}
            assessment_record["submitted_at"] = datetime.utcnow().isoformat()
            st.session_state.assessments.append(assessment_record)

            st.success("Assessment submitted successfully! Redirecting to admin...")
            st.session_state.data = DEFAULT_ASSESSMENT.copy()
            st.session_state.step = 1
            st.session_state.page = "admin"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def admin_view() -> None:
    st.markdown("<div class='assessment-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Admin Dashboard</h2>", unsafe_allow_html=True)
    st.markdown("<p class='muted' style='text-align:center;'>Secure view of completed assessments</p>", unsafe_allow_html=True)

    if not st.session_state.assessments:
        st.info("No assessments submitted yet.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Newest first using submitted_at fallback to index ordering
    def sort_key(entry: Dict[str, str]):
        ts = entry.get("submitted_at")
        try:
            return datetime.fromisoformat(ts) if ts else datetime.min
        except ValueError:
            return datetime.min

    for assessment in sorted(st.session_state.assessments, key=sort_key, reverse=True):
        name = f"{assessment.get('first_name','').strip()} {assessment.get('last_name','').strip()}".strip() or "Unnamed Client"
        client_id = assessment.get("client_id", "N/A")

        score, level, breakdown = calculate_risk(assessment)
        risk_class = f"risk-{level.lower()}"
        submitted_at = assessment.get("submitted_at")
        submitted_label = "Unknown submission time"
        if submitted_at:
            try:
                submitted_label = datetime.fromisoformat(submitted_at).strftime("%b %d, %Y • %I:%M %p UTC")
            except ValueError:
                submitted_label = submitted_at

        summary_title = (
            f"{name} • ID: {client_id} • "
            f"<span class='risk-badge {risk_class}'>Risk: {level}</span>"
            f" <span class='muted'>(Score: {score:.1f})</span>"
        )

        with st.expander(summary_title, expanded=False):
            col_meta, col_actions = st.columns([3, 1])
            with col_meta:
                st.write(f"**Submitted:** {submitted_label}")
            with col_actions:
                st.write("**Status:** Reviewed")

            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Age:** {assessment.get('age','—')} | **Height:** {assessment.get('height','—')} | **Weight:** {assessment.get('weight','—')} lbs")
                st.write(f"**Diagnoses:** {assessment.get('diagnoses','—')}")
                if assessment.get("diagnoses_details"):
                    st.markdown(f"<div class='inline-detail'>🔍 {assessment.get('diagnoses_details','')}</div>", unsafe_allow_html=True)
                st.write(f"**Seizures:** {assessment.get('seizures','—')}")
                if assessment.get("seizure_details"):
                    st.markdown(f"<div class='inline-detail'>⚡ {assessment.get('seizure_details','')}</div>", unsafe_allow_html=True)
            with col2:
                st.write(f"**Medications:** {assessment.get('medications','—')}")
                if assessment.get("medication_details"):
                    st.markdown(f"<div class='inline-detail'>💊 {assessment.get('medication_details','')}</div>", unsafe_allow_html=True)
                st.write(f"**Medical Assistance Needed:** {assessment.get('assist_medical','—')}")
                st.write(f"**Daily Activities:** {assessment.get('behavior_daily','—')}")
                st.write(f"**Mood:** {assessment.get('behavior_mood','—')} | **Sleep:** {assessment.get('behavior_sleep','—')}")
                st.write(f"**Social:** {assessment.get('behavior_social','—')}")
                if assessment.get("behavior_mental") == "Yes" and assessment.get("behavior_mental_details"):
                    st.markdown(f"<div class='inline-detail'>🧠 {assessment.get('behavior_mental_details','')}</div>", unsafe_allow_html=True)

            st.markdown("#### Risk Score Breakdown", unsafe_allow_html=True)
            st.markdown("<div class='risk-breakdown'>", unsafe_allow_html=True)
            for item in breakdown:
                st.write("• " + item)
            st.write(f"**Final Score:** {score:.1f} → **{level} Risk** (Thresholds: <60 Low, 60-104 Medium, 105+ High)")
            st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Back to Home", key="admin_back_home"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# Router
# ----------------------------------------------------------------------------
def main() -> None:
    ensure_session_defaults()

    if st.session_state.page == "home":
        home_view()
    elif st.session_state.page == "assessment":
        assessment_view()
    else:
        admin_view()


if __name__ == "__main__":
    main()
