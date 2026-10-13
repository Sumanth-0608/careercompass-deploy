"""
Automated Tests for Career Reality Simulator
Covers all 10 criteria specified in project requirements:
1. Default demo profile validation
2. Valid scenario comparison
3. Invalid budget, work-style, and priority values rejection (HTTP 400)
4. Deterministic recommendations for identical inputs
5. Meaningful recommendation changes when matching attributes change
6. Budget changes affecting learning-route suggestions without penalizing intrinsic career compatibility
7. Stable comparison when a career appears in both top-three lists (status "remained")
8. Correct explanation of score changes
9. Graceful handling of missing career metadata
10. API errors and persistence (saving and retrieving a comparison)
"""

import pytest
from app import app
from database import init_db
from recommender import (
    DEFAULT_DEMO_PROFILE,
    ALLOWED_BUDGETS,
    ALLOWED_WORK_STYLES,
    ALLOWED_PRIORITIES,
    compare_scenarios,
    simulate_scenario,
    calculate_simulator_match
)


@pytest.fixture
def sim_client(tmp_path):
    test_db_path = str(tmp_path / "test_sim.db")
    init_db(db_path=test_db_path, reset=True)

    app.config["TESTING"] = True
    app.config["DATABASE"] = test_db_path

    with app.test_client() as client:
        with app.app_context():
            yield client, test_db_path


# 1. Default Demo Profile Test
def test_default_demo_profile_values():
    assert DEFAULT_DEMO_PROFILE["education_budget"] == "moderate"
    assert DEFAULT_DEMO_PROFILE["work_style"] == "analytical"
    assert DEFAULT_DEMO_PROFILE["priority"] == "growth"


