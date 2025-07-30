# 🦷 DentalSözlük

Türkçe diş terimlerini başlık, açıklama, İngilizce ve Latince karşılıklarıyla sunan **Django** tabanlı sözlük uygulaması.

---

## Özellikler
- Terimleri listeleme, arama ve filtreleme  
- Hata bildirme sistemi  
- Mobil uyumlu (responsive) arayüz  

---

## Gereksinimler
- Python 3.8+  
- pip  
- (İsteğe bağlı) PostgreSQL — varsayılan olarak SQLite kullanılır  

---

## Kurulum
1. Depoyu klonla  
   ```bash
   git clone https://github.com/semanur-teke/dentalsozluk.git
   cd dentalsozluk
   ```
2. Sanal ortamı oluştur ve etkinleştir  
   ```bash
   python -m venv .venv
   # macOS/Linux
   source .venv/bin/activate
   # Windows
   .venv\Scripts\activate
   ```
3. Bağımlılıkları yükle  
   ```bash
   pip install -r requirements.txt
   ```
4. Veritabanını hazırla  
   ```bash
   python manage.py migrate
   ```
5. Geliştirme sunucusunu başlat  
   ```bash
   python manage.py runserver
   ```
   Tarayıcıda `http://localhost:8000/` adresine git.

---

## Katkıda Bulunma
1. Fork’la  
2. Yeni bir branch aç  
   ```bash
   git checkout -b feature/yeni-terim
   ```
3. Değişikliklerini commit’le  
   ```bash
   git commit -m "feat: yeni terim ekle"
   ```
4. Branch’i push’la ve Pull Request oluştur  

Detaylar için `CONTRIBUTING.md` dosyasına göz at.

---

## Lisans
Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.

---

## İletişim
Semanur Teke — info@dentalsozluk.com
