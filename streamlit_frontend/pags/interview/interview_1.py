import streamlit as st
from dotenv import load_dotenv
import requests
import os
import PyPDF2
import base64

# os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

BASE_URL = os.getenv('BASE_URL')


def explanation_of_test_interview():
    response = requests.post(
        url=f"{BASE_URL}/explanations",
        json={
            'type': 'interview'
        }
    )

    if response.status_code == 200:
        data = response.json()
        text_of_explanation = data['explanation']
        st.text_area("", text_of_explanation, height=150)
    else:
        st.error('Problem in request')

    uploaded_file = st.file_uploader('Upload your CV ot continue', type="pdf")

    if uploaded_file is not None:
        pdf_bytes = uploaded_file.read()
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

        response = requests.post(
            url=f"{BASE_URL}/store_cv_db",
            json={
                'user_id': st.session_state['user_id'],
                'pdf_base64': pdf_base64
            }
        )

        if response.status_code == 200:
            st.success("Success")
        else:
            st.error('Problem in request')

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("Do the test"):
            if uploaded_file is not None:
                st.session_state['page'] = 'report_activity_2'
                st.rerun()
            else:
                st.error("Please upload your CV")

    with col5:
        if st.button("Back"):
            st.session_state['page'] = 'choose_wtc'
            st.rerun()
