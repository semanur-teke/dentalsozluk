# 🦷 DentalSözlük

Türkçe diş terimlerini başlık, açıklama, İngilizce ve Latince karşılıklarıyla sunan **Django** tabanlı sözlük uygulaması.

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-5.2-green.svg)](https://www.djangoproject.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## ✨ Özellikler

- 🔍 **Gelişmiş Arama**: Türkçe, İngilizce ve Latince terimlerde arama
- 📱 **Responsive Tasarım**: Mobil, tablet ve masaüstü uyumlu
- 🌙 **Dark Mode**: Karanlık mod desteği
- 📊 **Alfabetik Filtreleme**: Harflere göre terim listeleme
- 🐛 **Hata Bildirimi**: Kullanıcılar hatalı terimleri bildirebilir
- ⚡ **Autocomplete**: Gerçek zamanlı arama önerileri
- 🔒 **Güvenlik**: CSRF, rate limiting, honeypot bot koruması
- 📈 **Analytics**: Google Analytics 4 entegrasyonu

---

## 🛠 Gereksinimler

- **Python**: 3.11+ (önerilen)
- **PostgreSQL**: 12+ (production için)
- **Redis**: 6+ (rate limiting ve cache için)
- **pip**: 21.0+

---

## 📦 Kurulum

### 1. Depoyu Klonla

```bash
git clone https://github.com/semanur-teke/dentalsozluk.git
cd dentalsozluk
```

### 2. Sanal Ortam Oluştur

```bash
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Bağımlılıkları Yükle

```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies (test, linting, etc.)
pip install -r requirements-dev.txt
```

### 4. Environment Variables

`.env` dosyası oluştur:

```bash
# Django Core
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL)
DATABASE_URL=postgres://user:password@localhost:5432/dentalsozluk

# Redis (Rate Limiting & Cache)
REDIS_URL=redis://127.0.0.1:6379/1

# CSRF & Security
CSRF_TRUSTED_ORIGINS=https://dentalsozluk.com,https://www.dentalsozluk.com

# Google Analytics (Optional)
GA_MEASUREMENT_ID=G-XXXXXXXXXX
```

**Önemli**: Production'da `DJANGO_DEBUG=False` yapın!

### 5. Veritabanını Hazırla

```bash
# Migrations oluştur
python manage.py makemigrations

# Migrations uygula
python manage.py migrate

# Superuser oluştur (admin paneli için)
python manage.py createsuperuser

# Static dosyaları topla (production için)
python manage.py collectstatic --noinput
```

### 6. Redis'i Başlat

```bash
# macOS (Homebrew)
brew services start redis

# Linux (systemd)
sudo systemctl start redis

# Docker
docker run -d -p 6379:6379 redis:7-alpine
```

### 7. Geliştirme Sunucusunu Başlat

```bash
python manage.py runserver
```

Tarayıcıda `http://localhost:8000/` adresine git.

---

## 🧪 Test & Kod Kalitesi

### Testleri Çalıştır

```bash
# Tüm testleri çalıştır
pytest

# Coverage raporu ile
pytest --cov=terms --cov-report=html

# Belirli bir test dosyası
pytest terms/test_views.py

# Yavaş testleri atla
pytest -m "not slow"
```

### Kod Kalitesi Kontrolleri

```bash
# Black (code formatting)
black .

# Flake8 (linting)
flake8

# isort (import sorting)
isort .

# Type checking
mypy terms/
```

### Coverage Raporu

```bash
pytest --cov
# HTML raporu: htmlcov/index.html
```

---

## 📊 CSV'den Veri İçe Aktarma

### Yeni Terimler Ekle (Silmeden)

```bash
python manage.py import_terms /path/to/terms.csv
```

### Mevcut Verileri Sil ve Yeniden Yükle

```bash
# UYARI: Tüm mevcut terimler silinir!
python manage.py import_terms /path/to/terms.csv --clear
```

### Duplicate Kontrol ile İçe Aktarma

```bash
python scripts/import_terms_skip_dupes.py /path/to/terms.csv --duplicates-file skipped.csv
```

