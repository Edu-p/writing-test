import streamlit as st
import requests 
import time

def show_conversation_summary():
    st.title("")
    st.subheader("")
    # get explanation
    response = requests.post(
        # TODO: change when deploy
        url='http://localhost:5000/get_english_level',
        json={
            "user_id": st.session_state['user_id'],
            "thread_id": st.session_state['thread_id']
        }
    ) 
    if response.status_code == 200:
        data = response.json()
        st.text_area("", f"You have achieved: {data['CEPR']}, you can be considered at {data['level']} level")
        if st.button("Back to main menu"):
            st.session_state['page'] = 'choose_wtd'
            st.rerun()
    else:
        st.error("Problem in request.")