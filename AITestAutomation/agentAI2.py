import asyncio
import os

from browser_use.agent.service import Agent
from browser_use.agent.views import ActionResult
from browser_use.controller.service import Controller
from langchain_google_genai import ChatGoogleGenerativeAI
from playwright.sync_api import BrowserContext
from posthog import api_key
from pydantic import SecretStr, BaseModel


class CheckoutResult(BaseModel):
    login_status: str
    cart_status: str
    checkout_status: str
    total_update_status: str
    delivery_location_status: str
    confirmation_message: str


controller = Controller(output_model=CheckoutResult)


@controller.action('Get Attribute and url of the page')
async def get_attr_url(browser : BrowserContext):
    page = await browser.get_current_page()
    current_url = page.url
    attr=page.get_by_text('Shop Name').get_attribute('class')
    print(current_url)
    return ActionResult(extracted_content=f'current url is {current_url} and attribute is {attr}')

async def SiteValidation():
    os.environ["GEMINI_API_KEY"] = "AIzaSyD0KeqcWM0eP-5tJocXHrNhyhhfEm9bt08"
    task = (
        'Important : I am UI Automation tester validating the tasks'
        'Open website https://rahulshettyacademy.com/loginpagePractise/'
        'If the url value is not "https://rahulshettyacademy.com/loginpagePractise/". Go to "https://rahulshettyacademy.com/loginpagePractise/" again.'
        'Login with username and password. login Details available in the same page'
        'Get Attribute and url of the page'
        'After login, select first 2 products and add them to cart'
        'Then checkout and store the total value you see in screen'
        'Increase the quantity of any product and check if total value update accordingly'
        'checkout and select country, agree terms and purchase '
        'verify thankyou message is displayed'
    )
    api_key = os.environ["GEMINI_API_KEY"]
    llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))
    agent = Agent(task=task, llm=llm, controller=controller, use_vision=True)
    history = await agent.run()
    history.save_to_file('agentresults.json')
    test_result = history.final_result()
    print(test_result)

    assert test_result.confirmation_message == "Thank you! Your order will be delivered in next few weeks :-)."


asyncio.run(SiteValidation())
