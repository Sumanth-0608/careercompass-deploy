"""
CareerCompass - Full-Stack Career Guidance Platform
Flask Application, REST API Routes, and View Controllers
"""

import os
import json
import uuid
import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, abort, redirect, url_for, g, make_response

# Load environment variables from local .env
load_dotenv()

openai_configured = bool(os.getenv("OPENAI_API_KEY"))

from database import (
    init_db, close_db, get_db,
    get_all_careers, get_career_by_id, get_career_by_slug,
    save_assessment, get_assessment,
    save_recommendations, get_recommendations_by_assessment,
    save_career_plan, get_career_plan, get_all_plans, update_milestone_status,
    save_career_comparison, get_career_comparison,
    save_scenario_comparison, get_scenario_comparison,
    get_opportunities, get_opportunity_by_id, get_career_quotes, get_custom_roadmap,
    get_appointment_types, get_appointment_type_by_id, get_appointment_providers,
    get_available_slots, book_appointment_slot, cancel_appointment_booking,
    reschedule_appointment_booking, get_booking_by_ref, get_bookings_by_email,
    save_ai_conversation, add_ai_message, get_ai_conversations,
    get_ai_messages, delete_ai_conversation, clear_all_ai_conversations
)
from ai_service import (
    get_providers_info, validate_chat_request, call_ai_provider,
    call_parent_career_guide, PARENT_GUIDE_LANGUAGES
)
from translation_service import translate_text, SUPPORTED_LANGUAGES
from recommender import (
    generate_recommendations, DISCLAIMER_TEXT,
    compare_scenarios, simulate_scenario,
    DEFAULT_DEMO_PROFILE, ALLOWED_BUDGETS, ALLOWED_WORK_STYLES, ALLOWED_PRIORITIES
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("careercompass")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-careercompass-secret-key-2026")
app.config["JSON_SORT_KEYS"] = False

# Ensure database is initialized on startup
with app.app_context():
    init_db()

@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(400)
def bad_request(error):
    if request.path.startswith("/api/"):
        msg = getattr(error, "description", "Bad Request")
        return jsonify({"error": msg, "status": 400}), 400
    return render_template("error.html", code=400, message=getattr(error, "description", "Bad Request")), 400

@app.errorhandler(404)
def not_found(error):
    if request.path.startswith("/api/"):
        msg = getattr(error, "description", "Resource not found")
        return jsonify({"error": msg, "status": 404}), 404
    return render_template("error.html", code=404, message="The requested page could not be found."), 404

@app.errorhandler(500)
def server_error(error):
    logger.error("Internal Server Error: %s", error)
    if request.path.startswith("/api/"):
        return jsonify({"error": "An internal server error occurred. Please try again.", "status": 500}), 500
    return render_template("error.html", code=500, message="An internal error occurred. Please try again later."), 500


# ============================================================================
# Frontend HTML View Routes
# ============================================================================

@app.route("/")
def index():
    """Landing Page"""
    return render_template("index.html")

@app.route("/assessment")
@app.route("/quiz")
def quiz():
    """Career Discovery Assessment Page"""
    return render_template("quiz.html")

@app.route("/recommendations")
def recommendations_view():
    """Career Recommendations Display Page"""
    assessment_id = request.args.get("assessment_id")
    return render_template("recommendations.html", assessment_id=assessment_id)

@app.route("/careers")
def careers_catalog():
    """Career Directory / Exploration Page"""
    category = request.args.get("category")
    careers = get_all_careers(category=category)
    return render_template("careers.html", careers=careers, selected_category=category)

@app.route("/careers/<int:career_id>")
@app.route("/careers/<string:career_slug>")
def career_detail(career_id=None, career_slug=None):
    """Career Detail and Reality Check Page"""
    if isinstance(career_id, int):
        career = get_career_by_id(career_id)
    else:
        # Check if passed as integer in string
        try:
            c_id = int(career_slug)
            career = get_career_by_id(c_id)
        except ValueError:
            career = get_career_by_slug(career_slug)

    if not career:
        abort(404, description="Career pathway not found.")

    # Related careers in the same category
    all_same_cat = get_all_careers(category=career["category"])
    related = [c for c in all_same_cat if c["id"] != career["id"]][:3]

    return render_template("career_detail.html", career=career, related_careers=related)

@app.route("/roadmap")
def roadmap_view():
    """Interactive Snake Roadmap View (supports plan_id, career_id, education_level)"""
    plan_id = request.args.get("plan_id")
    career_id = request.args.get("career_id")
    education_level = request.args.get("education_level", "Undergraduate")
    all_careers = get_all_careers()
    return render_template(
        "roadmap.html",
        plan_id=plan_id,
        career_id=career_id,
        education_level=education_level,
        careers=all_careers
    )

@app.route("/opportunities")
def opportunities_view():
    """Discover Entry-Level Work, Internships, Apprenticeships & Part-Time Opportunities"""
    categories = [
        "All",
        "Civil Engineering & Construction",
        "IT & Software",
        "Business & Finance",
        "Sports & Fitness",
        "Part-Time & Campus"
    ]
    cities = [
        "All Cities",
        "Delhi NCR",
        "Bengaluru",
        "Mumbai",
        "Pune",
        "Hyderabad",
        "Chennai",
        "Kolkata",
        "Jaipur",
        "Chandigarh",
        "Remote"
    ]
    opportunity_types = [
        "All",
        "Internship",
        "Apprenticeship",
        "Part-Time",
        "Entry-Level",
        "Freelance Project",
        "Campus Opportunity"
    ]
    return render_template(
        "opportunities.html",
        categories=categories,
        cities=cities,
        opportunity_types=opportunity_types
    )

@app.route("/appointments")
def appointments_view():
    """Real-Time Appointment Booking and Mentorship Page"""
    selected_category = request.args.get("category", "All")
    selected_format = request.args.get("format", "All")
    type_id = request.args.get("type_id")
    slot_date = request.args.get("date")

    categories = [
        "All",
        "Career Guidance",
        "Interview Preparation",
        "Employment & Internship Support",
        "Parent–Student Discussion"
    ]
    formats = [
        "All",
        "Virtual Video Call",
        "Phone Consultation",
        "In-Person Hub"
    ]
    appointment_types = get_appointment_types()
    providers = get_appointment_providers()

    return render_template(
        "appointments.html",
        categories=categories,
        formats=formats,
        appointment_types=appointment_types,
        providers=providers,
        selected_category=selected_category,
        selected_format=selected_format,
        selected_type_id=type_id,
        selected_date=slot_date
    )

@app.route("/sports-careers")
def sports_careers_view():
    """Dedicated Sports & Athletic Careers Exploration Hub"""
    sports_careers = get_all_careers(category="Sports & Fitness")
    return render_template("sports_careers.html", careers=sports_careers)

@app.route("/business-careers")
def business_careers_view():
    """Dedicated Business, Commerce & Finance Careers Hub"""
    business_careers = get_all_careers(category="Business & Finance")
    return render_template("business_careers.html", careers=business_careers)

@app.route("/compare")
def compare_view():
    """Student–Parent Career Bridge Comparison Page"""
    comparison_id = request.args.get("comparison_id")
    assessment_id = request.args.get("assessment_id")
    careers = get_all_careers()
    assessment_data = None
    if assessment_id:
        try:
            assessment_data = get_assessment(int(assessment_id))
        except Exception:
            pass
    return render_template(
        "compare.html",
        careers=careers,
        comparison_id=comparison_id,
        assessment_id=assessment_id,
        assessment_data=assessment_data
    )

@app.route("/plans")
def plans_view():
    """Saved Career Plans Dashboard"""
    plans = get_all_plans()
    return render_template("plans.html", plans=plans)

@app.route("/about")
def about_view():
    """About & How It Works Page"""
    return render_template("about.html")


def get_or_create_session_id():
    """Retrieves or generates a persistent, pseudonymous session identifier stored in cookie."""
    sid = request.cookies.get("cc_session_id")
    if not sid:
        sid = str(uuid.uuid4())
    return sid


@app.route("/ai-chat")
def ai_chat_view():
    """
    Multi-AI Career Guidance Chat Interface
    Supports Google Gemini, OpenAI, Anthropic Claude, Mistral, and Groq.
    """
    providers = get_providers_info()
    session_id = get_or_create_session_id()
    resp = make_response(render_template(
        "ai_chat.html",
        providers=providers,
        disclaimer=DISCLAIMER_TEXT
    ))
    if not request.cookies.get("cc_session_id"):
        resp.set_cookie("cc_session_id", session_id, max_age=30 * 86400, httponly=True, samesite="Lax")
    return resp

@app.route("/simulator")
def simulator_view():
    """Career Reality Simulator Page"""
    assessment_id = request.args.get("assessment_id")
    initial_profile = dict(DEFAULT_DEMO_PROFILE)

    # If student has a saved assessment, map it into initial profile
    if assessment_id:
        try:
            assess = get_assessment(int(assessment_id))
            if assess:
                b_raw = (assess.get("budget_range") or "").lower()
                if "low" in b_raw or "free" in b_raw:
                    initial_profile["education_budget"] = "low"
                elif "flex" in b_raw:
                    initial_profile["education_budget"] = "flexible"
                else:
                    initial_profile["education_budget"] = "moderate"

                ws_raw = (assess.get("preferred_work_style") or "").lower()
                if "creative" in ws_raw or "art" in ws_raw:
                    initial_profile["work_style"] = "creative"
                elif "people" in ws_raw or "team" in ws_raw:
                    initial_profile["work_style"] = "people"
                elif "hands" in ws_raw:
                    initial_profile["work_style"] = "hands_on"
                else:
                    initial_profile["work_style"] = "analytical"

                g_raw = (assess.get("career_goals") or "").lower()
                if "stability" in g_raw:
                    initial_profile["priority"] = "stability"
                elif "social" in g_raw or "impact" in g_raw:
                    initial_profile["priority"] = "social_impact"
                elif "independ" in g_raw or "flex" in g_raw or "entrepreneur" in g_raw:
                    initial_profile["priority"] = "independence"
                else:
                    initial_profile["priority"] = "growth"
        except Exception as e:
            logger.warning("Could not map assessment to simulator: %s", e)

    return render_template(
        "simulator.html",
        initial_profile=initial_profile,
        demo_profile=DEFAULT_DEMO_PROFILE,
        allowed_budgets=ALLOWED_BUDGETS,
        allowed_work_styles=ALLOWED_WORK_STYLES,
        allowed_priorities=ALLOWED_PRIORITIES
    )


# ============================================================================
# REST API Endpoints
# ============================================================================

@app.route("/api/health", methods=["GET"])
def api_health():
    """Health check endpoint returning system status."""
    return jsonify({
        "status": "healthy",
        "service": "CareerCompass API",
        "version": "1.0.0",
        "database": "connected"
    }), 200


@app.route("/api/careers", methods=["GET"])
def api_get_careers():
    """
    Get catalog of career pathways.
    Optional query parameter: ?category=<category_name>
    """
    category = request.args.get("category")
    careers = get_all_careers(category=category)
    return jsonify({
        "success": True,
        "count": len(careers),
        "category_filter": category,
        "careers": careers
    }), 200


@app.route("/api/careers/<int:career_id>", methods=["GET"])
def api_get_career(career_id):
    """Retrieve detailed specification for a specific career by ID."""
    career = get_career_by_id(career_id)
    if not career:
        return jsonify({"error": f"Career with ID {career_id} not found", "status": 404}), 404
    return jsonify({
        "success": True,
        "career": career,
        "disclaimer": DISCLAIMER_TEXT
    }), 200


@app.route("/api/assessments", methods=["POST"])
def api_create_assessment():
    """
    Validate and save assessment submission.
    Returns: { "success": True, "assessment_id": <id> }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON payload", "status": 400}), 400

    # Server-side validation
    education_level = data.get("education_level")
    if not education_level or not isinstance(education_level, str):
        return jsonify({"error": "Education level is required and must be text", "status": 400}), 400

    interests = data.get("interests", [])
    if not isinstance(interests, list) or len(interests) == 0:
        return jsonify({"error": "At least one interest must be selected", "status": 400}), 400

    strengths = data.get("strengths", [])
    if not isinstance(strengths, list) or len(strengths) == 0:
        return jsonify({"error": "At least one strength must be selected", "status": 400}), 400

    preferred_work_style = data.get("preferred_work_style")
    if not preferred_work_style or not isinstance(preferred_work_style, str):
        return jsonify({"error": "Preferred work style is required", "status": 400}), 400

    career_goals = data.get("career_goals")
    if not career_goals or not isinstance(career_goals, str):
        return jsonify({"error": "Career goal is required", "status": 400}), 400

    # Sanitize length
    for field in ["education_level", "current_stream", "preferred_work_style", "career_goals", "budget_range", "location_preference", "constraints"]:
        if data.get(field) and isinstance(data[field], str) and len(data[field]) > 500:
            return jsonify({"error": f"Input for {field} exceeds maximum length limit of 500 characters", "status": 400}), 400

    assessment_id = save_assessment(data)

    # Immediately generate and persist recommendations
    recs = generate_recommendations(data)
    save_recommendations(assessment_id, recs)

    return jsonify({
        "success": True,
        "assessment_id": assessment_id,
        "message": "Assessment recorded successfully.",
        "recommendations_count": len(recs)
    }), 201


@app.route("/api/recommendations", methods=["POST"])
def api_get_recommendations():
    """
    Accepts either an existing 'assessment_id' or raw assessment profile JSON.
    Returns ranked, explainable recommendations with disclaimers.
    """
    data = request.get_json(silent=True) or {}
    assessment_id = data.get("assessment_id")

    if assessment_id:
        assessment = get_assessment(assessment_id)
        if not assessment:
            return jsonify({"error": f"Assessment ID {assessment_id} not found", "status": 404}), 404
        profile = assessment
    else:
        # Validate minimal profile
        if not data.get("interests") and not data.get("strengths"):
            return jsonify({
                "error": "Provide either 'assessment_id' or valid answers containing 'interests' and 'strengths'",
                "status": 400
            }), 400
        profile = data

    recs = generate_recommendations(profile)

    # If assessment_id is provided, ensure persisted
    if assessment_id:
        save_recommendations(assessment_id, recs)

    return jsonify({
        "success": True,
        "assessment_id": assessment_id,
        "count": len(recs),
        "disclaimer": DISCLAIMER_TEXT,
        "recommendations": recs
    }), 200


@app.route("/api/assessments/<int:assessment_id>/recommendations", methods=["GET"])
def api_get_saved_recommendations(assessment_id):
    """Retrieve saved recommendations for a recorded assessment."""
    assessment = get_assessment(assessment_id)
    if not assessment:
        return jsonify({"error": f"Assessment {assessment_id} not found", "status": 404}), 404

    recs = get_recommendations_by_assessment(assessment_id)
    if not recs:
        # Generate them if not yet generated
        recs = generate_recommendations(assessment)
        save_recommendations(assessment_id, recs)
        recs = get_recommendations_by_assessment(assessment_id)

    return jsonify({
        "success": True,
        "assessment_id": assessment_id,
        "assessment_details": assessment,
        "recommendations": recs,
        "disclaimer": DISCLAIMER_TEXT
    }), 200


@app.route("/api/careers/<int:career_id>/roadmap", methods=["GET"])
def api_get_career_roadmap(career_id):
    """Return template roadmap milestones for a career."""
    career = get_career_by_id(career_id)
    if not career:
        return jsonify({"error": f"Career {career_id} not found", "status": 404}), 404

    roadmap = career.get("learning_roadmap", [])
    return jsonify({
        "success": True,
        "career_id": career_id,
        "career_title": career["title"],
        "roadmap": roadmap,
        "disclaimer": "Roadmaps represent suggested educational milestones and do not guarantee employment."
    }), 200


@app.route("/api/opportunities", methods=["GET"])
def api_get_opportunities():
    """
    Search and filter verified & student-friendly opportunities.
    Query parameters:
    - category: string ('Civil Engineering & Construction', 'IT & Software', etc.)
    - location / city: string ('Delhi NCR', 'Bengaluru', 'Mumbai', etc.)
    - work_mode: 'remote', 'hybrid', 'on_site', 'all'
    - type: 'Internship', 'Apprenticeship', 'Part-Time', etc.
    - q: keyword search string
    """
    category = request.args.get("category")
    city = request.args.get("location") or request.args.get("city")
    work_mode = request.args.get("work_mode")
    opp_type = request.args.get("type")
    query = request.args.get("q")
    limit = request.args.get("limit", 60, type=int)

    opps = get_opportunities(
        category=category,
        location_city=city,
        work_mode=work_mode,
        opportunity_type=opp_type,
        query=query,
        limit=limit
    )

    return jsonify({
        "success": True,
        "count": len(opps),
        "filters": {
            "category": category,
            "location": city,
            "work_mode": work_mode,
            "type": opp_type,
            "query": query
        },
        "opportunities": opps,
        "disclaimer": "All listings are curated from official portal frameworks. Verify active application cycles on the respective official provider websites."
    }), 200


@app.route("/api/opportunities/<int:opp_id>", methods=["GET"])
def api_get_opportunity(opp_id):
    """Retrieve detailed metadata for an individual opportunity."""
    opp = get_opportunity_by_id(opp_id)
    if not opp:
        return jsonify({"error": f"Opportunity {opp_id} not found", "status": 404}), 404

    return jsonify({
        "success": True,
        "opportunity": opp
    }), 200


@app.route("/api/quotes", methods=["GET"])
def api_get_quotes():
    """
    Retrieve Career Inspiration motivational quotes with field-specific guidance.
    Optional query parameter: ?category=<category_name>
    """
    category = request.args.get("category")
    quotes = get_career_quotes(category=category)
    return jsonify({
        "success": True,
        "count": len(quotes),
        "quotes": quotes
    }), 200


@app.route("/api/roadmap/custom", methods=["GET"])
def api_get_custom_roadmap():
    """
    Retrieve interactive Snake Roadmap with Stage A–G groupings, connected
    opportunities, and beginner projects.
    Query parameters:
    - career_id: int or career_slug: string
    - education_level: string ('Class 10', 'Class 11-12', 'Diploma', 'Undergraduate', 'B.Tech')
    """
    career_id = request.args.get("career_id")
    career_slug = request.args.get("career_slug")
    education_level = request.args.get("education_level", "Undergraduate")

    target = career_id or career_slug or "civil-engineer"

    roadmap_data = get_custom_roadmap(target, education_level=education_level)
    if not roadmap_data:
        return jsonify({"error": f"Roadmap for {target} not found", "status": 404}), 404

    return jsonify({
        "success": True,
        "roadmap": roadmap_data,
        "disclaimer": "Educational planning guidance only. Does not represent statutory admission/employment guarantees."
    }), 200


@app.route("/api/plans", methods=["POST"])
def api_create_plan():
    """
    Save a student's selected career plan and instantiate their milestone checklist.
    Payload: { "career_id": 1, "assessment_id": 2 (optional), "student_name": "Aarav", "notes": "..." }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON payload", "status": 400}), 400

    career_id = data.get("career_id")
    if not career_id:
        return jsonify({"error": "career_id is required", "status": 400}), 400

    career = get_career_by_id(career_id)
    if not career:
        return jsonify({"error": f"Career {career_id} not found", "status": 404}), 404

    student_name = (data.get("student_name") or "Student").strip()
    notes = (data.get("notes") or "").strip()
    assessment_id = data.get("assessment_id")

    plan_id = save_career_plan(
        career_id=career_id,
        assessment_id=assessment_id,
        student_name=student_name,
        notes=notes
    )

    plan = get_career_plan(plan_id)
    return jsonify({
        "success": True,
        "plan_id": plan_id,
        "plan": plan,
        "message": f"Career plan for {career['title']} created successfully."
    }), 201


@app.route("/api/plans/<int:plan_id>", methods=["GET"])
def api_get_plan(plan_id):
    """Retrieve a saved career plan with milestone completion status."""
    plan = get_career_plan(plan_id)
    if not plan:
        return jsonify({"error": f"Career plan {plan_id} not found", "status": 404}), 404
    return jsonify({
        "success": True,
        "plan": plan
    }), 200


@app.route("/api/plans/<int:plan_id>/milestones/<int:milestone_id>", methods=["PATCH"])
def api_update_milestone(plan_id, milestone_id):
    """
    Update completion status of a roadmap milestone.
    Payload: { "is_completed": true / false }
    """
    data = request.get_json(silent=True)
    if data is None or "is_completed" not in data:
        return jsonify({"error": "Payload must include 'is_completed' boolean", "status": 400}), 400

    is_completed = bool(data["is_completed"])
    updated = update_milestone_status(plan_id, milestone_id, is_completed)

    if not updated:
        return jsonify({"error": f"Milestone {milestone_id} in plan {plan_id} not found", "status": 404}), 404

    refreshed_plan = get_career_plan(plan_id)
    return jsonify({
        "success": True,
        "message": "Milestone status updated",
        "milestone_id": milestone_id,
        "is_completed": is_completed,
        "plan_progress": refreshed_plan["progress_percentage"]
    }), 200


@app.route("/api/comparisons", methods=["POST"])
def api_create_comparison():
    """
    Save a Student–Parent Career Bridge comparison.
    Payload: {
        "student_career_id": 1,
        "alternative_career_id": 8,
        "student_reasons": "...",
        "alternative_reasons": "...",
        "assessment_id": 1 (optional),
        "shared_decision_summary": "..." (optional)
    }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON payload", "status": 400}), 400

    student_career_id = data.get("student_career_id")
    alternative_career_id = data.get("alternative_career_id")

    if not student_career_id or not alternative_career_id:
        return jsonify({"error": "Both student_career_id and alternative_career_id are required", "status": 400}), 400

    c1 = get_career_by_id(student_career_id)
    c2 = get_career_by_id(alternative_career_id)

    if not c1 or not c2:
        return jsonify({"error": "One or both selected careers do not exist", "status": 404}), 404

    student_reasons = (data.get("student_reasons") or "").strip()
    alternative_reasons = (data.get("alternative_reasons") or "").strip()

    # Pre-populate constructive discussion questions
    discussion_questions = [
        f"What excites each of us most about '{c1['title']}' versus '{c2['title']}'?",
        f"How do the education costs ({c1['cost_category']} vs {c2['cost_category']}) fit our financial comfort zone?",
        f"What are the realistic work-life trade-offs between daily responsibilities in each career?",
        f"Can we try a beginner starter project or talk to a working professional before making any binding decision?",
        "How can we support the student's personal choice while keeping pragmatic backup plans open?"
    ]

    education_comparison = {
        "student_career": {
            "title": c1["title"],
            "requirements": c1["educational_requirements"],
            "min_level": c1["min_education_level"],
            "regulated": c1["regulated"]
        },
        "alternative_career": {
            "title": c2["title"],
            "requirements": c2["educational_requirements"],
            "min_level": c2["min_education_level"],
            "regulated": c2["regulated"]
        }
    }

    cost_comparison = {
        "student_career": {
            "category": c1["cost_category"],
            "detail": c1["cost_estimate_detail"],
            "low_cost_routes": c1["low_cost_routes"]
        },
        "alternative_career": {
            "category": c2["cost_category"],
            "detail": c2["cost_estimate_detail"],
            "low_cost_routes": c2["low_cost_routes"]
        }
    }

    challenges_comparison = {
        "student_career": c1.get("challenges", []),
        "alternative_career": c2.get("challenges", [])
    }

    comparison_record = {
        "assessment_id": data.get("assessment_id"),
        "student_career_id": student_career_id,
        "alternative_career_id": alternative_career_id,
        "student_reasons": student_reasons,
        "alternative_reasons": alternative_reasons,
        "education_comparison": education_comparison,
        "cost_comparison": cost_comparison,
        "challenges_comparison": challenges_comparison,
        "discussion_questions": discussion_questions,
        "shared_decision_summary": data.get("shared_decision_summary", ""),
        "alignment_status": data.get("alignment_status", "exploring")
    }

    comp_id = save_career_comparison(comparison_record)
    result = get_career_comparison(comp_id)

    return jsonify({
        "success": True,
        "comparison_id": comp_id,
        "comparison": result,
        "message": "Career comparison bridge created successfully."
    }), 201


@app.route("/api/comparisons/<int:comparison_id>", methods=["GET"])
def api_get_comparison(comparison_id):
    """Retrieve an existing Student–Parent comparison record."""
    comp = get_career_comparison(comparison_id)
    if not comp:
        return jsonify({"error": f"Comparison {comparison_id} not found", "status": 404}), 404
    return jsonify({
        "success": True,
        "comparison": comp
    }), 200


# ============================================================================
# Career Reality Simulator Endpoints
# ============================================================================

@app.route("/api/simulator/compare", methods=["POST"])
def api_simulator_compare():
    """
    Compares Baseline vs Alternative scenarios for Career Reality Simulator.
    Payload:
    {
        "baseline": { "education_budget": "moderate", "work_style": "analytical", "priority": "growth" },
        "alternative": { "education_budget": "low", "work_style": "creative", "priority": "stability" },
        "save": false (optional)
    }
    """
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid or missing JSON payload", "status": 400}), 400

    baseline_data = data.get("baseline")
    alternative_data = data.get("alternative")

    if not baseline_data or not isinstance(baseline_data, dict):
        return jsonify({"error": "Missing or invalid 'baseline' scenario object", "status": 400}), 400

    if not alternative_data or not isinstance(alternative_data, dict):
        return jsonify({"error": "Missing or invalid 'alternative' scenario object", "status": 400}), 400

    try:
        results = compare_scenarios(baseline_data, alternative_data)
    except ValueError as val_err:
        return jsonify({"error": str(val_err), "status": 400}), 400
    except Exception as exc:
        logger.error("Simulator error: %s", exc)
        return jsonify({"error": "Failed to compute scenario comparison", "status": 500}), 500

    comparison_id = None
    if data.get("save"):
        try:
            comparison_id = save_scenario_comparison(
                results["baseline_profile"],
                results["alternative_profile"],
                results
            )
            results["comparison_id"] = comparison_id
        except Exception as save_err:
            logger.warning("Could not auto-save scenario: %s", save_err)

    return jsonify({
        "success": True,
        **results
    }), 200


@app.route("/api/simulator/save", methods=["POST"])
def api_simulator_save():
    """
    Saves scenario comparison to SQLite database for persistent revisit.
    """
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid or missing JSON payload", "status": 400}), 400

    baseline_data = data.get("baseline")
    alternative_data = data.get("alternative")

    if not baseline_data or not isinstance(baseline_data, dict):
        return jsonify({"error": "Missing or invalid 'baseline' scenario object", "status": 400}), 400

    if not alternative_data or not isinstance(alternative_data, dict):
        return jsonify({"error": "Missing or invalid 'alternative' scenario object", "status": 400}), 400

    try:
        results = compare_scenarios(baseline_data, alternative_data)
        comp_id = save_scenario_comparison(
            results["baseline_profile"],
            results["alternative_profile"],
            results
        )
    except ValueError as val_err:
        return jsonify({"error": str(val_err), "status": 400}), 400
    except Exception as exc:
        logger.error("Save scenario error: %s", exc)
        return jsonify({"error": "Failed to save scenario comparison", "status": 500}), 500

    return jsonify({
        "success": True,
        "comparison_id": comp_id,
        "comparison": results,
        "message": "Scenario comparison saved successfully."
    }), 201


@app.route("/api/simulator/saved/<int:comparison_id>", methods=["GET"])
def api_get_saved_scenario(comparison_id):
    """Retrieves a saved scenario comparison from SQLite."""
    record = get_scenario_comparison(comparison_id)
    if not record:
        return jsonify({"error": f"Scenario comparison {comparison_id} not found", "status": 404}), 404

    return jsonify({
        "success": True,
        "comparison_id": record["id"],
        "baseline_profile": record["baseline_profile"],
        "alternative_profile": record["alternative_profile"],
        "results": record["comparison_results"],
        "created_at": record.get("created_at")
    }), 200


# ============================================================================
# Appointments REST API Endpoints
# ============================================================================

@app.route("/api/appointments/types", methods=["GET"])
def api_get_appointment_types():
    """Retrieve appointment types, optionally filtered by category or format."""
    category = request.args.get("category")
    format_filter = request.args.get("format")
    types = get_appointment_types(category=category, format_filter=format_filter)
    return jsonify({
        "success": True,
        "count": len(types),
        "types": types
    }), 200


@app.route("/api/appointments/slots", methods=["GET"])
def api_get_appointment_slots():
    """
    Fetch appointment slots.
    Query params:
    - type_id: filter by specific type
    - date: filter by YYYY-MM-DD
    - category: filter by type category
    - provider_id: filter by provider
    - include_booked: 1 to include booked slots (for calendar visualization)
    """
    type_id = request.args.get("type_id", type=int)
    slot_date = request.args.get("date")
    category = request.args.get("category")
    provider_id = request.args.get("provider_id", type=int)
    include_booked = request.args.get("include_booked") in ["1", "true", "True"]

    slots = get_available_slots(
        type_id=type_id,
        slot_date=slot_date,
        category=category,
        provider_id=provider_id,
        include_booked=include_booked
    )
    return jsonify({
        "success": True,
        "count": len(slots),
        "slots": slots
    }), 200


@app.route("/api/appointments/book", methods=["POST"])
def api_book_appointment():
    """
    Atomically book an appointment slot.
    Double-booking is prevented with atomic SQLite update.
    Returns 409 Conflict if slot is unavailable.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON request body", "status": 400}), 400

    slot_id = data.get("slot_id")
    student_name = data.get("student_name")
    student_email = data.get("student_email")

    if not slot_id or not isinstance(slot_id, int):
        return jsonify({"error": "Valid integer 'slot_id' is required", "status": 400}), 400

    if not student_name or not isinstance(student_name, str) or len(student_name.strip()) < 2:
        return jsonify({"error": "Full name is required (at least 2 characters)", "status": 400}), 400

    if not student_email or not isinstance(student_email, str) or "@" not in student_email:
        return jsonify({"error": "A valid email address is required", "status": 400}), 400

    booking, err = book_appointment_slot(
        slot_id=slot_id,
        student_name=student_name,
        student_email=student_email,
        student_phone=data.get("student_phone"),
        education_level=data.get("education_level", "Undergraduate"),
        current_career_interest=data.get("current_career_interest"),
        notes_or_questions=data.get("notes_or_questions")
    )

    if err:
        return jsonify({
            "error": err,
            "status": 409
        }), 409

    return jsonify({
        "success": True,
        "booking": booking,
        "message": f"Appointment confirmed! Your booking reference is {booking['booking_ref']}."
    }), 201


@app.route("/api/appointments/cancel", methods=["POST"])
def api_cancel_appointment():
    """
    Cancel an appointment booking by booking reference.
    Frees up the slot atomically for other students.
    """
    data = request.get_json(silent=True)
    if not data or not data.get("booking_ref"):
        return jsonify({"error": "Missing 'booking_ref' in request body", "status": 400}), 400

    booking_ref = data.get("booking_ref").strip()
    reason = data.get("reason", "Cancelled by student")

    booking, err = cancel_appointment_booking(booking_ref, reason=reason)
    if err:
        return jsonify({"error": err, "status": 400}), 400

    return jsonify({
        "success": True,
        "booking": booking,
        "message": f"Booking {booking_ref} has been cancelled and the slot is now open."
    }), 200


@app.route("/api/appointments/reschedule", methods=["POST"])
def api_reschedule_appointment():
    """
    Reschedule an existing booking to a new slot.
    """
    data = request.get_json(silent=True)
    if not data or not data.get("booking_ref") or not data.get("new_slot_id"):
        return jsonify({"error": "Both 'booking_ref' and 'new_slot_id' are required", "status": 400}), 400

    booking_ref = data.get("booking_ref").strip()
    new_slot_id = data.get("new_slot_id")

    booking, err = reschedule_appointment_booking(booking_ref, new_slot_id)
    if err:
        return jsonify({"error": err, "status": 409}), 409

    return jsonify({
        "success": True,
        "booking": booking,
        "message": f"Appointment rescheduled successfully to {booking['slot_date']} at {booking['start_time']}."
    }), 200


@app.route("/api/appointments/my-bookings", methods=["GET"])
def api_get_my_bookings():
    """
    Look up bookings by email or reference code.
    """
    email = request.args.get("email")
    ref = request.args.get("ref")

    if ref:
        booking = get_booking_by_ref(ref.strip())
        if not booking:
            return jsonify({"error": f"Booking reference {ref} not found", "status": 404}), 404
        return jsonify({
            "success": True,
            "bookings": [booking]
        }), 200

    if email:
        bookings = get_bookings_by_email(email.strip())
        return jsonify({
            "success": True,
            "count": len(bookings),
            "bookings": bookings
        }), 200

    return jsonify({"error": "Please provide 'email' or 'ref' query parameter", "status": 400}), 400


# ============================================================================
# Multi-AI Career Guidance Chat API Endpoints
# ============================================================================

@app.route("/api/ai/providers", methods=["GET"])
def api_get_ai_providers():
    """
    Returns list of supported AI providers, connection status, and model choices.
    Never exposes API keys or secrets.
    """
    providers = get_providers_info()
    return jsonify({
        "success": True,
        "count": len(providers),
        "providers": providers
    }), 200


@app.route("/api/ai/chat", methods=["POST"])
def api_ai_chat():
    """
    Unified AI chat endpoint for Google Gemini and ChatGPT (OpenAI).
    Validates request, calls the selected provider SDK adapter,
    saves the conversation to SQLite, and returns normalized response with career action chips.
    """
    payload = request.get_json(silent=True)
    if not payload or not isinstance(payload, dict):
        return jsonify({
            "success": False,
            "error": {
                "code": "invalid_request",
                "message": "Invalid JSON body provided."
            },
            "status": 400
        }), 400

    provider_id = (payload.get("provider") or "gemini").strip().lower()
    model_id = (payload.get("model") or "").strip()
    raw_messages = payload.get("messages", [])

    # Adapt single message + history format if provided
    if not raw_messages and payload.get("message"):
        history = payload.get("history") or []
        raw_messages = list(history) + [{"role": "user", "content": str(payload["message"])}]

    conv_id = (payload.get("conversation_id") or "").strip() or str(uuid.uuid4())
    use_profile = bool(payload.get("use_profile", False))
    profile_data = payload.get("profile_data") if use_profile else None

    # Validate chat request parameters and history
    is_valid, err_msg, validated = validate_chat_request(provider_id, model_id, raw_messages)
    if not is_valid:
        return jsonify({
            "success": False,
            "error": {
                "code": "validation_error",
                "message": err_msg
            },
            "status": 400
        }), 400

    session_id = get_or_create_session_id()
    all_careers = get_all_careers()

    try:
        # Call provider SDK adapter
        ai_result = call_ai_provider(
            provider_id=validated["provider_id"],
            model_id=validated["model_id"],
            messages=validated["messages"],
            user_profile=profile_data,
            careers_catalog=all_careers
        )

        # Generate conversation title from the first user message
        first_user_msg = next((m["content"] for m in validated["messages"] if m["role"] == "user"), "Career Guidance Session")
        title = first_user_msg[:60] + ("..." if len(first_user_msg) > 60 else "")

        # Persist conversation and messages in SQLite
        save_ai_conversation(
            conv_id=conv_id,
            session_id=session_id,
            provider=ai_result["provider"],
            model=ai_result["model"],
            title=title,
            profile_shared=use_profile
        )

        # Save user message
        latest_user_content = validated["messages"][-1]["content"]
        add_ai_message(conv_id, "user", latest_user_content)

        # Save assistant message with action chips
        add_ai_message(conv_id, "assistant", ai_result["content"], action_chips=ai_result.get("action_chips"))

        res_json = {
            "success": True,
            "provider": ai_result["provider"],
            "reply": ai_result["content"],
            "model": ai_result["model"],
            "conversation_id": conv_id,
            "provider_name": ai_result["provider_name"],
            "message": {
                "role": "assistant",
                "content": ai_result["content"],
                "action_chips": ai_result.get("action_chips", [])
            },
            "is_mock": ai_result.get("is_mock", False)
        }
        resp = jsonify(res_json)
        if not request.cookies.get("cc_session_id"):
            resp.set_cookie("cc_session_id", session_id, max_age=30 * 86400, httponly=True, samesite="Lax")
        return resp, 200

    except PermissionError as e:
        logger.warning("Auth error in api_ai_chat: %s", e)
        return jsonify({
            "success": False,
            "error": {
                "code": "auth_error",
                "message": str(e)
            },
            "status": 401
        }), 401
    except TimeoutError as e:
        logger.warning("Timeout in api_ai_chat: %s", e)
        return jsonify({
            "success": False,
            "error": {
                "code": "timeout",
                "message": str(e)
            },
            "status": 504
        }), 504
    except ConnectionError as e:
        logger.warning("Connection error in api_ai_chat: %s", e)
        return jsonify({
            "success": False,
            "error": {
                "code": "provider_unavailable",
                "message": str(e)
            },
            "status": 502
        }), 502
    except RuntimeError as e:
        logger.warning("Runtime error in api_ai_chat: %s", e)
        return jsonify({
            "success": False,
            "error": {
                "code": "provider_error",
                "message": str(e)
            },
            "status": 502
        }), 502
    except ValueError as e:
        logger.warning("Validation error in api_ai_chat: %s", e)
        return jsonify({
            "success": False,
            "error": {
                "code": "invalid_request",
                "message": str(e)
            },
            "status": 400
        }), 400
    except Exception as e:
        logger.error("Unexpected error in api_ai_chat: %s", e, exc_info=True)
        return jsonify({
            "success": False,
            "error": {
                "code": "internal_error",
                "message": "An internal error occurred while generating AI guidance. Please try again."
            },
            "status": 500
        }), 500


@app.route("/api/parent-career-guide", methods=["POST"])
def api_parent_career_guide():
    """
    Multilingual AI Parent Voice Canvass Endpoint.
    Generates empathetic, individualized career guidance for parents in Telugu, Hindi, or English
    based on the student's actual preferences in the Family Alignment & Agreement Mapping.
    """
    payload = request.get_json(silent=True)
    if not payload or not isinstance(payload, dict):
        return jsonify({
            "success": False,
            "error": {
                "code": "invalid_request",
                "message": "Invalid JSON body provided."
            },
            "status": 400
        }), 400

    language = (payload.get("language") or "en").strip().lower()
    if language not in PARENT_GUIDE_LANGUAGES:
        return jsonify({
            "success": False,
            "error": {
                "code": "unsupported_language",
                "message": f"Language '{language}' is not supported. Please choose from: {', '.join(PARENT_GUIDE_LANGUAGES.keys())}."
            },
            "status": 400
        }), 400

    student_profile = payload.get("student_profile") or {}
    if not isinstance(student_profile, dict):
        return jsonify({
            "success": False,
            "error": {
                "code": "invalid_profile",
                "message": "student_profile must be a dictionary of student career attributes."
            },
            "status": 400
        }), 400

    message = (payload.get("message") or "").strip()
    if len(message) > 2500:
        return jsonify({
            "success": False,
            "error": {
                "code": "message_too_long",
                "message": "Question exceeds maximum limit of 2,500 characters."
            },
            "status": 400
        }), 400

    history = payload.get("history") or []
    if not isinstance(history, list):
        history = []

    preferred_provider = (payload.get("provider") or "").strip().lower() or None

    try:
        result = call_parent_career_guide(
            language=language,
            student_profile=student_profile,
            message=message,
            history=history,
            preferred_provider=preferred_provider
        )
        return jsonify(result), 200

    except PermissionError as e:
        logger.warning("Auth error in api_parent_career_guide: %s", e)
        return jsonify({
            "success": False,
            "error": {
                "code": "missing_credentials",
                "message": str(e)
            },
            "status": 401
        }), 401
    except ValueError as e:
        logger.warning("Validation error in api_parent_career_guide: %s", e)
        return jsonify({
            "success": False,
            "error": {
                "code": "invalid_parameter",
                "message": str(e)
            },
            "status": 400
        }), 400
    except (ConnectionError, TimeoutError) as e:
        logger.warning("Connection error in api_parent_career_guide: %s", e)
        return jsonify({
            "success": False,
            "error": {
                "code": "connection_error",
                "message": "Failed to connect to AI provider. Please check network connection or retry."
            },
            "status": 504
        }), 504
    except RuntimeError as e:
        logger.warning("Runtime error in api_parent_career_guide: %s", e)
        return jsonify({
            "success": False,
            "error": {
                "code": "provider_error",
                "message": str(e)
            },
            "status": 502
        }), 502
    except Exception as e:
        logger.error("Unexpected error in api_parent_career_guide: %s", e, exc_info=True)
        return jsonify({
            "success": False,
            "error": {
                "code": "internal_error",
                "message": "An internal error occurred while generating parent career guidance."
            },
            "status": 500
        }), 500


@app.route("/api/translate", methods=["POST"])
def api_translate():
    """
    Non-AI translation endpoint supporting Telugu (te), Hindi (hi), and English (en).
    Accepts:
        {
            "text": "...",
            "source_language": "te" | "hi" | "en",
            "target_language": "te" | "hi" | "en"
        }
    Strictly uses no AI/LLM models.
    """
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": {
                "code": "invalid_payload",
                "message": "Request body must be valid JSON."
            },
            "status": 400
        }), 400

    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    if not text:
        return jsonify({
            "success": False,
            "error": {
                "code": "missing_text",
                "message": "Text to translate is required."
            },
            "status": 400
        }), 400

    if len(text) > 2500:
        return jsonify({
            "success": False,
            "error": {
                "code": "text_too_long",
                "message": "Text exceeds maximum limit of 2,500 characters."
            },
            "status": 400
        }), 400

    source_lang = (payload.get("source_language") or "").strip().lower()
    target_lang = (payload.get("target_language") or "").strip().lower()

    if source_lang not in SUPPORTED_LANGUAGES:
        return jsonify({
            "success": False,
            "error": {
                "code": "unsupported_source_language",
                "message": f"Unsupported source language '{source_lang}'. Supported: te (Telugu), hi (Hindi), en (English)."
            },
            "status": 400
        }), 400

    if target_lang not in SUPPORTED_LANGUAGES:
        return jsonify({
            "success": False,
            "error": {
                "code": "unsupported_target_language",
                "message": f"Unsupported target language '{target_lang}'. Supported: te (Telugu), hi (Hindi), en (English)."
            },
            "status": 400
        }), 400

    try:
        translated = translate_text(text, source_lang, target_lang)
        return jsonify({
            "success": True,
            "source_language": source_lang,
            "target_language": target_lang,
            "original_text": text,
            "translated_text": translated
        }), 200
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": {
                "code": "invalid_language",
                "message": str(e)
            },
            "status": 400
        }), 400
    except Exception as e:
        logger.warning("Translation error: %s", e)
        return jsonify({
            "success": False,
            "error": {
                "code": "translation_unavailable",
                "message": "Translation service is currently unavailable. Please check your text and try again."
            },
            "status": 502
        }), 502


