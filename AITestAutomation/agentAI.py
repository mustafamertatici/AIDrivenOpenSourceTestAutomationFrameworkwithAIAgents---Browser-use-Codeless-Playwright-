import asyncio
import os

from browser_use.agent.service import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from posthog import api_key
from pydantic import SecretStr
from dotenv import load_dotenv


async def SiteValidation():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    task=(
        'Important : I am UI Automation tester validating the tasks'
        'Open website https://the-internet.herokuapp.com/login'
        'Login with username and password. login Details available in the same page'
        'Verify that you have successfully logged in with the message "You are logged into a secure area!"'
    )
    api_key = os.environ["GEMINI_API_KEY"]
    llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp',api_key=SecretStr(api_key))
    agent=Agent(task,llm,use_vision=True)
    history=await agent.run()
    test_result=history.final_result()
    print(test_result)

asyncio.run(SiteValidation())