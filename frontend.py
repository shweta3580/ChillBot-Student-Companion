import streamlit as st
import requests

st.title("💬 Sukh-Dukh ka Sathi")

menu = ["Home", "Conversation History", "About"]
choice = st.sidebar.selectbox("Menu", menu)

backend_url = "http://127.0.0.1:5000"

if choice == "Home":
    st.write("Welcome to the Chatbot. Type a message below and press enter to start chatting.")

    user_input = st.text_input("You:")
    if st.button("Send"):
        if user_input:
            response = requests.post(f"{backend_url}/chat", json={"message": user_input})
            if response.status_code == 200:
                data = response.json()
                st.text_area("Chatbot:", value=data["chatbot_response"], height=100)
            else:
                st.error("Error communicating with chatbot.")

elif choice == "Conversation History":
    st.header("📜 Conversation History")
    history_response = requests.get(f"{backend_url}/history")

    if history_response.status_code == 200:
        history = history_response.json()
        with st.expander("Click to see Conversation History"):
            for chat in history:
                st.text(f"👤 User: {chat['user']}")
                st.text(f"🤖 Chatbot: {chat['bot']}")
                st.text(f"🕒 Time: {chat['time']}")
                st.markdown("---")
    else:
        st.error("Error fetching history.")

elif choice == "About":
    st.header("📖 About")
    st.write("""
        ## About the Chatbot
        This chatbot is designed to assist, guide, and support you in your learning journey. 🤖💡
    """)


