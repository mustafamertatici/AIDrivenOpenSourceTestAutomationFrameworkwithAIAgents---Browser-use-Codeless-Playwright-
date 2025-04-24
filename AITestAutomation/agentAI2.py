# Gerekli kütüphaneleri içe aktarıyoruz.
import asyncio
import os

# Proje içerisinde tanımlı agent (AI destekli) hizmetini ve yapılarını içe aktarıyoruz
from browser_use.agent.service import Agent
from browser_use.agent.views import ActionResult
from dotenv import load_dotenv

# Tüm kullanıcı işlemlerini yöneten controller yapısı
from browser_use.controller.service import Controller

# LangChain üzerinden Google Gemini API'sini kullanan LLM (Large Language Model)
from langchain_google_genai import ChatGoogleGenerativeAI

# Playwright senkron tarayıcı kontrolü için gerekli olan tarayıcı context yapısı
from playwright.sync_api import BrowserContext

from posthog import api_key

# Güvenli string ve veri modeli tanımlamaları için
from pydantic import SecretStr, BaseModel



# Test sonucunda dönecek çıktıları modelleyen sınıf
class CheckoutResult(BaseModel):
    login_status: str               # Giriş işleminin başarılı olup olmadığını belirtir
    cart_status: str                # Sepete ürün eklenme durumunu belirtir
    checkout_status: str            # Ödeme işleminin durumu
    total_update_status: str        # Sepet toplamının güncellenip güncellenmediği
    delivery_location_status: str   # Teslimat adresinin seçilip seçilmediği
    confirmation_message: str       # Satın alma sonrası gelen teşekkür mesajı

# Controller, testin sonucunu yukarıdaki CheckoutResult modeline göre yönetecek
controller = Controller(output_model=CheckoutResult)

@controller.action('open base website')     # Bu fonksiyon bir test aksiyonu olarak tanımlanır
async def open_website(browser:BrowserContext):
    # Aktif tarayıcı sekmesini alıyoruz
    page=await browser.get_current_page()

    # Hedef web sitesine yönlendiriyoruz
    await  page.goto('https://rahulshettyacademy.com/loginpagePractise/')

    # Test çıktısında bu bilginin görünebilmesi için sonucu döndürüyoruz
    return ActionResult(extracted_content='base website opened')

# LLM tarafından kullanılabilecek bir aksiyon tanımlıyoruz:
# Sayfadaki URL'yi ve 'Shop Name' yazılı elemanın class attribute'unu alıyoruz
@controller.action('Get Attribute and url of the page')
async def get_attr_url(browser : BrowserContext):
    # Aktif tarayıcı sekmesini alıyoruz
    page = await browser.get_current_page()
    # Sayfanın mevcut URL'sini alıyoruz
    current_url = page.url
    # 'Shop Name' yazısını içeren elementin class attribute'unu al
    attr = await page.get_by_text('Shop Name').get_attribute('class')
    # URL'yi terminale yazdır
    print(current_url)
    # Elde edilen verileri ActionResult objesi ile geri döndür
    return ActionResult(extracted_content=f'current url is {current_url} and attribute is {attr}')

# Ana test fonksiyonu: LLM'e test görevlerini doğal dille veriyoruz ve işlemleri o gerçekleştiriyor
async def SiteValidation():
    # Google Gemini API anahtarını çevresel değişken olarak ayarla
    load_dotenv()
    os.getenv("GEMINI_API_KEY") #
    # Gemini API anahtarını .env dosyasından güvenli şekilde alalım
    api_key = os.getenv("GEMINI_API_KEY")

    # LLM'e verilecek doğal dil ile yazılmış test task'ı
    task = (
        'Important : I am UI Automation tester validating the tasks. \n'
        'Open base website https://rahulshettyacademy.com/loginpagePractise/ \n'
        'Login with username and password. login Details available in the same page \n'
        'Get Attribute and url of the page.\n'
        'After login, select first 2 products and add them to cart. \n'
        'Then checkout and store the total value you see in screen \n'
        'Increase the quantity of any product and check if total value update accordingly \n'
        'checkout and select country, agree terms and purchase \n'
        'verify thankyou message is displayed \n'
    )



    # Google Gemini tabanlı Chat LLM'i başlat
    llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))

    # Agent (yapay zeka) görevleri yerine getirecek olan nesne
    agent = Agent(task=task, llm=llm, controller=controller, use_vision=True)

    # Agent çalıştırılıyor ve görev geçmişi (history) alınıyor
    history = await agent.run()

    # Test geçmişini dosyaya JSON formatında kaydet
    from  datetime import datetime
    filename=F"agentresults_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    history.save_to_file('agentresults.json')

    # Testin nihai sonucu (CheckoutResult formatında)
    test_result = history.final_result()
    print(test_result)
    validate_result=CheckoutResult.model_validate_json(test_result)

    # Test çıktısı terminale yazdırılıyor


    #(doğrulama)
    assert validate_result.confirmation_message == "Thank you! Your order will be delivered in next few weeks :-).", \
        f"Beklenen teşekkür mesajı bulunamadı. Gelen mesaj: {validate_result.confirmation_message}"

# asyncio modülü ile yukarıdaki asenkron fonksiyon başlatılıyor
asyncio.run(SiteValidation())
