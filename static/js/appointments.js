/**
 * CareerCompass — Real-Time Appointments & Mentorship Client Controller
 * Handles slot filtering, atomic reservation, double-booking prevention alerts,
 * and booking management (lookup and cancellation).
 */

let appState = {
  category: "All",
  format: "All",
  typeId: "All",
  date: "",
  includeBooked: false,
  allSlots: [],
  selectedSlot: null
};

document.addEventListener("DOMContentLoaded", () => {
  // Read URL query parameters
  const params = new URLSearchParams(window.location.search);
  if (params.has("category")) {
    appState.category = params.get("category");
  }
  if (params.has("format")) {
    appState.format = params.get("format");
  }
  if (params.has("type_id")) {
    appState.typeId = params.get("type_id");
  }
  if (params.has("date")) {
    appState.date = params.get("date");
    const dateInput = document.getElementById("filter-date-input");
    if (dateInput) dateInput.value = appState.date;
  }

  // Initialize Glassmorphism Custom Dropdowns
  initGlassDropdowns();

  // Sync initial query param states to glass dropdowns
  if (appState.category && appState.category !== "All") {
    syncGlassDropdown("dropdown-category", appState.category);
  }
  if (appState.format && appState.format !== "All") {
    syncGlassDropdown("dropdown-format", appState.format);
  }
  if (appState.typeId && appState.typeId !== "All") {
    syncGlassDropdown("dropdown-type", appState.typeId);
  }

  loadSlots();
});

// Tab Switcher
function switchAppointmentTab(tabName) {
  const scheduleTab = document.getElementById("tab-schedule-content");
  const manageTab = document.getElementById("tab-manage-content");
  const btnSchedule = document.getElementById("tab-btn-schedule");
  const btnManage = document.getElementById("tab-btn-manage");

  if (tabName === "schedule") {
    scheduleTab.style.display = "block";
    manageTab.style.display = "none";
    btnSchedule.classList.add("btn-primary");
    btnSchedule.classList.remove("btn-outline");
    btnManage.classList.add("btn-outline");
    btnManage.classList.remove("btn-primary");
  } else {
    scheduleTab.style.display = "none";
    manageTab.style.display = "block";
    btnManage.classList.add("btn-primary");
    btnManage.classList.remove("btn-outline");
    btnSchedule.classList.add("btn-outline");
    btnSchedule.classList.remove("btn-primary");
  }
}

// ---------------------------------------------------------------------------
// Glassmorphism Custom Dropdown Manager
// ---------------------------------------------------------------------------
function initGlassDropdowns() {
  const dropdowns = document.querySelectorAll(".glass-dropdown");

  dropdowns.forEach(dd => {
    const trigger = dd.querySelector(".glass-dropdown-trigger");
    const menu = dd.querySelector(".glass-dropdown-menu");
    const options = dd.querySelectorAll(".glass-dropdown-option");
    const valueDisplay = dd.querySelector(".glass-dropdown-value");

    if (!trigger || !menu) return;

    // Trigger button toggle
    trigger.addEventListener("click", (e) => {
      e.stopPropagation();
      const isOpen = dd.classList.contains("open");
      
      // Close all other dropdowns
      closeAllGlassDropdowns();

      if (!isOpen) {
        dd.classList.add("open");
        trigger.setAttribute("aria-expanded", "true");
        dd.setAttribute("aria-expanded", "true");
        // Focus currently selected option or first option
        const selectedOpt = dd.querySelector(".glass-dropdown-option.selected") || options[0];
        if (selectedOpt) selectedOpt.focus();
      }
    });

    // Options selection
    options.forEach(opt => {
      opt.addEventListener("click", (e) => {
        e.stopPropagation();
        selectGlassOption(dd, opt);
      });

      // Keyboard navigation on individual option
      opt.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          selectGlassOption(dd, opt);
        } else if (e.key === "ArrowDown") {
          e.preventDefault();
          const next = opt.nextElementSibling;
          if (next && next.classList.contains("glass-dropdown-option")) {
            next.focus();
          }
        } else if (e.key === "ArrowUp") {
          e.preventDefault();
          const prev = opt.previousElementSibling;
          if (prev && prev.classList.contains("glass-dropdown-option")) {
            prev.focus();
          } else {
            trigger.focus();
          }
        } else if (e.key === "Escape") {
          e.preventDefault();
          closeAllGlassDropdowns();
          trigger.focus();
        } else if (e.key === "Tab") {
          closeAllGlassDropdowns();
        }
      });
    });

    // Trigger keydown
    trigger.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown" || e.key === "Enter" || e.key === " ") {
        if (!dd.classList.contains("open")) {
          e.preventDefault();
          closeAllGlassDropdowns();
          dd.classList.add("open");
          trigger.setAttribute("aria-expanded", "true");
          dd.setAttribute("aria-expanded", "true");
          const selectedOpt = dd.querySelector(".glass-dropdown-option.selected") || options[0];
          if (selectedOpt) setTimeout(() => selectedOpt.focus(), 20);
        }
      } else if (e.key === "Escape") {
        closeAllGlassDropdowns();
      }
    });
  });

  // Global Outside-Click & Escape dismiss handler (idempotent listener)
  if (!window._glassDropdownsBound) {
    document.addEventListener("click", (e) => {
      if (!e.target.closest(".glass-dropdown")) {
        closeAllGlassDropdowns();
      }
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        closeAllGlassDropdowns();
      }
    });

    window._glassDropdownsBound = true;
  }
}

