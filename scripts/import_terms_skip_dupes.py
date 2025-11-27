import os
import sys

# Mevcut dosyanın konumu: .../dentalsozluk/scripts/import_terms_skip_dupes.py
# Proje kökünü almak için bir üst dizine çıkıyoruz:
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Şimdi Django ayarlarını yükleyebiliriz
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dentalsozluk.settings')

import django
django.setup()

# Devamında model import’u ve CSV işlemleri...
from terms.models import DentalTerm
import csv

def main():
    import argparse
    from django.db import transaction

    parser = argparse.ArgumentParser(
        description='CSV dosyasından duplicate kontrolüyle terim yükler'
    )
    parser.add_argument(
        'infile',
        help='İçe aktarılacak CSV dosyası'
    )
    parser.add_argument(
        '--duplicates-file',
        default='duplicates_skipped.csv',
        help='Atlanan duplike kayıtlar için dosya adı (default: duplicates_skipped.csv)'
    )

    args = parser.parse_args()
    infile = args.infile
    dupfile = args.duplicates_file

    # Dosya kontrolü
    if not os.path.exists(infile):
        print(f"❌ Hata: CSV dosyası bulunamadı: {infile}")
        sys.exit(1)

    # Mevcut slug'ları al
    seen = set(DentalTerm.objects.values_list('slug', flat=True))
    created_count = 0
    duplicate_count = 0

    try:
        with transaction.atomic():
            with open(infile, newline='', encoding='utf-8') as fin, \
                 open(dupfile, 'w', newline='', encoding='utf-8') as fdup:

                reader = csv.DictReader(fin)
                writerdup = csv.DictWriter(fdup, fieldnames=reader.fieldnames)
                writerdup.writeheader()

                for row in reader:
                    slug = row['slug']
                    if slug in seen:
                        writerdup.writerow(row)
                        duplicate_count += 1
                    else:
                        DentalTerm.objects.create(
                            title=row['title'],
                            description=row['description_tr'],
                            slug=slug
                        )
                        seen.add(slug)
                        created_count += 1

        print(f"✅ Başarılı: {created_count} terim eklendi.")
        print(f"⏭️  Atlandı: {duplicate_count} duplike (kaydedildi: {dupfile})")

    except KeyError as e:
        print(f"❌ Hata: CSV'de gerekli sütun bulunamadı: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Hata: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
