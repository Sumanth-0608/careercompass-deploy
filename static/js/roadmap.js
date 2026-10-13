/**
 * CareerCompass Interactive Snake Roadmap Controller
 * Features:
 * - Zigzag / Snake winding stage path with SVG curved connectors
 * - Responsive 2-column layout (left snake, right sticky detail panel)
 * - Stage-aware milestone generation for B.Tech Civil Engineering & all careers
 * - Persistent milestone completion tracking
 * - Part-time & internship opportunities beside each milestone
 * - Smooth hover, keyboard selection, and SVG path redraw on resize
 */

document.addEventListener('DOMContentLoaded', async () => {
  // Elements
  const headingEl = document.getElementById('roadmap-heading');
  const subtitleEl = document.getElementById('roadmap-subtitle');
  const progressPctEl = document.getElementById('progress-pct-text');
  const progressCountEl = document.getElementById('progress-count-text');
  const progressBarFill = document.getElementById('progress-bar-fill');
  const careerSelect = document.getElementById('career-select');
  const educationLevelSelect = document.getElementById('education-level-select');
  const studentNameInput = document.getElementById('student-name-input');
  const btnSavePlan = document.getElementById('btn-save-plan');
  const loadingEl = document.getElementById('roadmap-loading');
  const layoutEl = document.getElementById('roadmap-layout');
  const snakeNodesContainer = document.getElementById('snake-nodes-container');
  const svgPath = document.getElementById('snake-svg-path');
  const svgProgress = document.getElementById('snake-svg-progress');
  const svgLayer = document.getElementById('snake-svg-layer');

  // Detail Panel Elements
  const panelEmpty = document.getElementById('panel-empty');
  const panelContent = document.getElementById('panel-content');
  const detailStageBadge = document.getElementById('detail-stage-badge');
  const detailStepBadge = document.getElementById('detail-step-badge');
  const detailTitle = document.getElementById('detail-title');
  const btnToggleMilestone = document.getElementById('btn-toggle-milestone');
  const detailExplanation = document.getElementById('detail-explanation');
  const detailAction = document.getElementById('detail-action');
  const detailSkills = document.getElementById('detail-skills');
  const detailProject = document.getElementById('detail-project');
  const detailResource = document.getElementById('detail-resource');
  const detailDuration = document.getElementById('detail-duration');
  const detailOppsList = document.getElementById('detail-opportunities-list');

  // State
  const urlParams = new URLSearchParams(window.location.search);
  let activePlanId = window.CAREERCOMPASS_PLAN_ID || urlParams.get('plan_id');
  let activeCareerId = window.CAREERCOMPASS_CAREER_ID || urlParams.get('career_id') || (careerSelect ? careerSelect.value : 'civil-engineer');
  let activeEducationLevel = window.CAREERCOMPASS_EDUCATION_LEVEL || urlParams.get('education_level') || (educationLevelSelect ? educationLevelSelect.value : 'Undergraduate');

  let currentRoadmapData = null;
  let activeMilestoneIndex = 0;
  let completedMilestonesSet = new Set();

  // Initialize
  await loadRoadmap();

  // Dropdown listeners
  if (careerSelect) {
    careerSelect.addEventListener('change', () => {
      activeCareerId = careerSelect.value;
      activePlanId = null; // Switching career switches to template view
      loadRoadmap();
    });
  }

  if (educationLevelSelect) {
    educationLevelSelect.addEventListener('change', () => {
      activeEducationLevel = educationLevelSelect.value;
      loadRoadmap();
    });
  }

  // Save Plan Button Handler
  if (btnSavePlan) {
    btnSavePlan.addEventListener('click', async () => {
      btnSavePlan.disabled = true;
      btnSavePlan.textContent = 'Saving Plan... ⏳';

      const sName = (studentNameInput.value || 'Student').trim();
      const cId = currentRoadmapData ? currentRoadmapData.career_id : (parseInt(activeCareerId, 10) || 1);

      try {
        const res = await fetch('/api/plans', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            career_id: cId,
            student_name: sName
          })
        });
        const data = await res.json();
        if (res.ok && data.success && data.plan_id) {
          showToast(`Saved plan for ${data.plan.career_title}! Check off milestones as you progress.`, 'success');
          setTimeout(() => {
            window.location.href = `/roadmap?plan_id=${data.plan_id}`;
          }, 400);
        } else {
          btnSavePlan.disabled = false;
          btnSavePlan.textContent = '💾 Save Plan';
          showToast(data.error || 'Could not save plan.', 'error');
        }
      } catch (err) {
        console.error('Error saving plan:', err);
        btnSavePlan.disabled = false;
        btnSavePlan.textContent = '💾 Save Plan';
        showToast('Network error while saving plan.', 'error');
      }
    });
  }

  // --------------------------------------------------------------------------
  // Main Roadmap Loader
  // --------------------------------------------------------------------------
  async function loadRoadmap() {
    loadingEl.style.display = 'block';
    layoutEl.style.display = 'none';

    try {
      if (activePlanId) {
        // Load saved plan with persistent progress
        const res = await fetch(`/api/plans/${activePlanId}`);
        const data = await res.json();
        if (res.ok && data.success && data.plan) {
          const plan = data.plan;
          headingEl.textContent = `${plan.student_name}'s Active Roadmap: ${plan.career_title}`;
          subtitleEl.textContent = `Tracking sequential milestones for ${plan.career_title}. Status: ${plan.status.toUpperCase()}.`;

          // Mark completed milestones
          completedMilestonesSet.clear();
          (plan.milestones || []).forEach(m => {
            if (m.is_completed) completedMilestonesSet.add(m.step_number);
          });

          // Fetch enriched custom roadmap data for stages & opportunities
          const customRes = await fetch(`/api/roadmap/custom?career_id=${plan.career_id}&education_level=${encodeURIComponent(activeEducationLevel)}`);
          const customData = await customRes.json();

          if (customRes.ok && customData.success) {
            currentRoadmapData = customData.roadmap;
            // Merge saved plan completion states into custom milestones
            currentRoadmapData.milestones.forEach(m => {
              const matchedSaved = plan.milestones.find(sm => sm.step_number === m.step_number);
              if (matchedSaved) {
                m.is_completed = Boolean(matchedSaved.is_completed);
                m.plan_milestone_id = matchedSaved.id;
              }
            });
          }
          if (careerSelect) careerSelect.value = plan.career_id;
        }
      } else {
        // Load fresh customized roadmap
        const res = await fetch(`/api/roadmap/custom?career_id=${encodeURIComponent(activeCareerId)}&education_level=${encodeURIComponent(activeEducationLevel)}`);
        const data = await res.json();
        if (res.ok && data.success && data.roadmap) {
          currentRoadmapData = data.roadmap;
          headingEl.textContent = `Interactive Learning Roadmap: ${currentRoadmapData.career_title}`;
          subtitleEl.textContent = `Spacious snake pathway tailored for ${activeEducationLevel} students with 11 core competencies and connected opportunities.`;
          completedMilestonesSet.clear();
        }
      }

      loadingEl.style.display = 'none';

      if (!currentRoadmapData || !currentRoadmapData.milestones || currentRoadmapData.milestones.length === 0) {
        showToast('No roadmap milestones available for this pathway.', 'error');
        return;
      }

      layoutEl.style.display = 'grid';
      renderSnakeNodes(currentRoadmapData.milestones);
      updateProgressDisplay();

      // Default select milestone 0
      selectMilestone(0);

      // Redraw SVG connector path
      setTimeout(() => {
        drawSnakePath();
      }, 100);

    } catch (err) {
      console.error('Error loading roadmap:', err);
      loadingEl.style.display = 'none';
      showToast('Could not load roadmap data.', 'error');
    }
  }

  // --------------------------------------------------------------------------
  // Render Snake Zigzag Milestones
  // --------------------------------------------------------------------------
  function renderSnakeNodes(milestones) {
    snakeNodesContainer.innerHTML = '';

    milestones.forEach((m, idx) => {
      // Determine left or right zigzag alignment
      const isLeft = (idx % 2 === 0);
      const row = document.createElement('div');
      row.className = `snake-row ${isLeft ? 'snake-row-left' : 'snake-row-right'}`;
      row.style.display = 'flex';
      row.style.justifyContent = isLeft ? 'flex-start' : 'flex-end';
      row.style.width = '100%';
      row.style.padding = '0.5rem 1rem';

      const isCompleted = Boolean(m.is_completed || completedMilestonesSet.has(m.step_number));

      // Milestone Card Node
      const card = document.createElement('div');
      card.className = `snake-milestone-card ${isCompleted ? 'completed' : ''} ${idx === activeMilestoneIndex ? 'active-node' : ''}`;
      card.dataset.index = idx;
      card.id = `milestone-node-${idx}`;
      card.tabIndex = 0; // Accessible keyboard focus
      card.setAttribute('role', 'button');
      card.setAttribute('aria-label', `Step ${m.step_number}: ${m.title}`);

      card.innerHTML = `
        <div class="snake-node-pin">
          <div class="snake-node-marker ${isCompleted ? 'completed-marker' : ''}">
            ${isCompleted ? '✓' : m.step_number}
          </div>
        </div>
        <div class="snake-node-body">
          <div style="display: flex; gap: 0.4rem; align-items: center; margin-bottom: 0.35rem; flex-wrap: wrap;">
            <span class="badge badge-navy" style="font-size: 0.72rem;">${escapeHtml(m.stage_name)}</span>
            <span class="badge badge-mint" style="font-size: 0.72rem;">⏱️ ${escapeHtml(m.estimated_duration)}</span>
          </div>
          <h4 class="snake-node-title">${escapeHtml(m.title)}</h4>
          <p class="snake-node-snippet">${escapeHtml(m.suggested_action || m.explanation)}</p>
          ${m.opportunities && m.opportunities.length > 0 ? `
            <div style="margin-top: 0.45rem; font-size: 0.75rem; color: var(--primary-blue); font-weight: 700;">
              💼 ${m.opportunities.length} Connected Opportunity${m.opportunities.length > 1 ? 's' : ''}
            </div>
          ` : ''}
        </div>
      `;

      // Click handler
      card.addEventListener('click', () => {
        selectMilestone(idx);
      });

      // Keyboard navigation (Enter / Space)
      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          selectMilestone(idx);
        }
      });

      row.appendChild(card);
      snakeNodesContainer.appendChild(row);
    });
  }

  // --------------------------------------------------------------------------
  // Milestone Selection & Right Detail Panel Update (Feature 6 & 7)
  // --------------------------------------------------------------------------
  function selectMilestone(idx) {
    if (!currentRoadmapData || !currentRoadmapData.milestones[idx]) return;
    activeMilestoneIndex = idx;
    const m = currentRoadmapData.milestones[idx];

    // Highlight node in snake list
    document.querySelectorAll('.snake-milestone-card').forEach((el, i) => {
      if (i === idx) {
        el.classList.add('active-node');
        el.style.transform = 'scale(1.03)';
      } else {
        el.classList.remove('active-node');
        el.style.transform = 'scale(1)';
      }
    });

    // Populate Right Sticky Detail Panel
    panelEmpty.style.display = 'none';
    panelContent.style.display = 'block';

    detailStageBadge.textContent = `${m.stage_icon || '🎓'} ${m.stage_name}`;
    detailStepBadge.textContent = `Step ${m.step_number} of ${currentRoadmapData.total_milestones}`;
    detailTitle.textContent = m.title;

    detailExplanation.textContent = m.explanation;
    detailAction.textContent = m.suggested_action;
    detailProject.textContent = (m.beginner_projects && m.beginner_projects[0]) || 'Complete a practical capstone project solving a real community challenge.';
    detailResource.textContent = m.low_cost_route || 'Open courseware (NPTEL, SWAYAM, MIT OCW) and public engineering standards.';
    detailDuration.textContent = m.estimated_duration;

    // Render Skills Chips
    detailSkills.innerHTML = '';
    const skills = m.skills || ['Core Foundations', 'Problem Solving'];
    skills.forEach(s => {
      const chip = document.createElement('span');
      chip.className = 'badge badge-navy';
      chip.textContent = s;
      detailSkills.appendChild(chip);
    });

    // Toggle button state
    const isCompleted = Boolean(m.is_completed || completedMilestonesSet.has(m.step_number));
    updateToggleBtnUI(isCompleted);

    btnToggleMilestone.onclick = async () => {
      await handleToggleMilestone(idx);
    };

    // Render Connected Opportunities (Feature 7)
    renderMilestoneOpportunities(m.opportunities || []);

    // Scroll node into view gently if on mobile
    if (window.innerWidth <= 1024) {
      panelContent.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }

  function updateToggleBtnUI(isCompleted) {
    if (isCompleted) {
      btnToggleMilestone.textContent = '✓ Completed';
      btnToggleMilestone.className = 'btn btn-sm btn-navy';
      btnToggleMilestone.title = 'Click to mark as incomplete';
    } else {
      btnToggleMilestone.textContent = 'Mark Done ✓';
      btnToggleMilestone.className = 'btn btn-sm btn-outline';
      btnToggleMilestone.title = 'Click to mark as completed';
    }
  }

  // Toggle milestone completion (persisting to SQLite backend if in active plan)
  async function handleToggleMilestone(idx) {
    const m = currentRoadmapData.milestones[idx];
    const newStatus = !Boolean(m.is_completed || completedMilestonesSet.has(m.step_number));

    m.is_completed = newStatus;
    if (newStatus) {
      completedMilestonesSet.add(m.step_number);
    } else {
      completedMilestonesSet.delete(m.step_number);
    }

    // If viewing saved plan, persist via PATCH API
    if (activePlanId && m.plan_milestone_id) {
      try {
        const patchRes = await fetch(`/api/plans/${activePlanId}/milestones/${m.plan_milestone_id}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ is_completed: newStatus })
        });
        const patchData = await patchRes.json();
        if (patchRes.ok && patchData.success) {
          showToast(`Milestone ${m.step_number} ${newStatus ? 'completed' : 'unmarked'}!`, 'success');
        }
      } catch (err) {
        console.warn('Could not persist milestone PATCH:', err);
      }
    } else {
      showToast(`Milestone ${m.step_number} marked ${newStatus ? 'done' : 'pending'}. Save plan to persist permanently!`, 'info');
    }

    // Refresh UI
    updateToggleBtnUI(newStatus);
    const cardEl = document.getElementById(`milestone-node-${idx}`);
    if (cardEl) {
      if (newStatus) {
        cardEl.classList.add('completed');
        const marker = cardEl.querySelector('.snake-node-marker');
        if (marker) {
          marker.classList.add('completed-marker');
          marker.textContent = '✓';
        }
      } else {
        cardEl.classList.remove('completed');
        const marker = cardEl.querySelector('.snake-node-marker');
        if (marker) {
          marker.classList.remove('completed-marker');
          marker.textContent = m.step_number;
        }
      }
    }

    updateProgressDisplay();
    drawSnakePath();
  }

  // --------------------------------------------------------------------------
  // Connected Opportunities inside Detail Panel (Feature 7)
  // --------------------------------------------------------------------------
  function renderMilestoneOpportunities(opps) {
    detailOppsList.innerHTML = '';

    if (!opps || opps.length === 0) {
      detailOppsList.innerHTML = `
        <div style="font-size: 0.84rem; color: var(--text-subtle); padding: 0.5rem; background: rgba(255,255,255,0.4); border-radius: var(--radius-sm);">
          Opportunity type to explore: Practical summer internship, student engineering society, or local site visit.
          <a href="/opportunities" style="display: block; margin-top: 0.35rem; color: var(--primary-blue); font-weight: 700;">Explore Opportunity Catalog &rarr;</a>
        </div>
      `;
      return;
    }

    opps.forEach(opp => {
      const oppCard = document.createElement('div');
      oppCard.style.padding = '0.85rem';
      oppCard.style.background = 'rgba(255, 255, 255, 0.65)';
      oppCard.style.border = '1px solid rgba(37,99,235,0.18)';
      oppCard.style.borderRadius = 'var(--radius-sm)';

      oppCard.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem; margin-bottom: 0.3rem;">
          <strong style="font-size: 0.88rem; color: var(--text-heading);">${escapeHtml(opp.title)}</strong>
          <span class="badge badge-mint" style="font-size: 0.7rem;">${escapeHtml(opp.opportunity_type)}</span>
        </div>
        <div style="font-size: 0.78rem; color: var(--primary-blue); margin-bottom: 0.4rem;">
          🏛️ ${escapeHtml(opp.employer_or_source)} · 📍 ${escapeHtml(opp.location_city)}
        </div>
        <div style="font-size: 0.78rem; color: var(--text-muted); line-height: 1.4; margin-bottom: 0.6rem;">
          ${escapeHtml(opp.eligibility)}
        </div>
        <div style="display: flex; gap: 0.4rem;">
          <a href="${escapeHtml(opp.official_url)}" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-sm" style="flex: 1; font-size: 0.76rem; padding: 0.35rem 0.6rem;">
            Official Portal &rarr;
          </a>
          <button type="button" class="btn btn-outline btn-sm btn-bookmark-opp" data-id="${opp.id}" data-title="${escapeHtml(opp.title)}" style="font-size: 0.76rem; padding: 0.35rem 0.6rem;">
            🔖 Save
          </button>
        </div>
      `;

      const bBtn = oppCard.querySelector('.btn-bookmark-opp');
      bBtn.addEventListener('click', () => {
        bBtn.textContent = '✓ Saved';
        bBtn.classList.remove('btn-outline');
        bBtn.classList.add('btn-navy');
        showToast(`Bookmarked ${opp.title} alongside this roadmap milestone!`, 'success');
      });

      detailOppsList.appendChild(oppCard);
    });
  }

  // --------------------------------------------------------------------------
  // Update Live Progress Percentage Display
  // --------------------------------------------------------------------------
  function updateProgressDisplay() {
    if (!currentRoadmapData) return;
    const total = currentRoadmapData.total_milestones || 11;
    const completed = completedMilestonesSet.size;
    const pct = Math.round((completed / total) * 100);

    progressPctEl.textContent = `${pct}%`;
    progressCountEl.textContent = `${completed} of ${total} Milestones Completed`;
    progressBarFill.style.width = `${pct}%`;
  }

  // --------------------------------------------------------------------------
  // SVG Snake Path Generator
  // --------------------------------------------------------------------------
  function drawSnakePath() {
    if (!svgPath || !svgLayer) return;

    const cards = document.querySelectorAll('.snake-milestone-card');
    if (cards.length < 2) return;

    const layerRect = svgLayer.getBoundingClientRect();
    const points = [];

    cards.forEach(card => {
      const pin = card.querySelector('.snake-node-pin') || card;
      const rect = pin.getBoundingClientRect();
      // Center coordinates relative to the SVG layer
      const x = rect.left - layerRect.left + (rect.width / 2);
      const y = rect.top - layerRect.top + (rect.height / 2);
      points.push({ x, y });
    });

    if (points.length < 2) return;

    // Build smooth cubic bezier curve
    let d = `M ${points[0].x} ${points[0].y}`;
    for (let i = 0; i < points.length - 1; i++) {
      const p1 = points[i];
      const p2 = points[i + 1];

      // Curving inflection control points
      const dx = p2.x - p1.x;
      const dy = p2.y - p1.y;

      const cx1 = p1.x + (dx * 0.1);
      const cy1 = p1.y + (dy * 0.5);

      const cx2 = p2.x - (dx * 0.1);
      const cy2 = p2.y - (dy * 0.5);

      d += ` C ${cx1} ${cy1}, ${cx2} ${cy2}, ${p2.x} ${p2.y}`;
    }

    svgPath.setAttribute('d', d);

    // Illuminating Progress Line
    if (svgProgress) {
      const completedCount = completedMilestonesSet.size;
      if (completedCount > 1 && points.length > 1) {
        const lastIdx = Math.min(completedCount - 1, points.length - 1);
        let pd = `M ${points[0].x} ${points[0].y}`;
        for (let i = 0; i < lastIdx; i++) {
          const p1 = points[i];
          const p2 = points[i + 1];
          const dx = p2.x - p1.x;
          const dy = p2.y - p1.y;
          const cx1 = p1.x + (dx * 0.1);
          const cy1 = p1.y + (dy * 0.5);
          const cx2 = p2.x - (dx * 0.1);
          const cy2 = p2.y - (dy * 0.5);
          pd += ` C ${cx1} ${cy1}, ${cx2} ${cy2}, ${p2.x} ${p2.y}`;
        }
        svgProgress.setAttribute('d', pd);
      } else {
        svgProgress.setAttribute('d', '');
      }
    }
  }

  // Redraw path dynamically on window resize
  window.addEventListener('resize', () => {
    drawSnakePath();
  });
});
