import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("GEMENI_API_KEY")
os.environ["GOOGLE_API_KEY"]=api_key

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash")

prompt=PromptTemplate.from_template(
    template="Explain the topic of {topic} in simple terms."

)
llm_chain=prompt | llm

response = llm_chain.invoke({"topic": "Neural Network"})
print(response.content)