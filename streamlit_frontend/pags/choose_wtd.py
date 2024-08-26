import streamlit as st

def choose_what_to_do():
    st.markdown(
        """
        <style>
        .stButton button {
            width: 100%; 
            height: 100px; 
            font-size: 30px; 
            margin: 10px;
        }
        .centered-container {
            display: flex;
            justify-content: center; 
            align-items: center; 
            height: 70vh; 
            flex-wrap: wrap; 
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    
    with st.container():
        st.title("What do you want to do?")
        st.subheader("")
        st.markdown('<div class="centered-buttons">', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("Do a new test"):
                st.session_state['page'] = 'choose_wtc'

                st.rerun()
        
        with col4:
            if st.button("View your metrics"):
                st.session_state['page'] = 'view_overall'

                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
