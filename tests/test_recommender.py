"""
Unit Tests for CareerCompass Recommendation Engine
Verifies multi-factor matching, profile distinctiveness, trade-offs, and equity checks.
"""

import pytest
from database import init_db
from recommender import generate_recommendations, calculate_match, DISCLAIMER_TEXT

@pytest.fixture(scope="module", autouse=True)
def setup_test_db(tmp_path_factory):
    test_db = str(tmp_path_factory.mktemp("data") / "test_recs.db")
    init_db(db_path=test_db, reset=True)
    return test_db


def test_tech_profile_recommendations(setup_test_db):
    """Profile with tech/science interests should rank technical careers on top."""
    tech_profile = {
        "education_level": "Undergraduate",
        "current_stream": "Science - PCM",
        "favorite_subjects": ["Computer Science", "Mathematics"],
        "interests": ["technology", "science"],
        "strengths": ["analytical thinking", "practical problem-solving"],
        "preferred_work_style": "hands-on work",
        "career_goals": "learning",
        "budget_range": "low_free",
        "existing_skills": ["Basic Coding", "Python"]
    }

    recs = generate_recommendations(tech_profile, db_path=setup_test_db, top_n=5)
    assert len(recs) >= 3

    top_titles = [r["title"] for r in recs[:3]]
    # Top 3 should include technology or engineering pathways
    assert any("Software" in t or "Electronics" in t or "Cybersecurity" in t or "Data" in t for t in top_titles)

    # Verify score bounds and explanations
    for r in recs:
        assert 25.0 <= r["match_score"] <= 98.0
        assert len(r["match_reasons"]) > 0
        assert "alternative_routes" in r


def test_healthcare_profile_recommendations(setup_test_db):
    """Profile with healthcare/empathy interests should rank healthcare on top."""
    health_profile = {
        "education_level": "Class 11–12",
        "current_stream": "Science - PCB",
        "favorite_subjects": ["Biology", "Chemistry"],
        "interests": ["healthcare", "science"],
        "strengths": ["empathy", "communication"],
        "preferred_work_style": "people-oriented work",
        "career_goals": "social impact",
        "budget_range": "moderate",
        "existing_skills": []
    }

    recs = generate_recommendations(health_profile, db_path=setup_test_db, top_n=5)
    top_title = recs[0]["title"]
    assert "Healthcare" in top_title or "Psychologist" in top_title

    # Healthcare requires statutory licensing
    healthcare_rec = next(r for r in recs if "Healthcare" in r["title"])
    assert healthcare_rec["regulated"] == 1


def test_creative_design_profile_recommendations(setup_test_db):
    """Profile with creativity interests and independence goals should prioritize design."""
    creative_profile = {
        "education_level": "Undergraduate",
        "current_stream": "Arts / Humanities",
        "favorite_subjects": ["Art & Design"],
        "interests": ["creativity", "business"],
        "strengths": ["creativity", "communication"],
        "preferred_work_style": "individual work",
        "career_goals": "independence",
        "budget_range": "low_free",
        "existing_skills": ["Design / Drawing"]
    }

    recs = generate_recommendations(creative_profile, db_path=setup_test_db, top_n=5)
    top_titles = [r["title"] for r in recs[:3]]
    assert any("Graphic" in t or "UX" in t or "Entrepreneur" in t for t in top_titles)


def test_different_profiles_produce_different_rankings(setup_test_db):
    """Ensures algorithm produces meaningfully different recommendations when answers change."""
    p1 = {
        "interests": ["technology"],
        "strengths": ["analytical thinking"],
        "preferred_work_style": "hands-on work",
        "career_goals": "learning"
    }
    p2 = {
        "interests": ["healthcare"],
        "strengths": ["empathy"],
        "preferred_work_style": "people-oriented work",
        "career_goals": "social impact"
    }

    recs1 = generate_recommendations(p1, db_path=setup_test_db, top_n=3)
    recs2 = generate_recommendations(p2, db_path=setup_test_db, top_n=3)

    assert recs1[0]["career_id"] != recs2[0]["career_id"]


def test_missing_skills_identification(setup_test_db):
    """Checks that missing skills are identified from existing skills."""
    profile_with_python = {
        "interests": ["technology"],
        "strengths": ["analytical thinking"],
        "preferred_work_style": "teamwork",
        "career_goals": "learning",
        "existing_skills": ["Python / JavaScript"]
    }

    recs = generate_recommendations(profile_with_python, db_path=setup_test_db, top_n=5)
    sw_rec = next(r for r in recs if r["slug"] == "software-developer")

    # "Python / JavaScript" is already in existing_skills, so it should NOT be in missing_skills
    for skill in sw_rec["missing_skills"]:
        assert "Python / JavaScript" != skill


def test_low_budget_does_not_eliminate_careers(setup_test_db):
    """Low budget should not crash or eliminate pathways, but surface low-cost routes."""
    low_budget_profile = {
        "interests": ["healthcare", "science"],
        "strengths": ["empathy"],
        "preferred_work_style": "people-oriented work",
        "career_goals": "social impact",
        "budget_range": "low_free"
    }

    recs = generate_recommendations(low_budget_profile, db_path=setup_test_db, top_n=5)
    assert len(recs) >= 3
    # Check that alternative low-cost routes are surfaced
    assert any("government" in route.lower() or "free" in route.lower() or "scholarship" in route.lower()
               for r in recs for route in r["alternative_routes"])