function closeAllGlassDropdowns() {
  document.querySelectorAll(".glass-dropdown.open").forEach(dd => {
    dd.classList.remove("open");
    const trigger = dd.querySelector(".glass-dropdown-trigger");
    if (trigger) trigger.setAttribute("aria-expanded", "false");
    dd.setAttribute("aria-expanded", "false");
  });
}

function selectGlassOption(dd, opt) {
  const val = opt.getAttribute("data-value");
  const optTextEl = opt.querySelector(".opt-text");
  const displayLabel = optTextEl ? optTextEl.textContent.trim() : opt.textContent.trim();
  const valueDisplay = dd.querySelector(".glass-dropdown-value");
  const trigger = dd.querySelector(".glass-dropdown-trigger");

  // Update label
  if (valueDisplay) {
    valueDisplay.textContent = displayLabel;
  }

  // Update selection styling
  dd.querySelectorAll(".glass-dropdown-option").forEach(o => {
    o.classList.remove("selected");
    o.setAttribute("aria-selected", "false");
  });
  opt.classList.add("selected");
  opt.setAttribute("aria-selected", "true");

  // Close dropdown
  dd.classList.remove("open");
  if (trigger) {
    trigger.setAttribute("aria-expanded", "false");
    trigger.focus();
  }
  dd.setAttribute("aria-expanded", "false");

  // Dispatch filter action based on dropdown ID
  if (dd.id === "dropdown-category") {
    appState.category = val;
    // Sync category pills
    document.querySelectorAll("#category-filter-pills .filter-pill").forEach(p => {
      if (p.getAttribute("data-category") === val) p.classList.add("active");
      else p.classList.remove("active");
    });
    loadSlots();
  } else if (dd.id === "dropdown-format") {
    appState.format = val;
    const formatSelect = document.getElementById("filter-format-select");
    if (formatSelect) formatSelect.value = val;
    loadSlots();
  } else if (dd.id === "dropdown-type") {
    appState.typeId = val;
    const typeSelect = document.getElementById("filter-type-select");
    if (typeSelect) typeSelect.value = val;
    loadSlots();
  }
}

function syncGlassDropdown(dropdownId, value) {
  const dd = document.getElementById(dropdownId);
  if (!dd) return;

  const options = dd.querySelectorAll(".glass-dropdown-option");
  let found = false;

  options.forEach(opt => {
    const optVal = opt.getAttribute("data-value");
    if (optVal === String(value)) {
      found = true;
      opt.classList.add("selected");
      opt.setAttribute("aria-selected", "true");
      const optTextEl = opt.querySelector(".opt-text");
      const label = optTextEl ? optTextEl.textContent.trim() : opt.textContent.trim();
      const valDisplay = dd.querySelector(".glass-dropdown-value");
      if (valDisplay) valDisplay.textContent = label;
    } else {
      opt.classList.remove("selected");
      opt.setAttribute("aria-selected", "false");
    }
  });

  if (!found && value === "All") {
    const firstOpt = options[0];
    if (firstOpt) {
      firstOpt.classList.add("selected");
      firstOpt.setAttribute("aria-selected", "true");
      const valDisplay = dd.querySelector(".glass-dropdown-value");
      if (valDisplay) valDisplay.textContent = firstOpt.textContent.trim();
    }
  }
}

