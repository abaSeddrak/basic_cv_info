import streamlit as st
from PyPDF2 import PdfReader
import re
import spacy
import subprocess

#Title for the project 
st.title("Uploading cv")
cv_text = ""





#upload the pdf
file_upload = st.file_uploader("Upload Cv",type=["pdf"])

#Convert pdf to text 
if file_upload is not None:
    file_upload.seek(0)  
    reader = PdfReader(file_upload)

#Get text from pages 

    for pages_text in reader.pages:
     cv_text += pages_text.extract_text()

    st.title(cv_text)

#Show basic info

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # تحميل الموديل لو مش موجود
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")
    
name = cv_text.split("\n")[0]
st.title("Name")
st.title(name)

email_match = re.search(r'[\w\.-]+@[\w\.-]+', cv_text)
email = email_match.group(0) if email_match else "غير موجود"
st.title("Email")
st.title(email)


# رقم التليفون
phone_match = re.search(r'(\+?\d{1,3}[\s-]?)?\d{10}', cv_text)
phone = phone_match.group(0) if phone_match else "غير موجود"
st.title("Phone")
st.title(phone)



lines = cv_text.split("\n")

top_lines = lines[:5]

for line in top_lines:
    if any(word in line.lower() for word in ["university", "faculty", "company"]):
        continue

    doc = nlp(line)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            print("Most likely city:", ent.text)
            st.title("City")
            st.title(ent.text, ent.label_)
            break

search = st.text_input("Search by skill")

if search:
    if search.lower() in cv_text.lower():
        st.write("Matched Candidate ✅")
    else:
        st.write("Not Matched Candidate ")
