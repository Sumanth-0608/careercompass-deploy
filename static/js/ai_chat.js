/**
 * CareerCompass — Multi-AI Career Chat Client Controller
 * Manages provider/model selection, conversation lifecycle,
 * streaming-like UX, safe markdown rendering, and CareerCompass action chips.
 */

let aiChatState = {
  providers: [],
  activeProviderId: "gemini",
  activeModelId: "gemini-1.5-flash",
  conversationId: null,
  messages: [], // [{role: 'user'|'assistant', content: string, action_chips: []}]
  isLoading: false,
  profileOptIn: false,
  cachedProfile: null
};

document.addEventListener("DOMContentLoaded", async () => {
  initProfileData();
  await loadProviders();
  await loadConversationsList();
});

// ---------------------------------------------------------------------------
// 1. Providers & Models Management
// ---------------------------------------------------------------------------
async function loadProviders() {
  try {
    const res = await fetch("/api/ai/providers");
    if (!res.ok) throw new Error("Failed to load providers list");
    const data = await res.json();
    aiChatState.providers = data.providers || [];

    // Default to first configured provider if available, otherwise first provider
    const firstConfigured = aiChatState.providers.find(p => p.is_configured);
    const initialProvider = firstConfigured || aiChatState.providers[0];
    
    if (initialProvider) {
      selectProvider(initialProvider.id);
    }
  } catch (err) {
    console.error("Error loading providers:", err);
  }
}

function selectProvider(providerId) {
  const p = aiChatState.providers.find(item => item.id === providerId);
  if (!p) return;

  aiChatState.activeProviderId = p.id;
  aiChatState.activeModelId = p.default_model;

  // Update provider cards active state
  document.querySelectorAll(".provider-card").forEach(card => {
    if (card.getAttribute("data-provider-id") === p.id) {
      card.classList.add("active");
    } else {
      card.classList.remove("active");
    }
  });

  // Populate models dropdown
  const modelSelect = document.getElementById("model-select");
  if (modelSelect) {
    modelSelect.innerHTML = "";
    (p.models || []).forEach(m => {
      const opt = document.createElement("option");
      opt.value = m.id;
      opt.textContent = m.name;
      if (m.id === p.default_model) opt.selected = true;
      modelSelect.appendChild(opt);
    });
  }

  // Update chat header info
  const hIcon = document.getElementById("header-provider-icon");
  const hTitle = document.getElementById("header-provider-title");
  const hStatus = document.getElementById("header-status-pill");
  const hModel = document.getElementById("header-model-label");
  const typingAvatar = document.getElementById("typing-avatar");

  if (hIcon) hIcon.textContent = p.icon;
  if (typingAvatar) typingAvatar.textContent = p.icon;
  if (hTitle) hTitle.textContent = p.name;
  if (hModel) hModel.textContent = `Model: ${p.default_model}`;

  if (hStatus) {
    if (p.status === "configured" || p.is_configured) {
      hStatus.className = "status-pill status-configured";
      hStatus.textContent = "● Configured";
    } else if (p.status === "unavailable") {
      hStatus.className = "status-pill status-unavailable";
      hStatus.textContent = "⚠ Temporarily Unavailable";
    } else {
      hStatus.className = "status-pill status-not_configured";
      hStatus.textContent = "○ Not Configured";
    }
  }
}

function handleModelChange(modelId) {
  aiChatState.activeModelId = modelId;
  const hModel = document.getElementById("header-model-label");
  if (hModel) hModel.textContent = `Model: ${modelId}`;
}

// ---------------------------------------------------------------------------
// 2. Profile Opt-In Integration
// ---------------------------------------------------------------------------
function initProfileData() {
  // Read any saved profile info from localStorage or session
  try {
    const saved = localStorage.getItem("cc_profile_data");
    if (saved) {
      aiChatState.cachedProfile = JSON.parse(saved);
    }
  } catch (e) {
    aiChatState.cachedProfile = null;
  }
}

function toggleProfileSharing(checked) {
  aiChatState.profileOptIn = checked;
  const note = document.getElementById("profile-status-note");
  if (note) {
    note.style.display = checked ? "block" : "none";
  }
}

