// static/js/cookie-consent.js

document.addEventListener('DOMContentLoaded', () => {
  const BANNER_ID   = 'cookie-banner';
  const CONSENT_KEY = 'cookieConsent';

  const banner = document.getElementById(BANNER_ID);
  const saved = localStorage.getItem(CONSENT_KEY);
  if (!saved) banner.classList.remove('hidden');

  // Button’lar
  document.getElementById('accept-all')
    .addEventListener('click', () => setConsent({ analytics: true, functional: true, targeting: true }));
  document.getElementById('accept-necessary')
    .addEventListener('click', () => setConsent({ analytics: false, functional: false, targeting: false }));
  document.getElementById('show-settings')
    .addEventListener('click', () => {
      // Eğer ileride detaylı modal ekleyecekseniz burayı kullanın.
      alert('Çerez ayarları modalı henüz aktif değil.');
    });

  function setConsent({ analytics, functional, targeting }) {
    // Zorunlu her zaman true
    const consent = { necessary: true, analytics, functional, targeting };
    localStorage.setItem(CONSENT_KEY, JSON.stringify(consent));
    banner.classList.add('hidden');
    loadConditionalScripts(consent);
  }

function loadConditionalScripts(consent) {
  if (consent.analytics) {
    injectScript('https://www.googletagmanager.com/gtm.js?id=GA_MEASUREMENT_ID');
  }
  if (consent.functional) {
    injectScript(window.cookieConsentConfig.darkModeScript);
  }
  if (consent.targeting) {
    // injectScript(window.cookieConsentConfig.targetingScript);
  }
}


  function injectScript(src) {
    const s = document.createElement('script');
    s.src = src;
    s.async = true;
    document.head.appendChild(s);
  }

  // Eğer sayfa yüklendiğinde zaten onay varsa, script’leri hemen yükle
  if (saved) {
    const consent = JSON.parse(saved);
    loadConditionalScripts(consent);
  }
});
