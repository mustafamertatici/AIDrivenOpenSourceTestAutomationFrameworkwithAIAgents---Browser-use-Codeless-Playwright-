# 🤖 AI Destekli UI Test Otomasyonu — LangChain + Gemini + Playwright

Bu proje, klasik UI test otomasyon süreçlerini doğal dil ile otomatikleştirmek amacıyla LangChain ve Google Gemini LLM kullanılarak geliştirilmiştir. 
Yapay zeka destekli bu yapı, geleneksel kod yazma ihtiyacını azaltarak niyet odaklı test senaryolarının yürütülmesini sağlar.

---

## 🚀 Teknolojiler ve Kütüphaneler

- **LangChain**: LLM zincirleme yapıları ve görev tanımlamaları için
- **Google Gemini (gemini-2.0-flash-exp)**: Doğal dilde yazılan görevleri yorumlamak ve yürütmek için
- **Playwright**: UI otomasyon işlemlerini tarayıcı üzerinden kontrol etmek için
- **Python Asyncio**: Asenkron fonksiyonlarla yapının daha verimli çalışması
- **Pydantic**: Modelleme ve veri doğrulama

---

## 🧠 Proje Amacı

Bu proje ile klasik test otomasyonu sınırlarını genişletmeyi hedefliyoruz:

✅ Doğal dil ile test senaryosu tanımlama  
✅ Web arayüzü üzerinde ürün ekleme, login, ödeme gibi UI senaryolarını yürütme  
✅ Sonuçları `CheckoutResult` isimli özel bir model ile detaylı şekilde raporlama  
✅ Yapay zekanın adımları nasıl gerçekleştirdiğini `agentresults.json` dosyasına kaydetme  

---

## 📌 Uygulanan Senaryo (Natural Language Prompt)

```plaintext
- Web sitesini aç
- Giriş bilgilerini sayfadan alarak login ol
- Shop Name elementinin attribute’unu ve URL bilgisini al
- İlk 2 ürünü sepete ekle
- Ödeme adımına geç, toplam fiyatı kaydet
- Ürün miktarını artır ve toplam fiyatın güncellenip güncellenmediğini kontrol et
- Ülke seç, kuralları kabul et ve satın alma işlemini tamamla
- "Thank you!" mesajının görünüp görünmediğini doğrula
