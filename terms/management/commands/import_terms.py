import csv
from django.core.management.base import BaseCommand
from terms.models import DentalTerm

class Command(BaseCommand):
    help = "CSV dosyasından dental terimleri veritabanına aktarır."

    def handle(self, *args, **kwargs):
        DentalTerm.objects.all().delete()
        with open(r'C:\Users\seman\PycharmProjects\dentalsozluk\datas\veriler.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                DentalTerm.objects.create(
                    title=row['title'],
                    description=row['description_tr'],
                    slug=row['slug']
                )
        self.stdout.write(self.style.SUCCESS("Tüm terimler başarıyla içe aktarıldı."))
