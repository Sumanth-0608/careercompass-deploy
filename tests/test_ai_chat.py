"""
CareerCompass - AI Career Guidance Chat Tests (Gemini & OpenAI)
Verifies:
- Only Gemini and OpenAI are available (Claude, Mistral, Groq removed)
- Provider registry and honest configuration status
- Request validation (single message and message history)
- Safe error handling and missing API key reporting
- Standardized Task 5 response format
- Conversation persistence in SQLite
- Real SDK package availability
"""

import os
import json
import pytest
from app import app
from database import init_db


@pytest.fixture
def client(tmp_path):
    test_db = tmp_path / "test_ai_chat.db"
    app.config["TESTING"] = True
    app.config["DATABASE"] = str(test_db)
    init_db(db_path=str(test_db))

    with app.test_client() as client:
        yield client


def test_ai_chat_html_view(client):
    """Verifies that the /ai-chat page renders successfully with Gemini and OpenAI."""
    res = client.get("/ai-chat")
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "CareerCompass" in html
    assert "AI Chat" in html
    assert "Google Gemini" in html
    assert "OpenAI" in html or "ChatGPT" in html
    # Verify Claude, Mistral, Groq are removed
    assert "Anthropic Claude" not in html
    assert "Mistral AI" not in html
    assert "Groq Llama" not in html
    # Check navbar active state
    assert "active" in html
    # Check ambient background
    assert "blue-ambient-bg" in html


def test_get_ai_providers_endpoint(client):
    """Verifies /api/ai/providers returns exactly 2 providers (Gemini & OpenAI) with no secrets."""
    res = client.get("/api/ai/providers")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["count"] == 2

    provider_ids = [p["id"] for p in data["providers"]]
    assert set(provider_ids) == {"gemini", "openai"}

    for p in data["providers"]:
        assert p["id"] in ["gemini", "openai"]
        assert "name" in p
        assert "icon" in p
        assert "description" in p
        assert "is_configured" in p
        assert p["status"] in ["configured", "not_configured", "unavailable"]
        assert "models" in p
        assert len(p["models"]) >= 2
        # Ensure no secrets or API keys are exposed
        assert "api_key" not in p
        assert "env_key" not in p
        assert "key" not in p


def test_ai_chat_validation_failures(client):
    """Verifies request validation for invalid payloads, bad providers, and oversized text."""
    # Empty body
    res = client.post("/api/ai/chat", json=None)
    assert res.status_code == 400

    # Removed/invalid providers rejected
    for invalid_p in ["anthropic", "mistral", "groq", "unknown_ai"]:
        res = client.post("/api/ai/chat", json={
            "provider": invalid_p,
            "message": "Hello"
        })
        assert res.status_code == 400
        err = res.get_json()["error"]
        err_msg = err["message"] if isinstance(err, dict) else err
        assert "Invalid AI provider" in err_msg

    # Empty messages list
    res = client.post("/api/ai/chat", json={
        "provider": "gemini",
        "messages": []
    })
    assert res.status_code == 400
    err = res.get_json()["error"]
    err_msg = err["message"] if isinstance(err, dict) else err
    assert "cannot be empty" in err_msg

    # Message exceeds length limit
    res = client.post("/api/ai/chat", json={
        "provider": "gemini",
        "message": "A" * 3000
    })
    assert res.status_code == 400
    err = res.get_json()["error"]
    err_msg = err["message"] if isinstance(err, dict) else err
    assert "exceeds maximum allowed length" in err_msg