// ---------------------------------------------------------------------------
// 3. Conversation Lifecycle & Sidebar History
// ---------------------------------------------------------------------------
async function loadConversationsList() {
  const container = document.getElementById("conversation-list");
  if (!container) return;

  try {
    const res = await fetch("/api/ai/conversations");
    if (!res.ok) return;
    const data = await res.json();
    const convs = data.conversations || [];

    if (convs.length === 0) {
      container.innerHTML = `<div style="font-size: 0.82rem; color: var(--text-muted); text-align: center; padding: 1.25rem 0;">No past sessions yet.</div>`;
      return;
    }

    container.innerHTML = "";
    convs.forEach(c => {
      const item = document.createElement("div");
      item.className = `conv-history-item ${c.id === aiChatState.conversationId ? 'active' : ''}`;
      item.innerHTML = `
        <div class="conv-item-text" onclick="loadConversationDetail('${escapeHtml(c.id)}')">
          <div class="conv-title">${escapeHtml(c.title || 'Career Consultation')}</div>
          <div class="conv-meta">${escapeHtml(c.provider)} · ${formatDate(c.updated_at)}</div>
        </div>
        <button type="button" class="conv-del-btn" onclick="deleteConversation('${escapeHtml(c.id)}', event)" title="Delete session">&times;</button>
      `;
      container.appendChild(item);
    });
  } catch (err) {
    console.error("Failed to load conversation history:", err);
  }
}

async function loadConversationDetail(convId) {
  try {
    const res = await fetch(`/api/ai/conversations/${encodeURIComponent(convId)}`);
    if (!res.ok) throw new Error("Conversation could not be loaded");
    const data = await res.json();
    
    aiChatState.conversationId = convId;
    aiChatState.messages = (data.messages || []).map(m => ({
      role: m.role,
      content: m.content,
      action_chips: m.action_chips || []
    }));

    // Re-render messages feed
    renderMessagesFeed();

    // Switch mobile tab back to chat view if on mobile
    switchMobileAiTab("chat");

    // Highlight active in sidebar
    document.querySelectorAll(".conv-history-item").forEach(el => el.classList.remove("active"));
    await loadConversationsList();
  } catch (err) {
    alert(err.message || "Failed to load session");
  }
}

function startNewChat() {
  aiChatState.conversationId = null;
  aiChatState.messages = [];
  renderMessagesFeed();
  switchMobileAiTab("chat");
  const input = document.getElementById("chat-input");
  if (input) input.focus();
}

function clearCurrentChat() {
  if (confirm("Clear current conversation messages?")) {
    aiChatState.messages = [];
    renderMessagesFeed();
  }
}

async function clearAllConversations() {
  if (!confirm("Are you sure you want to delete all saved consultation sessions?")) return;
  try {
    await fetch("/api/ai/conversations/clear", { method: "POST" });
    startNewChat();
    await loadConversationsList();
  } catch (err) {
    console.error("Failed to clear sessions:", err);
  }
}

async function deleteConversation(convId, evt) {
  if (evt) evt.stopPropagation();
  if (!confirm("Delete this consultation session?")) return;

  try {
    const res = await fetch(`/api/ai/conversations/${encodeURIComponent(convId)}`, { method: "DELETE" });
    if (res.ok) {
      if (aiChatState.conversationId === convId) {
        startNewChat();
      }
      await loadConversationsList();
    }
  } catch (err) {
    console.error("Failed to delete session:", err);
  }
}

// ---------------------------------------------------------------------------
// 4. Message Submission & Streaming UX
// ---------------------------------------------------------------------------
function handleComposerInput(textarea) {
  const counter = document.getElementById("char-counter");
  if (counter) {
    counter.textContent = `${textarea.value.length} / 2500 characters`;
  }
  // Auto-resize textarea up to 140px
  textarea.style.height = "auto";
  textarea.style.height = `${Math.min(textarea.scrollHeight, 140)}px`;
}

function handleComposerKeydown(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    const form = document.getElementById("chat-composer-form");
    if (form) form.requestSubmit();
  }
}

function applyPromptChip(text) {
  const input = document.getElementById("chat-input");
  if (input) {
    input.value = text;
    handleComposerInput(input);
    const form = document.getElementById("chat-composer-form");
    if (form) form.requestSubmit();
  }
}

