# terms/views.py
import json
import logging

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, F, Func
from django.db.models.functions import Lower, Substr, Upper
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
from django_ratelimit.decorators import ratelimit

from .models import DentalTerm, ErrorReport

# Logger yapılandırması
logger = logging.getLogger(__name__)

app_name = 'terms'


def home(request):
    """Ana sayfa görünümü."""
    context = {
        'hide_search': True,
    }
    return render(request, 'home.html', context)

def hakkimizda(request):
    return render(request, 'static_pages/hakkimizda.html')

def cerez_politikasi(request):
    return render(request, 'static_pages/cerez_politikasi.html')

def gizlilik_ilkesi(request):
    return render(request, 'static_pages/gizlilik_ilkesi.html')

def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Disallow: /admin/\n"
        "Disallow: /report_error/\n"
        "Sitemap: https://www.dentalsozluk.com/sitemap.xml\n"
    )
    return HttpResponse(content, content_type="text/plain")


def search_results(request):
    query = request.GET.get('q', '')
    matched_term = None
    if query:
        matched_term = DentalTerm.objects.filter(
            Q(title__icontains=query) |
            Q(english_equivalent__icontains=query) |
            Q(latin_equivalent__icontains=query)
        ).first()
    return render(request, 'terms/search_results.html', {
        'query': query,
        'matched_term': matched_term,
    })




def term_detail(request, slug):
    term = get_object_or_404(DentalTerm, slug=slug)
    return render(request, 'terms/term_detail.html', {
        'term': term,
    })



@ratelimit(key='ip', rate='3/m', method='POST', block=True)
@require_POST
def report_error(request):
    """Terim hatası bildirimi endpoint'i."""
    if getattr(request, 'limited', False):
        logger.warning(f"Rate limit exceeded for IP: {request.META.get('REMOTE_ADDR')}")
        return JsonResponse({
            'status': 'error',
            'message': 'Çok sık deneme yaptınız. Lütfen 1 dakika bekleyin.'
        }, status=429)

    try:
        # Content-Type'a göre veri parse et
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body.decode('utf-8'))
                term_id = data.get('term_id')
                honeypot = data.get('honeypot', '')
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                logger.error(f"JSON parse error: {e}")
                term_id = request.POST.get('term_id')
                honeypot = request.POST.get('honeypot', '')
        else:
            term_id = request.POST.get('term_id')
            honeypot = request.POST.get('honeypot', '')

        # Session key oluştur
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

    except Exception as e:
        logger.error(f"Error parsing request data: {e}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': 'Geçersiz istek'}, status=400)

    # Bot kontrolü (honeypot)
    if honeypot:
        logger.warning(f"Bot detected from IP: {request.META.get('REMOTE_ADDR')}")
        return JsonResponse({'status': 'error', 'message': 'Bot tespit edildi'}, status=400)

    # term_id zorunlu
    if not term_id:
        logger.error("Missing term_id in request")
        return JsonResponse({'status': 'error', 'message': 'term_id eksik'}, status=400)

    try:
        term = DentalTerm.objects.get(pk=term_id)

        # Tekrar gönderim kontrolü (60 saniye)
        if ErrorReport.recently_reported(term_id, session_key, within_seconds=60):
            logger.info(f"Duplicate report attempt for term {term_id} from session {session_key}")
            return JsonResponse({'status': 'info', 'message': 'Zaten bildirildi'}, status=200)

        # Hata raporu oluştur
        ErrorReport.objects.create(
            term=term,
            honeypot=honeypot,
            session_key=session_key
        )

        logger.info(f"Error report created for term {term_id} (slug: {term.slug})")
        return JsonResponse({'status': 'success'})

    except DentalTerm.DoesNotExist:
        logger.error(f"Term not found: {term_id}")
        return JsonResponse({'status': 'error', 'message': 'Terim bulunamadı'}, status=404)
    except Exception as e:
        logger.error(f"Database error while creating error report: {e}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': 'Kayıt hatası'}, status=500)


def debug_count(request):
    """Debug: Toplam terim sayısını döndürür."""
    return JsonResponse({"count": DentalTerm.objects.count()})


def autocomplete_terms(request):
    """Arama kutusu için autocomplete önerileri."""
    q = (request.GET.get("q") or "").strip()
    if len(q) < 2:
        return JsonResponse([], safe=False)

    rows = (DentalTerm.objects
            .filter(
                Q(title__icontains=q) |
                Q(english_equivalent__icontains=q) |
                Q(latin_equivalent__icontains=q)
            )
            .order_by("title")
            .values("slug", "title")[:5])

    data = [{"title": r["title"],
             "url":  reverse("terms:term_detail", kwargs={"slug": r["slug"]})}
            for r in rows]
    return JsonResponse(data, safe=False)


RESULTS_PER_PAGE = 20

def _apply_alpha_filter(qs, letter: str):
    if not letter or letter.lower() == "all":
        return qs
    if letter == "0-9":
        return qs.filter(title__iregex=r"^[0-9]")
    # Lower(unaccent(title)) ile baş harf (index olmasa da çalışır)
    qs = qs.annotate(title_unaccent_lower=Lower(Func(F("title"), function="unaccent")))
    return qs.filter(title_unaccent_lower__startswith=letter.lower())

def _available_letters():
    letters = (
        DentalTerm.objects
        .annotate(first=Upper(Substr("title", 1, 1)))
        .values_list("first", flat=True)
        .distinct()
    )
    has_digit = any(l and l.isdigit() for l in letters)
    letters = sorted({l for l in letters if l and l.isalpha()})
    return letters, has_digit

def term_list(request):
    qs = (DentalTerm.objects
          .only("id","slug","title","english_equivalent","latin_equivalent","description")
          .order_by("title"))

    # GET parametreleri
    letter = request.GET.get("letter", "")
    q = (request.GET.get("q") or "").strip()

    # Harf filtresi
    qs = _apply_alpha_filter(qs, letter)

    # Basit metin arama
    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(english_equivalent__icontains=q) |
            Q(latin_equivalent__icontains=q)
        )

    # Sayfalama + elided range
    paginator   = Paginator(qs, RESULTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj    = paginator.get_page(page_number)
    page_range  = paginator.get_elided_page_range(number=page_obj.number, on_each_side=1, on_ends=1)

    # page dışındaki parametreleri koru
    preserved = request.GET.copy()
    preserved.pop("page", None)
    preserved_qs = preserved.urlencode()

    # Alfabe menüsü için mevcut harfler
    letters, has_digit = _available_letters()

    # DİKKAT: Template'in beklediği isimleri bozmayalım
    return render(request, 'terms/term_list.html', {
        'terms':         page_obj,        # template zaten bunu kullanıyordu
        'page_obj':      page_obj,
        'paginator':     paginator,
        'page_range':    page_range,
        'q':             q,
        'letter':        letter,
        'letters':       letters,
        'has_digit':     has_digit,
        'preserved_qs':  preserved_qs,
        'total_count':   paginator.count,
    })
