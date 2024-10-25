import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL')


def show_conversation_summary():
    st.markdown(
        """
        <style>
        /* Center and style the title */
        .summary-title {
            text-align: center;
            color: #333333;
            font-size: 32px;
            margin-top: 30px;
            margin-bottom: 20px;
        }

        /* Style the result card */
        .result-card {
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            line-height: 1.6;
            font-size: 16px;
            color: #333333;
        }

        /* Style the action button */
        div.action-button > button {
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
        div.action-button > button:hover {
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

    st.markdown('<div class="summary-title">Test Summary</div>',
                unsafe_allow_html=True)

    response = requests.post(
        url=f'{BASE_URL}/get_english_level',
        json={
            "user_id": st.session_state['user_id'],
            "thread_id": st.session_state['thread_id']
        }
    )

    if response.status_code == 200:
        data = response.json()
        cefr_level = data.get('CEFR', 'N/A')
        explanation = data.get('COT', 'No explanation available.')

        explanation = explanation.replace('\n', '<br>')

        st.markdown(f'''
            <div class="result-card">
                <h3>Your CEFR Level: <span style="color:#4CAF50;">{cefr_level}</span></h3>
                <p><strong>Explanation:</strong><br>{explanation}</p>
            </div>
        ''', unsafe_allow_html=True)

        st.markdown('<div class="action-button centered">',
                    unsafe_allow_html=True)
        if st.button("🏠 Back to Main Menu", key="back_to_main"):
            st.session_state['thread_id'] = None
            st.session_state['step_of_conversation'] = 0
            st.session_state['conversation'] = []

            st.session_state['page'] = 'choose_wtd'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error(
            "There was a problem retrieving your test results. Please try again later.")
