import streamlit as st
import requests
import time
import os
from dotenv import load_dotenv

# os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

BASE_URL = os.getenv('BASE_URL')


def show_import_tests():
    st.title("")
    st.subheader("")
    # get explanation

    user_id = st.session_state['user_id']

    if st.button("Back"):
        st.session_state['page'] = 'choose_wtd'
        st.rerun()

    response = requests.post(
        # TODO: change when deploy
        url=f'{BASE_URL}/return_all_tests',
        json={
            "user_id": user_id
        }
    )

    if response.status_code == 200:
        data = response.json()
        attempts = list(zip(data['cot'], data['grades']))
        total_attempts = len(attempts)

        for index, attempt in enumerate(reversed(attempts), start=1):
            original_index = total_attempts - index + 1
            st.text(f"Attempt number: {original_index}")
            st.text(f"CEPR: {attempt[1]}")
            st.text(f"Explanation: {attempt[0]}")
            st.text("-----")

    else:
        st.error("Problem in request.")
