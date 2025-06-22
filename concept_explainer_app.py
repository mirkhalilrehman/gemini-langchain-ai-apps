import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("GEMENI_API_KEY")
os.environ["GOOGLE_API_KEY"]=api_key
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash')

prompt=PromptTemplate.from_template("Explain the topic of {topic} in simple terms")
st.set_page_config(page_title="Concept Explainer", page_icon="📘")
st.title("📘 Concept Explainer with Gemini")
st.markdown("Ask anything and get a simple explanation using Google Gemini.")
llm_chain=prompt | llm
if 'history' not in st.session_state:
    st.session_state.history=[]

topic=st.text_input("🔍 Enter a topic to explain:")
if st.button('explain'):
    if topic:
        full_prompt=prompt.format(topic=topic)
        response=llm_chain.invoke(full_prompt)
        st.session_state.history.append({
            "topic": topic,
            "response": response.content
        })

    # Show response
        st.subheader(f"🧠 Explanation for: {topic}")
        st.write(response.content)
    else:
        st.warning("Please enter a topic.")

# History sidebar
st.sidebar.title("🕘 History")
for item in reversed(st.session_state.history):
    st.sidebar.markdown(f"**{item['topic']}**")
    st.sidebar.caption(item['response'][:100] + "...")
