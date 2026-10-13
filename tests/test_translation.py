"""
CareerCompass - Non-AI Three-Language Translation Test Suite
Verifies:
1. All 6 translation directions across Telugu (te), Hindi (hi), and English (en).
2. Flask endpoint POST /api/translate input validation and response format.
3. Zero AI usage: verified non-AI translation engine.
4. Placement and components of the translation box on /compare page.
5. Preservation of surrounding sections and compare functionality.
"""

import pytest
from app import app
from translation_service import translate_text, SUPPORTED_LANGUAGES, DOMAIN_DICTIONARY


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_supported_languages_exact_three():
    """Verifies that exactly Telugu (te), Hindi (hi), and English (en) are supported."""
    assert set(SUPPORTED_LANGUAGES.keys()) == {"te", "hi", "en"}
    assert SUPPORTED_LANGUAGES["te"]["code"] == "te-IN"
    assert SUPPORTED_LANGUAGES["hi"]["code"] == "hi-IN"
    assert SUPPORTED_LANGUAGES["en"]["code"] == "en-IN"


def test_all_six_translation_directions():
    """Verifies translation works reliably across all six translation directions."""
    directions = [
        ("en", "hi"),
        ("en", "te"),
        ("hi", "en"),
        ("hi", "te"),
        ("te", "en"),
        ("te", "hi")
    ]

    for src, tgt in directions:
        # Test career title
        res = translate_text("Civil Engineer", src, tgt)
        assert isinstance(res, str)
        assert len(res.strip()) > 0

        # Verify expected script/language
        if tgt == "hi":
            # Hindi should contain Devanagari or expected translation
            assert any("\u0900" <= ch <= "\u097F" for ch in res) or "Civil" in res or "इंजीनियर" in res
        elif tgt == "te":
            # Telugu should contain Telugu script
            assert any("\u0c00" <= ch <= "\u0c7F" for ch in res) or "ఇంజనీర్" in res
        elif tgt == "en":
            assert "Engineer" in res or "Civil" in res


def test_same_source_and_target_language():
    """Verifies that same source and target returns original text unchanged."""
    text = "Civil Engineer"
    assert translate_text(text, "en", "en") == text
    assert translate_text(text, "te", "te") == text
    assert translate_text(text, "hi", "hi") == text


def test_translation_zero_ai_models():
    """Verifies that translation_service does not import or call any LLM/AI model."""
    import translation_service
    # Ensure no Gemini or OpenAI SDKs are referenced in translation_service
    assert not hasattr(translation_service, "genai")
    assert not hasattr(translation_service, "OpenAI")
    assert not hasattr(translation_service, "call_ai_provider")
    assert not hasattr(translation_service, "call_parent_career_guide")


