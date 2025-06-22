import streamlit as st
import os
import random
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMENI_API_KEY")
os.environ["GOOGLE_API_KEY"] = api_key

# Init LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Prompt Template
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a geography expert that returns only the colors present in a country's flag. Return them as a comma-separated list (e.g. red, white, blue)."),
    ("human", "{country}")
])

# Countries list
country_list = ["France", "Pakistan", "Germany", "Japan", "Brazil", "India", "Italy", "Canada", "USA", "Turkey", "Argentina", "Mexico", "Norway"]

# Streamlit UI
st.set_page_config(page_title="Flag Color Quiz", page_icon="🚩")
st.title("🏁 Flag Color Quiz Game")
st.markdown("Guess the colors in the flag of each country. Earn points for each correct answer!")

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "round" not in st.session_state:
    st.session_state.round = 1
if "current_country" not in st.session_state:
    st.session_state.current_country = random.choice(country_list)

# Show current country
st.subheader(f"🌍 Round {st.session_state.round}")
st.markdown(f"**Guess the flag colors of:** `{st.session_state.current_country}`")
user_input = st.text_input("Your Answer (comma-separated):", key=st.session_state.round)

# Button to check answer
if st.button("Check Answer"):
    chain = chat_prompt | llm
    response = chain.invoke({"country": st.session_state.current_country})
    correct_colors = response.content.lower().replace(" ", "").split(',')
    user_colors = user_input.lower().replace(" ", "").split(',')

    if set(user_colors) == set(correct_colors):
        st.success("🎉 Correct!")
        st.session_state.score += 1
    else:
        st.error("❌ Incorrect!")
        st.info(f"✅ Correct colors were: **{', '.join(correct_colors)}**")

# Button to go to next round
if st.button("Next Question"):
    st.session_state.round += 1
    st.session_state.current_country = random.choice(country_list)
    st.experimental_rerun()

# Display score
st.sidebar.title("📊 Your Progress")
st.sidebar.metric("Score", st.session_state.score)
st.sidebar.metric("Rounds Played", st.session_state.round - 1)
