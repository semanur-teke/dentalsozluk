document.addEventListener('DOMContentLoaded', function() {
  const toggle = document.getElementById('darkModeToggle');
  if (!toggle) return;

  // Load state
  const isDark = localStorage.getItem('darkMode') === 'enabled';
  if (isDark) {
    document.documentElement.classList.add('dark-mode');
    toggle.textContent = '☀️ ';
  }

  // Click handler
  toggle.addEventListener('click', () => {
    const enabled = document.documentElement.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', enabled ? 'enabled' : 'disabled');
    toggle.textContent = enabled ? '☀️ ' : '🌙';
  });
});

