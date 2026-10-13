"""
Integration Tests for CareerCompass Flask REST API & SQLite Database
Tests all required endpoints, validations, error handling, and persistent data access.
"""

import os
import json
import sqlite3
import pytest
from app import app
from database import init_db

@pytest.fixture
def test_client(tmp_path):
    test_db_path = str(tmp_path / "test_api.db")
    init_db(db_path=test_db_path, reset=True)

    app.config["TESTING"] = True
    app.config["DATABASE"] = test_db_path

    with app.test_client() as client:
        with app.app_context():
            yield client, test_db_path


def test_health_check(test_client):
    client, _ = test_client
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "healthy"
    assert "CareerCompass" in data["service"]


def test_careers_list_and_category_filter(test_client):
    client, _ = test_client

    # Full list
    res = client.get("/api/careers")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["count"] >= 12
    assert len(data["careers"]) >= 12

    # Filtered by category
    res_filtered = client.get("/api/careers?category=Creative%20%26%20Design")
    assert res_filtered.status_code == 200
    filtered_data = res_filtered.get_json()
    assert filtered_data["count"] > 0
    for c in filtered_data["careers"]:
        assert c["category"] == "Creative & Design"


def test_career_details_valid_and_invalid(test_client):
    client, _ = test_client

    # Valid ID
    res = client.get("/api/careers/1")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "career" in data
    assert "disclaimer" in data

    # Invalid ID
    res_invalid = client.get("/api/careers/9999")
    assert res_invalid.status_code == 404
    err_data = res_invalid.get_json()
    assert "error" in err_data


def test_assessment_validation_failures(test_client):
    client, _ = test_client

    # Missing education_level
    res1 = client.post("/api/assessments", json={
        "interests": ["technology"],
        "strengths": ["analytical thinking"],
        "preferred_work_style": "hands-on work",
        "career_goals": "learning"
    })
    assert res1.status_code == 400
    assert "Education level" in res1.get_json()["error"]

    # Empty interests
    res2 = client.post("/api/assessments", json={
        "education_level": "Undergraduate",
        "interests": [],
        "strengths": ["analytical thinking"],
        "preferred_work_style": "hands-on work",
        "career_goals": "learning"
    })
    assert res2.status_code == 400
    assert "interest" in res2.get_json()["error"].lower()

    # Empty strengths
    res3 = client.post("/api/assessments", json={
        "education_level": "Undergraduate",
        "interests": ["technology"],
        "strengths": [],
        "preferred_work_style": "hands-on work",
        "career_goals": "learning"
    })
    assert res3.status_code == 400
    assert "strength" in res3.get_json()["error"].lower()


