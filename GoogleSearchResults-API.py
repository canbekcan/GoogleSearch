import csv
import sys
import os
from dotenv import load_dotenv
load_dotenv()
# Google Custom Search API için gerekli kütüphaneler
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- YAPILANDIRMA ---
# ÖNEMLİ: Kendi gerçek API anahtarınız ve CX ID'nizle güncellenmiştir.
API_KEY = os.getenv("API_KEY") # Lütfen burayı kendi API anahtarınızla değiştirin
CX_ID = os.getenv("CX_ID") # Lütfen burayı kendi CX ID'nizle değiştirin

# API başına maksimum 10 sonuç döndürebilir.
RESULTS_PER_PAGE = 10
# Kaç sayfa veri çekileceği (5 sayfa * 10 sonuç/sayfa = 50 toplam sonuç)
num_pages = 5

# Orijinal yer tutucu metinleri, kontrol mekanizmasında kullanılmak üzere tanımlıyoruz.
# Eğer API_KEY veya CX ID hala bu değerlere eşitse, kullanıcıya hata vermemiz gerekir.
PLACEHOLDER_API_KEY = "YOUR_GOOGLE_API_KEY"
PLACEHOLDER_CX_ID = "YOUR_CUSTOM_SEARCH_ENGINE_ID"

def run_google_search_api_scraper():
    """
    Google Custom Search API'si üzerinden arama sorgularını yürütür,
    sayfalama yapar ve sonuçları bir CSV dosyasına kaydeder.
    """
    # Kimlik bilgileri kontrolü
    # KONTROL MEKANİZMASI DÜZELTİLDİ: Artık gerçek anahtarlar yerine 
    # orijinal yer tutucu metinleri kontrol edecektir.
    is_key_missing = API_KEY == PLACEHOLDER_API_KEY
    is_cx_missing = CX_ID == PLACEHOLDER_CX_ID

    if is_key_missing or is_cx_missing:
        print("\n" + "="*50)
        print("HATA: Lütfen betikteki kimlik bilgilerini güncelleyin.")
        if is_key_missing:
            print("❌ API_KEY değişkeni eksik veya hatalı görünüyor.")
        if is_cx_missing:
            print("❌ CX_ID değişkeni eksik veya hatalı görünüyor.")
        print("Lütfen bu iki değeri de gerçek kimlik bilgilerinizle değiştirin.")
        print("="*50 + "\n")
        sys.exit(1)

    try:
        # Kullanıcıdan arama sorgusunu iste
        search_query = input("Arama sorgunuzu girin: ")
        
        # Kullanıcıdan CSV dosya adını iste
        csv_filename = input("CSV dosyasının adını girin (uzantısız): ") + ".csv"

        # Custom Search servisini başlat
        # 'customsearch' ve 'v1' servis adlarını kullanırız.
        service = build("customsearch", "v1", developerKey=API_KEY)

    except Exception as e:
        print(f"Genel Hata: Google API servisi başlatılamadı veya giriş başarısız oldu: {e}")
        return

    print(f"\nAranıyor: '{search_query}' ve {csv_filename} dosyasına kaydediliyor...")
    
    # CSV dosyasını yazma modunda aç
    # DÜZELTME: encoding='utf-8-sig' kullanılarak BOM (Byte Order Mark) eklendi.
    # Bu, Excel gibi programların dosyayı doğru UTF-8 kodlamasıyla açmasını sağlar.
    with open(csv_filename, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        # Başlık satırını yaz
        writer.writerow(["Sayfa", "Sıra", "Başlık", "Bağlantı", "Özet (Snippet)"])
        
        total_results_count = 0

        # İstenen sayfa sayısı kadar döngü kur
        for page_num in range(num_pages):
            # API'nin 'start' parametresi 1'den başlar (1, 11, 21, 31, vb.)
            start_index = (page_num * RESULTS_PER_PAGE) + 1
            
            # Google Custom Search API, en fazla 100 sonuç (start=1'den start=91'e kadar) sağlar.
            if start_index > 91:
                print("\nAPI limitine (maksimum 100 sonuç) ulaşıldı. Sayfalama durduruluyor.")
                break

            print(f"--- Sayfa {page_num + 1} Çekiliyor (Başlangıç Dizini: {start_index}) ---")

            try:
                # API isteğini yürüt
                res = service.cse().list(
                    q=search_query,
                    cx=CX_ID,
                    num=RESULTS_PER_PAGE,  # Sayfa başına sonuç sayısı
                    start=start_index      # Başlangıç indeksi
                ).execute()
                
                # Sonuçların varlığını kontrol et
                if 'items' not in res:
                    print(f"Sayfa {page_num + 1}'den sonra başka sonuç bulunamadı.")
                    break

                # Mevcut sayfadaki sonuçları işle
                for i, item in enumerate(res['items']):
                    total_results_count += 1
                    
                    # Verileri çek (Güvenli erişim için .get() kullanılır)
                    title = item.get('title', 'N/A')
                    link = item.get('link', 'N/A')
                    # HTML etiketlerini içermeyen sadeleştirilmiş metni alır
                    snippet = item.get('snippet', 'N/A') 
                    
                    rank = start_index + i
                    
                    # Sonucu CSV dosyasına yaz
                    writer.writerow([page_num + 1, rank, title, link, snippet])

                    # Sonucu konsola yazdır (isteğe bağlı)
                    print(f"  {rank}. Başlık: {title}")
                    print(f"     Bağlantı: {link}")
                    print(f"     Özet: {snippet[:100]}...") # Özeti kısaltarak yazdır
                
            except HttpError as e:
                # API Hatalarını yakala (örneğin, limit aşıldı, geçersiz anahtar)
                print(f"\n[API HATASI] Sayfa {page_num + 1} çekilemedi: {e}")
                print("Hata nedeniyle arama durduruluyor.")
                print("Lütfen API Anahtarınızın ve CX ID'nizin doğruluğunu, ayrıca günlük API kotanızı kontrol edin.")
                break
            
            except Exception as e:
                print(f"\n[GENEL HATA] Beklenmedik bir hata oluştu: {e}")
                print("Hata nedeniyle arama durduruluyor.")
                break
        
        print(f"\n✅ '{search_query}' sorgusu için toplam {total_results_count} sonuç {csv_filename} dosyasına başarıyla kaydedildi.")

if __name__ == "__main__":
    run_google_search_api_scraper()