// Filter setters
function setFilterCategory(cat) {
  appState.category = cat;
  // Update pill styles
  document.querySelectorAll("#category-filter-pills .filter-pill").forEach(p => {
    if (p.getAttribute("data-category") === cat) {
      p.classList.add("active");
    } else {
      p.classList.remove("active");
    }
  });
  // Sync category glass dropdown
  syncGlassDropdown("dropdown-category", cat);
  loadSlots();
}

function handleDateChange(val) {
  appState.date = val;
  loadSlots();
}

function clearDateFilter() {
  appState.date = "";
  const dateInput = document.getElementById("filter-date-input");
  if (dateInput) dateInput.value = "";
  loadSlots();
}

function handleFormatChange(val) {
  appState.format = val;
  syncGlassDropdown("dropdown-format", val);
  loadSlots();
}

function handleTypeChange(val) {
  appState.typeId = val;
  syncGlassDropdown("dropdown-type", val);
  loadSlots();
}

function toggleIncludeBooked(checked) {
  appState.includeBooked = checked;
  loadSlots();
}

function resetAllFilters() {
  appState.category = "All";
  appState.format = "All";
  appState.typeId = "All";
  appState.date = "";
  appState.includeBooked = false;

  const dateInput = document.getElementById("filter-date-input");
  if (dateInput) dateInput.value = "";
  const formatSelect = document.getElementById("filter-format-select");
  if (formatSelect) formatSelect.value = "All";
  const typeSelect = document.getElementById("filter-type-select");
  if (typeSelect) typeSelect.value = "All";
  const bookedCheck = document.getElementById("show-booked-checkbox");
  if (bookedCheck) bookedCheck.checked = false;

  document.querySelectorAll("#category-filter-pills .filter-pill").forEach(p => {
    if (p.getAttribute("data-category") === "All") p.classList.add("active");
    else p.classList.remove("active");
  });

  // Sync all glass dropdowns back to All
  syncGlassDropdown("dropdown-category", "All");
  syncGlassDropdown("dropdown-format", "All");
  syncGlassDropdown("dropdown-type", "All");

  loadSlots();
}

// Fetch Slots from API
async function loadSlots() {
  const countDisplay = document.getElementById("slots-count-display");
  const grid = document.getElementById("slots-grid-container");
  const emptyState = document.getElementById("slots-empty-state");

  if (countDisplay) countDisplay.textContent = "Checking live availability...";

  const queryParams = new URLSearchParams();
  if (appState.category && appState.category !== "All") {
    queryParams.append("category", appState.category);
  }
  if (appState.date) {
    queryParams.append("date", appState.date);
  }
  if (appState.typeId && appState.typeId !== "All") {
    queryParams.append("type_id", appState.typeId);
  }
  if (appState.includeBooked) {
    queryParams.append("include_booked", "1");
  }

  try {
    const res = await fetch(`/api/appointments/slots?${queryParams.toString()}`);
    const data = await res.json();

    if (!data.success) {
      if (countDisplay) countDisplay.textContent = "Error loading appointments.";
      return;
    }

    let slots = data.slots || [];

    // Client-side format filter if needed
    if (appState.format && appState.format !== "All") {
      slots = slots.filter(s => s.type_format === appState.format);
    }

    appState.allSlots = slots;

    if (countDisplay) {
      countDisplay.textContent = `${slots.length} session ${slots.length === 1 ? 'slot' : 'slots'} available for booking`;
    }

    if (slots.length === 0) {
      grid.innerHTML = "";
      emptyState.style.display = "block";
    } else {
      emptyState.style.display = "none";
      renderSlots(slots);
    }
  } catch (err) {
    console.error("Error fetching appointment slots:", err);
    if (countDisplay) countDisplay.textContent = "Could not connect to appointment service.";
  }
}

