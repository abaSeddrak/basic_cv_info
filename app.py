import streamlit as st
from PyPDF2 import PdfReader
import re
import spacy

# Title for the project 
st.title("Uploading CV")

cv_text = ""

nlp = spacy.load("en_core_web_sm")  # دلوقتي هيشتغل لأن الموديل مثبت من requirements

# Upload the PDF
file_upload = st.file_uploader("Upload CV", type=["pdf"])

if file_upload is not None:
    file_upload.seek(0)
    reader = PdfReader(file_upload)

    cv_text = ""
    for page in reader.pages:
        cv_text += page.extract_text()

    st.subheader("Full CV Text")
    st.text(cv_text)

    # Extract basic info
    name = cv_text.split("\n")[0]
    st.subheader("Name")
    st.text(name)

    email_match = re.search(r'[\w\.-]+@[\w\.-]+', cv_text)
    email = email_match.group(0) if email_match else "غير موجود"
    st.subheader("Email")
    st.text(email)

    phone_match = re.search(r'(\+?\d{1,3}[\s-]?)?\d{10}', cv_text)
    phone = phone_match.group(0) if phone_match else "غير موجود"
    st.subheader("Phone")
    st.text(phone)

    # Extract city
    lines = cv_text.split("\n")
    top_lines = lines[:5]

    for line in top_lines:
        if any(word in line.lower() for word in ["university", "faculty", "company"]):
            continue
        doc = nlp(line)
        for ent in doc.ents:
            if ent.label_ == "GPE":
                st.subheader("City")
                st.text(ent.text)
                break