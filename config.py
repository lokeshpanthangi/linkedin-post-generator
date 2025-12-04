from langchain_openai import ChatOpenAI
from dotenv import load_dotenv





load_dotenv()  # Load environment variables from .env file





model = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

