from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])  # Fix the method name here
    return response

def input_pdf_setup(uploaded_file):
    # Convert PDF to image
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="ATS Resume EXpert")
st.header("ATS Tracking System")
input_text = st.text_area("JOB Description", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("HOW can I Improvise my Skills")

# submit3=st.button("What are the Keywords That are Missing")

submit3 = st.button("Percentage match")

input_promt1 = """
You are the experienced HR with Tech Experience in the field of Data Science, Full stack, Web Development, big data Engineering, DevOps, Data analyst. Your task is to review the provided resume against the job description for these profiles. Please share your professional evaluation on whether the candidate's profile aligns with Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_promt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science, Full stack, Web Development, big data Engineering, DevOps, Data analyst, and deep ATS functionality. Your task is to evaluate the resume against the provided job description. First, the output should come as a percentage and then keywords missing and final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_promt1)  # Fix the variable name here
        st.subheader("The Response is ")
        st.write(response)
    else:
        st.write("please Upload the Resume")
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_promt3)  # Fix the variable name here
        st.subheader("The Response is ")
        st.write(response)
    else:
        st.write("please Upload the Resume")