async function handleChatSubmit(e) {
  e.preventDefault();
  if (aiChatState.isLoading) return;

  const input = document.getElementById("chat-input");
  const userText = (input.value || "").trim();
  if (!userText) return;

  // Clear composer & reset height
  input.value = "";
  handleComposerInput(input);

  // Append user message locally
  const userMsg = { role: "user", content: userText };
  aiChatState.messages.push(userMsg);
  appendSingleMessageDOM(userMsg);

  // Set loading state
  setLoadingState(true);

  // Prepare payload
  const payload = {
    provider: aiChatState.activeProviderId,
    model: aiChatState.activeModelId,
    message: userText,
    messages: aiChatState.messages.map(m => ({ role: m.role, content: m.content })),
    conversation_id: aiChatState.conversationId || undefined,
    use_profile: aiChatState.profileOptIn,
    profile_data: aiChatState.profileOptIn ? aiChatState.cachedProfile : undefined
  };

  try {
    const res = await fetch("/api/ai/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (!res.ok) {
      let errText = "The AI service returned an error. Please retry or select another provider.";
      if (data && data.error) {
        if (typeof data.error === "object" && data.error.message) {
          errText = data.error.message;
        } else if (typeof data.error === "string") {
          errText = data.error;
        }
      }
      renderErrorMessage(errText, userText);
      return;
    }

    if (data.conversation_id) {
      aiChatState.conversationId = data.conversation_id;
    }

    const replyContent = data.reply || (data.message && data.message.content) || "";
    const actionChips = (data.message && data.message.action_chips) || data.action_chips || [];

    const assistantMsg = {
      role: "assistant",
      content: replyContent,
      action_chips: actionChips
    };

    aiChatState.messages.push(assistantMsg);
    appendSingleMessageDOM(assistantMsg);

    // Refresh conversation list in sidebar
    loadConversationsList();

  } catch (err) {
    console.error("Chat error:", err);
    renderErrorMessage("Network connection error. Please verify your internet connection and retry.", userText);
  } finally {
    setLoadingState(false);
  }
}

function setLoadingState(loading) {
  aiChatState.isLoading = loading;
  const sendBtn = document.getElementById("btn-chat-send");
  const sendIcon = document.getElementById("send-btn-icon");
  const sendText = document.getElementById("send-btn-text");
  const typingIndicator = document.getElementById("typing-indicator");
  const messagesArea = document.getElementById("chat-messages-area");

  if (sendBtn) sendBtn.disabled = loading;
  if (sendIcon) sendIcon.textContent = loading ? "⏳" : "➤";
  if (sendText) sendText.textContent = loading ? "Sending..." : "Send";

  if (typingIndicator) {
    typingIndicator.style.display = loading ? "flex" : "none";
    if (loading && messagesArea) {
      messagesArea.scrollTop = messagesArea.scrollHeight;
    }
  }
}

// ---------------------------------------------------------------------------
// 5. Message Rendering & DOM Builders
// ---------------------------------------------------------------------------
function renderMessagesFeed() {
  const container = document.getElementById("dynamic-messages-container");
  if (!container) return;

  container.innerHTML = "";
  aiChatState.messages.forEach(msg => {
    appendSingleMessageDOM(msg);
  });

  const messagesArea = document.getElementById("chat-messages-area");
  if (messagesArea) {
    messagesArea.scrollTop = messagesArea.scrollHeight;
  }
}

function appendSingleMessageDOM(msg) {
  const container = document.getElementById("dynamic-messages-container");
  if (!container) return;

  const isUser = msg.role === "user";
  const pObj = aiChatState.providers.find(p => p.id === aiChatState.activeProviderId);
  const pIcon = pObj ? pObj.icon : "🤖";
  const pName = pObj ? pObj.name : "CareerCompass AI";

  const row = document.createElement("div");
  row.className = `chat-message-row ${isUser ? 'user-row' : 'assistant-row'}`;

  if (isUser) {
    row.innerHTML = `
      <div class="user-message-bubble">
        <div class="bubble-content">${escapeHtml(msg.content)}</div>
      </div>
    `;
  } else {
    const formattedHtml = formatMarkdownSafe(msg.content);
    const chipsHtml = buildActionChipsHtml(msg.action_chips);

    row.innerHTML = `
      <div class="ai-message-bubble">
        <div class="bubble-header">
          <div style="display: flex; align-items: center; gap: 0.45rem;">
            <span class="bubble-avatar">${pIcon}</span>
            <strong style="color: var(--text-heading); font-size: 0.90rem;">${escapeHtml(pName)}</strong>
          </div>
          <button type="button" class="btn-copy-bubble" onclick="copyMessageText(this)" title="Copy advice text">
            📋 Copy
          </button>
        </div>
        
        <div class="bubble-content formatted-markdown">
          ${formattedHtml}
        </div>

        ${chipsHtml}
      </div>
    `;
  }

  container.appendChild(row);

  const messagesArea = document.getElementById("chat-messages-area");
  if (messagesArea) {
    messagesArea.scrollTop = messagesArea.scrollHeight;
  }
}

