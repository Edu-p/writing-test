import streamlit as st
from pags.auth import show_auth_form

st.set_page_config(page_title="Writing Test Platform", layout="centered", initial_sidebar_state="collapsed")

st.session_state['page'] = 'auth'

if st.session_state['page'] == 'auth':
    show_auth_form()
elif True:
    pass