// Render Slots Grid
function renderSlots(slots) {
  const grid = document.getElementById("slots-grid-container");
  if (!grid) return;

  grid.innerHTML = slots.map(slot => {
    const isBooked = slot.is_booked === 1 || slot.status === "booked";
    const dateFormatted = formatSlotDate(slot.slot_date);
    const badgeCategory = getCategoryBadgeClass(slot.type_category);

    return `
      <div class="card glass-card apt-slot-card ${isBooked ? 'slot-booked' : ''}">
        
        <!-- Slot Header: Date & Time -->
        <div class="slot-datetime-bar">
          <div style="display: flex; align-items: center; gap: 0.4rem;">
            <span style="font-size: 1rem;">📅</span>
            <span style="font-weight: 800; font-size: 0.95rem; color: var(--text-heading);">${dateFormatted}</span>
          </div>
          <div class="slot-time-badge">
            ⏰ ${slot.start_time} – ${slot.end_time}
          </div>
        </div>

        <!-- Session Meta -->
        <div style="margin: 0.85rem 0 0.65rem;">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem; margin-bottom: 0.35rem;">
            <span class="badge ${badgeCategory}" style="font-size: 0.72rem;">${slot.type_category}</span>
            <span style="font-size: 0.78rem; font-weight: 700; color: var(--text-subtle);">⏱️ ${slot.duration_minutes}m · ${slot.type_format}</span>
          </div>
          <h4 style="font-size: 1.1rem; color: var(--text-heading); margin: 0 0 0.35rem; line-height: 1.35;">
            ${slot.type_icon || '📅'} ${slot.type_title}
          </h4>
          <p style="font-size: 0.86rem; color: var(--text-muted); line-height: 1.45; margin: 0;">
            ${slot.type_short_desc || ''}
          </p>
        </div>

        <!-- Mentor / Practitioner Details -->
        <div class="slot-provider-box">
          <div class="provider-avatar" style="background: ${slot.provider_avatar_bg || '#2563EB'};">
            ${slot.provider_initials || 'CC'}
          </div>
          <div style="flex: 1; min-width: 0;">
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 0.25rem;">
              <span style="font-weight: 700; font-size: 0.9rem; color: var(--text-heading); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                ${slot.provider_name}
              </span>
              <span style="font-size: 0.78rem; font-weight: 800; color: #D97706;">⭐ ${slot.provider_rating || '4.9'}</span>
            </div>
            <div style="font-size: 0.78rem; color: var(--text-muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
              ${slot.provider_title} · ${slot.provider_org}
            </div>
            <div style="margin-top: 0.25rem;">
              <span class="badge ${slot.provider_verified ? 'badge-verified' : 'badge-demo'}" style="font-size: 0.7rem; padding: 0.15rem 0.45rem;">
                ${slot.provider_verified ? '🛡️ ' : '🧪 '}${slot.provider_badge}
              </span>
            </div>
          </div>
        </div>

        <!-- Card Footer & Action -->
        <div class="slot-action-row" style="margin-top: 1rem; display: flex; justify-content: space-between; align-items: center; padding-top: 0.75rem; border-top: 1px solid rgba(37,99,235,0.1);">
          <div>
            <span style="font-size: 0.78rem; font-weight: 700; color: #059669;">
              ✅ ${slot.cost_label || 'Free / Institutional Subsidy'}
            </span>
          </div>

          ${isBooked ? `
            <span class="badge badge-muted" style="padding: 0.45rem 0.85rem; font-size: 0.82rem;">
              Already Reserved
            </span>
          ` : `
            <button type="button" class="btn btn-sm btn-primary" onclick="openBookingModal(${slot.id})" style="padding: 0.4rem 0.95rem;">
              Book This Slot &rarr;
            </button>
          `}
        </div>

      </div>
    `;
  }).join("");
}

// Helpers
function formatSlotDate(isoDateStr) {
  if (!isoDateStr) return "";
  try {
    const parts = isoDateStr.split("-");
    const d = new Date(parts[0], parts[1] - 1, parts[2]);
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const diffDays = Math.round((d - today) / (1000 * 60 * 60 * 24));
    const weekday = d.toLocaleDateString("en-US", { weekday: "short" });
    const month = d.toLocaleDateString("en-US", { month: "short" });
    const dayNum = d.getDate();

    if (diffDays === 0) return `Today (${weekday}, ${month} ${dayNum})`;
    if (diffDays === 1) return `Tomorrow (${weekday}, ${month} ${dayNum})`;
    return `${weekday}, ${month} ${dayNum}`;
  } catch (e) {
    return isoDateStr;
  }
}