function renderErrorMessage(errorText, retryText) {
  const container = document.getElementById("dynamic-messages-container");
  if (!container) return;

  const row = document.createElement("div");
  row.className = "chat-message-row assistant-row";
  row.innerHTML = `
    <div class="ai-message-bubble error-bubble">
      <div class="bubble-header" style="color: #DC2626;">
        <span class="bubble-avatar">⚠️</span>
        <strong>Provider Notice</strong>
      </div>
      <div class="bubble-content" style="color: #991B1B; font-size: 0.92rem; margin: 0.4rem 0;">
        ${escapeHtml(errorText)}
      </div>
      <div style="margin-top: 0.75rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
        <button type="button" class="btn btn-sm btn-outline" onclick="applyPromptChip('${escapeHtml(retryText).replace(/'/g, "\\'")}')">
          🔄 Retry Question
        </button>
        <button type="button" class="btn btn-sm btn-outline" onclick="switchMobileAiTab('sidebar')">
          ⚙️ Switch Provider
        </button>
      </div>
    </div>
  `;

  container.appendChild(row);
  const messagesArea = document.getElementById("chat-messages-area");
  if (messagesArea) messagesArea.scrollTop = messagesArea.scrollHeight;
}

function buildActionChipsHtml(chips) {
  if (!chips || !Array.isArray(chips) || chips.length === 0) return "";

  const items = chips.map(c => `
    <a href="${escapeHtml(c.url)}" class="action-chip-link" title="${escapeHtml(c.label)}">
      <span>${escapeHtml(c.icon || '🔗')}</span>
      <span>${escapeHtml(c.label)}</span>
      <span style="font-size: 0.75rem;">&rarr;</span>
    </a>
  `).join("");

  return `
    <div class="career-action-chips-box">
      <div class="action-chips-title">Recommended Career Actions:</div>
      <div class="action-chips-flex">
        ${items}
      </div>
    </div>
  `;
}

// ---------------------------------------------------------------------------
// 6. Safe Markdown Formatter & Helpers
// ---------------------------------------------------------------------------
function formatMarkdownSafe(rawText) {
  if (!rawText) return "";

  // 1. Escape all HTML entities first to prevent XSS
  let text = escapeHtml(rawText);

  // 2. Bold: **text**
  text = text.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");

  // 3. Italic: *text* or _text_
  text = text.replace(/\*([^\*]+?)\*/g, "<em>$1</em>");

  // 4. Inline code: `code`
  text = text.replace(/`([^`]+?)`/g, "<code>$1</code>");

  // 5. Numbered lists (e.g. "1. ")
  text = text.replace(/^\s*(\d+)\.\s+(.+)$/gm, "<div class='md-list-item'><span class='md-num'>$1.</span> <span>$2</span></div>");

  // 6. Bullet lists (e.g. "- " or "* ")
  text = text.replace(/^\s*[-•]\s+(.+)$/gm, "<div class='md-list-item'><span class='md-bullet'>•</span> <span>$1</span></div>");

  // 7. Paragraph line breaks
  text = text.replace(/\n\n+/g, "</p><p>");
  text = text.replace(/\n/g, "<br>");

  return `<p>${text}</p>`;
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function copyMessageText(btnEl) {
  const card = btnEl.closest(".ai-message-bubble");
  if (!card) return;
  const contentEl = card.querySelector(".bubble-content");
  if (!contentEl) return;

  const textToCopy = contentEl.innerText || contentEl.textContent;
  navigator.clipboard.writeText(textToCopy).then(() => {
    const originalText = btnEl.textContent;
    btnEl.textContent = "✓ Copied!";
    btnEl.classList.add("copied");
    setTimeout(() => {
      btnEl.textContent = originalText;
      btnEl.classList.remove("copied");
    }, 2000);
  }).catch(err => {
    console.error("Clipboard copy failed:", err);
  });
}

function formatDate(isoStr) {
  if (!isoStr) return "Recent";
  try {
    const d = new Date(isoStr);
    return d.toLocaleDateString([], { month: "short", day: "numeric" });
  } catch (e) {
    return "Recent";
  }
}

// ---------------------------------------------------------------------------
// 7. Mobile Tab Switcher
// ---------------------------------------------------------------------------
function switchMobileAiTab(tab) {
  const sidebar = document.getElementById("ai-sidebar");
  const chatPanel = document.getElementById("ai-chat-panel");
  const btnChat = document.getElementById("tab-btn-chat");
  const btnSidebar = document.getElementById("tab-btn-sidebar");

  if (!sidebar || !chatPanel) return;

  if (tab === "chat") {
    sidebar.classList.remove("mobile-visible");
    chatPanel.classList.remove("mobile-hidden");
    if (btnChat) { btnChat.classList.add("btn-primary"); btnChat.classList.remove("btn-outline"); }
    if (btnSidebar) { btnSidebar.classList.add("btn-outline"); btnSidebar.classList.remove("btn-primary"); }
  } else {
    sidebar.classList.add("mobile-visible");
    chatPanel.classList.add("mobile-hidden");
    if (btnSidebar) { btnSidebar.classList.add("btn-primary"); btnSidebar.classList.remove("btn-outline"); }
    if (btnChat) { btnChat.classList.add("btn-outline"); btnChat.classList.remove("btn-primary"); }
  }
}
