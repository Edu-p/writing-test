import streamlit as st
from pags.auth import show_auth_form
from pags.choose_wtd import choose_what_to_do
from pags.choose_wtc import choose_what_type_of_chat
from pags.report_activity.report_activity_1 import explanation_of_test
from pags.report_activity.report_activity_2 import report_test
from pags.report_activity.report_activity_3 import show_conversation_summary

from pags.view_metrics import view_overall_metrics
from pags.past_tests import show_import_tests

st.set_page_config(page_title="Writing Test Platform", layout="centered", initial_sidebar_state="collapsed")

if 'page' not in st.session_state:
    st.session_state['page'] = 'auth'
    st.session_state['user_id'] = ''

if st.session_state['page'] == 'auth':
    show_auth_form()
elif st.session_state['page'] == 'choose_wtd':
    choose_what_to_do()

# flux another test
elif st.session_state['page'] == 'choose_wtc':
    choose_what_type_of_chat()
elif st.session_state['page'] == 'report_activity_1':
    explanation_of_test()
elif st.session_state['page'] == 'report_activity_2':
    report_test()
elif st.session_state['page'] == 'report_activity_3':
    show_conversation_summary()

# flux see metrics
elif st.session_state['page'] == 'view_overall':
    view_overall_metrics()
elif st.session_state['page'] == 'past_tests':
    show_import_tests()

