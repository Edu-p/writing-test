import streamlit as st
import requests

def view_overall_metrics():
    st.title('')

    user_id = st.session_state['user_id']

    response_get_max_metric = requests.post(
            # TODO: change when deploy
            url='https://writing-test-1c8k.onrender.com/max_english_level',
            json={
                'user_id': user_id,
            }   
    )
    if response_get_max_metric.status_code == 200:
        data = response_get_max_metric.json()

        max_cepr = data['max_cepr']

        st.markdown(f"<h2 style='font-size:30px;'>Max level: {max_cepr}</h2>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h2 style='font-size:30px;'>To compute max level you need to do a test</h2>", unsafe_allow_html=True)

    st.write("")    
    if st.button("Back"):
        st.session_state['page'] = 'choose_wtd'
        st.rerun()
    st.write("")
    st.write("")
    st.write("")

    st.markdown("""
        <style>
        div.stButton > button {
            width: 100%; 
            height: 100px; 
            font-size: 70px; 
            margin: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("Past tests"):
        st.session_state['page'] = 'past_tests'
        st.rerun()
