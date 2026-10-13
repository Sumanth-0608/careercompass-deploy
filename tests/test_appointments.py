"""
Tests for CareerCompass Real-Time Appointments System & Expanded Career Taxonomy
Verifies:
1. Appointment types and providers querying
2. Slot availability filtering by category, date, and format
3. Atomic booking with double-booking prevention (409 Conflict)
4. Cancellation workflow and atomic slot release
5. Rescheduling workflow
6. Lookup by email and booking reference
7. Expanded 36-career taxonomy in database
8. Statutory regulations & spelling integrity (PCI, choreography, cryptography)
"""

import pytest
import json
import os
import tempfile
from app import app
from database import init_db, get_db, get_all_careers, get_career_by_slug

@pytest.fixture
def client():
    db_fd, temp_db_path = tempfile.mkstemp(suffix="_test_apt.db")
    app.config["DATABASE"] = temp_db_path
    app.config["TESTING"] = True

    with app.app_context():
        init_db(temp_db_path)

    with app.test_client() as test_client:
        yield test_client

    os.close(db_fd)
    if os.path.exists(temp_db_path):
        os.remove(temp_db_path)
    app.config.pop("DATABASE", None)


def test_appointment_types_endpoint(client):
    """Verifies listing appointment types with category filtering."""
    res = client.get("/api/appointments/types")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["count"] >= 8
    
    # Check specific categories exist
    categories = {t["category"] for t in data["types"]}
    assert "Career Guidance" in categories
    assert "Interview Preparation" in categories
    assert "Employment & Internship Support" in categories
    assert "Parent–Student Discussion" in categories

    # Filter by category
    filter_res = client.get("/api/appointments/types?category=Interview%20Preparation")
    assert filter_res.status_code == 200
    filter_data = filter_res.get_json()
    for t in filter_data["types"]:
        assert t["category"] == "Interview Preparation"


def test_appointment_slots_endpoint(client):
    """Verifies listing appointment slots with provider & type joins."""
    res = client.get("/api/appointments/slots")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["count"] > 0

    first_slot = data["slots"][0]
    assert "slot_date" in first_slot
    assert "start_time" in first_slot
    assert "end_time" in first_slot
    assert "type_title" in first_slot
    assert "provider_name" in first_slot
    assert "provider_badge" in first_slot
    assert first_slot["is_booked"] == 0  # Only available returned by default


def test_successful_booking_and_double_booking_prevention(client):
    """
    Critical test:
    1. Successfully book slot A.
    2. Attempt to book slot A a second time -> Must be rejected with 409 Conflict.
    """
    # 1. Get an available slot
    slots_res = client.get("/api/appointments/slots")
    slots = slots_res.get_json()["slots"]
    assert len(slots) > 0
    target_slot = slots[0]
    slot_id = target_slot["id"]

    # 2. First booking succeeds
    payload = {
        "slot_id": slot_id,
        "student_name": "Aarav Sharma",
        "student_email": "aarav.sharma@example.edu",
        "student_phone": "+91 9876543210",
        "education_level": "Undergraduate",
        "current_career_interest": "Software & Robotics",
        "notes_or_questions": "Interested in review of coding portfolio"
    }

    book_res = client.post("/api/appointments/book", json=payload)
    assert book_res.status_code == 201
    book_data = book_res.get_json()
    assert book_data["success"] is True
    booking = book_data["booking"]
    assert booking["booking_ref"].startswith("CC-APT-")
    assert booking["student_name"] == "Aarav Sharma"
    assert booking["student_email"] == "aarav.sharma@example.edu"
    assert booking["status"] == "confirmed"

    # 3. Second booking on the SAME slot MUST FAIL with 409 Conflict
    conflict_payload = {
        "slot_id": slot_id,
        "student_name": "Simran Kaur",
        "student_email": "simran.kaur@example.edu"
    }

    conflict_res = client.post("/api/appointments/book", json=conflict_payload)
    assert conflict_res.status_code == 409
    conflict_data = conflict_res.get_json()
    assert "error" in conflict_data
    assert "longer available" in conflict_data["error"] or "booked" in conflict_data["error"]


def test_lookup_and_cancellation_releases_slot(client):
    """
    Verifies:
    1. Booking a slot.
    2. Looking it up by booking reference and email.
    3. Cancelling the booking -> releases slot back to available.
    4. Re-booking the released slot succeeds.
    """
    slots_res = client.get("/api/appointments/slots")
    target_slot = slots_res.get_json()["slots"][0]
    slot_id = target_slot["id"]

    # Book slot
    payload = {
        "slot_id": slot_id,
        "student_name": "Meera Joshi",
        "student_email": "meera.joshi@example.org"
    }
    book_res = client.post("/api/appointments/book", json=payload)
    assert book_res.status_code == 201
    booking_ref = book_res.get_json()["booking"]["booking_ref"]

    # Lookup by reference
    lookup_ref_res = client.get(f"/api/appointments/my-bookings?ref={booking_ref}")
    assert lookup_ref_res.status_code == 200
    assert lookup_ref_res.get_json()["bookings"][0]["booking_ref"] == booking_ref

    # Lookup by email
    lookup_email_res = client.get("/api/appointments/my-bookings?email=meera.joshi@example.org")
    assert lookup_email_res.status_code == 200
    assert len(lookup_email_res.get_json()["bookings"]) >= 1

    # Cancel booking
    cancel_res = client.post("/api/appointments/cancel", json={
        "booking_ref": booking_ref,
        "reason": "Family schedule conflict"
    })
    assert cancel_res.status_code == 200
    cancel_data = cancel_res.get_json()
    assert cancel_data["success"] is True
    assert cancel_data["booking"]["status"] == "cancelled"

    # Confirm slot is available again
    slots_after_cancel = client.get("/api/appointments/slots").get_json()["slots"]
    available_ids = [s["id"] for s in slots_after_cancel]
    assert slot_id in available_ids

    # Re-booking the released slot now succeeds!
    rebook_res = client.post("/api/appointments/book", json={
        "slot_id": slot_id,
        "student_name": "Kavita Nair",
        "student_email": "kavita.nair@example.org"
    })
    assert rebook_res.status_code == 201
    assert rebook_res.get_json()["booking"]["student_name"] == "Kavita Nair"