**CSV Format**:
```csv
title,description_tr,slug
Diş Çürüğü,Diş minesi bozulması,dis-curugu
```

---

## 🚀 Production Deployment

### 1. Gunicorn ile Çalıştır

```bash
gunicorn dentalsozluk.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 60 \
    --access-logfile logs/gunicorn-access.log \
    --error-logfile logs/gunicorn-error.log
```

### 2. Systemd Service (Linux)

`/etc/systemd/system/dentalsozluk.service`:

```ini
[Unit]
Description=Dental Sozluk Gunicorn
After=network.target postgresql.service redis.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/dentalsozluk
Environment="PATH=/var/www/dentalsozluk/.venv/bin"
ExecStart=/var/www/dentalsozluk/.venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/run/dentalsozluk.sock \
    dentalsozluk.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable dentalsozluk
sudo systemctl start dentalsozluk
```

### 3. Nginx Configuration

```nginx
server {
    listen 80;
    server_name dentalsozluk.com;

    location /static/ {
        alias /var/www/dentalsozluk/staticfiles/;
    }

    location / {
        proxy_pass http://unix:/run/dentalsozluk.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4. SSL Sertifikası (Let's Encrypt)

```bash
sudo certbot --nginx -d dentalsozluk.com -d www.dentalsozluk.com
```

---

## 🐛 Troubleshooting

### 400 Bad Request

- `.env` dosyasında `ALLOWED_HOSTS` ayarını kontrol et
- `CSRF_TRUSTED_ORIGINS` doğru domain'leri içerdiğinden emin ol
- Nginx proxy header'larını kontrol et

### Rate Limit Hatası

```bash
# Redis çalışıyor mu kontrol et
redis-cli ping  # PONG döndürmeli
```

### Static Files Yüklenmiyor

```bash
python manage.py collectstatic --clear --noinput
```

### Database Migration Hataları

```bash
# Fake migration (dikkatli kullan!)
python manage.py migrate --fake terms

# Migration'ları sıfırla
python manage.py migrate terms zero
python manage.py migrate
```

### Logs Klasörü Yok

```bash
mkdir -p logs
chmod 755 logs
```

---

## 🔧 Yapılandırma

### Rate Limiting

`terms/views.py`:
```python
@ratelimit(key='ip', rate='3/m', method='POST', block=True)
```

- `3/m`: Dakikada 3 istek
- `key='ip'`: IP adresine göre limit
- `block=True`: Limiti aşanları engelle

### Cache Ayarları

`settings.py`:
```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
    }
}
```

---

## 📚 API Endpoints

| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/` | GET | Ana sayfa |
| `/terms/` | GET | Terim listesi (pagination + filter) |
| `/term/<slug>/` | GET | Terim detay |
| `/search/` | GET | Arama sonuçları |
| `/autocomplete/` | GET | Arama önerileri (JSON) |
| `/report_error/` | POST | Hata bildirimi (JSON) |

### Örnek: Autocomplete

```bash
curl "http://localhost:8000/autocomplete/?q=dis"
```

Response:
```json
[
  {"title": "Diş Çürüğü", "url": "/term/dis-curugu/"},
  {"title": "Diş Eti", "url": "/term/dis-eti/"}
]
```

---

## 🤝 Katkıda Bulunma

1. Fork'la
2. Yeni branch oluştur (`git checkout -b feature/amazing-feature`)
3. Değişikliklerini commit'le (`git commit -m 'feat: add amazing feature'`)
4. Branch'i push'la (`git push origin feature/amazing-feature`)
5. Pull Request aç

Detaylar için [`CONTRIBUTING.md`](CONTRIBUTING.md) dosyasına göz at.

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.

---

## 👥 İletişim

**Semanur Teke**
📧 info@dentalsozluk.com
🌐 [dentalsozluk.com](https://dentalsozluk.com)
📷 [@dentalsozlukcom](https://www.instagram.com/dentalsozlukcom/)

---

## 🙏 Teşekkürler

- Django Community
- Bootstrap 5
- Font Awesome
- Google Analytics
