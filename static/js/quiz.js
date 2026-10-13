/**
 * CareerCompass Assessment Controller
 * Multi-step navigation, client-side validation, and API submission.
 */

document.addEventListener('DOMContentLoaded', () => {
  let currentStep = 1;
  const totalSteps = 4;

  const stepTitles = [
    'Educational Background',
    'Interests & Strengths',
    'Work Style & Life Goals',
    'Budget, Mobility & Skills'
  ];

  const btnPrev = document.getElementById('btn-prev');
  const btnNext = document.getElementById('btn-next');
  const btnSubmit = document.getElementById('btn-submit');
  const stepIndicator = document.getElementById('step-indicator');
  const stepPercentage = document.getElementById('step-percentage');
  const progressBarFill = document.getElementById('progress-bar-fill');
  const form = document.getElementById('quiz-form');

  function updateStepUI() {
    // Show/hide step panels
    for (let i = 1; i <= totalSteps; i++) {
      const stepEl = document.getElementById(`step-${i}`);
      if (stepEl) {
        stepEl.classList.toggle('active', i === currentStep);
      }
    }

    // Update progress bar & label
    const pct = Math.round((currentStep / totalSteps) * 100);
    progressBarFill.style.width = `${pct}%`;
    stepIndicator.textContent = `Step ${currentStep} of ${totalSteps}: ${stepTitles[currentStep - 1]}`;
    stepPercentage.textContent = `${pct}% Completed`;

    // Button states
    btnPrev.style.display = currentStep === 1 ? 'none' : 'inline-flex';

    if (currentStep === totalSteps) {
      btnNext.style.display = 'none';
      btnSubmit.style.display = 'inline-flex';
    } else {
      btnNext.style.display = 'inline-flex';
      btnSubmit.style.display = 'none';
    }

    // Scroll to top of quiz card
    window.scrollTo({ top: form.offsetTop - 80, behavior: 'smooth' });
  }

  function validateStep(step) {
    if (step === 1) {
      const eduLevel = document.getElementById('education_level').value;
      const checkedSubs = form.querySelectorAll('input[name="favorite_subjects"]:checked');
      const errSub = document.getElementById('fav-sub-error');

      if (!eduLevel) {
        showToast('Please select your current education level.', 'warning');
        return false;
      }
      if (checkedSubs.length === 0) {
        errSub.style.display = 'block';
        showToast('Please select at least one favorite subject.', 'warning');
        return false;
      }
      errSub.style.display = 'none';
      return true;
    }

    if (step === 2) {
      const checkedInterests = form.querySelectorAll('input[name="interests"]:checked');
      const checkedStrengths = form.querySelectorAll('input[name="strengths"]:checked');
      const errInt = document.getElementById('interest-error');
      const errStr = document.getElementById('strength-error');

      let valid = true;
      if (checkedInterests.length === 0) {
        errInt.style.display = 'block';
        showToast('Please select at least one area of interest.', 'warning');
        valid = false;
      } else {
        errInt.style.display = 'none';
      }

      if (checkedStrengths.length === 0) {
        errStr.style.display = 'block';
        showToast('Please select at least one natural strength.', 'warning');
        valid = false;
      } else {
        errStr.style.display = 'none';
      }

      return valid;
    }

    if (step === 3) {
      const workStyle = form.querySelector('input[name="preferred_work_style"]:checked');
      const careerGoal = form.querySelector('input[name="career_goals"]:checked');

      if (!workStyle) {
        showToast('Please choose a preferred work style.', 'warning');
        return false;
      }
      if (!careerGoal) {
        showToast('Please select your primary career goal.', 'warning');
        return false;
      }
      return true;
    }

    if (step === 4) {
      const budget = document.getElementById('budget_range').value;
      if (!budget) {
        showToast('Please select your higher education budget preference.', 'warning');
        return false;
      }
      return true;
    }

    return true;
  }

  btnNext.addEventListener('click', () => {
    if (validateStep(currentStep)) {
      if (currentStep < totalSteps) {
        currentStep++;
        updateStepUI();
      }
    }
  });

  btnPrev.addEventListener('click', () => {
    if (currentStep > 1) {
      currentStep--;
      updateStepUI();
    }
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!validateStep(currentStep)) {
      return;
    }

    btnSubmit.disabled = true;
    btnSubmit.textContent = 'Generating Recommendations... ⏳';

    // Collect Form Data
    const formData = new FormData(form);
    const payload = {
      education_level: formData.get('education_level'),
      current_stream: formData.get('current_stream') || '',
      favorite_subjects: formData.getAll('favorite_subjects'),
      interests: formData.getAll('interests'),
      strengths: formData.getAll('strengths'),
      preferred_work_style: formData.get('preferred_work_style'),
      career_goals: formData.get('career_goals'),
      budget_range: formData.get('budget_range'),
      location_preference: formData.get('location_preference') || 'flexible_relocate',
      existing_skills: formData.getAll('existing_skills'),
      constraints: (formData.get('constraints') || '').trim()
    };

    try {
      const resp = await fetch('/api/assessments', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      const result = await resp.json();

      if (resp.ok && result.success && result.assessment_id) {
        showToast('Assessment submitted successfully! Redirecting...', 'success');
        setTimeout(() => {
          window.location.href = `/recommendations?assessment_id=${result.assessment_id}`;
        }, 400);
      } else {
        btnSubmit.disabled = false;
        btnSubmit.textContent = 'Generate My Recommendations 🚀';
        showToast(result.error || 'Failed to submit assessment. Please check your inputs.', 'error');
      }
    } catch (err) {
      console.error('Submission error:', err);
      btnSubmit.disabled = false;
      btnSubmit.textContent = 'Generate My Recommendations 🚀';
      showToast('Network error while saving assessment. Please try again.', 'error');
    }
  });
});
