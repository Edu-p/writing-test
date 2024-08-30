import streamlit as st
import requests 
import time

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
        url='https://writing-test-1c8k.onrender.com/return_all_tests',
        json={
            "user_id": user_id
        }
    ) 
    if response.status_code == 200:
        data = response.json()
        attempts = data
        attempts = list(attempts)
        total_attempts = len(attempts)

        for index, attempt in enumerate(reversed(attempts), start=1):
            original_index = total_attempts - index + 1
            st.text(f"Attempt number: {original_index}")
            st.text(f"CEPR: {attempt}")
            st.text("-----")

    else:
        st.error("Problem in request.")