# 2. Valid Scenario Comparison Test
def test_valid_scenario_comparison(sim_client):
    client, _ = sim_client
    payload = {
        "baseline": {
            "education_budget": "moderate",
            "work_style": "analytical",
            "priority": "growth"
        },
        "alternative": {
            "education_budget": "low",
            "work_style": "creative",
            "priority": "stability"
        }
    }
    res = client.post("/api/simulator/compare", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert len(data["baseline_recommendations"]) == 3
    assert len(data["alternative_recommendations"]) == 3
    assert len(data["comparison"]) > 0
    assert len(data["explanations"]) > 0


# 3. Invalid Budget, Work-Style, and Priority Values Rejection Test
def test_invalid_simulator_inputs(sim_client):
    client, _ = sim_client

    # Invalid budget
    res1 = client.post("/api/simulator/compare", json={
        "baseline": {"education_budget": "infinite_wealth", "work_style": "analytical", "priority": "growth"},
        "alternative": {"education_budget": "low", "work_style": "creative", "priority": "stability"}
    })
    assert res1.status_code == 400
    assert "education_budget" in res1.get_json()["error"]

    # Invalid work style
    res2 = client.post("/api/simulator/compare", json={
        "baseline": {"education_budget": "moderate", "work_style": "telepathic", "priority": "growth"},
        "alternative": {"education_budget": "low", "work_style": "creative", "priority": "stability"}
    })
    assert res2.status_code == 400
    assert "work_style" in res2.get_json()["error"]

    # Invalid priority
    res3 = client.post("/api/simulator/compare", json={
        "baseline": {"education_budget": "moderate", "work_style": "analytical", "priority": "world_domination"},
        "alternative": {"education_budget": "low", "work_style": "creative", "priority": "stability"}
    })
    assert res3.status_code == 400
    assert "priority" in res3.get_json()["error"]

    # Missing baseline object
    res4 = client.post("/api/simulator/compare", json={
        "alternative": {"education_budget": "low", "work_style": "creative", "priority": "stability"}
    })
    assert res4.status_code == 400


# 4. Deterministic Recommendations for Identical Inputs Test
def test_deterministic_simulator_results(sim_client):
    _, db_path = sim_client
    profile = {
        "education_budget": "moderate",
        "work_style": "analytical",
        "priority": "growth"
    }
    run1 = simulate_scenario(profile, db_path=db_path)
    run2 = simulate_scenario(profile, db_path=db_path)

    assert len(run1) == len(run2) == 3
    for r1, r2 in zip(run1, run2):
        assert r1["career_id"] == r2["career_id"]
        assert r1["match_score"] == r2["match_score"]
        assert r1["rank"] == r2["rank"]


# 5. Meaningful Changes when Matching Attributes Change Test
def test_meaningful_recommendation_changes(sim_client):
    _, db_path = sim_client
    analytical_profile = {
        "education_budget": "moderate",
        "work_style": "analytical",
        "priority": "growth"
    }
    creative_profile = {
        "education_budget": "moderate",
        "work_style": "creative",
        "priority": "independence"
    }

    res_analytical = simulate_scenario(analytical_profile, db_path=db_path)
    res_creative = simulate_scenario(creative_profile, db_path=db_path)

    top_analytical_titles = [r["title"] for r in res_analytical]
    top_creative_titles = [r["title"] for r in res_creative]

    # Top choices should be distinctly different
    assert top_analytical_titles[0] != top_creative_titles[0]
    assert any("Developer" in t or "Data" in t or "Cyber" in t for t in top_analytical_titles)
    assert any("Designer" in t or "Entrepreneur" in t for t in top_creative_titles)


# 6. Budget Changes Affecting Learning-Route Without Penalizing Compatibility Test
def test_budget_invariance_on_compatibility_score(sim_client):
    _, db_path = sim_client
    moderate_profile = {
        "education_budget": "moderate",
        "work_style": "analytical",
        "priority": "growth"
    }
    very_limited_profile = {
        "education_budget": "very_limited",
        "work_style": "analytical",
        "priority": "growth"
    }

    res_mod = simulate_scenario(moderate_profile, db_path=db_path)
    res_lim = simulate_scenario(very_limited_profile, db_path=db_path)

    # Intrinsic compatibility scores must be IDENTICAL
    for r_mod, r_lim in zip(res_mod, res_lim):
        assert r_mod["career_id"] == r_lim["career_id"]
        assert r_mod["match_score"] == r_lim["match_score"]

        # But route advice should differ to address the very limited budget
        assert r_mod["route_info"]["budget_tier"] == "Moderate"
        assert r_lim["route_info"]["budget_tier"] == "Very limited"
        assert "open" in r_lim["route_info"]["suggested_route"].lower() or "waiver" in r_lim["route_info"]["suggested_route"].lower()


# 7. Stable Comparison when Career Remains in Both Top-Three Lists Test
def test_stable_comparison_remained_status(sim_client):
    _, db_path = sim_client
    base = {
        "education_budget": "moderate",
        "work_style": "analytical",
        "priority": "growth"
    }
    alt = {
        "education_budget": "very_limited",
        "work_style": "analytical",
        "priority": "growth"
    }
    comparison_res = compare_scenarios(base, alt, db_path=db_path)

    for item in comparison_res["comparison"][:3]:
        assert item["status"] == "remained"
        assert item["status_label"] == "Maintained in Top 3"
        assert item["score_difference"] == 0.0


# 8. Correct Explanation of Score Changes Test
def test_explanation_reflects_actual_attributes(sim_client):
    _, db_path = sim_client
    base = {
        "education_budget": "moderate",
        "work_style": "analytical",
        "priority": "growth"
    }
    alt = {
        "education_budget": "low",
        "work_style": "creative",
        "priority": "stability"
    }
    res = compare_scenarios(base, alt, db_path=db_path)

    # Explanations should explicitly reference the changed attributes
    explanations_text = " ".join(res["explanations"])
    assert "Work Style Shift" in explanations_text
    assert "Creative and design-focused" in explanations_text
    assert "Career Priority Shift" in explanations_text
    assert "Stability" in explanations_text
    assert "Education Budget Shift" in explanations_text


# 9. Graceful Handling of Missing Career Metadata Test
def test_graceful_missing_career_metadata():
    # Incomplete career object missing strengths, categories, and roadmap
    partial_career = {
        "id": 999,
        "slug": "custom-specialist",
        "title": "Custom Specialist"
    }
    profile = {
        "education_budget": "moderate",
        "work_style": "analytical",
        "priority": "growth"
    }
    # Should not raise KeyError or AttributeError
    rec = calculate_simulator_match(profile, partial_career)
    assert rec["career_id"] == 999
    assert rec["title"] == "Custom Specialist"
    assert 25.0 <= rec["match_score"] <= 98.0
    assert "route_info" in rec


# 10. API Persistence and Error Handling Test
def test_simulator_save_and_retrieve_api(sim_client):
    client, _ = sim_client
    payload = {
        "baseline": {
            "education_budget": "moderate",
            "work_style": "analytical",
            "priority": "growth"
        },
        "alternative": {
            "education_budget": "flexible",
            "work_style": "people",
            "priority": "social_impact"
        }
    }

    # 1. Save comparison
    res_save = client.post("/api/simulator/save", json=payload)
    assert res_save.status_code == 201
    save_data = res_save.get_json()
    assert save_data["success"] is True
    assert "comparison_id" in save_data
    comp_id = save_data["comparison_id"]

    # 2. Retrieve comparison
    res_get = client.get(f"/api/simulator/saved/{comp_id}")
    assert res_get.status_code == 200
    retrieved = res_get.get_json()
    assert retrieved["success"] is True
    assert retrieved["comparison_id"] == comp_id
    assert retrieved["baseline_profile"]["work_style"] == "analytical"
    assert retrieved["alternative_profile"]["work_style"] == "people"

    # 3. Non-existent comparison
    res_404 = client.get("/api/simulator/saved/99999")
    assert res_404.status_code == 404
