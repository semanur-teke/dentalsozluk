
from django.db import models
from django.utils.text import slugify

class DentalTerm(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    english_equivalent = models.CharField(max_length=100, blank=True, null=True)
    latin_equivalent = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while DentalTerm.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


from django.utils import timezone
from datetime import timedelta

class ErrorReport(models.Model):
    term = models.ForeignKey(DentalTerm, on_delete=models.CASCADE, related_name='error_reports')
    description = models.TextField(blank=True, help_text="(Opsiyonel) Hata hakkında ekstra bilgi")
    honeypot = models.CharField(max_length=100, blank=True, help_text="Bot kontrolü için gizli alan")
    session_key = models.CharField(max_length=40, blank=True, null=True, help_text="Kullanıcı oturumu için")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Hata bildirimi: {self.term.title} @ {self.created:%Y-%m-%d %H:%M}"

    @classmethod
    def recently_reported(cls, term_id, session_key, within_seconds=60):
        now = timezone.now()
        return cls.objects.filter(
            term_id=term_id,
            session_key=session_key,
            created__gte=now - timedelta(seconds=within_seconds)
        ).exists()
