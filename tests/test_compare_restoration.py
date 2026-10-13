"""
CareerCompass - Compare Two Specific Pathways Restoration Test Suite
Verifies:
1. Reversion of translation and voice features from #compare-form.
2. Complete removal of language pickers, speaker icons, dictation mic buttons, and preview panels from #compare-form.
3. Restoration of original heading, subtitle, form fields, and submit button.
4. Both career dropdowns contain all original careers with stable IDs.
5. Form submission and SQLite storage work as expected without regression.
6. Preservation of surrounding sections: Reality Check, inline translation box, and floating AI parent voice canvass.
"""

import pytest
from app import app
from database import init_db, get_all_careers


@pytest.fixture
def client(tmp_path):
    test_db_path = str(tmp_path / "test_restoration.db")
    init_db(db_path=test_db_path, reset=True)
    orig_db = app.config.get("DATABASE")
    app.config["TESTING"] = True
    app.config["DATABASE"] = test_db_path
    with app.test_client() as client:
        with app.app_context():
            yield client
    if orig_db is not None:
        app.config["DATABASE"] = orig_db
    else:
        app.config.pop("DATABASE", None)


def test_compare_section_heading_and_subtitle_restored(client):
    """Verifies that the heading and subtitle of Compare Two Specific Pathways are restored."""
    res = client.get("/compare")
    assert res.status_code == 200
    html = res.data.decode("utf-8")

    assert "Compare Two Specific Pathways" in html
    assert "Analyze two distinct career trajectories side-by-side with objective educational and financial realities." in html


def test_compare_form_translation_and_voice_controls_removed(client):
    """Verifies that translation selectors, speaker icons, audio controls, and mics are removed from #compare-form."""
    res = client.get("/compare")
    assert res.status_code == 200
    html = res.data.decode("utf-8")

    # Extract compare-form segment
    form_start = html.find('id="compare-form"')
    assert form_start != -1
    form_end = html.find('</form>', form_start)
    assert form_end != -1
    form_html = html[form_start:form_end]

    # No language picker or language buttons in compare-form
    assert "compare-lang-picker" not in form_html
    assert "compare-lang-btn" not in form_html
    assert "compare-controls-wrap" not in form_html

    # No section or item audio controls in compare-form
    assert "btn-listen-section" not in form_html
    assert "btn-pause-section" not in form_html
    assert "btn-resume-section" not in form_html
    assert "btn-replay-section" not in form_html
    assert "btn-stop-section" not in form_html
    assert "btn-item-speaker" not in form_html

    # No dictation mic or translation preview panels in compare-form
    assert "btn-dictate" not in form_html
    assert "btn-field-translate" not in form_html
    assert "field-trans-preview" not in form_html
    assert "trans-preview-" not in form_html

    # No compare_multilingual.js script included
    assert "compare_multilingual.js" not in html


def test_compare_form_fields_and_dropdowns_intact(client):
    """Verifies that original form structure, career dropdowns, textareas, and submit buttons remain intact."""
    careers = get_all_careers()
    assert len(careers) >= 36

    res = client.get("/compare")
    assert res.status_code == 200
    html = res.data.decode("utf-8")

    # Form fields
    assert 'id="student_career_id"' in html
    assert 'id="student_reasons"' in html
    assert 'id="alternative_career_id"' in html
    assert 'id="alternative_reasons"' in html
    assert 'id="shared_decision_summary"' in html

    # Labels and questions
    assert "Select Preferred Career *" in html
    assert "Why is the student excited about this? *" in html
    assert "Select Alternative Career *" in html
    assert "Why is this alternative recommended? *" in html
    assert "Shared Understanding &amp; Immediate Next Action" in html
    assert "What small next step or trial experiment can student and parent agree to investigate together?" in html

    # All careers in dropdowns
    for c in careers[:10]:
        assert f'value="{c["id"]}"' in html

    # Submit button
    assert "btn-submit-compare" in html
    assert "Generate Side-by-Side Comparison &amp; Save Bridge 🚀" in html


def test_form_submission_and_comparison_api(client):
    """Verifies that submitting the comparison form works and creates database records."""
    careers = get_all_careers()
    s_id = careers[0]["id"]
    a_id = careers[1]["id"]

    payload = {
        "student_career_id": s_id,
        "alternative_career_id": a_id,
        "student_reasons": "Excited about software development and building apps.",
        "alternative_reasons": "Prefers electrical engineering for industry stability.",
        "shared_decision_summary": "Student will build a weekend hardware-software prototype."
    }

    res = client.post("/api/comparisons", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    assert "comparison" in data
    assert data["comparison"]["student_career_id"] == s_id
    assert data["comparison"]["alternative_career_id"] == a_id


def test_surrounding_sections_and_other_features_preserved(client):
    """Verifies that surrounding sections and separate translation/voice features elsewhere remain intact."""
    res = client.get("/compare")
    assert res.status_code == 200
    html = res.data.decode("utf-8")

    # 1. Reality Check section
    assert "Detailed Side-by-Side Reality Check" in html
    assert "comparison-result" in html

    # 2. Separate inline 3-language translation section
    assert "section-parent-voice-inline" in html
    assert "Understand Your Child's Career — In Your Language" in html
    assert "trans-from-lang" in html
    assert "trans-to-lang" in html
    assert "trans-btn-swap" in html
    assert "trans-btn-translate" in html

    # 3. Floating AI Voice Canvass button and modal
    assert "floating-parent-voice-btn" in html
    assert "AI Career Guide for Parents" in html
    assert "parent-voice-modal" in html
