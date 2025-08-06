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
    infile  = '/var/www/dentalsozluk/scripts/duplicates1.csv'
    dupfile = '/var/www/dentalsozluk/scripts/dup.csv'


    seen = set(DentalTerm.objects.values_list('slug', flat=True))

    with open(infile, newline='', encoding='utf-8') as fin, \
         open(dupfile, 'a', newline='', encoding='utf-8') as fdup:

        reader    = csv.DictReader(fin)
        writerdup = csv.DictWriter(fdup, fieldnames=reader.fieldnames)
        writerdup.writeheader()

        for row in reader:
            slug = row['slug']
            if slug in seen:
                writerdup.writerow(row)
            else:
                DentalTerm.objects.create(
                    title       = row['title'],
                    description = row['description_tr'],
                    slug        = slug
                )
                seen.add(slug)

    print(f"✅ {infile} Veritabanına eklendi. Atlananlar: {dupfile}")

if __name__ == '__main__':
    main()
