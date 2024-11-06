import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')

BASE_URL = os.getenv('BASE_URL')


def show_import_tests():
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
        .tests-title {
            text-align: center;
            color: #333333;
            font-size: 32px;
            margin-top: 30px;
            margin-bottom: 40px;
        }

        /* Style the attempt cards */
        .attempt-card {
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }

        .attempt-header {
            font-size: 22px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 10px;
        }

        .attempt-detail {
            font-size: 16px;
            color: #555555;
            margin-bottom: 5px;
        }

        /* Style for code blocks */
        pre.attempt-explanation {
            background-color: #f0f0f0;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    if st.button("← Back", key="back"):
        st.session_state['page'] = 'choose_wtd'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    user_id = st.session_state['user_id']

    st.markdown('<div class="tests-title">Your Past Tests</div>',
                unsafe_allow_html=True)

    response = requests.post(
        url=f'{BASE_URL}/return_all_tests',
        json={
            "user_id": user_id
        }
    )

    if response.status_code == 200:
        data = response.json()
        attempts = list(zip(data['cot'], data['grades']))
        total_attempts = len(attempts)

        if not attempts:
            st.info("You have not completed any tests yet.")
            return
        for index, attempt in enumerate(reversed(attempts), start=1):
            original_index = total_attempts - index + 1
            cot = attempt[0]
            grade = attempt[1]

            attempt_html = f"""
            <div class="attempt-card">
                <div class="attempt-header">Attempt #{original_index}</div>
                <div class="attempt-detail"><strong>CEFR Level:</strong> {grade}</div>
                <div class="attempt-detail"><strong>Explanation:</strong></div>
                <pre class="attempt-explanation">{cot}</pre>
            </div>
            """

            st.markdown(attempt_html, unsafe_allow_html=True)

    else:
        st.error(
            "There was a problem retrieving your past tests. Please try again later.")
