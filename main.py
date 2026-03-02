import streamlit as st
import google.generativeai as genai

# ১. টাইটেল এবং পেজ সেটআপ
st.set_page_config(page_title="Mike AI", page_icon="🤖")
st.title("🤖 Mike AI")

# ২. এপিআই কি (API Key) কানেক্ট করা
try:
    # এটি স্ট্রিমলিট সিক্রেটস থেকে কি-টা নেবে
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("গুগল এপিআই কি (API Key) পাওয়া যায়নি। দয়া করে সেটিংস চেক করো।")

# ৩. চ্যাট হিস্ট্রি বা মেমোরি সেটআপ
if "messages" not in st.session_state:
    st.session_state.messages = []

# ৪. আগের মেসেজগুলো স্ক্রিনে দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৫. ইউজারের ইনপুট নেওয়া এবং উত্তর দেওয়া
if prompt := st.chat_input("মাইককে কিছু জিজ্ঞেস করো..."):
    # ইউজারের মেসেজ সেভ করা
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # এআই-এর উত্তর জেনারেট করা
    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            full_response = response.text
            st.markdown(full_response)
            
            # এআই-এর মেসেজ সেভ করা
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"দুঃখিত, কোনো সমস্যা হয়েছে: {e}")
