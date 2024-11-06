import streamlit as st
from dotenv import load_dotenv
import requests
import os
import base64

load_dotenv(dotenv_path='../../.env')

BASE_URL = os.getenv('BASE_URL')

def explanation_of_test_interview():
    st.markdown(
        """
        <style>
        /* Style the back button */
        div.back-button > button {
            background-color: #f0f0f0;
            color: #333333;
            border: none;
            font-size: 18px;
            cursor: pointer;
            padding: 10px 20px;
            border-radius: 5px;
            margin-bottom: 20px;
            width: auto;
        }
        div.back-button > button:hover {
            background-color: #e0e0e0;
        }

        /* Center and style the title */
        .test-title {
            text-align: center;
            color: #333333;
            font-size: 32px;
            margin-top: 30px;
            margin-bottom: 20px;
        }

        /* Style the explanation card */
        .explanation-card {
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            line-height: 1.6;
            font-size: 16px;
            color: #333333;
        }

        /* Style the file uploader */
        .file-uploader {
            margin-bottom: 20px;
        }

        /* Style the action buttons */
        div.action-buttons > button {
            background-color: #4CAF50;
            color: white;
            padding: 15px 30px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px;
            width: auto;
        }
        div.action-buttons > button:hover {
            background-color: #45a049;
        }

        /* Center elements */
        .centered {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    if st.button("← Back", key="back"):
        st.session_state['page'] = 'choose_wtc'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="test-title">Interview Test Preparation</div>',
                unsafe_allow_html=True)

    response = requests.post(
        url=f"{BASE_URL}/explanations",
        json={
            'type': 'interview'
        }
    )

    if response.status_code == 200:
        data = response.json()
        text_of_explanation = data['explanation']
        text_of_explanation = text_of_explanation.replace('\n', '<br>')

        st.markdown(f'''
            <div class="explanation-card">
                {text_of_explanation}
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.error(
            'There was a problem retrieving the test explanation. Please try again later.')
        return

    st.markdown('<div class="file-uploader centered">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        'Please upload your CV in PDF format to continue:', type="pdf")
    st.markdown('</div>', unsafe_allow_html=True)

    upload_status = st.session_state.get('cv_uploaded', False)

    if uploaded_file is not None and not upload_status:
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
            st.success("CV uploaded successfully!")
            st.session_state['cv_uploaded'] = True
        else:
            st.error('There was a problem uploading your CV. Please try again.')
            return

    st.markdown('<div class="action-buttons centered">',
                unsafe_allow_html=True)
    if st.button("📝 Start the Test", key="do_test"):
        if uploaded_file is not None or st.session_state.get('cv_uploaded', False):
            st.session_state['page'] = 'interview_2'
            st.rerun()
        else:
            st.error("Please upload your CV before starting the test.")
    st.markdown('</div>', unsafe_allow_html=True)
