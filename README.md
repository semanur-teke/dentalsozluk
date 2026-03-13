# 🦷 DentalSözlük

> **Türkçe Diş Hekimliği Terminoloji Platformu**
> Diş hekimleri ve öğrenciler için Türkçe, İngilizce ve Latince karşılıklarıyla kapsamlı bir terim referansı.

🌐 **Canlı:** [dentalsozluk.com](https://www.dentalsozluk.com)

---

## 📌 Proje Hakkında

DentalSözlük; diş hekimleri, diş hekimliği öğrencileri ve sağlık profesyonelleri için geliştirilmiş açık kaynaklı bir terminoloji referans platformudur.
Her terim; Türkçe başlık ve açıklamasının yanı sıra İngilizce ve Latince karşılıklarıyla, alternatif yazılış takma adlarıyla ve SEO dostu kalıcı bağlantılarıyla kataloglanmıştır.

---

## ✨ Özellikler

### 🔍 Akıllı Arama
- Terim adı, İngilizce/Latince karşılık ve arama takma adlarında eş zamanlı arama
- **Öncelikli eşleşme**: önce başlangıç eşleşmeleri, sonra içerik eşleşmeleri
- Boşluklu/boşluksuz varyant desteği (örn. "miyokart" = "miyokart")
- Canlı **otomatik tamamlama** — 2 karakterden itibaren öneri

### 🔡 Türkçe Alfabe Tarama
- Türkçe alfabeye göre (A, B, C, Ç, D … Ş, U, Ü …) harf filtresi
- 0-9 rakamıyla başlayan terimleri ayrı gruplama
- Sayfalama: sayfa başına 20 terim, akıllı sayfa numarası ellipsis'i

### 🚩 Topluluk Destekli Hata Bildirimi
- Her terim için tek tıkla hata raporlama
- **Honeypot** bot koruması — gizli alan doluysa istek reddedilir
- **Rate limiting** — IP başına dakikada 3 istek (django-ratelimit)
- **Session tabanlı tekrar engeli** — 60 saniye içinde aynı bildirim kabul edilmez

### 🔒 Güvenlik & Üretim Hazırlığı
- `django-csp` ile Content Security Policy başlıkları
- `whitenoise` ile statik dosya sunumu (CDN olmadan)
- `gunicorn` WSGI sunucusu desteği
- `.env` tabanlı gizli yapılandırma (`python-dotenv`)
- PostgreSQL üretime hazır, SQLite geliştirme için varsayılan

### 🗺️ SEO
- `robots.txt` — admin ve report endpointleri taranmaz
- `sitemap.xml` — tüm terimler haftalık güncelleme, öncelik 0.8

---

## 🛠️ Teknoloji Yığını

| Katman            | Teknoloji                              |
|-------------------|----------------------------------------|
| Framework         | Django 5.2.4                           |
| Dil               | Python 3.8+                            |
| Veritabanı        | SQLite (geliştirme) / PostgreSQL (üretim) |
| WSGI Sunucusu     | Gunicorn 21.2                          |
| Statik Dosyalar   | WhiteNoise 6.6                         |
| Rate Limiting     | django-ratelimit 4.1                   |
| Güvenlik Başlıkları | django-csp 4.0                       |
| Ortam Değişkenleri | python-dotenv 1.0                     |

---

## 🗂️ Proje Yapısı

```
dentalsozluk/
├── terms/
│   ├── models.py          # DentalTerm, ErrorReport modelleri
│   ├── views.py           # term_list, term_detail, search, autocomplete, report_error
│   ├── urls.py
│   ├── sitemaps.py
│   └── management/        # Veri import komutları
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── partials/
│   └── static_pages/      # Hakkımızda, Gizlilik, Çerez politikası
├── static/
├── scripts/
│   └── import_terms_skip_dupes.py
├── manage.py
└── requirements.txt
```

---

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- pip
- (Opsiyonel) PostgreSQL

### Adımlar

```bash
# 1. Repoyu klonla
git clone https://github.com/semanur-teke/dentalsozluk.git
cd dentalsozluk

# 2. Sanal ortam oluştur ve etkinleştir
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. Ortam değişkenlerini ayarla
cp .env.example .env             # SECRET_KEY ve DATABASE_URL'yi doldur

# 5. Veritabanı migrasyonlarını çalıştır
python manage.py migrate

# 6. Geliştirme sunucusunu başlat
python manage.py runserver
```

Tarayıcıda aç: [http://localhost:8000](http://localhost:8000)

---

## 📦 Veri İçe Aktarma

Terim verilerini CSV/JSON'dan toplu içe aktarmak için:

```bash
python scripts/import_terms_skip_dupes.py
```

Mevcut terimler atlanır; yalnızca yeni kayıtlar eklenir.

---

## 🤝 Katkıda Bulunma

Katkılar memnuniyetle karşılanır!

1. Repoyu **fork** edin
2. Yeni bir dal oluşturun: `git checkout -b feature/ozellik-adi`
3. Değişikliklerinizi commit edin: `git commit -m "feat: açıklayıcı mesaj"`
4. Dalınıza push edin: `git push origin feature/ozellik-adi`
5. Bir **Pull Request** açın

Detaylı kurallar için [`CONTRIBUTING.md`](CONTRIBUTING.md) dosyasına bakın.

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.

---

## 📬 İletişim

**Semanur Teke** — [info@dentalsozluk.com](mailto:info@dentalsozluk.com) · [github.com/semanur-teke](https://github.com/semanur-teke)