def test_assessment_submission_and_recommendations(test_client):
    client, _ = test_client

    payload = {
        "education_level": "Undergraduate",
        "current_stream": "Science - PCM",
        "favorite_subjects": ["Computer Science", "Mathematics"],
        "interests": ["technology", "science"],
        "strengths": ["analytical thinking", "practical problem-solving"],
        "preferred_work_style": "hands-on work",
        "career_goals": "learning",
        "budget_range": "low_free",
        "location_preference": "flexible_relocate",
        "existing_skills": ["Python"],
        "constraints": "Need self-paced learning"
    }

    # Submit assessment
    res = client.post("/api/assessments", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    assert "assessment_id" in data
    assessment_id = data["assessment_id"]

    # Retrieve recommendations for this assessment
    rec_res = client.get(f"/api/assessments/{assessment_id}/recommendations")
    assert rec_res.status_code == 200
    rec_data = rec_res.get_json()
    assert rec_data["success"] is True
    assert len(rec_data["recommendations"]) >= 3
    assert "disclaimer" in rec_data

    # Check top recommendation has explainable match reasons
    top_rec = rec_data["recommendations"][0]
    assert "match_reasons" in top_rec
    assert len(top_rec["match_reasons"]) > 0
    assert "match_score" in top_rec


def test_recommendations_post_endpoint(test_client):
    client, _ = test_client

    # Test with direct payload
    direct_payload = {
        "interests": ["creativity", "business"],
        "strengths": ["creativity", "communication"],
        "preferred_work_style": "individual work",
        "career_goals": "independence"
    }
    res = client.post("/api/recommendations", json=direct_payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert len(data["recommendations"]) >= 3


def test_career_roadmap_endpoint(test_client):
    client, _ = test_client

    res = client.get("/api/careers/1/roadmap")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert len(data["roadmap"]) == 7
    assert data["roadmap"][0]["step"] == 1


def test_plan_lifecycle_and_milestone_patch(test_client):
    client, _ = test_client

    # Create plan
    plan_payload = {
        "career_id": 1,
        "student_name": "Priya",
        "notes": "Focused on open source web development"
    }
    res_create = client.post("/api/plans", json=plan_payload)
    assert res_create.status_code == 201
    plan_data = res_create.get_json()
    assert plan_data["success"] is True
    plan_id = plan_data["plan_id"]

    # Retrieve plan
    res_get = client.get(f"/api/plans/{plan_id}")
    assert res_get.status_code == 200
    fetched_plan = res_get.get_json()["plan"]
    assert fetched_plan["student_name"] == "Priya"
    assert len(fetched_plan["milestones"]) == 7
    assert fetched_plan["completed_count"] == 0
    assert fetched_plan["progress_percentage"] == 0.0

    # Milestone 1 ID
    m1_id = fetched_plan["milestones"][0]["id"]

    # Mark milestone 1 completed
    res_patch = client.patch(f"/api/plans/{plan_id}/milestones/{m1_id}", json={"is_completed": True})
    assert res_patch.status_code == 200
    patch_data = res_patch.get_json()
    assert patch_data["is_completed"] is True
    assert patch_data["plan_progress"] > 0.0

    # Verify updated plan reflects completion
    res_refreshed = client.get(f"/api/plans/{plan_id}")
    refreshed_plan = res_refreshed.get_json()["plan"]
    assert refreshed_plan["completed_count"] == 1
    assert refreshed_plan["milestones"][0]["is_completed"] == 1


def test_student_parent_comparison(test_client):
    client, _ = test_client

    comp_payload = {
        "student_career_id": 1,
        "alternative_career_id": 8,
        "student_reasons": "I am passionate about building modern web applications and coding.",
        "alternative_reasons": "Parents feel clinical healthcare offers superior lifelong societal stability.",
        "shared_decision_summary": "Student will shadow a programmer and family will evaluate nursing college merit fees."
    }

    res_post = client.post("/api/comparisons", json=comp_payload)
    assert res_post.status_code == 201
    created_comp = res_post.get_json()
    assert created_comp["success"] is True
    comp_id = created_comp["comparison_id"]

    # Retrieve comparison
    res_get = client.get(f"/api/comparisons/{comp_id}")
    assert res_get.status_code == 200
    comp_data = res_get.get_json()["comparison"]
    assert comp_data["student_career_title"] != comp_data["alternative_career_title"]
    assert len(comp_data["discussion_questions"]) > 0


def test_sqlite_persistence_after_reconnection(tmp_path):
    """
    Simulates application restart: creates records, closes connection,
    reconnects to the same SQLite file, and verifies data persistence.
    """
    db_file = str(tmp_path / "persistence_test.db")
    init_db(db_path=db_file, reset=True)

    # 1. Connect and insert
    conn1 = sqlite3.connect(db_file)
    cur1 = conn1.cursor()
    cur1.execute("""
        INSERT INTO assessments (
            education_level, current_stream, favorite_subjects,
            interests, strengths, preferred_work_style, career_goals,
            budget_range, location_preference, existing_skills
        ) VALUES ('Undergraduate', 'Commerce', '[]', '["business"]', '["leadership"]', 'teamwork', 'stability', 'moderate', 'local', '[]')
    """)
    inserted_id = cur1.lastrowid
    conn1.commit()
    conn1.close()

    # 2. Reconnect with a fresh connection to simulate server reboot
    conn2 = sqlite3.connect(db_file)
    cur2 = conn2.cursor()
    cur2.execute("SELECT * FROM assessments WHERE id = ?", (inserted_id,))
    row = cur2.fetchone()
    conn2.close()

    assert row is not None
    assert row[1] is not None  # created_at
    assert row[2] == "Undergraduate"  # education_level
