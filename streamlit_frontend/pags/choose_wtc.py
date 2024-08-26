import streamlit as st

def choose_what_type_of_chat():
    print('pass wtc')

    if st.button("Previous"):
        st.session_state['page'] = 'choose_wtd'
        st.rerun()
        
    st.title("")
    st.subheader("")

    st.markdown(
        """
        <style>
        .stButton button {
            width: 100%; 
            height: 100px; 
            font-size: 30px; 
            margin: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    
    with st.container():
        st.title("Choose what type of situation you want to be tested")
        st.subheader("")
        st.markdown('<div class="centered-buttons">', unsafe_allow_html=True)

        if st.button("Report activity situation"):
            st.session_state['page'] = 'report_activity_1'

            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
