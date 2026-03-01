import streamlit as st
import google.generativeai as genai

# তোমার দেওয়া API Key
GOOGLE_API_KEY = "AIzaSyB9xuw8eKRgFSQZ8mWdseWRI4vd8rDnPlU"

# Gemini AI সেটআপ
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# পাসওয়ার্ড
password = "baba"

st.set_page_config(page_title="Mike AI", page_icon="🤖")

# সেশন স্টেট (যাতে কথা মনে রাখতে পারে)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 I am Mike")

# পাসওয়ার্ড চেকিং
if not st.session_state.authenticated:
    st.subheader("পাসওয়ার্ড দিয়ে মাইক-কে আনলক করো")
    user_input = st.text_input("পাসওয়ার্ড লিখুন:", type="password")
    if st.button("Unlock Mike"):
        if user_input == password:
            st.session_state.authenticated = True
            st.success("স্বাগতম! মাইক এখন প্রস্তুত।")
            st.rerun()
        else:
            st.error("ভুল পাসওয়ার্ড! আবার চেষ্টা করো।")
else:
    # পুরনো মেসেজগুলো দেখানো
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # নতুন প্রশ্ন করার জায়গা
    if prompt := st.chat_input("মাইককে কিছু জিজ্ঞেস করো..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # মাইকের উত্তর তৈরি করা
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("এপিআই কি (API Key) তে সমস্যা হচ্ছে অথবা লিমিট শেষ।")

# সাইডবার
with st.sidebar:
    st.write("### Mike AI Chatbot")
    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()
