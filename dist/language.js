(() => {
  const storageKey = 'quukk-language';
  const language = document.documentElement.lang.startsWith('en') ? 'en' : 'zh';
  const path = window.location.pathname;
  const englishPages = { '/': '/en/', '/index.html': '/en/', '/brand.html': '/en/brand.html' };
  const chinesePages = { '/en/': '/', '/en/index.html': '/', '/en/brand.html': '/brand.html' };
  const currentURL = new URL(window.location.href);
  const requestedLanguage = currentURL.searchParams.get('lang');
  const explicitChoice = requestedLanguage === 'zh' || requestedLanguage === 'en';

  if (explicitChoice) {
    try { localStorage.setItem(storageKey, requestedLanguage); } catch { /* URL remains authoritative. */ }
    const target = requestedLanguage === 'en' ? englishPages[path] : chinesePages[path];
    if (target) {
      window.location.replace(target + window.location.search + window.location.hash);
      return;
    }
  }

  // Explicit English URLs always work; returning to the default entry honors the saved choice.
  try {
    if (!explicitChoice && language === 'zh' && englishPages[path] && localStorage.getItem(storageKey) === 'en') {
      window.location.replace(englishPages[path] + window.location.search + window.location.hash);
      return;
    }
  } catch { /* Browsing and switching still work when storage is unavailable. */ }

  document.addEventListener('DOMContentLoaded', () => {
    const links = [...document.querySelectorAll('[data-language]')];
    currentURL.searchParams.delete('lang');
    function retainSection() {
      links.forEach(link => {
        link.search = currentURL.search;
        link.hash = window.location.hash;
      });
    }
    retainSection();
    window.addEventListener('hashchange', retainSection);
    links.forEach(link => {
      link.addEventListener('click', () => {
        try { localStorage.setItem(storageKey, link.dataset.language); } catch {
          // Even read-only storage must never trap a visitor in the previous language.
          const target = new URL(link.href);
          target.searchParams.set('lang', link.dataset.language);
          link.href = target.href;
        }
      });
    });
  });
})();
