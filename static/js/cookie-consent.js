// static/js/cookie-consent.js

document.addEventListener('DOMContentLoaded', () => {
  const BANNER_ID   = 'cookie-banner';
  const CONSENT_KEY = 'cookieConsent';

  const banner = document.getElementById(BANNER_ID);
  const saved  = localStorage.getItem(CONSENT_KEY);
  if (!saved) {
    // Banner’ı göster
    banner.classList.remove('hidden');
  } else {
    // Daha önce onay verilmişse, hemen yükle
    loadConditionalScripts(JSON.parse(saved));
  }

  // Buton event’leri
  document.getElementById('accept-all')
    .addEventListener('click', () => setConsent({ analytics: true, functional: true, targeting: true }));
  document.getElementById('accept-necessary')
    .addEventListener('click', () => setConsent({ analytics: false, functional: false, targeting: false }));
  document.getElementById('show-settings')
    .addEventListener('click', () => {
      alert('Çerez ayarları modalı henüz aktif değil.');
    });

  function setConsent({ analytics, functional, targeting }) {
    const consent = { necessary: true, analytics, functional, targeting };
    localStorage.setItem(CONSENT_KEY, JSON.stringify(consent));
    banner.classList.add('hidden');
    loadConditionalScripts(consent);
  }

  function loadConditionalScripts(consent) {
    // ANALYTICS izni varsa
    if (consent.analytics && window.GA_MEASUREMENT_ID) {
      // 1) gtag.js kütüphanesini yükle
      injectScript(
        'https://www.googletagmanager.com/gtag/js?id=' + window.GA_MEASUREMENT_ID
      );
      // 2) ardından config çağrısını yap
      injectInlineGAConfig();
    }
    // FONKSİYONEL script
    if (consent.functional && window.cookieConsentConfig.darkModeScript) {
      injectScript(window.cookieConsentConfig.darkModeScript);
    }
    // TARGETING script (isteğe bağlı)
    if (consent.targeting && window.cookieConsentConfig.targetingScript) {
      injectScript(window.cookieConsentConfig.targetingScript);
    }
  }

  function injectScript(src) {
    const s = document.createElement('script');
    s.src   = src;
    s.async = true;
    document.head.appendChild(s);
  }

  function injectInlineGAConfig() {
    const inline = document.createElement('script');
    inline.innerHTML = `
      window.dataLayer = window.dataLayer || [];
      function gtag(){ dataLayer.push(arguments); }
      gtag('js', new Date());
      gtag('config', '${window.GA_MEASUREMENT_ID}', { anonymize_ip: true });
    `;
    document.head.appendChild(inline);
  }
});
