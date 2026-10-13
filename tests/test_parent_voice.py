"""
CareerCompass - AI Parent Voice Canvass Test Suite
Verifies:
1. Parent–Student Bridge page contains the right-side floating button, modal, language pills, audio controls, and mic.
2. Endpoint /api/parent-career-guide validates language allowlist (te, hi, en) and payload constraints.
3. Multilingual generation works for Telugu (te), Hindi (hi), and English (en).
4. Missing API keys return clear 401 missing_credentials when credentials are unconfigured.
5. Preserves existing Compare page features.
"""

import os
import pytest
from app import app
from ai_service import PARENT_GUIDE_LANGUAGES, build_parent_career_guide_prompt


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_compare_page_contains_parent_voice_canvass(client):
    """Verifies compare page includes floating voice button, modal, language selector, and audio controls."""
    res = client.get("/compare")
    assert res.status_code == 200
    html = res.data.decode("utf-8")

    # Floating button on right
    assert "floating-parent-voice-btn" in html
    assert "AI Career Guide for Parents" in html
    assert "Listen in your language" in html

    # Multilingual Modal & Title
    assert "parent-voice-modal" in html
    assert "Let&#39;s Talk About Your Child&#39;s Future" in html or "Let's Talk About Your Child's Future" in html

    # Three Languages
    assert "తెలుగు" in html
    assert "Telugu (te-IN)" in html
    assert "हिन्दी" in html
    assert "Hindi (hi-IN)" in html
    assert "English (en-IN)" in html

    # Audio Controls
    assert "pv-audio-play" in html
    assert "pv-audio-pause" in html
    assert "pv-audio-resume" in html
    assert "pv-audio-stop" in html
    assert "pv-audio-replay" in html

    # Voice Input (Mic)
    assert "pv-btn-mic" in html
    assert "pv-question-input" in html
    assert "pv-btn-send" in html

    # Script inclusion
    assert "parent_voice.js" in html


def test_parent_voice_languages_allowlist():
    """Verifies supported language codes strictly include te, hi, en."""
    assert set(PARENT_GUIDE_LANGUAGES.keys()) == {"te", "hi", "en"}
    assert PARENT_GUIDE_LANGUAGES["te"]["code"] == "te-IN"
    assert PARENT_GUIDE_LANGUAGES["hi"]["code"] == "hi-IN"
    assert PARENT_GUIDE_LANGUAGES["en"]["code"] == "en-IN"


def test_api_parent_career_guide_invalid_language(client):
    """Verifies rejection of unsupported languages."""
    res = client.post("/api/parent-career-guide", json={
        "language": "fr",
        "student_profile": {"preferred_career": "Civil Engineer"},
        "message": ""
    })
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert data["error"]["code"] == "unsupported_language"


def test_api_parent_career_guide_message_too_long(client):
    """Verifies rejection of excessively long messages (>2500 chars)."""
    res = client.post("/api/parent-career-guide", json={
        "language": "en",
        "student_profile": {"preferred_career": "Civil Engineer"},
        "message": "a" * 2600
    })
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert data["error"]["code"] == "message_too_long"


