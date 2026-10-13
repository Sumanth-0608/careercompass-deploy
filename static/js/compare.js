/**
 * CareerCompass Student–Parent Comparison Controller
 * Fosters constructive family dialogue with side-by-side career reality checks,
 * dynamic agreement mapping, and practical next steps.
 */

document.addEventListener('DOMContentLoaded', async () => {
  const form = document.getElementById('compare-form');
  const studentSelect = document.getElementById('student_career_id');
  const altSelect = document.getElementById('alternative_career_id');
  const studentReasonsInput = document.getElementById('student_reasons');
  const altReasonsInput = document.getElementById('alternative_reasons');
  const sharedSummaryInput = document.getElementById('shared_decision_summary');
  const resultContainer = document.getElementById('comparison-result');
  const compareCardsGrid = document.getElementById('compare-cards-grid');
  const questionsList = document.getElementById('discussion-questions-list');
  const savedBanner = document.getElementById('saved-bridge-banner');
  const bridgeIdText = document.getElementById('bridge-id-text');
  const btnSubmit = document.getElementById('btn-submit-compare');

  // Dynamic Alignment Checkboxes
  const sGoalBoxes = document.querySelectorAll('input[name="s_goal"]');
  const pWorryBoxes = document.querySelectorAll('input[name="p_worry"]');
  const alignmentPointsContainer = document.getElementById('alignment-points');

  const urlParams = new URLSearchParams(window.location.search);
  const comparisonId = window.CAREERCOMPASS_COMPARISON_ID || urlParams.get('comparison_id');
  const preStudentId = urlParams.get('student_career_id');
  const preAltId = urlParams.get('alternative_career_id');

  if (preStudentId) {
    studentSelect.value = preStudentId;
  }
  if (preAltId) {
    altSelect.value = preAltId;
  }

  // Set up dynamic alignment mapping updates
  sGoalBoxes.forEach(box => box.addEventListener('change', updateAlignmentMap));
  pWorryBoxes.forEach(box => box.addEventListener('change', updateAlignmentMap));
  updateAlignmentMap();

  // If existing comparison ID, load it
  if (comparisonId) {
    await loadComparison(comparisonId);
  }

  function updateAlignmentMap() {
    if (!alignmentPointsContainer) return;
    const selectedS = Array.from(sGoalBoxes).filter(b => b.checked).map(b => b.value);
    const selectedP = Array.from(pWorryBoxes).filter(b => b.checked).map(b => b.value);

    let mutualText = 'Both want long-term self-reliance, recognized skills, and sustainable financial peace of mind.';
    let bridgeText = 'Student seeks creative flexibility; Parents are worried about tuition loans or uncertain hiring cycles.';

    if (selectedS.includes('growth') && selectedP.includes('stability')) {
      bridgeText = 'Balance student excitement for high-growth tech with parent desire for accredited degree credentials and predictable campus hiring.';
    } else if (selectedS.includes('creativity') && selectedP.includes('tuition')) {
      bridgeText = 'Explore public/subsidized institutions, open learning portfolios, and state scholarships to relieve tuition anxiety while encouraging creative talent.';
    } else if (selectedS.includes('impact') && selectedP.includes('burnout')) {
      bridgeText = 'Discuss balanced pacing: pursuing impactful fields (civil/social) while planning manageable study hours and health boundaries.';
    }

    alignmentPointsContainer.innerHTML = `
      <div style="background: rgba(220,252,231,0.65); padding: 0.85rem; border-radius: var(--radius-sm); border: 1px solid rgba(34,197,94,0.3);">
        <strong style="color: #166534; font-size: 0.88rem;">🟢 Core Shared Ground:</strong>
        <p style="margin: 0.25rem 0 0; color: #166534; line-height: 1.4;">${escapeHtml(mutualText)}</p>
      </div>
      <div style="background: rgba(254,243,199,0.7); padding: 0.85rem; border-radius: var(--radius-sm); border: 1px solid rgba(245,158,11,0.3);">
        <strong style="color: #92400E; font-size: 0.88rem;">🟡 Practical Focus to Bridge:</strong>
        <p style="margin: 0.25rem 0 0; color: #92400E; line-height: 1.4;">${escapeHtml(bridgeText)}</p>
      </div>
    `;
  }

  async function loadComparison(id) {
    try {
      const res = await fetch(`/api/comparisons/${id}`);
      const data = await res.json();

      if (!res.ok || !data.success || !data.comparison) {
        showToast('Comparison record not found.', 'warning');
        return;
      }

      const comp = data.comparison;
      savedBanner.style.display = 'block';
      bridgeIdText.textContent = comp.id;

      studentSelect.value = comp.student_career_id;
      altSelect.value = comp.alternative_career_id;
      studentReasonsInput.value = comp.student_reasons || '';
      altReasonsInput.value = comp.alternative_reasons || '';
      sharedSummaryInput.value = comp.shared_decision_summary || '';

      renderComparisonDetails(comp);
    } catch (err) {
      console.error('Error loading comparison:', err);
      showToast('Could not load comparison record.', 'error');
    }
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const sId = parseInt(studentSelect.value, 10);
    const aId = parseInt(altSelect.value, 10);

    if (!sId || !aId) {
      showToast('Please select both careers to compare.', 'warning');
      return;
    }

    if (sId === aId) {
      showToast('Please choose two different career pathways to compare.', 'warning');
      return;
    }

    btnSubmit.disabled = true;
    btnSubmit.textContent = 'Generating Comparison... ⏳';

    const payload = {
      student_career_id: sId,
      alternative_career_id: aId,
      student_reasons: studentReasonsInput.value.trim(),
      alternative_reasons: altReasonsInput.value.trim(),
      shared_decision_summary: sharedSummaryInput.value.trim()
    };

    try {
      const res = await fetch('/api/comparisons', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      btnSubmit.disabled = false;
      btnSubmit.textContent = 'Generate Side-by-Side Comparison & Save Bridge 🚀';

      if (res.ok && data.success && data.comparison) {
        savedBanner.style.display = 'block';
        bridgeIdText.textContent = data.comparison.id;

        const newUrl = `${window.location.pathname}?comparison_id=${data.comparison.id}`;
        window.history.pushState({ path: newUrl }, '', newUrl);

        renderComparisonDetails(data.comparison);
        showToast('Comparison saved to SQLite! Side-by-side realities generated below.', 'success');

        resultContainer.scrollIntoView({ behavior: 'smooth' });
      } else {
        showToast(data.error || 'Failed to generate comparison.', 'error');
      }
    } catch (err) {
      console.error('Submission error:', err);
      btnSubmit.disabled = false;
      btnSubmit.textContent = 'Generate Side-by-Side Comparison & Save Bridge 🚀';
      showToast('Network error while saving comparison.', 'error');
    }
  });

  function renderComparisonDetails(comp) {
    resultContainer.style.display = 'block';

    const costComp = comp.cost_comparison || {};
    const sCost = costComp.student_career || {};
    const aCost = costComp.alternative_career || {};

    const sChallenges = comp.student_career_challenges || [];
    const aChallenges = comp.alternative_career_challenges || [];

    compareCardsGrid.innerHTML = `
      <!-- Student Choice Column -->
      <div class="card glass-card" style="border-top: 5px solid var(--primary-blue);">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
          <span class="badge badge-mint">Student Choice</span>
          <span class="badge badge-navy">${escapeHtml(comp.student_career_category)}</span>
        </div>
        <h3 style="font-size: 1.5rem; margin-bottom: 0.75rem; color: var(--text-heading);">${escapeHtml(comp.student_career_title)}</h3>

        <div style="background: rgba(255,255,255,0.6); padding: 1rem; border-radius: var(--radius-sm); margin-bottom: 1.25rem; border: 1px solid var(--border-color);">
          <strong style="font-size: 0.82rem; color: var(--text-subtle); text-transform: uppercase;">Student's Motivation:</strong>
          <p style="margin: 0.35rem 0 0; font-size: 0.95rem; color: var(--text-main); line-height: 1.5;">
            "${escapeHtml(comp.student_reasons || 'Excited by the domain problem-solving and creative growth.')}"
          </p>
        </div>

        <div style="margin-bottom: 1rem;">
          <strong style="font-size: 0.88rem; color: var(--deep-navy);">🎓 Education Pathway &amp; Entry:</strong>
          <p style="font-size: 0.88rem; color: var(--text-muted); margin: 0.25rem 0 0; line-height: 1.5;">
            ${escapeHtml(comp.student_career_education || 'Degree / Portfolio')}
          </p>
        </div>

        <div style="margin-bottom: 1rem;">
          <strong style="font-size: 0.88rem; color: var(--deep-navy);">💰 Estimated Tuition Realities:</strong>
          <p style="font-size: 0.88rem; color: var(--text-muted); margin: 0.25rem 0 0; line-height: 1.5;">
            ${escapeHtml(comp.student_career_cost || sCost.detail || 'Moderate')}
          </p>
          <div style="font-size: 0.82rem; color: var(--text-muted); background: var(--pale-blue); padding: 0.5rem 0.75rem; border-radius: var(--radius-sm); margin-top: 0.35rem; border: 1px solid rgba(59, 130, 246, 0.25);">
            🌱 <strong>Lower-Cost Route:</strong> ${escapeHtml(sCost.low_cost_routes || 'Open-source and government programs available.')}
          </div>
        </div>

        <div style="margin-bottom: 1rem;">
          <strong style="font-size: 0.88rem; color: var(--deep-navy);">🛠️ Transferable Skills:</strong>
          <p style="font-size: 0.84rem; color: var(--text-muted); margin: 0.25rem 0 0;">
            Problem Solving, Technical Analysis, Project Management, Digital Literacy.
          </p>
        </div>

        <div>
          <strong style="font-size: 0.88rem; color: #DC2626;">⚠️ Honest Realities &amp; Trade-offs:</strong>
          <ul style="padding-left: 1.2rem; font-size: 0.85rem; color: #9A3412; margin-top: 0.25rem; line-height: 1.6;">
            ${sChallenges.slice(0, 3).map(c => `<li>${escapeHtml(c)}</li>`).join('')}
          </ul>
        </div>
      </div>

      <!-- Alternative Choice Column -->
      <div class="card glass-card" style="border-top: 5px solid var(--deep-navy);">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
          <span class="badge badge-navy">Parent / Alternative Choice</span>
          <span class="badge badge-navy">${escapeHtml(comp.alternative_career_category)}</span>
        </div>
        <h3 style="font-size: 1.5rem; margin-bottom: 0.75rem; color: var(--text-heading);">${escapeHtml(comp.alternative_career_title)}</h3>

        <div style="background: rgba(255,255,255,0.6); padding: 1rem; border-radius: var(--radius-sm); margin-bottom: 1.25rem; border: 1px solid var(--border-color);">
          <strong style="font-size: 0.82rem; color: var(--text-subtle); text-transform: uppercase;">Parent's Perspective:</strong>
          <p style="margin: 0.35rem 0 0; font-size: 0.95rem; color: var(--text-main); line-height: 1.5;">
            "${escapeHtml(comp.alternative_reasons || 'Emphasizes long-term stability, recognizable degrees, and clear examination pathways.')}"
          </p>
        </div>

        <div style="margin-bottom: 1rem;">
          <strong style="font-size: 0.88rem; color: var(--deep-navy);">🎓 Education Pathway &amp; Entry:</strong>
          <p style="font-size: 0.88rem; color: var(--text-muted); margin: 0.25rem 0 0; line-height: 1.5;">
            ${escapeHtml(comp.alternative_career_education || 'Accredited degree / Licensure')}
          </p>
        </div>

        <div style="margin-bottom: 1rem;">
          <strong style="font-size: 0.88rem; color: var(--deep-navy);">💰 Estimated Tuition Realities:</strong>
          <p style="font-size: 0.88rem; color: var(--text-muted); margin: 0.25rem 0 0; line-height: 1.5;">
            ${escapeHtml(comp.alternative_career_cost || aCost.detail || 'Moderate')}
          </p>
          <div style="font-size: 0.82rem; color: var(--text-muted); background: var(--pale-blue); padding: 0.5rem 0.75rem; border-radius: var(--radius-sm); margin-top: 0.35rem; border: 1px solid rgba(59, 130, 246, 0.25);">
            🌱 <strong>Lower-Cost Route:</strong> ${escapeHtml(aCost.low_cost_routes || 'State universities or subsidized fees available.')}
          </div>
        </div>

        <div style="margin-bottom: 1rem;">
          <strong style="font-size: 0.88rem; color: var(--deep-navy);">🛠️ Transferable Skills:</strong>
          <p style="font-size: 0.84rem; color: var(--text-muted); margin: 0.25rem 0 0;">
            Institutional Compliance, Rigorous Analysis, Financial / Systemic Literacy.
          </p>
        </div>

        <div>
          <strong style="font-size: 0.88rem; color: #DC2626;">⚠️ Honest Realities &amp; Trade-offs:</strong>
          <ul style="padding-left: 1.2rem; font-size: 0.85rem; color: #9A3412; margin-top: 0.25rem; line-height: 1.6;">
            ${aChallenges.slice(0, 3).map(c => `<li>${escapeHtml(c)}</li>`).join('')}
          </ul>
        </div>
      </div>
    `;

    // Render Discussion Prompts
    const questions = comp.discussion_questions || [];
    questionsList.innerHTML = questions.map(q => `<li style="margin-bottom: 0.65rem;">${escapeHtml(q)}</li>`).join('');
  }
});
