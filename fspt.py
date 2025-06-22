import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("GEMENI_API_KEY")
os.environ["GOOGLE_API_KEY"]=api_key

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import FewShotPromptTemplate,PromptTemplate

llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash")

examples = [
    {"question": "What is 2+2?", "answer": "4"},
    {"question": "What is the capital of France?", "answer": "Paris"},
]

example_prompt = PromptTemplate.from_template("Question: {question}\nAnswer: {answer}\n")
prompt=FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Question: {input}",
    input_variables=["input"]
)

llm_chain=prompt | llm

response = llm_chain.invoke({"input": "What is the largest ocean in the world?"})
print(response.content)