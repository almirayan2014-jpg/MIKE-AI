import streamlit as st
import google.generativeai as genai

# ১. পেজ সেটআপ
st.set_page_config(page_title="Mike AI", page_icon="🤖")
st.title("🤖 Mike AI")

# ২. এপিআই কি কানেক্ট করা
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("Secrets-এ API Key পাওয়া যায়নি!")

# ৩. চ্যাট হিস্ট্রি ধরে রাখা
if "messages" not in st.session_state:
    st.session_state.messages = []

# আগের মেসেজগুলো স্ক্রিনে দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৪. ইউজারের ইনপুট এবং উত্তর
if prompt := st.chat_input("মাইককে কিছু জিজ্ঞেস করো..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # এখানে 'gemini-pro' ব্যবহার করেছি কারণ এটি সবচেয়ে স্টেবল
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
