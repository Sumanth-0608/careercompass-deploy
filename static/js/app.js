/**
 * CareerCompass Global Client JavaScript
 * Handles notifications, escaping, mobile navigation, navbar scroll effects, and shared utilities.
 */

// Safe HTML escaping utility to prevent XSS
function escapeHtml(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// Global Toast Notification Helper
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.setAttribute('role', 'alert');
  toast.innerHTML = `
    <span>${escapeHtml(message)}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 300);
  }, 4000);
}

// Sticky Navbar Scroll Listener for Glass Surface Transition
function initNavbarScroll() {
  const navbar = document.querySelector('.navbar');
  if (!navbar) return;

  const handleScroll = () => {
    if (window.scrollY > 15) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll(); // Initial check
}

// Mobile Menu Navigation Controller
function initMobileNav() {
  const toggleBtn = document.querySelector('.mobile-toggle');
  const navLinks = document.querySelector('.nav-links');

  if (!toggleBtn || !navLinks) return;

  const closeMenu = () => {
    if (navLinks.classList.contains('show')) {
      navLinks.classList.remove('show');
      toggleBtn.setAttribute('aria-expanded', 'false');
      toggleBtn.textContent = '☰';
    }
  };

  toggleBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    const isOpen = navLinks.classList.toggle('show');
    toggleBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    toggleBtn.textContent = isOpen ? '✕' : '☰';
  });

  // Close menu when a navigation item is selected
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      closeMenu();
    });
  });

  // Close when clicking outside of navbar
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.navbar') && navLinks.classList.contains('show')) {
      closeMenu();
    }
  });

  // Close on Escape key press
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && navLinks.classList.contains('show')) {
      closeMenu();
      toggleBtn.focus();
    }
  });
}

/**
 * Career Inspiration Quote Rotator
 */
async function initHomeCareerInspiration() {
  const card = document.getElementById('home-inspiration-card');
  if (!card) return;

  const quoteText = document.getElementById('home-quote-text');
  const quoteTip = document.getElementById('home-quote-tip');
  const quoteAction = document.getElementById('home-quote-action');
  const btnPrev = document.getElementById('home-btn-prev-quote');
  const btnNext = document.getElementById('home-btn-next-quote');

  let quotes = [];
  let currentIndex = 0;

  try {
    const res = await fetch('/api/quotes');
    const data = await res.json();
    if (res.ok && data.success && data.quotes && data.quotes.length > 0) {
      quotes = data.quotes;
    }
  } catch (e) {
    console.warn('Could not load quotes for home banner', e);
  }

  function renderQuote() {
    if (!quotes || quotes.length === 0) return;
    const q = quotes[currentIndex];
    card.style.opacity = '0.4';
    setTimeout(() => {
      if (quoteText) quoteText.textContent = `"${q.quote}"`;
      if (quoteTip) quoteTip.textContent = q.practical_tip;
      if (quoteAction) quoteAction.textContent = `👉 ${q.suggested_action}`;
      card.style.opacity = '1';
      card.style.transition = 'opacity 0.25s ease';
    }, 150);
  }

  if (btnPrev) {
    btnPrev.addEventListener('click', () => {
      if (quotes.length > 0) {
        currentIndex = (currentIndex - 1 + quotes.length) % quotes.length;
        renderQuote();
      }
    });
  }

  if (btnNext) {
    btnNext.addEventListener('click', () => {
      if (quotes.length > 0) {
        currentIndex = (currentIndex + 1) % quotes.length;
        renderQuote();
      }
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  initNavbarScroll();
  initMobileNav();
  initHomeCareerInspiration();
});
