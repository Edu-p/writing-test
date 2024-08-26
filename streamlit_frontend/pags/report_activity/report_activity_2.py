import streamlit as st
import requests
import time 

def report_test():
    st.title("Chatbot Conversation")

    # verifications in session state
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = '' 
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    if 'thread_id' not in st.session_state:
        st.session_state['thread_id'] = None
    if 'step_of_conversation' not in st.session_state:
        st.session_state['step_of_conversation'] = 0

    # get thread_id to start conversation
    user_id = st.session_state['user_id']
    thread_id = st.session_state['thread_id']

    if thread_id:
        print('Thread ID exists:', thread_id)
    else:
        response_to_thread_id = requests.post(
            # TODO: change when deploy
            url='http://localhost:5000/get_conversation',
            json={
                'user_id': user_id,
                'type_of_test': 'report'   
            }   
        )
        
        data = response_to_thread_id.json()
        st.session_state['thread_id'] = data['thread_id']
        thread_id = st.session_state['thread_id']

        # print(f"\n\n\n thread_id:{thread_id} -- {type(thread_id)} \n\n")


    conversation_display = "\n".join(st.session_state.conversation)
    st.text_area("Conversation", conversation_display, height=300, disabled=True)

    user_input = st.text_input("Your message:")

    if st.button("Send"):
        if user_input:
            st.session_state['step_of_conversation'] += 1
            if st.session_state['step_of_conversation'] <= 3:
                st.session_state.conversation.append(f"You: {user_input}")
                response_to_input = requests.post(
                    # TODO: change when deploy
                    url='http://localhost:5000/chat',
                    json={
                        'user_id': user_id,
                        'thread_id': thread_id,
                        'content': user_input   
                    }   
                )

                data = response_to_input.json()
                llm_response = data['response'] 

                response = (f"Bot: {llm_response}\n{st.session_state['step_of_conversation']} exchange\n")
                print(f"Bot: {llm_response}', thread_id -> {thread_id}")

                st.session_state.conversation.append(response)

                st.rerun()
            else:
                st.session_state.conversation.append(f"You: {user_input}")
                response_to_input = requests.post(
                    # TODO: change when deploy
                    url='http://localhost:5000/chat',
                    json={
                        'user_id': user_id,
                        'thread_id': thread_id,
                        'content': user_input   
                    }   
                )

                data = response_to_input.json()
                llm_response = data['response'] 

                response = (f"Bot: {llm_response}\n{st.session_state['step_of_conversation']} exchange\n")
                print(f"Bot: {llm_response}', thread_id -> {thread_id}")

                st.session_state.conversation.append(response)
                time.sleep(2)

                st.session_state['page'] = 'report_activity_3'

                st.rerun()