function getCategoryBadgeClass(category) {
  if (!category) return "badge-blue";
  if (category.includes("Guidance")) return "badge-blue";
  if (category.includes("Interview")) return "badge-purple";
  if (category.includes("Employment") || category.includes("Internship")) return "badge-mint";
  if (category.includes("Parent")) return "badge-gold";
  return "badge-blue";
}

// Booking Modal Logic
function openBookingModal(slotId) {
  const slot = appState.allSlots.find(s => s.id === slotId);
  if (!slot) return;

  appState.selectedSlot = slot;

  document.getElementById("form-slot-id").value = slot.id;
  document.getElementById("modal-type-icon").textContent = slot.type_icon || "📅";
  document.getElementById("modal-type-title").textContent = slot.type_title;
  document.getElementById("modal-type-meta").textContent = `${slot.type_category} · ${slot.duration_minutes} mins · ${slot.type_format}`;
  document.getElementById("modal-slot-datetime").textContent = `${formatSlotDate(slot.slot_date)} · ${slot.start_time} – ${slot.end_time}`;
  document.getElementById("modal-provider-name").textContent = slot.provider_name;
  
  const badgeEl = document.getElementById("modal-provider-badge");
  if (badgeEl) {
    badgeEl.className = slot.provider_verified ? "badge badge-verified" : "badge badge-demo";
    badgeEl.textContent = slot.provider_verified ? `🛡️ ${slot.provider_badge}` : `🧪 ${slot.provider_badge}`;
  }

  // Reset form views
  document.getElementById("booking-modal-form-view").style.display = "block";
  document.getElementById("booking-modal-success-view").style.display = "none";
  const submitBtn = document.getElementById("submit-booking-btn");
  submitBtn.disabled = false;
  submitBtn.innerHTML = `<span>Lock &amp; Confirm Booking</span>`;

  const modal = document.getElementById("booking-modal");
  modal.style.display = "block";
  modal.setAttribute("aria-hidden", "false");
}

function closeBookingModal() {
  const modal = document.getElementById("booking-modal");
  modal.style.display = "none";
  modal.setAttribute("aria-hidden", "true");
}

