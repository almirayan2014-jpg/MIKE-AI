import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mike AI", page_icon="🤖")
st.title("🤖 Mike AI")

if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Secrets-এ API Key নেই!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Hi Mike!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # চেষ্টা ১: লেটেস্ট মডেল
            model = genai.GenerativeModel("gemini-pro") 
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
