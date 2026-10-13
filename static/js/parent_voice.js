/**
 * CareerCompass - Multilingual Guidance & 3-Language Non-AI Translation
 * 
 * 1. Three-Language Translation Box (Non-AI):
 *    - Positioned between "Detailed Side-by-Side Reality Check" and "Compare Two Specific Pathways"
 *    - 3 Languages: Telugu (te), Hindi (hi), English (en)
 *    - All 6 Translation Pairs: te->hi, te->en, hi->te, hi->en, en->te, en->hi
 *    - Automatic exclusion of source language from destination choices
 *    - Language Swap (⇄) button
 *    - Source pre-population from student's career choice, reasons, goals
 *    - Clear button and prominent blue Translate button
 *    - Read-only translated result card
 *    - Copy Translation button with "Copied!" feedback
 *    - Text-to-Speech with Play, Pause, Resume, Stop controls using target language voice
 *    - Strictly ZERO AI models (calls POST /api/translate)
 * 
 * 2. Floating AI Voice Assistant Modal:
 *    - Preserved for parents requesting the interactive conversational modal.
 */

(function () {
  'use strict';

  // Supported languages config
  const LANGUAGES = {
    en: { code: 'en-IN', name: 'English', native: 'English', voiceMatch: ['en-in', 'en', 'india'] },
    te: { code: 'te-IN', name: 'Telugu', native: 'తెలుగు', voiceMatch: ['te', 'telugu'] },
    hi: { code: 'hi-IN', name: 'Hindi', native: 'हिन्दी', voiceMatch: ['hi', 'hindi'] }
  };

  // State
  const state = {
    // Translation tool state
    fromLang: 'en',
    toLang: 'te',
    currentTranslation: '',
    availableVoices: [],
    isSpeaking: false,
    isPaused: false,
    speechChunks: [],
    chunkIndex: 0,
    hasUserEditedSource: false,

    // Modal state (preserved for floating modal)
    modalLang: 'en',
    studentProfile: null,
    isModalOpen: false,
    modalAiReply: '',
    recognition: null,
    isListening: false
  };

  // DOM Elements - Translation Box
  let fromLangSelect, toLangSelect, btnSwap;
  let sourceText, btnClear, btnTranslate;
  let statusMsg, resultCard, resultBody, resultLangBadge;
  let btnCopy, copyLabel, copyIcon;
  let btnListen, listenLabel, btnPause, btnResume, btnStop;
  let speechWave, waveLangName, voiceNotice;

  // DOM Elements - Floating Modal
  let modal, closeBtn, triggerBtns, modalContextBar, modalLangPills;
  let modalAudioBar, modalVoiceIndicator, modalSpeakingIndicator;
  let modalBtnPlay, modalBtnPause, modalBtnResume, modalBtnStop, modalBtnReplay;
  let modalVoiceNotice, modalTranscript, modalSuggestionsSection, modalSuggestionsChips;
  let modalInputQuery, modalBtnSend, modalBtnMic, modalMicStatus, modalMicLangLabel;

  document.addEventListener('DOMContentLoaded', () => {
    initElements();
    initSpeechSynthesis();
    initSpeechRecognition();
    setupTranslationBox();
    setupModal();
    bindEvents();
  });

  // ---------------------------------------------------------------------------
  // 1. Initialization of DOM Elements
  // ---------------------------------------------------------------------------
  function initElements() {
    // Translation Box Elements
    fromLangSelect = document.getElementById('trans-from-lang');
    toLangSelect = document.getElementById('trans-to-lang');
    btnSwap = document.getElementById('trans-btn-swap');
    sourceText = document.getElementById('trans-source-text');
    btnClear = document.getElementById('trans-btn-clear');
    btnTranslate = document.getElementById('trans-btn-translate');
    statusMsg = document.getElementById('trans-status-msg');
    resultCard = document.getElementById('trans-result-card');
    resultBody = document.getElementById('trans-result-body');
    resultLangBadge = document.getElementById('trans-result-lang-badge');

    btnCopy = document.getElementById('trans-btn-copy');
    copyLabel = document.getElementById('trans-copy-label');
    copyIcon = document.getElementById('trans-copy-icon');

    btnListen = document.getElementById('trans-btn-listen');
    listenLabel = document.getElementById('trans-listen-label');
    btnPause = document.getElementById('trans-btn-pause');
    btnResume = document.getElementById('trans-btn-resume');
    btnStop = document.getElementById('trans-btn-stop');
    speechWave = document.getElementById('trans-speech-wave');
    waveLangName = document.getElementById('trans-wave-lang-name');
    voiceNotice = document.getElementById('trans-voice-notice');

    // Floating Modal Elements
    modal = document.getElementById('parent-voice-modal');
    closeBtn = document.getElementById('pv-close-btn');
    triggerBtns = document.querySelectorAll('.pv-trigger-btn');
    modalContextBar = document.getElementById('pv-student-context-bar');
    modalLangPills = document.querySelectorAll('.pv-lang-pill');

    modalAudioBar = document.getElementById('pv-audio-bar');
    modalVoiceIndicator = document.getElementById('pv-voice-indicator');
    modalSpeakingIndicator = document.getElementById('pv-speaking-indicator');
    modalBtnPlay = document.getElementById('pv-audio-play');
    modalBtnPause = document.getElementById('pv-audio-pause');
    modalBtnResume = document.getElementById('pv-audio-resume');
    modalBtnStop = document.getElementById('pv-audio-stop');
    modalBtnReplay = document.getElementById('pv-audio-replay');

    modalVoiceNotice = document.getElementById('pv-voice-notice');
    modalTranscript = document.getElementById('pv-transcript');
    modalSuggestionsSection = document.getElementById('pv-suggestions-section');
    modalSuggestionsChips = document.getElementById('pv-suggestions-chips');

    modalInputQuery = document.getElementById('pv-question-input');
    modalBtnSend = document.getElementById('pv-btn-send');
    modalBtnMic = document.getElementById('pv-btn-mic');
    modalMicStatus = document.getElementById('pv-mic-status');
    modalMicLangLabel = document.getElementById('pv-mic-lang-label');
  }

  // ---------------------------------------------------------------------------
  // 2. Three-Language Non-AI Translation Box Logic
  // ---------------------------------------------------------------------------
  function setupTranslationBox() {
    if (!fromLangSelect || !toLangSelect) return;

    // Set default initial languages
    fromLangSelect.value = state.fromLang;
    updateTargetDropdown(state.fromLang, state.toLang);

    // Pre-populate source text area with student info
    prepopulateSourceText();

    // Source textarea edit tracking
    if (sourceText) {
      sourceText.addEventListener('input', () => {
        state.hasUserEditedSource = true;
      });
    }

    // Auto-update pre-population when user changes career dropdown in compare form
    const studentSelect = document.getElementById('student_career_id');
    if (studentSelect) {
      studentSelect.addEventListener('change', () => {
        if (!state.hasUserEditedSource) {
          prepopulateSourceText(true);
        }
      });
    }

    const studentReasonsInput = document.getElementById('student_reasons');
    if (studentReasonsInput) {
      studentReasonsInput.addEventListener('change', () => {
        if (!state.hasUserEditedSource) {
          prepopulateSourceText(true);
        }
      });
    }
  }

  function updateTargetDropdown(sourceLang, targetLangToSet) {
    if (!toLangSelect) return;
    const currentTarget = targetLangToSet || toLangSelect.value;
    const availableTargets = ['en', 'te', 'hi'].filter(c => c !== sourceLang);

    toLangSelect.innerHTML = '';
    availableTargets.forEach(code => {
      const opt = document.createElement('option');
      opt.value = code;
      opt.textContent = code === 'en' ? 'English' : `${LANGUAGES[code].name} — ${LANGUAGES[code].native}`;
      toLangSelect.appendChild(opt);
    });

    if (availableTargets.includes(currentTarget)) {
      toLangSelect.value = currentTarget;
    } else {
      toLangSelect.value = availableTargets[0];
    }
    state.toLang = toLangSelect.value;
    updateTargetBadge();
  }

  function swapLanguages() {
    if (!fromLangSelect || !toLangSelect) return;
    const oldFrom = fromLangSelect.value;
    const oldTo = toLangSelect.value;

    fromLangSelect.value = oldTo;
    state.fromLang = oldTo;

    updateTargetDropdown(oldTo, oldFrom);
    toLangSelect.value = oldFrom;
    state.toLang = oldFrom;

    // If there is an existing translated text in result card, swap it to the source text area
    if (resultBody && sourceText) {
      const currentRes = resultBody.innerText.trim();
      if (currentRes && !currentRes.startsWith('Click')) {
        sourceText.value = currentRes;
        state.hasUserEditedSource = true;
      }
    }

    updateTargetBadge();
    stopTTS();
  }

  function updateTargetBadge() {
    if (!resultLangBadge) return;
    const cfg = LANGUAGES[state.toLang] || LANGUAGES.te;
    resultLangBadge.textContent = `${cfg.name} (${cfg.code})`;
  }

  function prepopulateSourceText(force = false) {
    if (!sourceText) return;
    if (sourceText.value.trim() && !force) return;

    const studentSelect = document.getElementById('student_career_id');
    const studentReasonsInput = document.getElementById('student_reasons');

    let careerTitle = '';
    if (studentSelect && studentSelect.value) {
      const opt = studentSelect.options[studentSelect.selectedIndex];
      if (opt && opt.value) careerTitle = opt.text.trim();
    }
    if (!careerTitle && studentSelect && studentSelect.options.length > 1) {
      const firstReal = studentSelect.options[1];
      if (firstReal && firstReal.value) careerTitle = firstReal.text.trim();
    }
    if (!careerTitle) careerTitle = 'Civil Engineer (Engineering & Technology)';

    // Clean title for natural readability
    const cleanTitle = careerTitle.replace(/\s*\([^)]*\)/, '');

    const reasons = (studentReasonsInput && studentReasonsInput.value.trim())
      ? studentReasonsInput.value.trim()
      : 'I enjoy designing buildings and practical structures';

    const checkedGoals = Array.from(document.querySelectorAll('input[name="s_goal"]:checked'))
      .map(cb => {
        const parentLabel = cb.closest('label');
        return parentLabel ? parentLabel.textContent.trim() : cb.value;
      });

    const goalsText = checkedGoals.length > 0
      ? checkedGoals.join(', ')
      : 'Creative Freedom, Fast Skill Growth';

    sourceText.value = `My child is interested in ${cleanTitle}. Reasons: ${reasons}. Top priorities: ${goalsText}.`;
  }

  async function handleTranslate() {
    if (!sourceText) return;
    const text = sourceText.value.trim();

    if (!text) {
      showStatusNotice('Please enter or pre-populate text to translate.', 'warning');
      sourceText.focus();
      return;
    }

    const fromLang = fromLangSelect ? fromLangSelect.value : 'en';
    const toLang = toLangSelect ? toLangSelect.value : 'te';

    if (fromLang === toLang) {
      showStatusNotice('Source and target languages are identical. Please choose different languages.', 'info');
      return;
    }

    hideStatusNotice();
    setTranslateLoading(true);

    try {
      const response = await fetch('/api/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: text,
          source_language: fromLang,
          target_language: toLang
        })
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        const errMessage = (data.error && data.error.message)
          ? data.error.message
          : 'Translation could not be completed. Please check your text or try again.';
        showStatusNotice(errMessage, 'danger');
        return;
      }

      // Success: Render translated result
      const translated = data.translated_text || '';
      state.currentTranslation = translated;
      if (resultBody) {
        resultBody.textContent = translated;
      }
      updateTargetBadge();
      stopTTS();

    } catch (err) {
      console.error('Translation error:', err);
      showStatusNotice('Network connection error while translating. Please retry.', 'danger');
    } finally {
      setTranslateLoading(false);
    }
  }

  function handleClear() {
    if (sourceText) {
      sourceText.value = '';
      sourceText.focus();
    }
    state.hasUserEditedSource = true;
    hideStatusNotice();
  }

  async function handleCopy() {
    if (!resultBody) return;
    const text = resultBody.innerText.trim();

    if (!text || text.startsWith('Click')) {
      showStatusNotice('No translated text available to copy yet.', 'info');
      return;
    }

    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(text);
      } else {
        const ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
      }

      if (copyLabel) copyLabel.textContent = 'Copied! ✓';
      if (copyIcon) copyIcon.textContent = '✅';

      setTimeout(() => {
        if (copyLabel) copyLabel.textContent = 'Copy Translation';
        if (copyIcon) copyIcon.textContent = '📋';
      }, 2000);

    } catch (err) {
      console.warn('Clipboard copy error:', err);
      showStatusNotice('Unable to copy automatically. You can copy the text manually above.', 'warning');
    }
  }

  function setTranslateLoading(isLoading) {
    if (!btnTranslate) return;
    btnTranslate.disabled = isLoading;
    if (isLoading) {
      btnTranslate.innerHTML = '<span>Translating...</span> ⏳';
    } else {
      btnTranslate.innerHTML = '<span>Translate</span> ➔';
    }
  }

  function showStatusNotice(message, type = 'info') {
    if (!statusMsg) return;
    statusMsg.className = `trans-notice ${type}`;
    statusMsg.textContent = message;
    statusMsg.style.display = 'flex';
  }

  function hideStatusNotice() {
    if (!statusMsg) return;
    statusMsg.style.display = 'none';
    statusMsg.textContent = '';
  }

  // ---------------------------------------------------------------------------
  // 3. Web Speech API — Text-to-Speech (TTS) for Translation Result
  // ---------------------------------------------------------------------------
  function initSpeechSynthesis() {
    if (!('speechSynthesis' in window)) return;
    loadVoices();
    window.speechSynthesis.onvoiceschanged = () => {
      loadVoices();
    };
  }

  function loadVoices() {
    if (!('speechSynthesis' in window)) return;
    state.availableVoices = window.speechSynthesis.getVoices() || [];
  }

  function findMatchingVoice(langCode) {
    if (!state.availableVoices || !state.availableVoices.length) loadVoices();
    const cfg = LANGUAGES[langCode] || LANGUAGES.en;

    // 1. Direct locale code match (te-IN, hi-IN, en-IN)
    let match = state.availableVoices.find(v => v.lang.toLowerCase() === cfg.code.toLowerCase());
    if (match) return match;

    // 2. Prefix match (te, hi, en)
    match = state.availableVoices.find(v => v.lang.toLowerCase().startsWith(langCode));
    if (match) return match;

    // 3. Name search
    match = state.availableVoices.find(v => {
      const vName = v.name.toLowerCase();
      return cfg.voiceMatch.some(k => vName.includes(k));
    });
    if (match) return match;

    // 4. Fallback for English
    if (langCode === 'en') {
      return state.availableVoices.find(v => v.lang.toLowerCase().startsWith('en')) || state.availableVoices[0] || null;
    }

    return null;
  }

  function speakTranslation() {
    if (!('speechSynthesis' in window)) {
      showStatusNotice('Web Speech Synthesis is not supported in this browser.', 'warning');
      return;
    }

    const text = (resultBody ? resultBody.innerText.trim() : '') || state.currentTranslation;
    if (!text || text.startsWith('Click')) {
      showStatusNotice('Please translate your text before listening.', 'info');
      return;
    }

    stopTTS();

    const targetLang = toLangSelect ? toLangSelect.value : state.toLang;
    const cfg = LANGUAGES[targetLang] || LANGUAGES.en;
    const voice = findMatchingVoice(targetLang);

    if (waveLangName) {
      waveLangName.textContent = `${cfg.name} (${cfg.code})`;
    }

    // Split text into readable chunks
    const cleanText = text.replace(/[*#_`]/g, '').trim();
    const rawChunks = cleanText.match(/[^.!?।\n]+[.!?।\n]+/g) || [cleanText];
    state.speechChunks = rawChunks.map(c => c.trim()).filter(c => c.length > 0);
    state.chunkIndex = 0;

    if (!state.speechChunks.length) return;

    state.isSpeaking = true;
    state.isPaused = false;
    updateAudioControlsUI(true, false);

    speakNextChunk(voice, targetLang);
  }

  function speakNextChunk(voice, targetLang) {
    if (!state.isSpeaking || state.chunkIndex >= state.speechChunks.length) {
      stopTTS();
      return;
    }

    const chunk = state.speechChunks[state.chunkIndex];
    const utterance = new SpeechSynthesisUtterance(chunk);

    if (voice) {
      utterance.voice = voice;
      utterance.lang = voice.lang;
    } else {
      utterance.lang = LANGUAGES[targetLang].code;
    }

    utterance.rate = 0.95;
    utterance.pitch = 1.0;

    utterance.onend = () => {
      state.chunkIndex++;
      speakNextChunk(voice, targetLang);
    };

    utterance.onerror = (e) => {
      console.warn('TTS playback error:', e);
      state.chunkIndex++;
      speakNextChunk(voice, targetLang);
    };

    window.speechSynthesis.speak(utterance);
  }

  function pauseTTS() {
    if ('speechSynthesis' in window && state.isSpeaking) {
      window.speechSynthesis.pause();
      state.isPaused = true;
      updateAudioControlsUI(true, true);
    }
  }

  function resumeTTS() {
    if ('speechSynthesis' in window && state.isSpeaking && state.isPaused) {
      window.speechSynthesis.resume();
      state.isPaused = false;
      updateAudioControlsUI(true, false);
    }
  }

  function stopTTS() {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    state.isSpeaking = false;
    state.isPaused = false;
    state.chunkIndex = 0;
    updateAudioControlsUI(false, false);
  }

  function updateAudioControlsUI(speaking, paused) {
    if (speechWave) {
      speechWave.style.display = (speaking && !paused) ? 'flex' : 'none';
    }

    if (btnListen) {
      btnListen.style.display = speaking ? 'none' : 'inline-flex';
    }
    if (btnPause) {
      btnPause.style.display = (speaking && !paused) ? 'inline-flex' : 'none';
    }
    if (btnResume) {
      btnResume.style.display = (speaking && paused) ? 'inline-flex' : 'none';
    }
    if (btnStop) {
      btnStop.style.display = speaking ? 'inline-flex' : 'none';
    }
  }

  // ---------------------------------------------------------------------------
  // 4. Floating Modal AI Voice Assistant (Preserved)
  // ---------------------------------------------------------------------------
  function setupModal() {
    refreshStudentProfile();
  }

  function extractStudentCareerInfo() {
    const studentSelect = document.getElementById('student_career_id');
    const studentReasonsInput = document.getElementById('student_reasons');
    const altSelect = document.getElementById('alternative_career_id');
    const altReasonsInput = document.getElementById('alternative_reasons');
    const sharedSummaryInput = document.getElementById('shared_decision_summary');

    const checkedGoals = Array.from(document.querySelectorAll('input[name="s_goal"]:checked'))
      .map(cb => {
        const parentLabel = cb.closest('label');
        return parentLabel ? parentLabel.textContent.trim() : cb.value;
      });

    const checkedWorries = Array.from(document.querySelectorAll('input[name="p_worry"]:checked'))
      .map(cb => {
        const parentLabel = cb.closest('label');
        return parentLabel ? parentLabel.textContent.trim() : cb.value;
      });

    let careerTitle = '';
    let careerId = '';
    if (studentSelect && studentSelect.value) {
      careerId = studentSelect.value;
      const opt = studentSelect.options[studentSelect.selectedIndex];
      if (opt && opt.value) careerTitle = opt.text.trim();
    }
    if (!careerTitle && studentSelect && studentSelect.options.length > 1) {
      const firstReal = studentSelect.options[1];
      if (firstReal && firstReal.value) {
        careerTitle = firstReal.text.trim();
        careerId = firstReal.value;
      }
    }

    let altTitle = '';
    if (altSelect && altSelect.value) {
      const opt = altSelect.options[altSelect.selectedIndex];
      if (opt && opt.value) altTitle = opt.text.trim();
    }

    const assessmentData = window.CAREERCOMPASS_ASSESSMENT_DATA || null;

    return {
      hasSelection: Boolean(careerTitle && careerTitle !== '-- Choose Career --'),
      preferred_career: careerTitle || 'Civil Engineer (Engineering & Technology)',
      career_id: careerId,
      reasons: studentReasonsInput ? studentReasonsInput.value.trim() : '',
      goals: checkedGoals.length ? checkedGoals : ['Creative Freedom & Building Things', 'Fast Skill Growth'],
      parent_concerns: checkedWorries.length ? checkedWorries : ['Predictable Employment & Stability', 'Managing High College Tuition Costs'],
      alternative_career: altTitle,
      alternative_reasons: altReasonsInput ? altReasonsInput.value.trim() : '',
      shared_next_step: sharedSummaryInput ? sharedSummaryInput.value.trim() : '',
      education_level: assessmentData ? assessmentData.current_education_level : 'Undergraduate',
      budget_limit: assessmentData ? assessmentData.budget_limit : 'Moderate',
      interests: assessmentData ? (assessmentData.interests || []) : ['Problem-solving', 'Design', 'Technology'],
      strengths: assessmentData ? (assessmentData.strengths || []) : ['Analytical thinking', 'Practical execution']
    };
  }

  function refreshStudentProfile() {
    state.studentProfile = extractStudentCareerInfo();
    renderModalStudentContext(state.studentProfile);
  }

  function renderModalStudentContext(profile) {
    if (!modalContextBar) return;
    const goalsHtml = profile.goals.map(g => `<span class="pv-chip">${escapeHtml(g)}</span>`).join('');
    const worriesHtml = profile.parent_concerns.map(w => `<span class="pv-chip pv-chip-worry">${escapeHtml(w)}</span>`).join('');

    modalContextBar.innerHTML = `
      <div class="pv-context-card">
        <div class="pv-context-row">
          <div>
            <span class="pv-context-label">🎓 Student Pathway:</span>
            <strong class="pv-context-val">${escapeHtml(profile.preferred_career)}</strong>
          </div>
          ${profile.reasons ? `
            <div style="margin-top: 0.25rem;">
              <span class="pv-context-label">💬 Reason:</span>
              <span style="font-style: italic;">"${escapeHtml(profile.reasons)}"</span>
            </div>
          ` : ''}
        </div>
        <div class="pv-context-tags">
          <div class="pv-tag-group"><span class="pv-tag-label">🎯 Goals:</span><div class="pv-chip-wrap">${goalsHtml}</div></div>
          <div class="pv-tag-group"><span class="pv-tag-label">👨‍👩‍👧 Concerns:</span><div class="pv-chip-wrap">${worriesHtml}</div></div>
        </div>
      </div>
    `;
  }

  function setModalLanguage(lang) {
    if (!LANGUAGES[lang]) return;
    state.modalLang = lang;
    modalLangPills.forEach(pill => {
      const match = pill.dataset.lang === lang;
      pill.classList.toggle('active', match);
      pill.setAttribute('aria-checked', match ? 'true' : 'false');
    });
    if (modalMicLangLabel) modalMicLangLabel.textContent = LANGUAGES[lang].name;
    stopTTS();
  }

  async function submitModalQuestion(preset) {
    const text = (preset || (modalInputQuery ? modalInputQuery.value : '')).trim();
    if (!text) return;

    if (modalInputQuery) modalInputQuery.value = '';
    appendMessageToModalTranscript('user', text, 'Parent');
    if (modalBtnSend) modalBtnSend.disabled = true;

    try {
      const payload = {
        language: state.modalLang,
        student_profile: state.studentProfile,
        message: text
      };

      const res = await fetch('/api/parent-career-guide', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      if (!res.ok || !data.success) {
        appendMessageToModalTranscript('assistant', data.error ? data.error.message : 'Error retrieving response.', 'System');
        return;
      }

      state.modalAiReply = data.reply || '';
      appendMessageToModalTranscript('assistant', state.modalAiReply, LANGUAGES[state.modalLang].name);

    } catch (err) {
      console.error('Modal question error:', err);
      appendMessageToModalTranscript('assistant', 'Network error connecting to guidance service.', 'System');
    } finally {
      if (modalBtnSend) modalBtnSend.disabled = false;
    }
  }

  function appendMessageToModalTranscript(role, text, speakerName) {
    if (!modalTranscript) return;
    const msgEl = document.createElement('div');
    msgEl.className = `pv-msg pv-msg-${role === 'user' ? 'user' : 'ai'}`;
    const formatted = formatMarkdown(text);
    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    if (role === 'user') {
      msgEl.innerHTML = `
        <div class="pv-msg-bubble pv-bubble-user">
          <div class="pv-msg-header"><span class="pv-msg-speaker">👨‍👩‍👧 ${escapeHtml(speakerName)}</span><span class="pv-msg-time">${timeStr}</span></div>
          <div class="pv-msg-content">${formatted}</div>
        </div>
      `;
    } else {
      msgEl.innerHTML = `
        <div class="pv-msg-bubble pv-bubble-ai">
          <div class="pv-msg-header">
            <span class="pv-msg-speaker">✨ Career Guide (${escapeHtml(speakerName)})</span>
            <span class="pv-msg-time">${timeStr}</span>
          </div>
          <div class="pv-msg-content">${formatted}</div>
        </div>
      `;
    }

    modalTranscript.appendChild(msgEl);
    modalTranscript.scrollTop = modalTranscript.scrollHeight;
  }

  function openModal() {
    if (!modal) return;
    state.isModalOpen = true;
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    refreshStudentProfile();
  }

  function closeModal() {
    if (!modal) return;
    state.isModalOpen = false;
    modal.style.display = 'none';
    document.body.style.overflow = '';
    stopTTS();
    stopListening();
  }

  function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return;

    try {
      state.recognition = new SpeechRecognition();
      state.recognition.continuous = false;
      state.recognition.interimResults = false;

      state.recognition.onstart = () => {
        state.isListening = true;
        if (modalBtnMic) modalBtnMic.classList.add('listening');
        if (modalMicStatus) modalMicStatus.style.display = 'flex';
      };

      state.recognition.onresult = (event) => {
        if (event.results && event.results[0] && event.results[0][0]) {
          const transcript = event.results[0][0].transcript;
          if (modalInputQuery) modalInputQuery.value = transcript;
        }
      };

      state.recognition.onerror = () => {
        stopListening();
      };

      state.recognition.onend = () => {
        stopListening();
      };
    } catch (err) {
      console.warn('SpeechRecognition init error:', err);
    }
  }

  function toggleListening() {
    if (!state.recognition) {
      if (modalInputQuery) modalInputQuery.focus();
      return;
    }
    if (state.isListening) {
      state.recognition.stop();
      stopListening();
    } else {
      try {
        state.recognition.lang = LANGUAGES[state.modalLang].code;
        state.recognition.start();
      } catch (err) {
        stopListening();
      }
    }
  }

  function stopListening() {
    state.isListening = false;
    if (modalBtnMic) modalBtnMic.classList.remove('listening');
    if (modalMicStatus) modalMicStatus.style.display = 'none';
  }

  // ---------------------------------------------------------------------------
  // 5. Event Bindings
  // ---------------------------------------------------------------------------
  function bindEvents() {
    // Translation Box Controls
    if (fromLangSelect) {
      fromLangSelect.addEventListener('change', () => {
        state.fromLang = fromLangSelect.value;
        updateTargetDropdown(state.fromLang);
      });
    }

    if (toLangSelect) {
      toLangSelect.addEventListener('change', () => {
        state.toLang = toLangSelect.value;
        updateTargetBadge();
      });
    }

    if (btnSwap) btnSwap.addEventListener('click', swapLanguages);
    if (btnTranslate) btnTranslate.addEventListener('click', handleTranslate);
    if (btnClear) btnClear.addEventListener('click', handleClear);
    if (btnCopy) btnCopy.addEventListener('click', handleCopy);

    // TTS Controls for Translated Result
    if (btnListen) btnListen.addEventListener('click', speakTranslation);
    if (btnPause) btnPause.addEventListener('click', pauseTTS);
    if (btnResume) btnResume.addEventListener('click', resumeTTS);
    if (btnStop) btnStop.addEventListener('click', stopTTS);

    // Modal Trigger Buttons
    triggerBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        openModal();
      });
    });

    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
      });
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && state.isModalOpen) closeModal();
    });

    // Modal Language Pills
    modalLangPills.forEach(pill => {
      pill.addEventListener('click', () => setModalLanguage(pill.dataset.lang));
    });

    // Modal Audio Controls
    if (modalBtnPlay) modalBtnPlay.addEventListener('click', () => speakTranslation());
    if (modalBtnPause) modalBtnPause.addEventListener('click', pauseTTS);
    if (modalBtnResume) modalBtnResume.addEventListener('click', resumeTTS);
    if (modalBtnStop) modalBtnStop.addEventListener('click', stopTTS);
    if (modalBtnReplay) modalBtnReplay.addEventListener('click', () => speakTranslation());

    // Modal Composer
    if (modalBtnMic) modalBtnMic.addEventListener('click', toggleListening);
    if (modalBtnSend) modalBtnSend.addEventListener('click', () => submitModalQuestion());
    if (modalInputQuery) {
      modalInputQuery.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          submitModalQuestion();
        }
      });
    }
  }

  // ---------------------------------------------------------------------------
  // 6. Helpers
  // ---------------------------------------------------------------------------
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function formatMarkdown(text) {
    if (!text) return '';
    let escaped = escapeHtml(text);
    escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    return escaped;
  }

  // Expose global API
  window.CareerCompassTranslation = {
    translate: handleTranslate,
    swap: swapLanguages,
    clear: handleClear,
    copy: handleCopy,
    speak: speakTranslation,
    stop: stopTTS
  };

})();