@app.route("/api/ai/conversations", methods=["GET"])
def api_get_ai_conversations():
    """Retrieves conversation history for current session."""
    session_id = get_or_create_session_id()
    conversations = get_ai_conversations(session_id)
    return jsonify({
        "success": True,
        "count": len(conversations),
        "conversations": conversations
    }), 200


@app.route("/api/ai/conversations/<string:conversation_id>", methods=["GET"])
def api_get_ai_conversation_detail(conversation_id):
    """Retrieves all messages for a specific conversation belonging to this session."""
    session_id = get_or_create_session_id()
    messages = get_ai_messages(conversation_id, session_id=session_id)
    if messages is None:
        return jsonify({"error": "Conversation not found or access denied.", "status": 404}), 404
    return jsonify({
        "success": True,
        "conversation_id": conversation_id,
        "count": len(messages),
        "messages": messages
    }), 200


@app.route("/api/ai/conversations/<string:conversation_id>", methods=["DELETE"])
def api_delete_ai_conversation(conversation_id):
    """Deletes a conversation belonging to current session."""
    session_id = get_or_create_session_id()
    deleted = delete_ai_conversation(conversation_id, session_id=session_id)
    if not deleted:
        return jsonify({"error": "Conversation not found or could not be deleted.", "status": 404}), 404
    return jsonify({"success": True, "message": "Conversation deleted successfully."}), 200


@app.route("/api/ai/conversations/clear", methods=["POST"])
def api_clear_ai_conversations():
    """Clears all conversations for current session."""
    session_id = get_or_create_session_id()
    cleared_count = clear_all_ai_conversations(session_id)
    return jsonify({"success": True, "cleared_count": cleared_count}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting CareerCompass Web Application on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)

