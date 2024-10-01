import streamlit as st
import requests
import time
import os
from dotenv import load_dotenv

# os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

BASE_URL = os.getenv('BASE_URL')


def show_conversation_summary():
    st.title("")
    st.subheader("")
    # get explanation
    response = requests.post(
        url=f'{BASE_URL}/get_english_level',
        json={
            "user_id": st.session_state['user_id'],
            "thread_id": st.session_state['thread_id']
        }
    )
    if response.status_code == 200:
        data = response.json()
        st.text_area(
            "", f"You have achieved: {data['CEPR']} <COT IN FUTURE>")
        if st.button("Back to main menu"):
            st.session_state['thread_id'] = None
            st.session_state['step_of_conversation'] = 0
            st.session_state.conversation = []

            st.session_state['page'] = 'choose_wtd'
            st.rerun()
    else:
        st.error("Problem in request.")