def test_ai_chat_missing_api_key_handling(client, monkeypatch):
    """Verifies that an unconfigured provider returns a safe 401 error explaining setup."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("AI_TEST_MODE", raising=False)

    res = client.post("/api/ai/chat", json={
        "provider": "gemini",
        "message": "What is civil engineering?"
    })
    assert res.status_code == 401
    data = res.get_json()
    assert data["success"] is False
    assert "error" in data
    err = data["error"]
    err_msg = err["message"] if isinstance(err, dict) else err
    assert "not configured yet" in err_msg or "GEMINI_API_KEY" in err_msg


def test_ai_chat_mock_mode_gemini_and_openai(client, monkeypatch):
    """
    Verifies execution in test mode for Gemini and OpenAI,
    confirming normalized output, reply field, and career action chips.
    """
    monkeypatch.setenv("AI_TEST_MODE", "1")

    for pid in ["gemini", "openai"]:
        res = client.post("/api/ai/chat", json={
            "provider": pid,
            "message": "I am interested in software engineering and civil engineering."
        })
        assert res.status_code == 200, f"Provider {pid} failed: {res.get_data(as_text=True)}"
        data = res.get_json()
        assert data["success"] is True
        assert data["provider"] == pid
        assert "reply" in data
        assert len(data["reply"]) > 20
        assert "model" in data
        assert "message" in data
        assert data["message"]["role"] == "assistant"
        # Check career action chips
        assert "action_chips" in data["message"]
        assert len(data["message"]["action_chips"]) > 0


def test_ai_chat_task5_standard_request_format(client, monkeypatch):
    """Verifies Task 5 standardized single-message + history format."""
    monkeypatch.setenv("AI_TEST_MODE", "1")

    res = client.post("/api/ai/chat", json={
        "provider": "gemini",
        "message": "Suggest career pathways for a student interested in civil engineering.",
        "history": []
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["provider"] == "gemini"
    assert "reply" in data
    assert "model" in data
    assert len(data["reply"]) > 0


def test_ai_conversation_persistence_lifecycle(client, monkeypatch):
    """Verifies creating, listing, viewing, and deleting AI conversations in SQLite."""
    monkeypatch.setenv("AI_TEST_MODE", "1")

    # Send a message to create a conversation
    chat_res = client.post("/api/ai/chat", json={
        "provider": "gemini",
        "message": "How do I become an astronomer?"
    })
    assert chat_res.status_code == 200
    conv_id = chat_res.get_json()["conversation_id"]

    # List conversations for session
    list_res = client.get("/api/ai/conversations")
    assert list_res.status_code == 200
    conv_list = list_res.get_json()["conversations"]
    assert len(conv_list) >= 1
    assert any(c["id"] == conv_id for c in conv_list)

    # Get conversation messages
    detail_res = client.get(f"/api/ai/conversations/{conv_id}")
    assert detail_res.status_code == 200
    messages = detail_res.get_json()["messages"]
    assert len(messages) >= 2
    assert messages[0]["role"] == "user"
    assert "astronomer" in messages[0]["content"].lower()
    assert messages[1]["role"] == "assistant"

    # Delete conversation
    del_res = client.delete(f"/api/ai/conversations/{conv_id}")
    assert del_res.status_code == 200

    # Confirm it is no longer listed
    list_res2 = client.get("/api/ai/conversations")
    conv_list2 = list_res2.get_json()["conversations"]
    assert not any(c["id"] == conv_id for c in conv_list2)


def test_ai_profile_opt_in_context(client, monkeypatch):
    """Verifies that opt-in student profile context is accepted."""
    monkeypatch.setenv("AI_TEST_MODE", "1")

    profile_payload = {
        "education_level": "Undergraduate",
        "current_stream": "Computer Science",
        "budget_range": "moderate",
        "interests": ["technology", "robotics"],
        "strengths": ["problem_solving", "coding"]
    }

    res = client.post("/api/ai/chat", json={
        "provider": "openai",
        "use_profile": True,
        "profile_data": profile_payload,
        "message": "Help me plan my tech career roadmap."
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["provider"] == "openai"
    assert data["message"]["role"] == "assistant"


def test_official_sdks_installed():
    """Verifies google-genai and openai packages are installed and importable."""
    import google.genai
    import openai
    import dotenv
    assert google.genai is not None
    assert openai is not None
    assert dotenv is not None


def test_openai_missing_api_key_reporting(client, monkeypatch):
    """Verifies that unconfigured OpenAI returns an honest 401 explaining OPENAI_API_KEY setup."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("AI_TEST_MODE", raising=False)

    res = client.post("/api/ai/chat", json={
        "provider": "openai",
        "message": "What skills are needed for artificial intelligence?"
    })
    assert res.status_code == 401
    data = res.get_json()
    assert data["success"] is False
    assert "error" in data
    err = data["error"]
    err_msg = err["message"] if isinstance(err, dict) else err
    assert "not configured yet" in err_msg or "OPENAI_API_KEY" in err_msg


def test_openai_model_configuration_override(client, monkeypatch):
    """Verifies that OPENAI_MODEL configured in environment is permitted and reflected in providers list."""
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4o")
    monkeypatch.setenv("AI_TEST_MODE", "1")

    res = client.get("/api/ai/providers")
    assert res.status_code == 200
    openai_meta = next(p for p in res.get_json()["providers"] if p["id"] == "openai")
    assert openai_meta["default_model"] == "gpt-4o"


def test_send_button_css_rules():
    """Verifies that the Send button in style.css has robust blue rules across normal and hover states."""
    css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "css", "style.css")
    with open(css_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "#btn-chat-send" in content
    assert ".ai-send-button" in content
    assert "#2563EB" in content
    # Verify no undefined --navy-accent in the composer button rule
    composer_idx = content.find("AI Chat Send Button")
    assert composer_idx != -1
    composer_chunk = content[composer_idx:composer_idx + 1200]
    assert "--navy-accent" not in composer_chunk
    assert "background: #2563EB !important;" in composer_chunk

