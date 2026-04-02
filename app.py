import streamlit as st
from PyPDF2 import PdfReader
import re
import spacy
import subprocess

st.title("CV Analyzer")

cv_text = ""

# تحميل موديل spaCy تلقائيًا لو مش موجود
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# رفع ملف PDF
file_upload = st.file_uploader("Upload CV", type=["pdf"])

if file_upload is not None:
    file_upload.seek(0)
    reader = PdfReader(file_upload)

    # استخراج النص
    for page in reader.pages:
        text = page.extract_text()
        if text:
            cv_text += text + "\n"

    st.subheader("Full Text from CV")
    st.text(cv_text)

    # استخراج الاسم
    name = cv_text.split("\n")[0] if cv_text else "غير موجود"
    st.subheader("Name")
    st.text(name)

    # استخراج الإيميل
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', cv_text)
    email = email_match.group(0) if email_match else "غير موجود"
    st.subheader("Email")
    st.text(email)

    # استخراج رقم الهاتف
    phone_match = re.search(r'(\+?\d{1,3}[\s-]?)?\d{10}', cv_text)
    phone = phone_match.group(0) if phone_match else "غير موجود"
    st.subheader("Phone")
    st.text(phone)

    # استخراج المدينة من أول 5 أسطر
    lines = cv_text.split("\n")
    city_found = "غير موجود"
    for line in lines[:5]:
        doc = nlp(line)
        for ent in doc.ents:
            if ent.label_ == "GPE":
                city_found = ent.text
                break
        if city_found != "غير موجود":
            break

    st.subheader("City")
    st.text(city_found)

    # البحث عن مهارات
    search = st.text_input("Search by skill")
    if search:
        if search.lower() in cv_text.lower():
            st.success("Matched Candidate ✅")
        else:
            st.error("Not Matched Candidate ❌")