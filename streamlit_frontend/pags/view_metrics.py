import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL')


def view_overall_metrics():
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
        .metrics-title {
            text-align: center;
            color: #333333;
            font-size: 32px;
            margin-top: 30px;
            margin-bottom: 40px;
        }

        /* Style the metric cards */
        .metric-card {
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
        }

        .metric-card h3 {
            font-size: 24px;
            color: #333333;
            margin-bottom: 10px;
        }

        .metric-card .value {
            font-size: 40px;
            font-weight: bold;
            color: #4CAF50;
        }

        .metric-card .description {
            font-size: 16px;
            color: #666666;
            margin-top: 10px;
        }

        /* Style the progress bar */
        .progress-bar {
            width: 100%;
            background-color: #ddd;
            border-radius: 13px;
            overflow: hidden;
            margin-top: 15px;
        }

        .progress-bar-inner {
            height: 20px;
            border-radius: 13px;
            background-color: #4CAF50;
            width: 0%;
            transition: width 0.5s ease-in-out;
        }

        /* Style the action buttons */
        div.action-buttons div.stButton > button {
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
            width: 100%;
            font-size: 20px;
            font-weight: bold;
            color: #333333;
            margin-top: 20px;
        }
        div.action-buttons div.stButton > button:hover {
            background-color: #e6e6e6;
            transform: scale(1.02);
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

    response_get_max_metric = requests.post(
        url=f'{BASE_URL}/max_english_level',
        json={
            'user_id': user_id,
        }
    )

    response_get_mean_ar = requests.post(
        url=f'{BASE_URL}/evals',
        json={
            'user_id': user_id
        }
    )

    st.markdown('<div class="metrics-title">Your Metrics</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        max_level_html = '<div class="metric-card">'
        max_level_html += '<h3>🏆 Your Max Level Achieved</h3>'
        if response_get_max_metric.status_code == 200:
            data = response_get_max_metric.json()
            max_CEFR = data['max_CEFR']
            max_level_html += f"<div class='value'>{max_CEFR}</div>"
        else:
            max_level_html += "<div class='value'>N/A</div>"
            max_level_html += "<div class='description'>Complete a test to see your max level.</div>"
        max_level_html += '</div>'
        st.markdown(max_level_html, unsafe_allow_html=True)

    with col2:
        mean_ar_html = '<div class="metric-card">'
        mean_ar_html += '<h3>🤖 LLMs Response Quality</h3>'
        if response_get_mean_ar.status_code == 200:
            data = response_get_mean_ar.json()
            mean_ar = data['mean_ar']
            mean_ar_percentage = int(100 * mean_ar)
            mean_ar_html += f"<div class='value'>{mean_ar_percentage}%</div>"
            mean_ar_html += '''
            <div class="progress-bar">
                <div class="progress-bar-inner" style="width: {width}%;"></div>
            </div>
            '''.format(width=mean_ar_percentage)
            mean_ar_html += "<div class='description'>This represents the quality of the AI's responses during your tests.</div>"
        else:
            mean_ar_html += "<div class='value'>N/A</div>"
            mean_ar_html += "<div class='description'>Complete a test to see the LLM's response quality.</div>"
        mean_ar_html += '</div>'
        st.markdown(mean_ar_html, unsafe_allow_html=True)

    st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
    if st.button("📄 View Past Tests", key="past_tests"):
        st.session_state['page'] = 'past_tests'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
