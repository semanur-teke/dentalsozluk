# terms/views.py

from django.shortcuts              import render, get_object_or_404
from django.core.paginator         import Paginator
from django.db.models              import Q
from django.http                   import JsonResponse
from django.views.decorators.http  import require_POST
from django.views.decorators.csrf  import csrf_exempt
import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import ErrorReport, DentalTerm
from django.http import HttpResponse


try:
    from ratelimit.decorators import ratelimit
    print("✅ ratelimit başarıyla yüklendi")
except ImportError as e:
    print(f"❌ ratelimit import hatası: {e}")
    def ratelimit(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

from django.shortcuts      import render
from django.core.paginator  import Paginator
from .models               import DentalTerm
from .models                       import DentalTerm, ErrorReport


app_name = 'terms'


from django.shortcuts import render


def home(request):
    context = {
        'hide_search': True,  # Bu satır navbar'daki arama kutusunu gizler
    }
    return render(request, 'home.html', context)


# Eğer class-based view kullanıyorsanız:
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'terms/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_search'] = True  # Bu satır navbar'daki arama kutusunu gizler
        return context


from django.shortcuts import render

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



def term_list(request):
    queryset   = DentalTerm.objects.all().order_by('title')
    paginator  = Paginator(queryset, 10)
    page_number= request.GET.get('page')
    page_terms = paginator.get_page(page_number)

    return render(request, 'terms/term_list.html', {
        'terms':    page_terms,   # ← template'in beklediği isim
        'page_obj': page_terms,   # ← paginasyon UI'si için opsiyonel
    })

def term_detail(request, slug):
    term = get_object_or_404(DentalTerm, slug=slug)
    return render(request, 'terms/term_detail.html', {
        'term': term,
    })



@ratelimit(key='ip', rate='5/m', method='POST', block=False)
@require_POST
def report_error(request):
    if getattr(request, 'limited', False):
        return JsonResponse({
            'status': 'error',
            'message': 'Çok sık deneme yaptınız. Lütfen 1 dakika bekleyin.'
        }, status=429)
    try:
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body.decode('utf-8'))
                term_id = data.get('term_id')
                honeypot = data.get('honeypot', '')
            except:
                term_id = request.POST.get('term_id')
                honeypot = request.POST.get('honeypot', '')
        else:
            term_id = request.POST.get('term_id')
            honeypot = request.POST.get('honeypot', '')

        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    if honeypot:
        return JsonResponse({'status': 'error', 'message': 'Bot tespit edildi'}, status=400)

    if not term_id:
        return JsonResponse({'status': 'error', 'message': 'term_id eksik'}, status=400)

    try:
        term = DentalTerm.objects.get(pk=term_id)

        # ✅ Tekrar gönderim kontrolü (örnek: 60 saniye)
        if ErrorReport.recently_reported(term_id, session_key, within_seconds=60):
            return JsonResponse({'status': 'info', 'message': 'Zaten bildirildi'}, status=200)

        ErrorReport.objects.create(
            term=term,
            honeypot=honeypot,
            session_key=session_key
        )

        return JsonResponse({'status': 'success'})
    except DentalTerm.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Terim bulunamadı'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'Kayıt hatası'}, status=500)
