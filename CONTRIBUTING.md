# Katkıda Bulunma Rehberi

Merhaba! Dental Sözlük’e katkıda bulunmak istediğin için teşekkürler.

---

## 1. Gereksinimler

- **Python 3.8+**
- `pip`
- `flake8`, `black`, `pytest` (geliştirici bağımlılıkları)

Yerel ortamı kurmak için:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # varsa
```

---

## 2. Nasıl Katkı Sağlarsın?

1. GitHub’da bir **issue** aç veya mevcut issue’lardan birini üstlen.  
2. Repoyu **fork** et ve aşağıdaki kurala göre yeni bir branch aç:  
   - Özellik: `feature/ozellik-adi`  
   - Hata: `bugfix/hata-kodu`  
3. Değişiklikleri yap, testleri çalıştır:  
   ```bash
   pytest
   ```  
4. Kod stilini denetle:  
   ```bash
   black .
   flake8
   ```  
5. Anlamlı bir commit mesajı yaz (Conventional Commits tavsiye edilir):  
   ```
   feat: yeni terim ekleme sayfası
   ```  
6. Branch’ini kendi repona **push** et ve Pull Request (PR) aç.

---

## 3. Pull Request Kontrol Listesi

- [ ] Kod **PEP8** uyumlu mu? (`flake8` sıfır hata)  
- [ ] Yeni fonksiyonellik için test eklendi mi?  
- [ ] README veya dokümantasyon güncellendi mi?  
- [ ] CI pipeline (GitHub Actions) başarıyla geçti mi?  

PR açıklamasında: **Amaç**, **Yapılan Değişiklikler** ve **Test Adımları** başlıklarını ekle.

---

## 4. Sorular ve Destek

- Genel sorular için GitHub Discussions veya **info@dentalsozluk.com**  
- Güvenlik açıkları için doğrudan e‑posta gönder.

---

## 5. Kod Davranış Kuralları

Bu projede [Contributor Covenant](https://www.contributor-covenant.org/) davranış kuralları geçerlidir. Katkıda bulunmadan önce lütfen göz at.

---

Keyifli kodlamalar!
