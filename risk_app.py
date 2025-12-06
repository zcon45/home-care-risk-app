import streamlit as st
from pathlib import Path
from datetime import datetime

# Try to import PDF tools
try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False

try:
    from PyPDF2 import PdfReader, PdfWriter
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

# ---------------------------------------------------
# LOCAL DEV STORAGE PATH (PRACTICE ONLY)
# ---------------------------------------------------

BASE_SAVE_PATH = Path(
    r"C:\Users\zach_\OneDrive\Documents\Personal Risk Assessment Project\Practice Assessments"
)
BASE_SAVE_PATH.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------
# HELPERS FOR FILE SAVING & PDF GENERATION
# ---------------------------------------------------

def save_uploaded_file_to_disk(file_bytes: bytes, original_name: str, suffix: str = "") -> Path:
    """
    Save an uploaded file (bytes) under BASE_SAVE_PATH with a timestamped name.
    Returns full path.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    original = Path(original_name)
    new_name = f"{original.stem}{suffix}_{timestamp}{original.suffix}"
    out_path = BASE_SAVE_PATH / new_name
    with open(out_path, "wb") as f:
        f.write(file_bytes)
    return out_path


def build_ai_style_summary(data, score: float, level: str) -> str:
    """
    Simple rule-based 'AI-style' summary of the assessment.
    No external API – runs locally.
    """
    lines = []
    lines.append(f"Overall, this client is assessed as {level.lower()} with a risk score of {score:.1f}.")
    lines.append("Key factors considered in this assessment include age, weight, height, seizure history, "
                 "medication use, mobility level, adult supervision, and any additional notes provided.")

    # Age factor
    try:
        age = int(data.get("age", 0))
        if age >= 80:
            lines.append("Advanced age contributes to increased risk for falls and medical complications.")
        elif age >= 65:
            lines.append("Older adult status is a moderate risk factor.")
        else:
            lines.append("Age does not appear to be a primary risk driver in this case.")
    except Exception:
        pass

    # Seizure factor
    if data.get("seizures") == "Yes":
        stype = data.get("seizure_type", "unspecified")
        lines.append(f"There is a history of seizures ({stype}), which elevates safety and supervision needs.")

    # Medications
    if data.get("medications") == "Yes":
        if data.get("med_list"):
            lines.append("The client takes one or more medications, which may increase complexity of care "
                         "and the need for monitoring adherence and side effects.")
        else:
            lines.append("Medication use is reported, but no specific medications were entered.")

    # Mobility
    mobility_label = data.get("mobility_label", "")
    if mobility_label:
        lines.append(f"Mobility level is documented as: {mobility_label}.")
        if "Non-mobile" in mobility_label or "bedridden" in mobility_label:
            lines.append("Limited or absent mobility significantly increases risk for pressure injuries and "
                         "dependence on caregivers for transfers.")
        elif "Uses mobility aid" in mobility_label or "hands-on assist" in mobility_label:
            lines.append("Mobility support is required, increasing fall and transfer risk.")
        else:
            lines.append("Mobility appears relatively independent, which lowers physical risk in some areas.")

    # Adult supervision
    if data.get("adult_present") == "Yes":
        lines.append("An adult is expected to be present during care, which may help mitigate risk and "
                     "support safe decision-making.")
    else:
        lines.append("No consistent adult supervision is expected during care, which can increase overall risk.")

    # Notes
    notes = data.get("notes", "").strip()
    if notes:
        lines.append("Additional notes were provided and should be reviewed for context and specific concerns.")

    lines.append("This summary is intended to support clinical judgment and does not replace a full professional "
                 "assessment or care plan.")
    return "\n\n".join(lines)


def generate_summary_pdf(data, score: float, level: str, client_full_name: str, dob_str: str) -> Path:
    """
    Generate a PDF summarizing the assessment & AI-style narrative.
    Requires FPDF. Returns path to the summary PDF.
    """
    if not FPDF_AVAILABLE:
        raise RuntimeError("FPDF is not installed. Please run 'pip install fpdf2'.")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)

    pdf.cell(0, 10, "Home Care Risk Assessment Summary", ln=True)
    pdf.ln(4)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Client: {client_full_name}", ln=True)
    pdf.cell(0, 8, f"Date of Birth: {dob_str}", ln=True)
    pdf.cell(0, 8, f"Client ID: {data.get('client_id','')}", ln=True)
    pdf.ln(4)

    pdf.cell(0, 8, f"Risk Level: {level}", ln=True)
    pdf.cell(0, 8, f"Risk Score: {score:.1f}", ln=True)
    pdf.ln(6)

    # Section: Raw assessment details
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "Assessment Details", ln=True)
    pdf.ln(3)
    pdf.set_font("Arial", "", 11)

    # Simple helper for wrapping text
    def add_line(label, value):
        pdf.set_font("Arial", "B", 11)
        pdf.multi_cell(0, 6, f"{label}", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, f"{value}", ln=True)
        pdf.ln(1)

    add_line("Age:", data.get("age", ""))
    add_line("Height (feet/inches):",
             f"{data.get('height_feet','')} ft {data.get('height_inches','')} in")
    add_line("Weight (lbs):", data.get("weight", ""))

    add_line("History of Seizures:", data.get("seizures", ""))
    if data.get("seizures") == "Yes":
        add_line("Seizure Type:", data.get("seizure_type", ""))

    add_line("Takes Medication:", data.get("medications", ""))
    if data.get("medications") == "Yes":
        meds = data.get("med_list", [])
        if meds:
            med_texts = []
            for idx, med in enumerate(meds, start=1):
                med_texts.append(
                    f"{idx}. {med['name']} – {med['dosage']} – {med['frequency']}"
                )
            add_line("Medications:", "\n".join(med_texts))
        else:
            add_line("Medications:", "Reported, but no specific medications entered.")

    add_line("Mobility Level:", data.get("mobility_label", ""))
    add_line("Adult Present During Care:", data.get("adult_present", ""))
    if data.get("adult_present") == "Yes":
        adult_lines = []
        if data.get("adult1"):
            adult_lines.append(f"Adult #1: {data.get('adult1')} ({data.get('rel1')})")
        if data.get("adult2"):
            rel2 = data.get("rel2", "")
            adult_lines.append(f"Adult #2: {data.get('adult2')} ({rel2})" if rel2 else f"Adult #2: {data.get('adult2')}")
        if adult_lines:
            add_line("Adults Present:", "\n".join(adult_lines))

    notes = data.get("notes", "").strip()
    if notes:
        add_line("Additional Notes:", notes)

    # AI-style narrative summary
    summary_text = build_ai_style_summary(data, score, level)
    pdf.ln(4)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "AI-Style Summary", ln=True)
    pdf.ln(2)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, summary_text)

    # Save summary PDF
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_name = client_full_name.replace("/", "_")
    out_name = f"{safe_name}_assessment_summary_{timestamp}.pdf"
    out_path = BASE_SAVE_PATH / out_name
    pdf.output(str(out_path))

    return out_path


def merge_pdfs(uploaded_pdf: Path, summary_pdf: Path, final_path: Path) -> Path:
    """
    Merge the uploaded client PDF + assessment summary PDF into a single file.
    uploaded_pdf comes first, then summary.
    Requires PyPDF2.
    """
    if not PYPDF2_AVAILABLE:
        raise RuntimeError("PyPDF2 not installed. Please run 'pip install PyPDF2'.")

    writer = PdfWriter()

    # Add uploaded PDF pages
    if uploaded_pdf and uploaded_pdf.exists():
        reader1 = PdfReader(str(uploaded_pdf))
        for page in reader1.pages:
            writer.add_page(page)

    # Add summary PDF pages
    reader2 = PdfReader(str(summary_pdf))
    for page in reader2.pages:
        writer.add_page(page)

    with open(final_path, "wb") as f:
        writer.write(f)

    return final_path


def build_final_pdf(data, score: float, level: str):
    """
    High-level helper:
      - Save uploaded PDF (if any)
      - Generate summary PDF
      - Merge into final single PDF if PyPDF2 is available
    Returns (final_path, message_string).
    """
    first = data.get("first_name", "").strip()
    last = data.get("last_name", "").strip()
    dob_date = data.get("dob")
    if dob_date:
        dob_str = dob_date.strftime("%Y-%m-%d")
    else:
        dob_str = "Unknown-DOB"

    client_full_name = f"{first} {last}".strip()
    if not client_full_name:
        client_full_name = "Unknown Client"

    # Base final file name: LastName, FirstName - DOB.pdf
    if last and first and dob_str != "Unknown-DOB":
        final_filename = f"{last}, {first} - {dob_str}.pdf"
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        final_filename = f"{client_full_name.replace(' ', '_')}_{timestamp}.pdf"

    final_path = BASE_SAVE_PATH / final_filename

    # Step 1: Save uploaded pdf (if present)
    uploaded_saved_path = None
    if data.get("uploaded_pdf_bytes") and data.get("uploaded_pdf_name"):
        uploaded_saved_path = save_uploaded_file_to_disk(
            data.uploaded_pdf_bytes,
            data.uploaded_pdf_name,
            suffix="_original"
        )

    # Step 2: Create summary PDF
    summary_pdf_path = generate_summary_pdf(data, score, level, client_full_name, dob_str)

    # Step 3: Try merging
    if uploaded_saved_path and PYPDF2_AVAILABLE:
        merge_pdfs(uploaded_saved_path, summary_pdf_path, final_path)
        msg = f"Final combined PDF (client upload + assessment summary) saved to:\n{final_path}"
    else:
        # If no uploaded or no PyPDF2, just copy the summary as the final
        summary_pdf_path.replace(final_path)
        if not uploaded_saved_path:
            msg = f"No uploaded PDF. Summary PDF saved to:\n{final_path}"
        else:
            msg = (
                "PyPDF2 is not installed, so the uploaded PDF and summary "
                f"were not merged. Summary-only PDF saved to:\n{final_path}"
            )

    return final_path, msg


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Home Care Risk Assessment",
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
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SESSION STATE INIT (HOME CARE ONLY)
# ---------------------------------------------------

if "step" not in st.session_state:
    st.session_state.step = 1

if "med_list" not in st.session_state:
    st.session_state.med_list = []

# store uploaded pdf in session_state
for key in ["uploaded_pdf_bytes", "uploaded_pdf_name"]:
    if key not in st.session_state:
        st.session_state[key] = None

data = st.session_state

STEPS = {
    1: "Client Info & Upload",
    2: "Demographics",
    3: "Medical History",
    4: "Medications",
    5: "Mobility & Safety",
    6: "Review & Submit"
}
TOTAL_STEPS = len(STEPS)


def next_step():
    st.session_state.step += 1


def prev_step():
    st.session_state.step -= 1


def reset_flow():
    # Clear only relevant keys, not entire session
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.session_state.step = 1
    st.session_state.med_list = []
    st.session_state.uploaded_pdf_bytes = None
    st.session_state.uploaded_pdf_name = None


# ---------------------------------------------------
# HOME CARE RISK ASSESSMENT FLOW
# ---------------------------------------------------

def run_home_care_risk_assessment():
    data = st.session_state

    st.markdown(f"### Home Care Risk Assessment — Step {data.step} of {TOTAL_STEPS} · {STEPS[data.step]}")
    st.progress(data.step / TOTAL_STEPS)

    # STEP 1 – Client Info + PDF Upload
    if data.step == 1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            data.first_name = st.text_input("First Name (required)", value=data.get("first_name", ""))
        with col2:
            data.last_name = st.text_input("Last Name (required)", value=data.get("last_name", ""))

        data.dob = st.date_input(
            "Date of Birth (required)",
            value=data.get("dob", datetime(2000, 1, 1)),
        )

        data.client_id = st.text_input("Client ID (optional)", value=data.get("client_id", ""))

        st.markdown("**Upload Client PDF** (e.g., prior records, referral, or intake form)")
        uploaded_file = st.file_uploader(
            "Please upload a PDF labeled like: 'Last name, First name - DOB'",
            type=["pdf"]
        )
        if uploaded_file is not None:
            data.uploaded_pdf_bytes = uploaded_file.getvalue()
            data.uploaded_pdf_name = uploaded_file.name
            st.success(f"Uploaded: {uploaded_file.name}")

        first_ok = bool(data.first_name.strip())
        last_ok = bool(data.last_name.strip())
        dob_ok = data.dob is not None

        colA, colB = st.columns(2)
        with colA:
            st.button("Reset", on_click=reset_flow, key="reset1")
        with colB:
            st.button(
                "Next →",
                on_click=next_step,
                disabled=not (first_ok and last_ok and dob_ok),
                key="next1",
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # STEP 2 – Demographics
    elif data.step == 2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        data.age = st.text_input("Age", value=data.get("age", ""))
        data.weight = st.text_input("Weight (lbs)", value=data.get("weight", ""))

        st.markdown("**Height**")
        col1, col2 = st.columns(2)
        with col1:
            data.height_feet = st.text_input("Feet", value=data.get("height_feet", ""))
        with col2:
            data.height_inches = st.text_input("Inches (0–11)", value=data.get("height_inches", ""))

        def demo_valid():
            try:
                age = int(data.age)
                weight = float(data.weight)
                ft = int(data.height_feet)
                inch = int(data.height_inches)
                return age > 0 and weight > 0 and ft >= 0 and 0 <= inch <= 11
            except Exception:
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
            ["No", "Yes"],
            horizontal=True,
            index=0 if data.get("seizures", "No") == "No" else 1
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
            current = data.get("seizure_type", "Select seizure type...")
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
            ["No", "Yes"],
            horizontal=True,
            index=0 if data.get("medications", "No") == "No" else 1
        )

        meds_ok = True

        if data.medications == "Yes":
            with st.expander("Add Medication"):
                m_name = st.text_input("Medication Name", key="new_med_name")
                m_dose = st.text_input("Dosage", key="new_med_dose")
                m_freq = st.text_input("Frequency", key="new_med_freq")

                can_add = bool(m_name.strip() and m_dose.strip() and m_freq.strip())

                if st.button("Add Medication", disabled=not can_add, key="add_med"):
                    data.med_list.append(
                        {
                            "name": m_name.strip(),
                            "dosage": m_dose.strip(),
                            "frequency": m_freq.strip()
                        }
                    )
                    # Do not directly mutate widget keys; user can overwrite manually.

            st.markdown("### Current Medications")

            if not data.med_list:
                st.caption("No medications added yet.")
                meds_ok = False
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

                meds_ok = True
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
            ["No", "Yes"],
            horizontal=True,
            index=0 if data.get("adult_present", "No") == "No" else 1
        )

        adults_ok = True

        data.adult1 = data.get("adult1", "")
        data.rel1 = data.get("rel1", "")
        data.adult2 = data.get("adult2", "")
        data.rel2 = data.get("rel2", "")

        if data.adult_present == "Yes":
            col1, col2 = st.columns(2)
            with col1:
                data.adult1 = st.text_input("Adult #1 Name", value=data.adult1)
            with col2:
                data.rel1 = st.text_input("Relationship (required)", value=data.rel1)

            col3, col4 = st.columns(2)
            with col3:
                data.adult2 = st.text_input("Adult #2 Name", value=data.adult2)
            with col4:
                data.rel2 = st.text_input("Relationship", value=data.rel2)

            adults_ok = bool(data.adult1.strip() and data.rel1.strip())
            if data.adult2.strip() and not data.rel2.strip():
                adults_ok = False

        data.notes = st.text_area("Additional medical notes", value=data.get("notes", ""))

        colA, colB = st.columns(2)
        with colA:
            st.button("← Back", on_click=prev_step, key="back5")
        with colB:
            st.button("Next →", on_click=next_step, disabled=not adults_ok, key="next5")

        st.markdown("</div>", unsafe_allow_html=True)

    # STEP 6 – Review & Submit
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

        st.write(f"**Client Name:** {data.first_name} {data.last_name}")
        st.write(f"**Date of Birth:** {data.dob.strftime('%Y-%m-%d') if data.dob else ''}")
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
        st.write(f"**Mobility Level:** {data.get('mobility_label', '')}")
        st.write(f"**Adult Present During Care:** {data.adult_present}")
        if data.adult_present == "Yes":
            st.write(f"**Adult #1:** {data.adult1} ({data.rel1})")
            if data.adult2.strip():
                rel2 = f" ({data.rel2})" if data.rel2 else ""
                st.write(f"**Adult #2:** {data.adult2}{rel2}")
        st.write(f"**Additional Notes:** {data.get('notes', '')}")

        if not FPDF_AVAILABLE:
            st.error("FPDF is not installed. Please run 'pip install fpdf2' to enable PDF generation.")
        if data.uploaded_pdf_bytes is None:
            st.warning("No client PDF uploaded. Final document will include only the assessment summary.")

        colA, colB, colC = st.columns([1, 1, 2])
        with colA:
            st.button("← Back", on_click=prev_step, key="back6")
        with colB:
            if st.button("Start Over", on_click=reset_flow, key="reset6"):
                pass
        with colC:
            submit_disabled = not FPDF_AVAILABLE
            if st.button("Submit & Generate PDF", disabled=submit_disabled, key="submit_final"):
                try:
                    final_path, msg = build_final_pdf(data, score, level)
                    st.success("Assessment submitted and PDF generated.")
                    st.info(msg)
                except Exception as e:
                    st.error(f"Something went wrong while generating the PDF: {e}")

        st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------
# RUN APP
# ---------------------------------------------------

run_home_care_risk_assessment()
