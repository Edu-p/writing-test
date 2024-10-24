import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL')


def explanation_of_test():
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

        /* Style the action buttons */
        div.centered > button {
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
        div.centered > button:hover {
            background-color: #45a049;
        }

        /* Center elements */
        .centered {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: row;
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
    st.markdown('<div class="test-title">Report Activity Test</div>',
                unsafe_allow_html=True)

    response = requests.post(
        url=f'{BASE_URL}/explanations',
        json={
            'type': 'report'
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
            "There was a problem retrieving the test explanation. Please try again later.")

    st.markdown('<div class="centered">', unsafe_allow_html=True)
    if st.button("📝 Do the Test", key="do_test"):
        st.session_state['page'] = 'report_activity_2'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
