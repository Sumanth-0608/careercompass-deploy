"""
End-to-End Demo Flow Test
Validates the full 10-step hackathon demo flow specified in project requirements:
1. Open homepage
2. Complete career discovery assessment
3. Submit answers to Flask API
4. Store assessment in SQLite
5. Display three explainable career recommendations
6. Open a career's details
7. Generate and save a roadmap
8. Mark a roadmap milestone complete
9. Compare two career choices in the student–parent view
10. Verify persistent access to saved data
"""

import pytest
from app import app
from database import init_db

def test_full_hackathon_demo_flow(tmp_path):
    test_db = str(tmp_path / "demo_flow.db")
    init_db(db_path=test_db, reset=True)

    app.config["TESTING"] = True
    app.config["DATABASE"] = test_db

    client = app.test_client()

    # Step 1: Open homepage
    res1 = client.get("/")
    assert res1.status_code == 200
    assert b"Your future starts with understanding yourself" in res1.data

    # Step 2 & 3: Submit assessment answers to Flask API
    assess_payload = {
        "education_level": "Undergraduate",
        "current_stream": "Science - PCM",
        "favorite_subjects": ["Computer Science", "Mathematics"],
        "interests": ["technology", "science"],
        "strengths": ["analytical thinking", "practical problem-solving"],
        "preferred_work_style": "hands-on work",
        "career_goals": "learning",
        "budget_range": "low_free",
        "location_preference": "flexible_relocate",
        "existing_skills": ["Basic Coding"],
        "constraints": "Self-funded study"
    }
    res3 = client.post("/api/assessments", json=assess_payload)
    assert res3.status_code == 201
    assess_data = res3.get_json()
    assert assess_data["success"] is True

    # Step 4: Assessment stored in SQLite
    assess_id = assess_data["assessment_id"]
    assert assess_id > 0

    # Step 5: Display at least three explainable career recommendations
    res5 = client.get(f"/api/assessments/{assess_id}/recommendations")
    assert res5.status_code == 200
    rec_data = res5.get_json()
    recs = rec_data["recommendations"]
    assert len(recs) >= 3

    target_career_id = recs[0]["career_id"]
    assert len(recs[0]["match_reasons"]) > 0

    # Step 6: Open career's details
    res6 = client.get(f"/careers/{target_career_id}")
    assert res6.status_code == 200
    assert bytes(recs[0]["title"], "utf-8") in res6.data

    # Step 7: Generate and save roadmap
    plan_payload = {
        "career_id": target_career_id,
        "student_name": "Demo Student",
        "assessment_id": assess_id,
        "notes": "Tri-City Hackathon Demo Roadmap"
    }
    res7 = client.post("/api/plans", json=plan_payload)
    assert res7.status_code == 201
    plan_id = res7.get_json()["plan_id"]

    # Step 8: Mark a roadmap milestone complete
    plan_obj = client.get(f"/api/plans/{plan_id}").get_json()["plan"]
    m_id = plan_obj["milestones"][0]["id"]
    res8 = client.patch(f"/api/plans/{plan_id}/milestones/{m_id}", json={"is_completed": True})
    assert res8.status_code == 200
    progress = res8.get_json()["plan_progress"]
    assert progress > 0

    # Step 9: Compare two career choices in student-parent view
    alt_career_id = recs[2]["career_id"]
    comp_payload = {
        "student_career_id": target_career_id,
        "alternative_career_id": alt_career_id,
        "student_reasons": "I want to build software products.",
        "alternative_reasons": "Parents want to explore cybersecurity for government sector security.",
        "shared_decision_summary": "We agreed to start the beginner project milestone together this weekend."
    }
    res9 = client.post("/api/comparisons", json=comp_payload)
    assert res9.status_code == 201
    comp_id = res9.get_json()["comparison_id"]

    # Step 10: Verify persistence of all saved data
    comp_retrieved = client.get(f"/api/comparisons/{comp_id}").get_json()["comparison"]
    assert comp_retrieved["student_career_id"] == target_career_id
    plan_retrieved = client.get(f"/api/plans/{plan_id}").get_json()["plan"]
    assert plan_retrieved["completed_count"] == 1
    assert plan_retrieved["milestones"][0]["is_completed"] == 1
