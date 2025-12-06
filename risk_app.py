# ================================
# HOME CARE RISK ASSESSMENT APP
# FULL STABLE RELEASE — PDF SAFE
# ================================

import streamlit as st
from pathlib import Path
from datetime import datetime

# -------------------------------
# OPTIONAL DEPENDENCIES
# -------------------------------

try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except:
    FPDF_AVAILABLE = False

try:
    from PyPDF2 import PdfReader, PdfWriter
    PYPDF2_AVAILABLE = True
except:
    PYPDF2_AVAILABLE = False


# -------------------------------
# SAVE LOCATION (PRACTICE ONLY)
# -------------------------------

BASE_SAVE_PATH = Path(
    r"C:\Users\zach_\OneDrive\Documents\Personal Risk Assessment Project\Practice Assessments"
)

BASE_SAVE_PATH.mkdir(parents=True, exist_ok=True)


# -------------------------------
# TEXT SAFETY FOR PDF
# -------------------------------

def wrap_pdf_text(txt: str) -> str:
    """
    Converts problem unicode to safe ASCII so
    FPDF never crashes.
    """
    replacements = {
        "–": "-",
        "—": "-",
        "’": "'",
        "“": '"',
        "”": '"',
        "•": "-",
        "\u00A0": " "
    }

    for k, v in replacements.items():
        txt = txt.replace(k, v)

    return txt.encode("latin-1", errors="ignore").decode("latin-1")


# -------------------------------
# SAVE UPLOADED PDF
# -------------------------------

def save_uploaded_file(file_bytes, original_name):
    t = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    p = Path(original_name)
    name = f"{p.stem}_{t}{p.suffix}"
    out = BASE_SAVE_PATH / name

    with open(out, "wb") as f:
        f.write(file_bytes)

    return out


# -------------------------------
# AI SUMMARY BUILDER
# -------------------------------

def build_ai_style_summary(data, score, level):

    s = []

    s.append(f"Overall risk assigned as {level.lower()} "
             f"with score of {score:.1f}.")

    age = int(data.get("age", 0) or 0)

    if age >= 80:
        s.append("Advanced age increases fall and complication risk.")
    elif age >= 65:
        s.append("Older adult status contributes to moderate baseline risk.")

    if data.get("seizures") == "Yes":
        s.append(f"History of seizures ({data.get('seizure_type','')}).")

    if data.get("medications") == "Yes":
        s.append("Medication use adds complexity of care and monitoring burden.")

    s.append(f"Mobility documented as: {data.get('mobility_label','')}.")

    if data.get("adult_present") == "Yes":
        s.append("Adult supervision present.")
    else:
        s.append("No adult supervision available during care.")

    if data.get("notes"):
        s.append("Additional provider notes reviewed.")

    s.append("This summary supports care planning but does not replace "
             "professional judgment.")

    return wrap_pdf_text("\n\n".join(s))


# -------------------------------
# SAFE PDF GENERATOR
# -------------------------------

def generate_summary_pdf(data, score, level, fullname, dob):

    if not FPDF_AVAILABLE:
        raise RuntimeError("FPDF missing. Run pip install fpdf2.")

    pdf = FPDF()
    pdf.set_auto_page_break(True, margin=12)
    pdf.set_margins(12, 12, 12)
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    def block(title, value):
        pdf.set_font("Arial", "B", 11)
        pdf.multi_cell(0, 6, wrap_pdf_text(str(title)))
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 6, wrap_pdf_text(str(value)))
        pdf.ln(2)

    pdf.set_font("Arial", "B", 16)
    pdf.multi_cell(0, 10, "Home Care Risk Assessment Summary")
    pdf.ln(3)

    block("Client:", fullname)
    block("DOB:", dob)
    block("Client ID:", data.get("client_id", ""))
    block("Risk Level:", level)
    block("Risk Score:", f"{score:.1f}")

    block("Age:", data.get("age",""))
    block("Height:",
          f"{data.get('height_feet','')} ft {data.get('height_inches','')} in")
    block("Weight:", data.get("weight",""))

    block("History of Seizures:", data.get("seizures",""))
    if data.get("seizures")=="Yes":
        block("Seizure Type:", data.get("seizure_type",""))

    block("Medications:", data.get("medications",""))

    meds = data.get("med_list", [])
    if meds:
        med_txt = []
        for i,m in enumerate(meds,1):
            med_txt.append(
                f"{i}. {m['name']} - {m['dosage']} - {m['frequency']}"
            )
        block("Medication List:", "\n".join(med_txt))

    block("Mobility:", data.get("mobility_label",""))
    block("Adult Present:", data.get("adult_present",""))

    if data.get("adult_present")=="Yes":
        adults = []
        if data.get("adult1"):
            adults.append(f"{data['adult1']} ({data.get('rel1','')})")
        if data.get("adult2"):
            adults.append(f"{data['adult2']} ({data.get('rel2','')})")
        block("Adults:", "\n".join(adults))

    if data.get("notes"):
        block("Notes:", data["notes"])

    pdf.set_font("Arial","B",14)
    pdf.multi_cell(0,8,"AI Summary")
    pdf.ln(2)
    pdf.set_font("Arial",11)
    pdf.multi_cell(0,6, build_ai_style_summary(data, score, level))

    t = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fname = fullname.replace("/", "_")
    out = BASE_SAVE_PATH / f"{fname}_summary_{t}.pdf"

    pdf.output(str(out))
    return out


# -------------------------------
# MERGE PDF
# -------------------------------

