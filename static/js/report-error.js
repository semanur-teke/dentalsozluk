// static/js/error-report.js - CSRF uyumlu düzeltilmiş kod

function getCookie(name) {
  let value = null;
  document.cookie.split(';').forEach(c => {
    c = c.trim();
    if (c.startsWith(name + '=')) value = decodeURIComponent(c.split('=')[1]);
  });
  return value;
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.error-report-form').forEach(form => {
    form.addEventListener('submit', e => {
      e.preventDefault();

      const honeypot = form.querySelector('input[name="honeypot"]').value;
      if (honeypot) return; // Bot kontrolü

      const termId = form.querySelector('input[name="term_id"]').value;
      const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

      // FormData kullanarak CSRF uyumlu gönderim
      const formData = new FormData();
      formData.append('term_id', termId);
      formData.append('honeypot', honeypot);
      formData.append('csrfmiddlewaretoken', csrfToken);

      // Butonu devre dışı bırak
      const btn = form.querySelector('.error-report-btn');
      const originalText = btn.textContent;
      btn.textContent = '⏳ Gönderiliyor...';
      btn.disabled = true;

      fetch('/report_error/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
        },
        body: formData  // JSON yerine FormData kullan
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          btn.textContent = '✅ Bildirildi';
          btn.classList.add('success');
        } else if (data.status === 'info') {
          btn.textContent = 'ℹ️ Zaten bildirilmiş';
          btn.classList.add('info');
        } else {
          btn.textContent = originalText;
          btn.disabled = false;
          alert(data.message || 'Bir hata oluştu.');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        btn.textContent = originalText;
        btn.disabled = false;
        alert('Sunucuya ulaşılamadı.');
      });
    });
  });
});

// Alternatif: URLSearchParams kullanarak
function reportErrorAlternative(termId, csrfToken, honeypot = '') {
  const params = new URLSearchParams();
  params.append('term_id', termId);
  params.append('honeypot', honeypot);
  params.append('csrfmiddlewaretoken', csrfToken);

  return fetch('/report_error/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': csrfToken,
    },
    body: params
  });
}

// Global hata yakalama için (opsiyonel)
window.addEventListener('error', function(event) {
  console.error('JavaScript hatası yakalandı:', event.error);
  // İsteğe bağlı olarak sunucuya hata raporu gönderebilirsiniz
});

// Promise rejection yakalama (opsiyonel)
window.addEventListener('unhandledrejection', function(event) {
  console.error('Promise rejection yakalandı:', event.reason);
});