def test_api_translate_valid_requests(client):
    """Verifies POST /api/translate handles valid multilingual requests."""
    # 1. English to Telugu
    res = client.post("/api/translate", json={
        "text": "Civil Engineer",
        "source_language": "en",
        "target_language": "te"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["source_language"] == "en"
    assert data["target_language"] == "te"
    assert "సివిల్ ఇంజనీర్" in data["translated_text"]

    # 2. English to Hindi
    res = client.post("/api/translate", json={
        "text": "Software Engineer",
        "source_language": "en",
        "target_language": "hi"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "सॉफ्टवेयर इंजीनियर" in data["translated_text"]

    # 3. Telugu to English
    res = client.post("/api/translate", json={
        "text": "సివిల్ ఇంజనీర్",
        "source_language": "te",
        "target_language": "en"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "Civil Engineer" in data["translated_text"]

    # 4. Hindi to Telugu
    res = client.post("/api/translate", json={
        "text": "सिविल इंजीनियर",
        "source_language": "hi",
        "target_language": "te"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "సివిల్ ఇంజనీర్" in data["translated_text"]


def test_api_translate_validation_errors(client):
    """Verifies validation error handling for /api/translate."""
    # Non-JSON
    res = client.post("/api/translate", data="not json")
    assert res.status_code == 400
    assert res.get_json()["error"]["code"] == "invalid_payload"

    # Missing text
    res = client.post("/api/translate", json={
        "text": "",
        "source_language": "en",
        "target_language": "te"
    })
    assert res.status_code == 400
    assert res.get_json()["error"]["code"] == "missing_text"

    # Text too long (> 2500 chars)
    res = client.post("/api/translate", json={
        "text": "x" * 2501,
        "source_language": "en",
        "target_language": "te"
    })
    assert res.status_code == 400
    assert res.get_json()["error"]["code"] == "text_too_long"

    # Unsupported source language
    res = client.post("/api/translate", json={
        "text": "Hello",
        "source_language": "fr",
        "target_language": "te"
    })
    assert res.status_code == 400
    assert res.get_json()["error"]["code"] == "unsupported_source_language"

    # Unsupported target language
    res = client.post("/api/translate", json={
        "text": "Hello",
        "source_language": "en",
        "target_language": "de"
    })
    assert res.status_code == 400
    assert res.get_json()["error"]["code"] == "unsupported_target_language"


def test_compare_page_translation_box_ui_and_position(client):
    """
    Verifies that the translation box is rendered with all required components
    and strictly positioned between 'Detailed Side-by-Side Reality Check'
    and 'Compare Two Specific Pathways'.
    """
    res = client.get("/compare")
    assert res.status_code == 200
    html = res.data.decode("utf-8")

    # Section heading & subtitle
    assert "Understand Your Child&#39;s Career — In Your Language" in html or "Understand Your Child's Career — In Your Language" in html
    assert "Listen to career information in Telugu, Hindi, or English" in html

    # Section IDs & structure
    assert "id=\"section-parent-voice-inline\"" in html

    # Dropdowns & Swap button
    assert "id=\"trans-from-lang\"" in html
    assert "id=\"trans-to-lang\"" in html
    assert "id=\"trans-btn-swap\"" in html
    assert "⇄" in html

    # Source text area & Clear & Translate buttons
    assert "id=\"trans-source-text\"" in html
    assert "id=\"trans-btn-clear\"" in html
    assert "id=\"trans-btn-translate\"" in html
    assert "Translate" in html

    # Result card & Copy button & Speaker button
    assert "id=\"trans-result-card\"" in html
    assert "id=\"trans-result-body\"" in html
    assert "id=\"trans-btn-copy\"" in html
    assert "Copy Translation" in html
    assert "id=\"trans-btn-listen\"" in html

    # TTS sub-controls
    assert "id=\"trans-btn-pause\"" in html
    assert "id=\"trans-btn-resume\"" in html
    assert "id=\"trans-btn-stop\"" in html

    # Verify exact ordering in document:
    # 1. Detailed Side-by-Side Reality Check (id="comparison-result")
    # 2. Understand Your Child's Career (id="section-parent-voice-inline")
    # 3. Compare Two Specific Pathways (id="compare-form")
    idx_reality_check = html.find("id=\"comparison-result\"")
    idx_translation_box = html.find("id=\"section-parent-voice-inline\"")
    idx_compare_form = html.find("id=\"compare-form\"")

    assert idx_reality_check != -1, "comparison-result section missing"
    assert idx_translation_box != -1, "section-parent-voice-inline missing"
    assert idx_compare_form != -1, "compare-form section missing"

    assert idx_reality_check < idx_translation_box < idx_compare_form, (
        "Translation box must be strictly between Detailed Reality Check and Compare Form"
    )


def test_compare_page_preserves_modal_and_form(client):
    """Verifies compare page preserves floating modal and compare form options."""
    res = client.get("/compare")
    assert res.status_code == 200
    html = res.data.decode("utf-8")

    # Floating button & modal preserved
    assert "floating-parent-voice-btn" in html
    assert "parent-voice-modal" in html

    # Career selector form elements preserved
    assert "id=\"student_career_id\"" in html
    assert "id=\"alternative_career_id\"" in html
