import os
import zipfile
import tempfile
import pymupdf
import pandas as pd
import streamlit as st

from typing import TypedDict, Annotated, Optional, List
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# ---------------- ENV ----------------
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("gemini")

# ---------------- STREAMLIT ----------------
st.set_page_config(page_title="ZIP Resume Analyzer", layout="wide")
st.title("📦 Resume Analyzer & CSV Generator")


st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }

    .stApp {
        background: #0f2027; 
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }

    /* Title Style */
    .main-title {
        font-size: 36px;
        font-weight: 700;
        color: #FFD700;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.6);
        padding-bottom: 10px;
    }

    /* Text area */
    textarea {
        border-radius: 10px !important;
        font-size: 16px !important;
        padding: 12px !important;
    }

    /* Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #ff7e5f, #feb47b);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: 600;
        border: none;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        transition: 0.2s ease;
        opacity: 0.95;
    }

    /* Code Box */
    .stCodeBlock {
        border-radius: 10px !important;
        background: rgba(255,255,255,0.1) !important;
            
    }
    </style>
""", unsafe_allow_html=True)
# ---------------- MODEL ----------------
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.3
)

# ---------------- STRUCTURED SCHEMA ----------------
class DataFormat(TypedDict):
    summary: str
    experience: Optional[int]
    skills: List[str]
    links: Annotated[
        List[str],
        "If any links are found in the resume text, return them as a list of strings"
    ]

structured_model = model.with_structured_output(DataFormat)

# ---------------- PDF READER ----------------
def read_pdf(path: str) -> str:
    doc = pymupdf.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# ---------------- ZIP UPLOAD ----------------
uploaded_zip = st.file_uploader(
    "Upload ZIP file containing PDF resumes",
    type=["zip"]
)

if uploaded_zip:
    if st.button("🚀 Extract & Generate CSV"):

        all_records = []

        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "resumes.zip")

            with open(zip_path, "wb") as f:
                f.write(uploaded_zip.read())

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)

            for file in os.listdir(temp_dir):
                if file.lower().endswith(".pdf"):
                    pdf_path = os.path.join(temp_dir, file)

                    resume_text = read_pdf(pdf_path)
                    response = structured_model.invoke(resume_text)

                    record = dict(response)
                    record["skills"] = ", ".join(record["skills"])
                    record["links"] = ", ".join(record["links"])

                    all_records.append(record)

        # ---------------- DATAFRAME ----------------
        df = pd.DataFrame(all_records)

        st.subheader("📊 Extracted Resume Dataset")
        st.dataframe(df, use_container_width=True)

        # ---------------- CSV ----------------
        csv_data = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇ Download CSV",
            data=csv_data,
            file_name="resume_structured_output.csv",
            mime="text/csv"
        )

        st.success("✅ ZIP processed successfully!")
