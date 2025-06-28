import streamlit as st
import os
import math
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = api_key

# Init LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
@tool
def count_r_in_word(word):
    """this method counts number of r in any word """
    count=0
    for i in word:
        if i=='r':
            count+=1
    return count

@tool
def calculate_triangle_area(base: float, height: float) -> float:
    """Calculates the area of a triangle given base and height."""
    return 0.5 * base * height

# Create the agent
app = create_react_agent(model=llm, tools=[count_r_in_word,calculate_triangle_area])

# Create a query
query = "How many r's are in the word 'ribbonrorrr'?"

# Invoke the agent and store the response
response = app.invoke({"messages": [("human", query)]})

# Print the agent's response
print(response['messages'][-1].content)
message_history = response["messages"]
new_query = "What about one with sides 12 and 14?"
response = app.invoke({"messages": message_history + [HumanMessage(content=new_query)]})

# Extract the human and AI messages from the result
filtered_messages = [
    msg for msg in response["messages"]
    if isinstance(msg, (HumanMessage, AIMessage)) and msg.content.strip()
]

# Print final outputs
print({
    "user_input": new_query,
    "agent_output": [f"{msg.__class__.__name__}: {msg.content}" for msg in filtered_messages]
})