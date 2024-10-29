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
        /* Include Google Fonts */
        @import url('https://fonts.googleapis.com/css?family=Roboto&display=swap');

        body {
            font-family: 'Roboto', sans-serif;
            background-color: #F0F2F6;
        }

        /* Center and style the title */
        .summary-title {
            text-align: center;
            color: #333333;
            font-size: 36px;
            font-weight: bold;
            margin-top: 30px;
            margin-bottom: 20px;
        }

        /* Style the result card */
        .result-card {
            background-color: #FFFFFF;
            border: 1px solid #DDDDDD;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            line-height: 1.8;
            font-size: 18px;
            color: #333333;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        /* Style for the main CEFR Level */
        .result-card h1.cefr-level {
            font-size: 48px;
            margin-bottom: 20px;
            color: #4CAF50;
        }

        /* Style for the sub-levels */
        .result-card h3.sub-level {
            font-size: 20px;
            margin-bottom: 10px;
            color: #333333;
        }

        .result-card p {
            font-size: 16px;
            color: #555555;
        }

        div.action-button > button {
            background-color: #4CAF50;
            color: white;
            padding: 15px 30px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 20px auto;
            display: block;
        }
        div.action-button > button:hover {
            background-color: #45a049;
        }

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
        cefr_gs = data.get('CEFR_GS', 'N/A')
        cefr_vw = data.get('CEFR_VW', 'N/A')
        cefr_cc = data.get('CEFR_CC', 'N/A')
        cefr_ce = data.get('CEFR_CE', 'N/A')

        explanation = explanation.replace('\n', '<br>')

        st.markdown(f'''
            <div class="result-card">
                <h1 class="cefr-level">Your CEFR Level: <span>{cefr_level}</span></h1>
                <h3 class="sub-level">Grammar and Syntax: <span>{cefr_gs}</span></h3>
                <h3 class="sub-level">Vocabulary and Word Choice: <span>{cefr_vw}</span></h3>
                <h3 class="sub-level">Coherence and Cohesion: <span>{cefr_cc}</span></h3>
                <h3 class="sub-level">Clarity of Expressions: <span>{cefr_ce}</span></h3>
                <p><strong>Explanation:</strong><br>{explanation}</p>
            </div>
        ''', unsafe_allow_html=True)

        st.session_state['thread_id'] = None
        st.session_state['step_of_conversation'] = 0
        st.session_state['conversation'] = []

        st.markdown('<div class="action-button centered">',
                    unsafe_allow_html=True)

        if st.button("🏠 Back to Main Menu", key="back_to_main"):
            st.session_state['page'] = 'choose_wtd'
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.error(
            "There was a problem retrieving your test results. Please try again later.")
