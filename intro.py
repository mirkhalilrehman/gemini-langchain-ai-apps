from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch API Key from .env and set for LangChain
api_key = os.getenv("GEMENI_API_KEY")
if not api_key:
    raise ValueError("GEMENI_API_KEY not found in .env file.")
os.environ["GOOGLE_API_KEY"] = api_key

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load Gemini model using LangChain
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Prompt template
# prompt = PromptTemplate(
#     input_variables=["topic"],
#     template="Explain the topic of {topic} in simple terms."
# )

# # Create the chain
# chain = LLMChain(llm=llm, prompt=prompt)

# # Run the chain with a test topic
# response = chain.run("attention in neural networks")
# print("\n📘 Response:\n", response)

response=llm.invoke("attention in neural networks")
print(response.content)