def test_reschedule_booking(client):
    """Verifies rescheduling an appointment moves booking and frees old slot."""
    slots = client.get("/api/appointments/slots").get_json()["slots"]
    assert len(slots) >= 2
    slot_1 = slots[0]
    slot_2 = slots[1]

    # Book slot 1
    book_res = client.post("/api/appointments/book", json={
        "slot_id": slot_1["id"],
        "student_name": "Vikram Patel",
        "student_email": "vikram.patel@example.com"
    })
    assert book_res.status_code == 201
    booking_ref = book_res.get_json()["booking"]["booking_ref"]

    # Reschedule to slot 2
    resched_res = client.post("/api/appointments/reschedule", json={
        "booking_ref": booking_ref,
        "new_slot_id": slot_2["id"]
    })
    assert resched_res.status_code == 200
    resched_data = resched_res.get_json()
    assert resched_data["success"] is True
    assert resched_data["booking"]["slot_id"] == slot_2["id"]
    assert resched_data["booking"]["status"] == "rescheduled"

    # Slot 1 should now be open again
    slots_now = client.get("/api/appointments/slots").get_json()["slots"]
    available_ids = [s["id"] for s in slots_now]
    assert slot_1["id"] in available_ids
    assert slot_2["id"] not in available_ids


def test_appointments_html_view(client):
    """Verifies rendering the /appointments view template with lively blue background and glass dropdowns."""
    res = client.get("/appointments")
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "Book an Appointment" in html
    assert "Real-Time Appointment Scheduling" in html
    assert "Verified Guidance Network" in html
    assert "Book a Session" in html
    assert "Manage / Look Up Booking" in html
    # Verify animated blue ambient background
    assert "blue-ambient-bg" in html
    assert "ambient-light-field" in html
    assert "ambient-orb" in html
    # Verify glassmorphic custom dropdowns
    assert "dropdown-category" in html
    assert "dropdown-format" in html
    assert "dropdown-type" in html
    assert "glass-dropdown" in html
    assert "filter-card-container" in html


def test_expanded_careers_catalog_and_integrity(client):
    """
    Verifies that all 36 careers exist, including:
    - Pharmacist (with statutory PCI requirement)
    - Biotechnologist
    - Astronomer & Space Scientist
    - Astronaut (with demanding qualifications note)
    - Robotics Engineer
    - Electrical Engineer
    - Aerospace Engineer
    - Video Editor
    - Music Producer
    - 3D Animator
    - Choreographer (strictly correct spelling: choreography)
    - Civil Services / Public Policy
    - Cybersecurity Analyst (strictly correct spelling: cryptography, authorized penetration testing)
    """
    careers = get_all_careers()
    assert len(careers) >= 36
    slugs = {c["slug"] for c in careers}

    expected_slugs = [
        "pharmacist", "biotechnologist", "astronomer-space-scientist",
        "astronaut", "robotics-engineer", "electrical-engineer",
        "aerospace-engineer", "video-editor-media-producer", "music-producer-audio",
        "animator-visual-artist", "choreographer-performer", "public-policy-civil-services",
        "civil-engineer", "cybersecurity-analyst"
    ]

    for expected in expected_slugs:
        assert expected in slugs, f"Missing expected slug: {expected}"

    # Statutory PCI check on Pharmacist
    pharma = get_career_by_slug("pharmacist")
    assert pharma is not None
    assert pharma["regulated"] == 1
    assert "Pharmacy Council of India" in pharma["educational_requirements"] or "PCI" in pharma["educational_requirements"]

    # Astronaut demanding selection check
    astro = get_career_by_slug("astronaut")
    assert astro is not None
    assert astro["regulated"] == 1
    assert "ISRO" in astro["educational_requirements"] or "NASA" in astro["educational_requirements"]

    # Choreography correct spelling check
    choreo = get_career_by_slug("choreographer-performer")
    assert choreo is not None
    assert "choreography" in choreo["title"].lower() or "choreographer" in choreo["title"].lower()
    assert "choregraphy" not in json.dumps(dict(choreo)).lower(), "Spelling error: 'choregraphy' detected instead of 'choreography'"

    # Cryptography in cybersecurity check
    cyber = get_career_by_slug("cybersecurity-analyst")
    assert cyber is not None
    assert "cryptogaphy" not in json.dumps(dict(cyber)).lower(), "Spelling error: 'cryptogaphy' detected instead of 'cryptography'"
