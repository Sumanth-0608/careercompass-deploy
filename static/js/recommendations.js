/**
 * CareerCompass Recommendations Controller
 * Fetches and renders explainable recommendation cards with safe escaping.
 */

document.addEventListener('DOMContentLoaded', async () => {
  const loadingEl = document.getElementById('loading-spinner');
  const emptyEl = document.getElementById('empty-state');
  const containerEl = document.getElementById('recommendations-container');

  const urlParams = new URLSearchParams(window.location.search);
  const assessmentId = window.CAREERCOMPASS_ASSESSMENT_ID || urlParams.get('assessment_id');

  if (!assessmentId) {
    loadingEl.style.display = 'none';
    emptyEl.style.display = 'block';
    return;
  }

  try {
    const res = await fetch(`/api/assessments/${assessmentId}/recommendations`);
    const data = await res.json();

    loadingEl.style.display = 'none';

    if (!res.ok || !data.success || !data.recommendations || data.recommendations.length === 0) {
      emptyEl.style.display = 'block';
      return;
    }

    containerEl.style.display = 'flex';
    containerEl.innerHTML = '';

    data.recommendations.forEach((rec, idx) => {
      const card = document.createElement('div');
      card.className = 'rec-card';

      // Badges
      let regulatedBadge = '';
      if (rec.regulated) {
        regulatedBadge = `<span class="badge badge-regulated" title="Statutory licensing or regulated degree required">Statutory Licensure Required</span>`;
      }

      let costBadge = `<span class="badge badge-mint">${escapeHtml(rec.cost_category || 'Moderate')}</span>`;
      let rankBadge = `<span class="badge badge-navy">Top Recommendation #${idx + 1}</span>`;

      // Why matches list
      let reasonsHtml = '';
      if (rec.match_reasons && rec.match_reasons.length > 0) {
        reasonsHtml = `
          <div class="match-reasons-list">
            <h4>💡 Why this fits your profile:</h4>
            <ul>
              ${rec.match_reasons.map(r => `<li>${escapeHtml(r)}</li>`).join('')}
            </ul>
          </div>
        `;
      }

      // Missing skills tags
      let missingSkillsHtml = '';
      if (rec.missing_skills && rec.missing_skills.length > 0) {
        missingSkillsHtml = `
          <div style="margin: 1rem 0;">
            <strong style="font-size: 0.85rem; color: var(--text-subtle); display: block; margin-bottom: 0.35rem;">
              🎯 Key Skills to Build:
            </strong>
            <div class="chip-grid">
              ${rec.missing_skills.map(s => `<span class="badge badge-navy" style="font-size: 0.8rem;">+ ${escapeHtml(s)}</span>`).join('')}
            </div>
          </div>
        `;
      }

      // Trade-offs
      let tradeoffsHtml = '';
      if (rec.trade_offs && rec.trade_offs.length > 0) {
        tradeoffsHtml = `
          <div style="margin: 0.75rem 0; font-size: 0.88rem; color: #991B1B; background: rgba(254, 226, 226, 0.5); padding: 0.75rem 1rem; border-radius: var(--radius-sm); border: 1px solid rgba(239, 68, 68, 0.25); border-left: 4px solid #EF4444;">
            <strong>⚠️ Reality Check & Trade-offs:</strong>
            ${escapeHtml(rec.trade_offs[0])}
          </div>
        `;
      }

      // Low cost routes
      let lowCostHtml = '';
      if (rec.alternative_routes && rec.alternative_routes.length > 0) {
        lowCostHtml = `
          <div style="margin: 0.75rem 0; font-size: 0.88rem; color: var(--deep-navy); background: var(--pale-blue); padding: 0.75rem 1rem; border-radius: var(--radius-sm); border: 1px solid rgba(59, 130, 246, 0.25); border-left: 4px solid var(--primary-blue);">
            <strong>🌱 Low-Cost Alternative Route:</strong>
            ${escapeHtml(rec.alternative_routes[0])}
          </div>
        `;
      }

      card.innerHTML = `
        <div class="rec-card-top">
          <div>
            <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.5rem;">
              ${rankBadge}
              <span class="badge badge-navy">${escapeHtml(rec.category)}</span>
              ${costBadge}
              ${regulatedBadge}
            </div>
            <h3 style="font-size: 1.6rem; margin-bottom: 0.5rem;">${escapeHtml(rec.title)}</h3>
            <p style="margin-bottom: 0; color: var(--text-muted);">${escapeHtml(rec.short_description)}</p>
          </div>

          <div class="rec-score-box">
            <div class="score-number">${rec.match_score}%</div>
            <div class="score-label">Guidance Match</div>
          </div>
        </div>

        ${reasonsHtml}
        ${missingSkillsHtml}
        ${tradeoffsHtml}
        ${lowCostHtml}

        <div class="rec-actions">
          <a href="/careers/${rec.career_id}?assessment_id=${assessmentId}" class="btn btn-navy btn-sm">
            📖 Deep Reality Check
          </a>
          <a href="/roadmap?career_id=${rec.career_id}&assessment_id=${assessmentId}" class="btn btn-primary btn-sm">
            🗺️ Start Personalized Roadmap
          </a>
          <a href="/compare?student_career_id=${rec.career_id}&assessment_id=${assessmentId}" class="btn btn-secondary btn-sm">
            🤝 Student–Parent Comparison
          </a>
        </div>
      `;

      containerEl.appendChild(card);
    });

  } catch (err) {
    console.error('Error fetching recommendations:', err);
    loadingEl.style.display = 'none';
    showToast('Failed to load recommendations. Please refresh or retake the assessment.', 'error');
  }
});
