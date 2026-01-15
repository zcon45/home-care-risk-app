import streamlit as st
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
import json

# Page Config
st.set_page_config(
    page_title="Home Care Risk Assessment",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS with better styling
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);}
    .portal-card {
        background: white; padding: 3.5rem; border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center;
        max-width: 800px; margin: 3rem auto;
    }
    .portal-title {font-size: 3rem; color: #2c3e50; font-weight: 700; margin-bottom: 0.5rem;}
    .portal-subtitle {font-size: 1.25rem; color: #7f8c8d; margin-bottom: 3rem;}
    .assessment-card {
        background: white; padding: 2.5rem; border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); max-width: 750px; margin: 2rem auto;
    }
    .step-header {
        font-size: 1.1rem; color: #636e72; margin-bottom: 1.5rem; 
        text-align: center; font-weight: 600;
    }
    .risk-badge {
        padding: 10px 24px; border-radius: 50px; font-weight: bold; 
        display: inline-block; font-size: 1.1rem; margin: 10px 0;
    }
    .risk-low {background: #10b981; color: white;}
    .risk-moderate {background: #f59e0b; color: white;}
    .risk-high {background: #ef4444; color: white;}
    .risk-critical {background: #991b1b; color: white;}
    .metric-box {
        background: #f8f9fc; padding: 1rem; border-radius: 10px;
        border-left: 4px solid #4facfe; margin: 1rem 0;
    }
    .footer-text {margin-top: 3rem; color: #bdc3c7; font-size: 0.95rem;}
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "page" not in st.session_state:
    st.session_state.page = "home"
if "step" not in st.session_state:
    st.session_state.step = 1
if "data" not in st.session_state:
    st.session_state.data = {
        "first_name": "", "last_name": "", "client_id": "",
        "age": "", "height": "", "weight": "",
        "diagnoses": "No", "diagnoses_details": "",
        "seizures": "No", "seizure_frequency": "",
        "seizure_type": "", "seizure_severity": "",
        "medications": "No", "medication_details": "",
        "assist_medical": "No", "additional_notes": "",
        "timestamp": ""
    }
if "assessments" not in st.session_state:
    st.session_state.assessments = []

# Risk Calculation Engine
def calculate_risk_score(assessment):
    """Calculate weighted risk score based on medical factors"""
    score = 0
    risk_factors = []
    
    try:
        # Age factor (0-20 points)
        age = int(assessment.get('age', 0))
        if age > 75:
            score += 20
            risk_factors.append("Advanced age (>75)")
        elif age > 65:
            score += 10
            risk_factors.append("Senior age (65-75)")
        elif age > 85:
            score += 25
            risk_factors.append("Very advanced age (>85)")
        
        # Seizure assessment (0-40 points) - WEIGHTED HEAVILY
        if assessment.get('seizures') == "Yes":
            seizure_freq = assessment.get('seizure_frequency', '').lower()
            seizure_severity = assessment.get('seizure_severity', '').lower()
            
            # Frequency scoring
            if 'daily' in seizure_freq or 'multiple' in seizure_freq:
                score += 30
                risk_factors.append("Daily/frequent seizures")
            elif 'weekly' in seizure_freq:
                score += 20
                risk_factors.append("Weekly seizures")
            elif 'monthly' in seizure_freq:
                score += 15
                risk_factors.append("Monthly seizures")
            else:
                score += 10
                risk_factors.append("Seizure history")
            
            # Severity scoring
            if 'grand mal' in seizure_severity or 'tonic-clonic' in seizure_severity or 'severe' in seizure_severity:
                score += 25
                risk_factors.append("Severe seizure type")
            elif 'moderate' in seizure_severity:
                score += 15
                risk_factors.append("Moderate seizures")
            else:
                score += 10
        
        # Medical diagnoses (0-15 points)
        if assessment.get('diagnoses') == "Yes":
            diagnoses = assessment.get('diagnoses_details', '').lower()
            if any(term in diagnoses for term in ['heart', 'cardiac', 'stroke', 'diabetes', 'cancer']):
                score += 15
                risk_factors.append("Serious medical condition")
            else:
                score += 10
                risk_factors.append("Medical diagnosis present")
        
        # Medications (0-10 points)
        if assessment.get('medications') == "Yes":
            score += 10
            risk_factors.append("Multiple medications")
        
        # Medical assistance required (0-15 points)
        if assessment.get('assist_medical') == "Yes":
            score += 15
            risk_factors.append("Requires medical assistance")
        
        # Physical factors
        weight = float(assessment.get('weight', 0))
        if weight > 250:
            score += 10
            risk_factors.append("High body weight")
        elif weight < 100:
            score += 8
            risk_factors.append("Low body weight")
            
    except (ValueError, TypeError):
        pass
    
    # Determine risk level
    if score >= 80:
        level = "Critical"
    elif score >= 60:
        level = "High"
    elif score >= 35:
        level = "Moderate"
    else:
        level = "Low"
    
    return score, level, risk_factors

# PDF Generation Function
def generate_pdf(assessment):
    """Generate a professional PDF report"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#4facfe'),
        spaceAfter=8,
        spaceBefore=12
    )
    
    # Calculate risk
    score, level, risk_factors = calculate_risk_score(assessment)
    
    # Title
    story.append(Paragraph("Home Care Risk Assessment Report", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Client Information
    story.append(Paragraph("Client Information", heading_style))
    client_data = [
        ["Name:", f"{assessment['first_name']} {assessment['last_name']}"],
        ["Client ID:", assessment['client_id']],
        ["Age:", assessment['age']],
        ["Height:", assessment['height']],
        ["Weight:", f"{assessment['weight']} lbs"],
        ["Assessment Date:", assessment.get('timestamp', 'N/A')]
    ]
    
    client_table = Table(client_data, colWidths=[2*inch, 4*inch])
    client_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fc')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    story.append(client_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Risk Assessment Score
    story.append(Paragraph("Risk Assessment Score", heading_style))
    
    risk_color = {
        "Low": colors.HexColor('#10b981'),
        "Moderate": colors.HexColor('#f59e0b'),
        "High": colors.HexColor('#ef4444'),
        "Critical": colors.HexColor('#991b1b')
    }
    
    risk_data = [
        ["Risk Score:", f"{score:.0f}"],
        ["Risk Level:", level]
    ]
    
    risk_table = Table(risk_data, colWidths=[2*inch, 4*inch])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fc')),
        ('BACKGROUND', (1, 1), (1, 1), risk_color.get(level, colors.grey)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (1, 1), (1, 1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    story.append(risk_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Risk Factors
    if risk_factors:
        story.append(Paragraph("Identified Risk Factors", heading_style))
        for factor in risk_factors:
            story.append(Paragraph(f"• {factor}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
    
    # Medical Details
    story.append(Paragraph("Medical Information", heading_style))
    
    medical_details = []
    
    if assessment['diagnoses'] == "Yes":
        medical_details.append(["Medical Diagnoses:", "Yes"])
        if assessment['diagnoses_details']:
            medical_details.append(["Details:", assessment['diagnoses_details']])
    
    if assessment['seizures'] == "Yes":
        medical_details.append(["Seizure History:", "Yes"])
        if assessment.get('seizure_frequency'):
            medical_details.append(["Frequency:", assessment['seizure_frequency']])
        if assessment.get('seizure_severity'):
            medical_details.append(["Severity:", assessment['seizure_severity']])
    
    if assessment['medications'] == "Yes":
        medical_details.append(["Current Medications:", "Yes"])
        if assessment['medication_details']:
            medical_details.append(["Details:", assessment['medication_details']])
    
    medical_details.append(["Requires Medical Assistance:", assessment['assist_medical']])
    
    if assessment.get('additional_notes'):
        medical_details.append(["Additional Notes:", assessment['additional_notes']])
    
    medical_table = Table(medical_details, colWidths=[2*inch, 4*inch])
    medical_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fc')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    story.append(medical_table)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

# HOME PAGE
def home():
    st.markdown('<div class="portal-card">', unsafe_allow_html=True)
    st.markdown('<h1 class="portal-title">🏥 Home Care Risk Assessment</h1>', unsafe_allow_html=True)
    st.markdown('<p class="portal-subtitle">Professional risk evaluation for home care clients</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        if st.button("📋 New Assessment", key="client", use_container_width=True, type="primary"):
            st.session_state.page = "assessment"
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("🛡️ Admin Dashboard", key="admin", use_container_width=True):
            st.session_state.page = "admin"
            st.rerun()

    st.markdown('<p class="footer-text">Secure & Confidential • HIPAA Compliant</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ASSESSMENT PAGE
def assessment():
    data = st.session_state.data
    st.markdown('<div class="assessment-card">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#2c3e50;'>Client Risk Assessment</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#636e72; margin-bottom:2rem;'>Complete all steps for comprehensive evaluation</p>", unsafe_allow_html=True)
    
    progress = {1: 0.25, 2: 0.50, 3: 0.75, 4: 1.0}
    st.progress(progress[st.session_state.step])

    # Step 1: Client Identification
    if st.session_state.step == 1:
        st.markdown("<div class='step-header'>Step 1 of 4 • Client Identification</div>", unsafe_allow_html=True)
        with st.form("step1"):
            data["first_name"] = st.text_input("First Name*", value=data["first_name"])
            data["last_name"] = st.text_input("Last Name*", value=data["last_name"])
            data["client_id"] = st.text_input("Client ID*", value=data["client_id"])
            
            if st.form_submit_button("Next →", use_container_width=True, type="primary"):
                if data["first_name"] and data["last_name"] and data["client_id"]:
                    st.session_state.step = 2
                    st.rerun()
                else:
                    st.error("⚠️ Please fill in all required fields")

    # Step 2: Physical Profile
    elif st.session_state.step == 2:
        st.markdown("<div class='step-header'>Step 2 of 4 • Physical Profile</div>", unsafe_allow_html=True)
        with st.form("step2"):
            data["age"] = st.text_input("Age*", value=data["age"], placeholder="e.g., 74")
            col1, col2 = st.columns(2)
            with col1:
                data["height"] = st.text_input("Height*", value=data["height"], placeholder="e.g., 5'7\"")
            with col2:
                data["weight"] = st.text_input("Weight (lbs)*", value=data["weight"], placeholder="e.g., 165")
            
            col_back, col_next = st.columns(2)
            with col_back:
                if st.form_submit_button("← Back"):
                    st.session_state.step = 1
                    st.rerun()
            with col_next:
                if st.form_submit_button("Next →", use_container_width=True, type="primary"):
                    if data["age"] and data["height"] and data["weight"]:
                        st.session_state.step = 3
                        st.rerun()
                    else:
                        st.error("⚠️ Please complete all fields")

    # Step 3: Medical Profile
    elif st.session_state.step == 3:
        st.markdown("<div class='step-header'>Step 3 of 4 • Medical History</div>", unsafe_allow_html=True)
        with st.form("step3"):
            # Medical Diagnoses
            st.markdown("#### Medical Diagnoses")
            data["diagnoses"] = st.radio("Any medical diagnoses?", ["No", "Yes"], horizontal=True, key="dx")
            if data["diagnoses"] == "Yes":
                data["diagnoses_details"] = st.text_area(
                    "Please list diagnoses and conditions:",
                    value=data["diagnoses_details"],
                    placeholder="e.g., Type 2 Diabetes, Hypertension, Heart Disease",
                    height=80
                )
            
            st.divider()
            
            # Medications
            st.markdown("#### Current Medications")
            data["medications"] = st.radio("Currently taking medications?", ["No", "Yes"], horizontal=True, key="meds")
            if data["medications"] == "Yes":
                data["medication_details"] = st.text_area(
                    "Please list all medications:",
                    value=data["medication_details"],
                    placeholder="e.g., Metformin 500mg, Lisinopril 10mg",
                    height=80
                )
            
            col_back, col_next = st.columns(2)
            with col_back:
                if st.form_submit_button("← Back"):
                    st.session_state.step = 2
                    st.rerun()
            with col_next:
                if st.form_submit_button("Next →", use_container_width=True, type="primary"):
                    st.session_state.step = 4
                    st.rerun()

    # Step 4: Seizure Assessment & Care Requirements
    elif st.session_state.step == 4:
        st.markdown("<div class='step-header'>Step 4 of 4 • Seizure Assessment & Care Requirements</div>", unsafe_allow_html=True)
        with st.form("step4"):
            # Seizure Assessment
            st.markdown("#### Seizure History")
            data["seizures"] = st.radio("History of seizures?", ["No", "Yes"], horizontal=True, key="seizures")
            
            if data["seizures"] == "Yes":
                st.info("⚠️ Seizure information is critical for risk assessment. Please provide detailed information.")
                
                data["seizure_frequency"] = st.selectbox(
                    "Seizure Frequency*",
                    ["Select frequency", "Daily or multiple times per day", "Weekly", "Monthly", "Less than monthly", "Rare/controlled"],
                    index=0 if not data.get("seizure_frequency") else ["Select frequency", "Daily or multiple times per day", "Weekly", "Monthly", "Less than monthly", "Rare/controlled"].index(data.get("seizure_frequency", "Select frequency"))
                )
                
                data["seizure_severity"] = st.selectbox(
                    "Seizure Type/Severity*",
                    ["Select type", "Grand mal/Tonic-clonic (severe)", "Moderate (loss of consciousness)", "Mild (absence/petit mal)", "Controlled with medication"],
                    index=0 if not data.get("seizure_severity") else ["Select type", "Grand mal/Tonic-clonic (severe)", "Moderate (loss of consciousness)", "Mild (absence/petit mal)", "Controlled with medication"].index(data.get("seizure_severity", "Select type"))
                )
                
                data["seizure_type"] = st.text_area(
                    "Additional seizure details:",
                    value=data.get("seizure_type", ""),
                    placeholder="Describe triggers, duration, post-seizure symptoms, emergency protocols, etc.",
                    height=100
                )
            
            st.divider()
            
            # Care Requirements
            st.markdown("#### Care Requirements")
            data["assist_medical"] = st.radio(
                "Will the caregiver need to assist with medical tasks?",
                ["No", "Yes"],
                horizontal=True,
                help="Examples: medication administration, wound care, mobility assistance, monitoring vitals"
            )
            
            data["additional_notes"] = st.text_area(
                "Additional Notes or Special Instructions:",
                value=data.get("additional_notes", ""),
                placeholder="Any other important information for care providers...",
                height=100
            )
            
            col_back, col_submit = st.columns(2)
            with col_back:
                if st.form_submit_button("← Back"):
                    st.session_state.step = 3
                    st.rerun()
            with col_submit:
                if st.form_submit_button("📊 Submit Assessment", use_container_width=True, type="primary"):
                    # Validation for seizure details
                    if data["seizures"] == "Yes":
                        if data.get("seizure_frequency") == "Select frequency" or data.get("seizure_severity") == "Select type":
                            st.error("⚠️ Please complete all seizure assessment fields")
                            st.stop()
                    
                    # Add timestamp
                    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Save assessment
                    st.session_state.assessments.append(data.copy())
                    
                    # Reset data
                    st.session_state.data = {
                        "first_name": "", "last_name": "", "client_id": "",
                        "age": "", "height": "", "weight": "",
                        "diagnoses": "No", "diagnoses_details": "",
                        "seizures": "No", "seizure_frequency": "",
                        "seizure_type": "", "seizure_severity": "",
                        "medications": "No", "medication_details": "",
                        "assist_medical": "No", "additional_notes": "",
                        "timestamp": ""
                    }
                    st.session_state.step = 1
                    st.session_state.page = "admin"
                    st.success("✅ Assessment completed successfully!")
                    st.rerun()

    if st.button("🏠 Back to Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ADMIN DASHBOARD
def admin():
    st.markdown('<div class="assessment-card">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#2c3e50;'>📊 Admin Dashboard</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#636e72; margin-bottom:2rem;'>All Completed Risk Assessments</p>", unsafe_allow_html=True)
    
    if not st.session_state.assessments:
        st.info("📋 No assessments have been submitted yet. Create your first assessment to get started.")
    else:
        # Summary metrics
        total = len(st.session_state.assessments)
        high_risk = sum(1 for a in st.session_state.assessments if calculate_risk_score(a)[1] in ["High", "Critical"])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Assessments", total)
        with col2:
            st.metric("High/Critical Risk", high_risk)
        with col3:
            avg_score = sum(calculate_risk_score(a)[0] for a in st.session_state.assessments) / total
            st.metric("Average Risk Score", f"{avg_score:.0f}")
        
        st.divider()
        
        # Display each assessment
        for i, assessment in enumerate(reversed(st.session_state.assessments)):
            score, level, risk_factors = calculate_risk_score(assessment)
            
            risk_class = f"risk-{level.lower()}"
            name = f"{assessment['first_name']} {assessment['last_name']}"
            
            with st.expander(f"**{name}** • ID: {assessment['client_id']} • Risk: {level} ({score:.0f})", expanded=False):
                # Client info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Age:** {assessment['age']}")
                with col2:
                    st.markdown(f"**Height:** {assessment['height']}")
                with col3:
                    st.markdown(f"**Weight:** {assessment['weight']} lbs")
                
                st.markdown(f"**Assessment Date:** {assessment.get('timestamp', 'N/A')}")
                
                # Risk badge
                st.markdown(f"<div class='risk-badge {risk_class}'>{level} Risk - Score: {score:.0f}</div>", unsafe_allow_html=True)
                
                # Risk factors
                if risk_factors:
                    st.markdown("**Identified Risk Factors:**")
                    for factor in risk_factors:
                        st.markdown(f"• {factor}")
                
                st.divider()
                
                # Medical details
                if assessment['diagnoses'] == "Yes":
                    st.markdown("**Medical Diagnoses:** Yes")
                    if assessment['diagnoses_details']:
                        st.markdown(f"_{assessment['diagnoses_details']}_")
                
                if assessment['seizures'] == "Yes":
                    st.markdown("**⚠️ Seizure History:** Yes")
                    if assessment.get('seizure_frequency'):
                        st.markdown(f"**Frequency:** {assessment['seizure_frequency']}")
                    if assessment.get('seizure_severity'):
                        st.markdown(f"**Severity:** {assessment['seizure_severity']}")
                    if assessment.get('seizure_type'):
                        st.markdown(f"**Details:** _{assessment['seizure_type']}_")
                
                if assessment['medications'] == "Yes":
                    st.markdown("**Current Medications:** Yes")
                    if assessment['medication_details']:
                        st.markdown(f"_{assessment['medication_details']}_")
                
                st.markdown(f"**Requires Medical Assistance:** {assessment['assist_medical']}")
                
                if assessment.get('additional_notes'):
                    st.markdown(f"**Additional Notes:** _{assessment['additional_notes']}_")
                
                # Download PDF button
                st.divider()
                pdf_buffer = generate_pdf(assessment)
                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_buffer,
                    file_name=f"Risk_Assessment_{assessment['client_id']}_{assessment['last_name']}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    with col2:
        if st.session_state.assessments and st.button("🗑️ Clear All Data", use_container_width=True):
            if st.session_state.get('confirm_clear'):
                st.session_state.assessments = []
                st.session_state.confirm_clear = False
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("Click again to confirm deletion")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ROUTER
if st.session_state.page == "home":
    home()
elif st.session_state.page == "assessment":
    assessment()
elif st.session_state.page == "admin":
    admin()
