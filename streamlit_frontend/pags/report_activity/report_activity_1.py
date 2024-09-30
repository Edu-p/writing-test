import streamlit as st
import requests
import time
import os
from dotenv import load_dotenv

# os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

BASE_URL = os.getenv('BASE_URL')


def explanation_of_test():
    # get explanation
    response = requests.post(
        # TODO: change when deploy
        url=f'{BASE_URL}/explanations',
        json={
            'type': 'report'
        }
    )
    if response.status_code == 200:
        data = response.json()
        # display the main button
        text_of_explanation = data['explanation']
        st.text_area("", text_of_explanation, height=150)
    else:
        st.error("Problem in request.")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("Do the test"):
            st.session_state['page'] = 'report_activity_2'
            st.rerun()
    with col5:
        if st.button("Back"):
            st.session_state['page'] = 'choose_wtc'
            st.rerun()
