import streamlit as st

st.title("AI Chatbot with Avatar")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.markdown(f"**{message['role'].capitalize()}:** {message['content']}")

user_input = st.text_input("Type your message:")

if st.button("Send") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Call your backend here to get the chatbot response and video