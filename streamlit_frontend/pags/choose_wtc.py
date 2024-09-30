import streamlit as st


def choose_what_type_of_chat():
    if st.button("Back"):
        st.session_state['page'] = 'choose_wtd'
        st.rerun()

    st.title("")
    st.subheader("")


    with st.container():
        st.title("Choose what type of situation you want to be tested")
        st.subheader("")
        st.markdown('<div class="centered-buttons">', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Report activity situation"):
                st.session_state['page'] = 'report_activity_1'
                st.rerun()
        with col3:
            if st.button("Interview situation"):
                st.session_state['page'] = 'interview_1'
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