def test_api_parent_career_guide_telugu_mock_flow(client, monkeypatch):
    """Verifies Telugu initial explanation generation in mock test mode."""
    monkeypatch.setenv("AI_TEST_MODE", "1")
    payload = {
        "language": "te",
        "student_profile": {
            "preferred_career": "Civil Engineer",
            "reasons": "I enjoy designing buildings and practical structures",
            "goals": ["Creative Freedom", "Growth"],
            "parent_concerns": ["Tuition costs", "Employment stability"]
        },
        "message": ""
    }
    res = client.post("/api/parent-career-guide", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["language"] == "te"
    assert "నమస్కారం" in data["reply"]
    assert "Civil Engineer" in data["reply"]


def test_api_parent_career_guide_hindi_mock_flow(client, monkeypatch):
    """Verifies Hindi initial explanation generation in mock test mode."""
    monkeypatch.setenv("AI_TEST_MODE", "1")
    payload = {
        "language": "hi",
        "student_profile": {
            "preferred_career": "Software Engineer",
            "reasons": "Passionate about programming and modern web systems",
            "goals": ["Tech Innovation"],
            "parent_concerns": ["Job market stability"]
        },
        "message": ""
    }
    res = client.post("/api/parent-career-guide", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["language"] == "hi"
    assert "नमस्ते" in data["reply"]
    assert "Software Engineer" in data["reply"]


def test_api_parent_career_guide_english_parent_question(client, monkeypatch):
    """Verifies answering a parent's question in English."""
    monkeypatch.setenv("AI_TEST_MODE", "1")
    payload = {
        "language": "en",
        "student_profile": {
            "preferred_career": "Data Scientist",
            "reasons": "Loves math and statistical patterns"
        },
        "message": "What education will my child need?",
        "history": [
            {"role": "assistant", "content": "Welcome to the Parent Guide."}
        ]
    }
    res = client.post("/api/parent-career-guide", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["language"] == "en"
    assert "Data Scientist" in data["reply"]


def test_api_parent_career_guide_missing_credentials(client, monkeypatch):
    """Verifies honest 401 when live mode is active but credentials are missing."""
    monkeypatch.delenv("AI_TEST_MODE", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    payload = {
        "language": "te",
        "student_profile": {"preferred_career": "Civil Engineer"},
        "message": ""
    }
    res = client.post("/api/parent-career-guide", json=payload)
    assert res.status_code == 401
    data = res.get_json()
    assert data["success"] is False
    assert data["error"]["code"] == "missing_credentials"
    assert "AI service credentials are required" in data["error"]["message"]


def test_system_prompt_builder_contains_student_profile():
    """Verifies prompt builder integrates verified student attributes and ethical rules."""
    profile = {
        "preferred_career": "Mechanical Engineer",
        "reasons": "Enjoys robotics and mechanics",
        "goals": ["Growth", "Innovation"],
        "parent_concerns": ["Tuition fees"],
        "education_level": "Undergraduate",
        "budget_limit": "Moderate"
    }
    prompt = build_parent_career_guide_prompt("te", profile)
    assert "Mechanical Engineer" in prompt
    assert "Enjoys robotics and mechanics" in prompt
    assert "Tuition fees" in prompt
    assert "Telugu" in prompt
    assert "NO EMOTIONAL PRESSURE OR MANIPULATION" in prompt


def test_inline_section_exact_position_between_sections(client):
    """
    Acceptance Test 1 & 2:
    Verifies that the new section appears immediately after 'Detailed Side-by-Side Reality Check'
    and immediately before 'Compare Two Specific Pathways'.
    """
    res = client.get("/compare")
    assert res.status_code == 200
    html = res.data.decode("utf-8")

    reality_check_str = "Detailed Side-by-Side Reality Check"
    new_section_str = "Understand Your Child&#39;s Career — In Your Language"
    new_section_plain = "Understand Your Child's Career — In Your Language"
    compare_form_str = "Compare Two Specific Pathways"

    pos_reality_check = html.find(reality_check_str)
    pos_new_section = html.find(new_section_str)
    if pos_new_section == -1:
        pos_new_section = html.find(new_section_plain)
    pos_compare_form = html.find(compare_form_str)

    assert pos_reality_check != -1, "Detailed Side-by-Side Reality Check section must exist"
    assert pos_new_section != -1, "Understand Your Child's Career section must exist"
    assert pos_compare_form != -1, "Compare Two Specific Pathways section must exist"

    # Strict sequence check: Reality Check -> New Section -> Compare Form
    assert pos_reality_check < pos_new_section, "New section must appear after Detailed Side-by-Side Reality Check"
    assert pos_new_section < pos_compare_form, "Compare Two Specific Pathways must appear after the new section"


def test_inline_section_controls_and_buttons(client):
    """Verifies heading, subtitle, speaker button, mic button, and composer in the inline section."""
    res = client.get("/compare")
    assert res.status_code == 200
    html = res.data.decode("utf-8")

    # Subtitle
    assert "Listen to career information in Telugu, Hindi, or English, and ask questions using your voice." in html

    # Speaker button with required exact label
    assert "Listen to Career Guidance" in html
    assert "pv-inline-btn-listen" in html
    assert "pv-inline-btn-pause" in html
    assert "pv-inline-btn-resume" in html
    assert "pv-inline-btn-stop" in html
    assert "pv-inline-btn-replay" in html

    # Microphone button with required exact label
    assert "Ask a Question by Voice" in html
    assert "pv-inline-btn-mic" in html

    # Input placeholder
    assert "Ask a question about your child&#39;s career..." in html or "Ask a question about your child's career..." in html
    assert "pv-inline-question-input" in html
    assert "pv-inline-btn-send" in html

    # Three Languages in inline selector
    assert "te-IN" in html
    assert "hi-IN" in html
    assert "en-IN" in html

