/**
 * CareerCompass Opportunities Controller
 * Handles location-aware discovery, category/type filtering,
 * voluntary geolocation with fallback, and Career Inspiration quote rotation.
 */

document.addEventListener('DOMContentLoaded', async () => {
  // DOM Elements
  const citySelect = document.getElementById('city-select');
  const customLocationInput = document.getElementById('custom-location-input');
  const btnGeolocation = document.getElementById('btn-geolocation');
  const workModeSelect = document.getElementById('work-mode-select');
  const searchInput = document.getElementById('search-input');
  const btnSearch = document.getElementById('btn-search');
  const locationStatusBar = document.getElementById('location-label-text');
  const oppCountBadge = document.getElementById('opp-count-badge');
  const categoryChips = document.getElementById('category-chips');
  const typeChips = document.getElementById('type-chips');
  const loadingEl = document.getElementById('loading-opportunities');
  const gridEl = document.getElementById('opportunities-grid');
  const emptyEl = document.getElementById('empty-opportunities');
  const btnResetFilters = document.getElementById('btn-reset-filters');

  // Quote Widget Elements
  const quoteText = document.getElementById('quote-text');
  const quoteTip = document.getElementById('quote-tip');
  const quoteAction = document.getElementById('quote-action');
  const btnPrevQuote = document.getElementById('btn-prev-quote');
  const btnNextQuote = document.getElementById('btn-next-quote');

  // State
  let activeCategory = 'All';
  let activeType = 'All';
  let activeCity = 'All Cities';
  let activeWorkMode = 'all';
  let activeSearch = '';
  let quotesList = [];
  let currentQuoteIndex = 0;

  // Initialize
  await initQuotes();
  await loadOpportunities();

  // --------------------------------------------------------------------------
  // Event Listeners for Filters
  // --------------------------------------------------------------------------

  // City dropdown
  citySelect.addEventListener('change', () => {
    activeCity = citySelect.value;
    customLocationInput.value = '';
    updateLocationLabel(`Selected: ${activeCity}`, 'Curated regional listings');
    loadOpportunities();
  });

  // Search button & Enter key
  btnSearch.addEventListener('click', () => {
    applySearchAndCustomLocation();
  });

  searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      applySearchAndCustomLocation();
    }
  });

  customLocationInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      applySearchAndCustomLocation();
    }
  });

  // Work mode select
  workModeSelect.addEventListener('change', () => {
    activeWorkMode = workModeSelect.value;
    loadOpportunities();
  });

  // Category chips
  categoryChips.querySelectorAll('.chip-label').forEach(chip => {
    chip.addEventListener('click', () => {
      categoryChips.querySelectorAll('.chip-label').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeCategory = chip.dataset.category;
      loadOpportunities();
    });
  });

  // Type chips
  typeChips.querySelectorAll('.chip-label').forEach(chip => {
    chip.addEventListener('click', () => {
      typeChips.querySelectorAll('.chip-label').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeType = chip.dataset.type;
      loadOpportunities();
    });
  });

  // Reset filters
  if (btnResetFilters) {
    btnResetFilters.addEventListener('click', () => {
      resetFilters();
    });
  }

  // Voluntary Geolocation Auto-Detect
  btnGeolocation.addEventListener('click', () => {
    handleVoluntaryGeolocation();
  });

  function applySearchAndCustomLocation() {
    activeSearch = searchInput.value.trim();
    const customLoc = customLocationInput.value.trim();
    if (customLoc) {
      activeCity = customLoc;
      citySelect.value = 'All Cities';
      updateLocationLabel(`Location provided by user: "${customLoc}"`, 'Search area configured manually');
    } else {
      activeCity = citySelect.value;
    }
    loadOpportunities();
  }

  function resetFilters() {
    activeCategory = 'All';
    activeType = 'All';
    activeCity = 'All Cities';
    activeWorkMode = 'all';
    activeSearch = '';

    citySelect.value = 'All Cities';
    customLocationInput.value = '';
    searchInput.value = '';
    workModeSelect.value = 'all';

    categoryChips.querySelectorAll('.chip-label').forEach(c => c.classList.remove('active'));
    categoryChips.querySelector('[data-category="All"]').classList.add('active');

    typeChips.querySelectorAll('.chip-label').forEach(c => c.classList.remove('active'));
    typeChips.querySelector('[data-type="All"]').classList.add('active');

    updateLocationLabel('All Cities & Remote', 'Location not independently tracked');
    loadOpportunities();
  }

  function updateLocationLabel(label, note) {
    if (locationStatusBar) {
      locationStatusBar.innerHTML = `
        ℹ️ Showing opportunities based on: <strong>${escapeHtml(label)}</strong> (${escapeHtml(note)})
      `;
    }
  }

  // --------------------------------------------------------------------------
  // Voluntary Geolocation Handler (Non-blocking with courteous fallback)
  // --------------------------------------------------------------------------
  function handleVoluntaryGeolocation() {
    if (!('geolocation' in navigator)) {
      showToast('Geolocation is not supported by your browser. Please select your city from the dropdown.', 'info');
      return;
    }

    btnGeolocation.disabled = true;
    btnGeolocation.textContent = '📍 Locating...';

    navigator.geolocation.getCurrentPosition(
      (position) => {
        btnGeolocation.disabled = false;
        btnGeolocation.textContent = '📍 Auto-Detect';

        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        // Approximate major Indian city regions by coordinates
        const approximatedCity = approximateIndianCity(lat, lon);
        activeCity = approximatedCity;
        customLocationInput.value = approximatedCity;
        updateLocationLabel(`Detected via browser: ${approximatedCity}`, 'Approximate coordinates provided with permission');
        showToast(`Location detected: ${approximatedCity}`, 'success');
        loadOpportunities();
      },
      (error) => {
        btnGeolocation.disabled = false;
        btnGeolocation.textContent = '📍 Auto-Detect';
        // Graceful error handling - never breaks website
        if (error.code === error.PERMISSION_DENIED) {
          showToast('Location access was denied. You can voluntarily enter or choose your city anytime.', 'info');
          updateLocationLabel('Manual selection active (Location permission denied)', 'Website fully functional without GPS');
        } else {
          showToast('Could not retrieve current location. Please select your city from the list.', 'info');
        }
      },
      { timeout: 8000, maximumAge: 600000 }
    );
  }

  function approximateIndianCity(lat, lon) {
    // Metro reference centers with Euclidean distance approximation
    const centers = [
      { name: 'Delhi NCR', lat: 28.6139, lon: 77.2090 },
      { name: 'Bengaluru', lat: 12.9716, lon: 77.5946 },
      { name: 'Mumbai', lat: 19.0760, lon: 72.8777 },
      { name: 'Pune', lat: 18.5204, lon: 73.8567 },
      { name: 'Hyderabad', lat: 17.3850, lon: 78.4867 },
      { name: 'Chennai', lat: 13.0827, lon: 80.2707 },
      { name: 'Kolkata', lat: 22.5726, lon: 88.3639 },
      { name: 'Jaipur', lat: 26.9124, lon: 75.7873 },
      { name: 'Chandigarh', lat: 30.7333, lon: 76.7794 }
    ];

    let closest = centers[0];
    let minDistance = Infinity;

    centers.forEach(c => {
      const d = Math.hypot(c.lat - lat, c.lon - lon);
      if (d < minDistance) {
        minDistance = d;
        closest = c;
      }
    });

    // If within ~300km (approx 3 degrees)
    if (minDistance < 3.0) {
      return closest.name;
    }
    return 'Remote';
  }

  // --------------------------------------------------------------------------
  // Fetch & Render Opportunities
  // --------------------------------------------------------------------------
  async function loadOpportunities() {
    loadingEl.style.display = 'block';
    gridEl.style.display = 'none';
    emptyEl.style.display = 'none';

    try {
      const params = new URLSearchParams();
      if (activeCategory && activeCategory !== 'All') {
        params.append('category', activeCategory);
      }
      if (activeCity && activeCity !== 'All Cities') {
        params.append('location', activeCity);
      }
      if (activeWorkMode && activeWorkMode !== 'all') {
        params.append('work_mode', activeWorkMode);
      }
      if (activeType && activeType !== 'All') {
        params.append('type', activeType);
      }
      if (activeSearch) {
        params.append('q', activeSearch);
      }

      const res = await fetch(`/api/opportunities?${params.toString()}`);
      const data = await res.json();

      loadingEl.style.display = 'none';

      if (!res.ok || !data.success) {
        showToast('Could not load opportunities.', 'error');
        return;
      }

      const opps = data.opportunities || [];
      oppCountBadge.textContent = `${opps.length} Opportunities Found`;

      if (opps.length === 0) {
        emptyEl.style.display = 'block';
        return;
      }

      renderOpportunityCards(opps);
      gridEl.style.display = 'grid';

    } catch (err) {
      console.error('Error fetching opportunities:', err);
      loadingEl.style.display = 'none';
      emptyEl.style.display = 'block';
      showToast('Network error while loading opportunities.', 'error');
    }
  }

  function renderOpportunityCards(opps) {
    gridEl.innerHTML = '';

    opps.forEach(opp => {
      const card = document.createElement('div');
      card.className = 'card glass-card';
      card.style.display = 'flex';
      card.style.flexDirection = 'column';
      card.style.justifyContent = 'space-between';
      card.style.transition = 'var(--transition-smooth)';

      // Work mode styling
      let modeBadgeClass = 'badge-navy';
      if (opp.work_mode === 'remote') modeBadgeClass = 'badge-mint';
      else if (opp.work_mode === 'hybrid') modeBadgeClass = 'badge-primary';

      // Type badge color
      let typeBadge = 'badge-primary';
      if (opp.opportunity_type === 'Apprenticeship') typeBadge = 'badge-navy';
      else if (opp.opportunity_type === 'Part-Time') typeBadge = 'badge-mint';

      const skills = Array.isArray(opp.skills_required) ? opp.skills_required : [];

      card.innerHTML = `
        <div>
          <!-- Header Badges -->
          <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.85rem;">
            <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
              <span class="badge ${typeBadge}">${escapeHtml(opp.opportunity_type)}</span>
              <span class="badge ${modeBadgeClass}">📍 ${escapeHtml(opp.location_city)} (${escapeHtml(opp.work_mode.replace('_', ' '))})</span>
            </div>
            <span class="badge badge-success" title="Verified against official portal framework" style="font-size: 0.76rem;">
              ✓ Verified Portal
            </span>
          </div>

          <!-- Role Title & Source -->
          <h3 style="font-size: 1.25rem; margin-bottom: 0.35rem; color: var(--text-heading); line-height: 1.3;">
            ${escapeHtml(opp.title)}
          </h3>
          <div style="font-size: 0.88rem; font-weight: 700; color: var(--primary-blue); margin-bottom: 0.85rem;">
            🏛️ ${escapeHtml(opp.employer_or_source)}
          </div>

          <!-- Description -->
          <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 1rem;">
            ${escapeHtml(opp.description)}
          </p>

          <!-- Eligibility & Schedule -->
          <div style="background: rgba(255, 255, 255, 0.5); padding: 0.85rem; border-radius: var(--radius-sm); border: 1px solid var(--border-color); font-size: 0.84rem; margin-bottom: 1rem;">
            <div style="margin-bottom: 0.3rem;">
              <strong style="color: var(--text-heading);">Eligibility:</strong>
              <span style="color: var(--text-main);">${escapeHtml(opp.eligibility)}</span>
            </div>
            <div style="margin-bottom: 0.3rem;">
              <strong style="color: var(--text-heading);">Schedule:</strong>
              <span style="color: var(--text-main);">${escapeHtml(opp.schedule_type)}</span>
            </div>
            ${opp.stipend_or_compensation ? `
            <div>
              <strong style="color: var(--text-heading);">Compensation:</strong>
              <span style="color: #065F46; font-weight: 700;">${escapeHtml(opp.stipend_or_compensation)}</span>
            </div>` : ''}
          </div>

          <!-- Skills Chips -->
          <div style="margin-bottom: 1.25rem;">
            <div style="font-size: 0.78rem; font-weight: 700; color: var(--text-subtle); margin-bottom: 0.4rem; text-transform: uppercase;">
              Skills Recommended:
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 0.35rem;">
              ${skills.map(s => `<span class="badge badge-navy" style="font-size: 0.76rem;">${escapeHtml(s)}</span>`).join('')}
            </div>
          </div>
        </div>

        <!-- Card Footer -->
        <div style="padding-top: 1rem; border-top: 1px solid var(--border-color); display: flex; flex-direction: column; gap: 0.75rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.78rem; color: var(--text-subtle);">
            <span>Checked: ${escapeHtml(opp.last_verified || 'Recent')}</span>
            <span>Deadline: ${escapeHtml(opp.application_deadline || 'Rolling')}</span>
          </div>

          <div style="display: flex; gap: 0.5rem;">
            <a href="${escapeHtml(opp.official_url)}" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-sm" style="flex: 1; text-align: center;">
              Official Portal Application &rarr;
            </a>
            <button type="button" class="btn btn-outline btn-sm btn-bookmark" data-opp-id="${opp.id}" data-title="${escapeHtml(opp.title)}" title="Bookmark this opportunity">
              🔖 Bookmark
            </button>
          </div>
        </div>
      `;

      // Bookmark Handler
      const bookmarkBtn = card.querySelector('.btn-bookmark');
      bookmarkBtn.addEventListener('click', () => {
        const title = bookmarkBtn.dataset.title;
        saveBookmark(opp.id, title);
        bookmarkBtn.textContent = '✓ Saved';
        bookmarkBtn.classList.remove('btn-outline');
        bookmarkBtn.classList.add('btn-navy');
        showToast(`Saved "${title}" to your career planning bookmarks!`, 'success');
      });

      gridEl.appendChild(card);
    });
  }

  function saveBookmark(oppId, title) {
    try {
      const saved = JSON.parse(localStorage.getItem('careercompass_saved_opps') || '[]');
      if (!saved.some(o => o.id === oppId)) {
        saved.push({ id: oppId, title: title, saved_at: new Date().toISOString() });
        localStorage.setItem('careercompass_saved_opps', JSON.stringify(saved));
      }
    } catch (e) {
      console.warn('LocalStorage not available for bookmarks', e);
    }
  }

  // --------------------------------------------------------------------------
  // Career Inspiration Quote Widget
  // --------------------------------------------------------------------------
  async function initQuotes() {
    try {
      const res = await fetch('/api/quotes');
      const data = await res.json();
      if (res.ok && data.success && data.quotes && data.quotes.length > 0) {
        quotesList = data.quotes;
        renderCurrentQuote();
      }
    } catch (err) {
      console.warn('Could not load quotes:', err);
    }

    if (btnPrevQuote) {
      btnPrevQuote.addEventListener('click', () => {
        if (quotesList.length > 0) {
          currentQuoteIndex = (currentQuoteIndex - 1 + quotesList.length) % quotesList.length;
          renderCurrentQuote();
        }
      });
    }

    if (btnNextQuote) {
      btnNextQuote.addEventListener('click', () => {
        if (quotesList.length > 0) {
          currentQuoteIndex = (currentQuoteIndex + 1) % quotesList.length;
          renderCurrentQuote();
        }
      });
    }
  }

  function renderCurrentQuote() {
    if (!quotesList || quotesList.length === 0) return;
    const q = quotesList[currentQuoteIndex];

    // Smooth subtle opacity transition
    const card = document.getElementById('inspiration-card');
    if (card) card.style.opacity = '0.4';

    setTimeout(() => {
      quoteText.textContent = `"${q.quote}"`;
      quoteTip.textContent = q.practical_tip;
      quoteAction.textContent = `👉 ${q.suggested_action}`;
      if (card) {
        card.style.opacity = '1';
        card.style.transition = 'opacity 0.25s ease';
      }
    }, 150);
  }
});
