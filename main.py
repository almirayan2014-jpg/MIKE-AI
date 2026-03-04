import streamlit as st
import google.generativeai as genai

# অ্যাপের টাইটেল
st.set_page_config(page_title="Mike AI", page_icon="🤖")
st.title("🤖 Mike AI")

# সিক্রেটস থেকে এপিআই কি নেওয়া
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("দয়া করে Streamlit Settings > Secrets-এ GOOGLE_API_KEY যোগ করো!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# চ্যাট মেমোরি সেটআপ
if "messages" not in st.session_state:
    st.session_state.messages = []

# পুরনো মেসেজগুলো দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ইউজারের ইনপুট এবং মাইকের উত্তর
if prompt := st.chat_input("Hi Mike!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # এই মডেলটি সব ভার্সনে কাজ করে
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
        
