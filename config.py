
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()


config = {
    "openai_api_key" : os.getenv(key="OPENAI_API_KEY")
}


model = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