// Submit Booking Form with Atomic Double-Booking Check
async function handleBookingSubmit(event) {
  event.preventDefault();

  const submitBtn = document.getElementById("submit-booking-btn");
  submitBtn.disabled = true;
  submitBtn.innerHTML = `<span>⏳ Reserving slot...</span>`;

  const payload = {
    slot_id: parseInt(document.getElementById("form-slot-id").value, 10),
    student_name: document.getElementById("form-student-name").value.trim(),
    student_email: document.getElementById("form-student-email").value.trim(),
    student_phone: document.getElementById("form-student-phone").value.trim(),
    education_level: document.getElementById("form-education-level").value,
    current_career_interest: document.getElementById("form-career-interest").value.trim(),
    notes_or_questions: document.getElementById("form-notes").value.trim()
  };

  try {
    const res = await fetch("/api/appointments/book", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const result = await res.json();

    if (res.status === 409 || !result.success) {
      // Double-booking collision or validation error
      alert(`⚠️ Reservation Notice:\n${result.error || "This slot was just reserved by another user. The schedule will now refresh."}`);
      closeBookingModal();
      loadSlots();
      return;
    }

    // Success: Show confirmation view
    const booking = result.booking;
    document.getElementById("booking-modal-form-view").style.display = "none";
    document.getElementById("booking-modal-success-view").style.display = "block";

    document.getElementById("success-booking-ref").textContent = booking.booking_ref;
    document.getElementById("success-type-title").textContent = booking.type_title;
    document.getElementById("success-datetime").textContent = `${formatSlotDate(booking.slot_date)} from ${booking.start_time} to ${booking.end_time}`;
    document.getElementById("success-provider").textContent = `${booking.provider_name} (${booking.provider_title})`;
    document.getElementById("success-meeting-mode").textContent = booking.meeting_mode;

  } catch (err) {
    console.error("Booking error:", err);
    alert("An error occurred while booking. Please try again.");
    submitBtn.disabled = false;
    submitBtn.innerHTML = `<span>Lock &amp; Confirm Booking</span>`;
  }
}

function copyBookingRef() {
  const refText = document.getElementById("success-booking-ref").textContent;
  if (navigator.clipboard) {
    navigator.clipboard.writeText(refText).then(() => {
      alert(`Booking reference ${refText} copied to clipboard!`);
    });
  } else {
    alert(`Reference: ${refText}`);
  }
}

// Manage / Lookup Bookings
async function handleManageLookup(event) {
  event.preventDefault();
  const input = document.getElementById("manage-lookup-input").value.trim();
  const resultsContainer = document.getElementById("manage-results-container");

  resultsContainer.innerHTML = `<p style="text-align: center; color: var(--text-muted);">Searching records...</p>`;

  let url = "/api/appointments/my-bookings?";
  if (input.includes("@")) {
    url += `email=${encodeURIComponent(input)}`;
  } else {
    url += `ref=${encodeURIComponent(input)}`;
  }

  try {
    const res = await fetch(url);
    const data = await res.json();

    if (!data.success || !data.bookings || data.bookings.length === 0) {
      resultsContainer.innerHTML = `
        <div class="card glass-card" style="text-align: center; padding: 2rem;">
          <p style="color: var(--text-muted); margin: 0;">No active bookings found for "${input}". Please check your email or booking reference code.</p>
        </div>
      `;
      return;
    }

    resultsContainer.innerHTML = data.bookings.map(b => {
      const isCancelled = b.status === "cancelled";
      return `
        <div class="card glass-card" style="margin-bottom: 1.25rem; padding: 1.5rem; border-left: 4px solid ${isCancelled ? '#9CA3AF' : '#2563EB'};">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; flex-wrap: wrap;">
            <div>
              <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.35rem;">
                <span style="font-family: monospace; font-weight: 800; font-size: 1.1rem; color: var(--primary-blue);">${b.booking_ref}</span>
                <span class="badge ${isCancelled ? 'badge-muted' : 'badge-mint'}">${b.status.toUpperCase()}</span>
              </div>
              <h4 style="margin: 0 0 0.25rem; color: var(--text-heading); font-size: 1.15rem;">${b.type_title}</h4>
              <div style="font-size: 0.9rem; color: var(--text-muted);">
                📅 ${formatSlotDate(b.slot_date)} · ⏰ ${b.start_time} – ${b.end_time}
              </div>
              <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.35rem;">
                Practitioner: <strong>${b.provider_name}</strong> · ${b.provider_badge}
              </div>
            </div>

            <div style="display: flex; gap: 0.5rem; align-items: center;">
              ${!isCancelled ? `
                <button type="button" class="btn btn-sm btn-outline" style="color: #DC2626; border-color: rgba(220,38,38,0.3);" onclick="cancelBooking('${b.booking_ref}')">
                  Cancel Session
                </button>
              ` : `
                <span style="font-size: 0.8rem; color: var(--text-subtle);">Cancelled on ${b.cancelled_at ? b.cancelled_at.split('T')[0] : ''}</span>
              `}
            </div>
          </div>
        </div>
      `;
    }).join("");

  } catch (err) {
    console.error("Lookup error:", err);
    resultsContainer.innerHTML = `<p style="text-align: center; color: #DC2626;">Error retrieving booking records.</p>`;
  }
}

// Cancel Booking
async function cancelBooking(bookingRef) {
  if (!confirm(`Are you sure you want to cancel booking ${bookingRef}? This will release the slot back into the calendar for other students.`)) {
    return;
  }

  try {
    const res = await fetch("/api/appointments/cancel", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ booking_ref: bookingRef })
    });

    const data = await res.json();
    if (!data.success) {
      alert(`Could not cancel: ${data.error}`);
      return;
    }

    alert(`✅ ${data.message}`);
    // Refresh manage lookup results
    const input = document.getElementById("manage-lookup-input");
    if (input && input.value) {
      handleManageLookup(new Event("submit"));
    }
    // Refresh schedule slots
    loadSlots();

  } catch (err) {
    console.error("Cancellation error:", err);
    alert("An error occurred during cancellation.");
  }
}