def merge_pdfs(uploaded, summary_pdf, final_path):

    if not PYPDF2_AVAILABLE:
        return summary_pdf

    writer = PdfWriter()

    if uploaded:
        r1 = PdfReader(str(uploaded))
        for p in r1.pages:
            writer.add_page(p)

    r2 = PdfReader(str(summary_pdf))
    for p in r2.pages:
        writer.add_page(p)

    with open(final_path, "wb") as f:
        writer.write(f)

    return final_path


# -------------------------------
# FINAL PDF WORKFLOW
# -------------------------------

def build_final_pdf(data, score, level):

    first = data["first_name"]
    last = data["last_name"]
    dob = data["dob"].strftime("%Y-%m-%d")

    full = f"{first} {last}"

    final_name = BASE_SAVE_PATH / f"{last}, {first} - {dob}.pdf"

    original = None

    if data.get("uploaded_pdf_bytes"):
        original = save_uploaded_file(
            data.uploaded_pdf_bytes,
            data.uploaded_pdf_name
        )

    summary = generate_summary_pdf(data, score, level, full, dob)

    if original and PYPDF2_AVAILABLE:
        merge_pdfs(original, summary, final_name)
        return final_name

    summary.replace(final_name)
    return final_name


# -------------------------------
# STREAMLIT CONFIG
# -------------------------------

st.set_page_config("Home Care Risk Assessment","centered")


# -------------------------------
# SESSION STATE
# -------------------------------

for k in ["step", "med_list", "uploaded_pdf_bytes", "uploaded_pdf_name"]:
    if k not in st.session_state:
        st.session_state[k] = [] if k=="med_list" else None

if st.session_state.step is None:
    st.session_state.step=1

data = st.session_state


# -------------------------------
# STEPS
# -------------------------------

TOTAL=6
STEP_NAMES = {
    1:"Client Info",
    2:"Demographics",
    3:"Seizures",
    4:"Medications",
    5:"Mobility",
    6:"Review"
}

def next_step(): data.step+=1
def prev_step(): data.step-=1

def reset():
    st.session_state.clear()
    st.session_state.step=1
    st.session_state.med_list=[]


# -------------------------------
# UI LOOP
# -------------------------------

st.title("🏡 Home Care Risk Assessment")
st.caption(f"Step {data.step} of {TOTAL} — {STEP_NAMES[data.step]}")
st.progress(data.step/TOTAL)

# ------------- STEP 1 -------------

if data.step==1:

    data.first_name = st.text_input("First Name")
    data.last_name  = st.text_input("Last Name")
    data.dob = st.date_input("DOB", datetime(2000,1,1))
    data.client_id  = st.text_input("Client ID (optional)")

    f = st.file_uploader("Upload Intake PDF", type="pdf")
    if f:
        data.uploaded_pdf_bytes = f.getvalue()
        data.uploaded_pdf_name=f.name

    if st.button("Next", disabled=not(data.first_name and data.last_name)):
        next_step()

# ------------- STEP 2 -------------

elif data.step==2:

    data.age = st.text_input("Age")
    data.weight = st.text_input("Weight (lbs)")
    data.height_feet = st.text_input("Height (feet)")
    data.height_inches = st.text_input("Height (inches 0–11)")

    if st.button("Back"): prev_step()
    if st.button("Next"): next_step()

# ------------- STEP 3 -------------

elif data.step==3:

    data.seizures = st.radio("History of seizures", ["No","Yes"], horizontal=True)
    if data.seizures=="Yes":
        data.seizure_type = st.selectbox(
            "Seizure Type",
            ["Tonic-clonic","Atonic","Tonic only","Myoclonic","Focal","Absence"]
        )

    if st.button("Back"): prev_step()
    if st.button("Next"): next_step()

# ------------- STEP 4 -------------

elif data.step==4:

    data.medications = st.radio("Medication use",["No","Yes"], horizontal=True)

    if data.medications=="Yes":
        n=st.text_input("Medication")
        d=st.text_input("Dosage")
        f=st.text_input("Frequency")

        if st.button("Add drug") and n and d and f:
            data.med_list.append({"name":n,"dosage":d,"frequency":f})

        for m in data.med_list:
            st.write(f"• {m['name']} — {m['dosage']} — {m['frequency']}")

    if st.button("Back"): prev_step()
    if st.button("Next"): next_step()

# ------------- STEP 5 -------------

elif data.step==5:

    mob_map={
        "Walks independently":1,
        "Occasional supervision":2,
        "Uses assist device":3,
        "Hands-on assist":4,
        "Non mobile":5
        }

    data.mobility_label = st.selectbox(
        "Mobility",
        mob_map.keys()
    )
    data.mobility = mob_map[data.mobility_label]

    data.adult_present = st.radio("Adult present?",["No","Yes"], horizontal=True)

    if data.adult_present=="Yes":
        data.adult1=st.text_input("Adult 1 name")
        data.rel1=st.text_input("Relationship")

    data.notes=st.text_area("Notes")

    if st.button("Back"): prev_step()
    if st.button("Next"): next_step()

# ------------- STEP 6 -------------

elif data.step==6:

    age=int(data.age)
    weight=float(data.weight)
    height=int(data.height_feet)*12+int(data.height_inches)

    score = age*0.2 + weight*0.05 + height*0.05 + data.mobility*5

    if data.seizures=="Yes": score+=10
    if data.medications=="Yes": score+=10
    if data.adult_present=="Yes": score-=5

    level = "Low Risk" if score<=45 else "Medium Risk" if score<=70 else "High Risk"

    st.metric("Risk Score", round(score,1))
    st.subheader(level)

    if st.button("SUBMIT & GENERATE PDF"):
        final = build_final_pdf(data, score, level)
        st.success("PDF Saved Successfully")
        st.code(str(final))

    if st.button("Back"): prev_step()
    if st.button("Start Over"): reset()
