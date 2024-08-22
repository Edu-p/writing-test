import streamlit as st
import requests

def report_test():
    if 'conversation' not in st.session_state:
        st.session_state['conversation'] = []

    # if 'user_id' not in st.session_state:
    #     st.session_state['user_id'] = ''
    
    # if 'entered_report_test' not in st.session_state:
    #     st.session_state['entered_report_test'] = False

    # if not st.session_state['entered_report_test']:
    #     response_to_thread_id = requests.post(
    #         url='http://localhost:5000/get_conversation',
    #         json={
    #             'user_id': st.session_state['user_id'],
    #             'type_of_test': 'report'
    #         }
    #     )
        
    #     data = response_to_thread_id.json()
    #     thread_id = data['thread_id']
    #     print(f"\n\n\n thread_id:{thread_id} \n\n")

    #     st.session_state['entered_report_test'] = True

    
    # data = response_to_thread_id.json()
    # thread_id = data['thread_id']

    # print(f"\n\n\n thread_id:{thread_id} \n\n")

    st.title('Conversation')

    conversation_display = "\n".join(st.session_state['conversation'])
    st.text_area("", conversation_display, height=300, disabled=True)

    user_input = st.text_input("Your message:")

    if st.button("Send"):
        if user_input:
            st.session_state.conversation.append(f"You: {user_input}")

            # requests = requests.post(
            #     url=
            # )

            response = f"Bot: This is a response to '{user_input}'"
            st.session_state['conversation'].append(response)

            st.rerun()

report_test()