import streamlit as st
import requests 
import time

def explanation_of_test():
    # get explanation
    response = requests.post(
        # TODO: change when deploy
        url='http://localhost:5000/explanations',
        json={
            'type': 'report'
        }
    ) 
    if response.status_code == 200:
        data = response.json()
        # display the main button 
        text_of_explanation = data['explanation']
        st.text_area("", text_of_explanation)
    else:
        st.error("Problem in request.")
    
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("Do the test"):
            st.session_state['page'] = 'report_activity_2'
            st.rerun()
    with col5:
        if st.button("Previous page"):
            st.session_state['page'] = 'choose_wtc'
            st.rerun()










