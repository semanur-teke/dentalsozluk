import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from terms.models import DentalTerm


class Command(BaseCommand):
    help = "CSV dosyasından dental terimleri veritabanına aktarır."

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_path',
            type=str,
            help='CSV dosyasının tam yolu'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Mevcut terimleri silip baştan yükler (TEHLİKELİ!)'
        )

    def handle(self, *args, **options):
        csv_path = options['csv_path']
        clear_existing = options['clear']

        # Dosya kontrolü
        if not os.path.exists(csv_path):
            raise CommandError(f'CSV dosyası bulunamadı: {csv_path}')

        # Silme onayı
        if clear_existing:
            existing_count = DentalTerm.objects.count()
            self.stdout.write(
                self.style.WARNING(
                    f'UYARI: {existing_count} adet mevcut terim silinecek!'
                )
            )
            confirm = input('Devam etmek istiyor musunuz? (yes/no): ')
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.ERROR('İşlem iptal edildi.'))
                return

        try:
            with transaction.atomic():
                # Sadece clear flag'i varsa sil
                if clear_existing:
                    deleted_count = DentalTerm.objects.all().delete()[0]
                    self.stdout.write(
                        self.style.WARNING(f'{deleted_count} terim silindi.')
                    )

                # CSV'den oku ve yükle
                created_count = 0
                with open(csv_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        DentalTerm.objects.create(
                            title=row['title'],
                            description=row['description_tr'],
                            slug=row['slug']
                        )
                        created_count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Başarıyla {created_count} terim içe aktarıldı.'
                    )
                )

        except KeyError as e:
            raise CommandError(f'CSV dosyasında gerekli sütun bulunamadı: {e}')
        except Exception as e:
            raise CommandError(f'İçe aktarma hatası: {e}')
