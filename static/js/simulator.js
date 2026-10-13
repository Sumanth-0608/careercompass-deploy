/**
 * CareerCompass Reality Simulator Controller
 * Handles scenario comparison, what-if controls, safe DOM rendering, and API communication.
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const baseBudget = document.getElementById('base_budget');
  const baseStyle = document.getElementById('base_style');
  const basePriority = document.getElementById('base_priority');

  const altBudget = document.getElementById('alt_budget');
  const altStyle = document.getElementById('alt_style');
  const altPriority = document.getElementById('alt_priority');

  const btnCompare = document.getElementById('btn-compare-scenarios');
  const btnReset = document.getElementById('btn-reset-demo');
  const btnSave = document.getElementById('btn-save-scenario');

  const loadingEl = document.getElementById('sim-loading');
  const errorBanner = document.getElementById('sim-error-banner');
  const errorText = document.getElementById('sim-error-text');
  const resultsEl = document.getElementById('sim-results');

  const explanationsList = document.getElementById('sim-explanations-list');
  const recsContainerA = document.getElementById('recs-scenario-a');
  const recsContainerB = document.getElementById('recs-scenario-b');
  const matrixContainer = document.getElementById('comparison-matrix-container');
  const budgetTradeoffsContainer = document.getElementById('budget-tradeoffs-container');
  const nextActionsContainer = document.getElementById('next-actions-container');

  const demoDefaults = window.CAREERCOMPASS_DEFAULT_DEMO || {
    education_budget: 'moderate',
    work_style: 'analytical',
    priority: 'growth'
  };

  // Safe DOM node creation helper
  function makeEl(tag, className = '', text = '') {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (text) el.textContent = text;
    return el;
  }

  function showError(msg) {
    loadingEl.style.display = 'none';
    resultsEl.style.display = 'none';
    errorText.textContent = msg;
    errorBanner.style.display = 'block';
  }

  function clearError() {
    errorBanner.style.display = 'none';
    errorText.textContent = '';
  }

  async function runComparison(saveOnSubmit = false) {
    clearError();
    loadingEl.style.display = 'block';
    resultsEl.style.display = 'none';

    const payload = {
      baseline: {
        education_budget: baseBudget.value,
        work_style: baseStyle.value,
        priority: basePriority.value
      },
      alternative: {
        education_budget: altBudget.value,
        work_style: altStyle.value,
        priority: altPriority.value
      },
      save: saveOnSubmit
    };

    try {
      const endpoint = saveOnSubmit ? '/api/simulator/save' : '/api/simulator/compare';
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      loadingEl.style.display = 'none';

      if (!res.ok || !data.success) {
        showError(data.error || 'Failed to calculate scenario comparison. Please check your selections.');
        return;
      }

      const results = saveOnSubmit ? data.comparison : data;
      renderSimulatorResults(results);

      if (saveOnSubmit && data.comparison_id) {
        showToast(`Comparison saved to database with ID #${data.comparison_id}!`, 'success');
      }

    } catch (err) {
      console.error('Simulator error:', err);
      showError('Network error while connecting to the Career Reality Simulator API. Please try again.');
    }
  }

  function renderSimulatorResults(data) {
    resultsEl.style.display = 'block';
    btnSave.style.display = 'inline-flex';

    // 1. Render High-Level Explanations
    explanationsList.innerHTML = '';
    const explanations = data.explanations || [];
    if (explanations.length === 0) {
      const li = makeEl('li', '', 'Scenarios evaluated successfully. Review the side-by-side matrices below.');
      explanationsList.appendChild(li);
    } else {
      explanations.forEach(exp => {
        const li = makeEl('li', '', exp);
        explanationsList.appendChild(li);
      });
    }

    // 2. Render Scenario A Recommendations (Top 3)
    recsContainerA.innerHTML = '';
    (data.baseline_recommendations || []).forEach(r => {
      recsContainerA.appendChild(createScenarioCard(r, 'scenario-a'));
    });

    // 3. Render Scenario B Recommendations (Top 3)
    recsContainerB.innerHTML = '';
    (data.alternative_recommendations || []).forEach(r => {
      recsContainerB.appendChild(createScenarioCard(r, 'scenario-b'));
    });

    // 4. Render Side-by-Side Comparison Matrix
    matrixContainer.innerHTML = '';
    const comparisons = data.comparison || [];
    comparisons.forEach(item => {
      const row = makeEl('div', 'card');
      row.style.padding = '1.25rem';

      const topRow = makeEl('div');
      topRow.style.display = 'flex';
      topRow.style.justifyContent = 'space-between';
      topRow.style.alignItems = 'flex-start';
      topRow.style.flexWrap = 'wrap';
      topRow.style.gap = '0.75rem';
      topRow.style.marginBottom = '0.75rem';

      const titleBox = makeEl('div');
      const titleLink = makeEl('a', '', item.title);
      titleLink.href = `/careers/${item.career_id}`;
      titleLink.style.fontSize = '1.25rem';
      titleLink.style.fontWeight = '700';
      titleLink.style.color = 'var(--text-heading)';
      titleBox.appendChild(titleLink);

      const catBadge = makeEl('span', 'badge badge-navy', item.category);
      catBadge.style.marginLeft = '0.5rem';
      titleBox.appendChild(catBadge);
      topRow.appendChild(titleBox);

      // Status Badge
      let statusBadgeClass = 'badge badge-navy';
      if (item.status === 'entered') statusBadgeClass = 'badge badge-mint';
      else if (item.status === 'left') statusBadgeClass = 'badge badge-warning';
      const statusBadge = makeEl('span', statusBadgeClass, item.status_label);
      topRow.appendChild(statusBadge);
      row.appendChild(topRow);

      // Score Comparison Pills
      const scoreBar = makeEl('div');
      scoreBar.style.display = 'flex';
      scoreBar.style.alignItems = 'center';
      scoreBar.style.gap = '1rem';
      scoreBar.style.flexWrap = 'wrap';
      scoreBar.style.background = 'var(--bg-subtle)';
      scoreBar.style.padding = '0.75rem 1rem';
      scoreBar.style.borderRadius = 'var(--radius-sm)';
      scoreBar.style.marginBottom = '0.75rem';
      scoreBar.style.fontSize = '0.9rem';

      const scoreA = makeEl('span', '', `Scenario A: ${item.baseline_score}% (${item.baseline_label})`);
      scoreA.style.fontWeight = '600';

      const arrow = makeEl('span', '', '➔');
      arrow.style.color = 'var(--text-subtle)';

      const scoreB = makeEl('span', '', `Scenario B: ${item.alternative_score}% (${item.alternative_label})`);
      scoreB.style.fontWeight = '700';
      scoreB.style.color = item.score_difference >= 0 ? 'var(--primary-blue)' : '#b91c1c';

      let diffText = item.score_difference > 0 ? `+${item.score_difference}%` : `${item.score_difference}%`;
      const diffBadge = makeEl('span', 'badge', `Score Shift: ${diffText}`);
      diffBadge.style.background = item.score_difference >= 0 ? 'var(--soft-blue)' : '#fee2e2';
      diffBadge.style.color = item.score_difference >= 0 ? 'var(--primary-blue-hover)' : '#991b1b';

      scoreBar.appendChild(scoreA);
      scoreBar.appendChild(arrow);
      scoreBar.appendChild(scoreB);
      scoreBar.appendChild(diffBadge);

      if (item.is_close) {
        const closeTag = makeEl('span', 'badge badge-warning', 'Similarly Compatible');
        scoreBar.appendChild(closeTag);
      }

      row.appendChild(scoreBar);

      // Grounded Reason for change
      const reasonP = makeEl('p', '', item.change_explanation);
      reasonP.style.fontSize = '0.9rem';
      reasonP.style.color = 'var(--text-main)';
      reasonP.style.marginBottom = '0.5rem';
      row.appendChild(reasonP);

      // Skills to consider
      if (item.skills_to_consider && item.skills_to_consider.length > 0) {
        const skillsBox = makeEl('div');
        skillsBox.style.fontSize = '0.85rem';
        skillsBox.style.color = 'var(--text-subtle)';
        const strong = makeEl('strong', '', 'Skills to build: ');
        skillsBox.appendChild(strong);
        skillsBox.appendChild(document.createTextNode(item.skills_to_consider.join(', ')));
        row.appendChild(skillsBox);
      }

      matrixContainer.appendChild(row);
    });

    // 5. Render Budget Learning Route Trade-offs
    budgetTradeoffsContainer.innerHTML = '';
    const routeChanges = data.budget_route_changes || [];
    if (routeChanges.length > 0) {
      routeChanges.forEach(rc => {
        const itemBox = makeEl('div', 'card');
        itemBox.style.padding = '1.25rem';
        itemBox.style.background = 'var(--bg-subtle)';
        itemBox.style.borderLeft = '4px solid var(--primary-blue)';

        const heading = makeEl('h4', '', rc.career_title);
        heading.style.marginBottom = '0.5rem';
        itemBox.appendChild(heading);

        const routeP = makeEl('p', '', `Updated Suggested Route: ${rc.alternative_route}`);
        routeP.style.fontSize = '0.9rem';
        routeP.style.marginBottom = '0.35rem';
        itemBox.appendChild(routeP);

        const feasibilityP = makeEl('p', '', `Feasibility & Advice: ${rc.feasibility}`);
        feasibilityP.style.fontSize = '0.85rem';
        feasibilityP.style.color = 'var(--text-muted)';
        feasibilityP.style.marginBottom = '0.25rem';
        itemBox.appendChild(feasibilityP);

        const notesP = makeEl('div', '', `Cost Detail: ${rc.cost_notes}`);
        notesP.style.fontSize = '0.85rem';
        notesP.style.color = 'var(--text-subtle)';
        itemBox.appendChild(notesP);

        budgetTradeoffsContainer.appendChild(itemBox);
      });
    } else {
      const noBudgetChange = makeEl('div', 'card');
      noBudgetChange.style.padding = '1.25rem';
      noBudgetChange.style.background = 'var(--bg-subtle)';
      const p = makeEl(
        'p',
        '',
        'Both scenarios share the same budget preference. To explore how financial constraints shift learning routes (e.g. self-learning vs state college vs private academy), adjust the Education Budget control.'
      );
      p.style.margin = '0';
      p.style.fontSize = '0.9rem';
      noBudgetChange.appendChild(p);
      budgetTradeoffsContainer.appendChild(noBudgetChange);
    }

    // 6. Render Suggested Next Steps & Actions
    nextActionsContainer.innerHTML = '';
    (data.alternative_recommendations || []).forEach(r => {
      const actionCard = makeEl('div', 'card');
      actionCard.style.padding = '1.25rem';
      actionCard.style.background = 'var(--bg-subtle)';

      const cardTitle = makeEl('h4', '', r.title);
      cardTitle.style.fontSize = '1.1rem';
      cardTitle.style.marginBottom = '0.5rem';
      actionCard.appendChild(cardTitle);

      const projP = makeEl('p', '', `Starter Experiment: ${r.starter_project}`);
      projP.style.fontSize = '0.85rem';
      projP.style.color = 'var(--text-main)';
      projP.style.marginBottom = '0.75rem';
      actionCard.appendChild(projP);

      const linkBtn = makeEl('a', 'btn btn-sm btn-outline-mint', 'Explore Pathway &rarr;');
      linkBtn.href = `/careers/${r.career_id}`;
      actionCard.appendChild(linkBtn);

      nextActionsContainer.appendChild(actionCard);
    });

    resultsEl.scrollIntoView({ behavior: 'smooth' });
  }

  function createScenarioCard(rec, type) {
    const card = makeEl('div', 'card');
    card.style.padding = '1.25rem';
    card.style.borderLeft = type === 'scenario-a' ? '4px solid var(--deep-navy)' : '4px solid var(--primary-blue)';

    const top = makeEl('div');
    top.style.display = 'flex';
    top.style.justifyContent = 'space-between';
    top.style.alignItems = 'flex-start';
    top.style.marginBottom = '0.5rem';

    const titleLink = makeEl('a', '', rec.title);
    titleLink.href = `/careers/${rec.career_id}`;
    titleLink.style.fontSize = '1.15rem';
    titleLink.style.fontWeight = '700';
    titleLink.style.color = 'var(--text-heading)';
    top.appendChild(titleLink);

    const scoreBadge = makeEl('span', type === 'scenario-a' ? 'badge badge-navy' : 'badge badge-mint', `${rec.match_score}%`);
    scoreBadge.style.fontSize = '0.85rem';
    top.appendChild(scoreBadge);
    card.appendChild(top);

    const labelDiv = makeEl('div', '', rec.match_label);
    labelDiv.style.fontSize = '0.8rem';
    labelDiv.style.fontWeight = '600';
    labelDiv.style.color = 'var(--text-subtle)';
    labelDiv.style.marginBottom = '0.5rem';
    card.appendChild(labelDiv);

    const desc = makeEl('p', '', rec.short_description);
    desc.style.fontSize = '0.85rem';
    desc.style.color = 'var(--text-muted)';
    desc.style.marginBottom = '0.75rem';
    card.appendChild(desc);

    // Reasons
    if (rec.reasons && rec.reasons.length > 0) {
      const reasonBox = makeEl('div');
      reasonBox.style.fontSize = '0.8rem';
      reasonBox.style.color = 'var(--text-main)';
      reasonBox.style.background = 'var(--bg-subtle)';
      reasonBox.style.padding = '0.5rem 0.75rem';
      reasonBox.style.borderRadius = 'var(--radius-sm)';
      reasonBox.style.marginBottom = '0.75rem';
      reasonBox.textContent = `💡 ${rec.reasons[0]}`;
      card.appendChild(reasonBox);
    }

    const routeDiv = makeEl('div');
    routeDiv.style.fontSize = '0.8rem';
    routeDiv.style.color = 'var(--text-subtle)';
    routeDiv.textContent = `Route: ${rec.route_info.suggested_route}`;
    card.appendChild(routeDiv);

    return card;
  }

  // Button Listeners
  btnCompare.addEventListener('click', () => {
    runComparison(false);
  });

  btnReset.addEventListener('click', () => {
    baseBudget.value = demoDefaults.education_budget;
    baseStyle.value = demoDefaults.work_style;
    basePriority.value = demoDefaults.priority;

    // Set alternative with subtle difference so comparison is immediately educational
    altBudget.value = demoDefaults.education_budget;
    altStyle.value = 'creative';
    altPriority.value = 'stability';

    showToast('Controls reset to default demo scenario.', 'info');
    runComparison(false);
  });

  btnSave.addEventListener('click', () => {
    runComparison(true);
  });

  // Automatically trigger initial comparison on load so user immediately sees results
  runComparison(false);
});
