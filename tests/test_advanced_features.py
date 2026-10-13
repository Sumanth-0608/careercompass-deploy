"""
Unit and Integration Tests for CareerCompass Advanced Features
Tests:
- Job Opportunities API and location/category/work_mode filtering
- Single opportunity retrieval
- Career Inspiration Quotes API and categories
- Interactive Snake Roadmap API with B.Tech Civil Engineering 11-step journey & stages A-G
- Sports Careers & Business Careers catalogs
- Navigation routes: /opportunities, /sports-careers, /business-careers, /roadmap, /compare
"""

import pytest
from app import app
from database import init_db, get_opportunities, get_custom_roadmap, get_all_careers

@pytest.fixture
def test_client(tmp_path):
    test_db_path = str(tmp_path / "test_advanced.db")
    init_db(db_path=test_db_path, reset=True)

    app.config["TESTING"] = True
    app.config["DATABASE"] = test_db_path

    with app.test_client() as client:
        with app.app_context():
            yield client, test_db_path


def test_opportunities_api_and_filters(test_client):
    client, _ = test_client

    # 1. Full list of opportunities
    res = client.get("/api/opportunities")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["count"] >= 10
    assert len(data["opportunities"]) >= 10

    # 2. Category filter: Civil Engineering
    res_civil = client.get("/api/opportunities?category=Civil%20Engineering%20%26%20Construction")
    assert res_civil.status_code == 200
    civil_data = res_civil.get_json()
    assert civil_data["count"] >= 2
    for opp in civil_data["opportunities"]:
        assert opp["category"] == "Civil Engineering & Construction"

    # 3. Location filter: Delhi
    res_delhi = client.get("/api/opportunities?location=Delhi")
    assert res_delhi.status_code == 200
    delhi_data = res_delhi.get_json()
    assert delhi_data["count"] >= 1

    # 4. Work mode filter: remote
    res_remote = client.get("/api/opportunities?work_mode=remote")
    assert res_remote.status_code == 200
    remote_data = res_remote.get_json()
    assert remote_data["count"] >= 1
    for opp in remote_data["opportunities"]:
        assert opp["work_mode"] == "remote"

    # 5. Keyword search: CAD
    res_search = client.get("/api/opportunities?q=CAD")
    assert res_search.status_code == 200
    search_data = res_search.get_json()
    assert search_data["count"] >= 1


def test_single_opportunity_api(test_client):
    client, _ = test_client
    res = client.get("/api/opportunities/1")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "title" in data["opportunity"]
    assert "employer_or_source" in data["opportunity"]

    # Invalid ID
    res_invalid = client.get("/api/opportunities/99999")
    assert res_invalid.status_code == 404


def test_career_quotes_api(test_client):
    client, _ = test_client
    res = client.get("/api/quotes")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["count"] >= 5
    for q in data["quotes"]:
        assert "quote" in q
        assert "practical_tip" in q
        assert q["author"] == "CareerCompass Guidance"

    # Filtered by Civil Engineering category
    res_civil = client.get("/api/quotes?category=Civil%20Engineering")
    assert res_civil.status_code == 200
    civil_quotes = res_civil.get_json()
    assert civil_quotes["count"] >= 1


def test_custom_snake_roadmap_civil_engineering(test_client):
    client, _ = test_client

    # Request B.Tech Civil Engineering roadmap
    res = client.get("/api/roadmap/custom?career_slug=civil-engineer&education_level=Undergraduate")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    roadmap = data["roadmap"]

    # Verify Feature 5 requirements: 11 sequential milestones
    assert roadmap["career_slug"] == "civil-engineer"
    assert roadmap["total_milestones"] == 11
    assert len(roadmap["milestones"]) == 11

    # Verify first milestone
    m1 = roadmap["milestones"][0]
    assert m1["step_number"] == 1
    assert "Core Civil Engineering" in m1["title"]
    assert m1["stage_code"] in ["C", "A"]

    # Verify milestone 7 (internships)
    m7 = roadmap["milestones"][6]
    assert m7["step_number"] == 7
    assert "Internship" in m7["title"]
    assert m7["stage_code"] == "E"
    assert len(m7["opportunities"]) >= 1

    # Verify stage groups A-G present
    assert len(roadmap["stages"]) == 7


def test_sports_and_business_catalogs(test_client):
    client, _ = test_client

    # Sports Careers
    sports_careers = get_all_careers(category="Sports & Fitness")
    assert len(sports_careers) >= 4
    sports_slugs = [c["slug"] for c in sports_careers]
    assert "sports-analyst" in sports_slugs
    assert "sports-physiotherapist" in sports_slugs

    # Verify Sports Physiotherapy is marked regulated with BPT requirement
    physio = next(c for c in sports_careers if c["slug"] == "sports-physiotherapist")
    assert physio["regulated"] == 1
    assert "Physiotherapy" in physio["educational_requirements"]

    # Business & Commerce Careers
    biz_careers = get_all_careers(category="Business & Finance")
    assert len(biz_careers) >= 5
    biz_slugs = [c["slug"] for c in biz_careers]
    assert "business-analyst" in biz_slugs
    assert "marketing-specialist" in biz_slugs


def test_html_views_render_successfully(test_client):
    client, _ = test_client

    # Opportunities page
    res_opps = client.get("/opportunities")
    assert res_opps.status_code == 200
    assert b"Discover Student-Friendly Opportunities" in res_opps.data

    # Sports careers page
    res_sports = client.get("/sports-careers")
    assert res_sports.status_code == 200
    assert b"Sports, Athletics" in res_sports.data

    # Business careers page
    res_biz = client.get("/business-careers")
    assert res_biz.status_code == 200
    assert b"Business, Commerce" in res_biz.data

    # Snake Roadmap page
    res_roadmap = client.get("/roadmap")
    assert res_roadmap.status_code == 200
    assert b"Interactive Snake Roadmap" in res_roadmap.data
    assert b"snake-svg-layer" in res_roadmap.data

    # Compare page
    res_compare = client.get("/compare")
    assert res_compare.status_code == 200
    assert b"Parent &amp; Student Career Explorer" in res_compare.data
