"""
CareerCompass Recommendation Engine
Transparent, rule-based career matching algorithm.
Evaluates interest overlap, strength alignment, work style fit, career goals,
and educational compatibility without black-box AI dependencies.
"""

import json
from database import get_all_careers, get_career_by_id

# Disclaimer attached to every recommendation output
DISCLAIMER_TEXT = (
    "CareerCompass match scores are reflective guidance and educational orientation tools, "
    "not scientific psychometric assessments, clinical diagnostics, or employment guarantees. "
    "Your future is shaped by curiosity, dedication, and personal choice."
)

WORK_STYLE_MAP = {
    "people-oriented": [
        "healthcare-professional", "teacher-educator", "ux-ui-designer", "business-analyst",
        "entrepreneur", "clinical-psychologist", "sports-coach", "sports-physiotherapist",
        "hr-specialist", "marketing-specialist", "choreographer-performer", "public-policy-civil-services"
    ],
    "people-oriented work": [
        "healthcare-professional", "teacher-educator", "ux-ui-designer", "business-analyst",
        "entrepreneur", "clinical-psychologist", "sports-coach", "sports-physiotherapist",
        "hr-specialist", "marketing-specialist", "choreographer-performer", "public-policy-civil-services"
    ],
    "hands-on": [
        "electronics-engineer", "mechanical-engineer", "environmental-scientist", "software-developer",
        "civil-engineer", "sports-coach", "robotics-engineer", "electrical-engineer",
        "aerospace-engineer", "video-editor-media-producer", "music-producer-audio", "choreographer-performer", "astronaut"
    ],
    "hands-on work": [
        "electronics-engineer", "mechanical-engineer", "environmental-scientist", "software-developer",
        "civil-engineer", "sports-coach", "robotics-engineer", "electrical-engineer",
        "aerospace-engineer", "video-editor-media-producer", "music-producer-audio", "choreographer-performer", "astronaut"
    ],
    "research": [
        "data-analyst", "environmental-scientist", "clinical-psychologist", "cybersecurity-analyst",
        "sports-analyst", "sports-science-specialist", "biotechnologist", "astronomer-space-scientist",
        "public-policy-civil-services", "pharmacist"
    ],
    "teamwork": [
        "software-developer", "business-analyst", "teacher-educator", "healthcare-professional",
        "entrepreneur", "civil-engineer", "sports-event-manager", "sports-coach", "product-manager",
        "supply-chain-manager", "robotics-engineer", "aerospace-engineer", "video-editor-media-producer",
        "public-policy-civil-services", "choreographer-performer", "astronaut"
    ],
    "individual": [
        "graphic-designer", "software-developer", "data-analyst", "chartered-accountant",
        "clinical-psychologist", "sports-analyst", "video-editor-media-producer", "music-producer-audio",
        "animator-visual-artist", "astronomer-space-scientist"
    ],
    "individual work": [
        "graphic-designer", "software-developer", "data-analyst", "chartered-accountant",
        "clinical-psychologist", "sports-analyst", "video-editor-media-producer", "music-producer-audio",
        "animator-visual-artist", "astronomer-space-scientist"
    ]
}

GOAL_MAP = {
    "stability": [
        "chartered-accountant", "teacher-educator", "cybersecurity-analyst", "healthcare-professional",
        "civil-engineer", "supply-chain-manager", "pharmacist", "electrical-engineer", "public-policy-civil-services"
    ],
    "social impact": [
        "healthcare-professional", "teacher-educator", "environmental-scientist", "clinical-psychologist",
        "civil-engineer", "sports-coach", "pharmacist", "biotechnologist", "public-policy-civil-services"
    ],
    "social_impact": [
        "healthcare-professional", "teacher-educator", "environmental-scientist", "clinical-psychologist",
        "civil-engineer", "sports-coach", "pharmacist", "biotechnologist", "public-policy-civil-services"
    ],
    "learning": [
        "software-developer", "data-analyst", "electronics-engineer", "cybersecurity-analyst",
        "mechanical-engineer", "civil-engineer", "sports-science-specialist", "robotics-engineer",
        "aerospace-engineer", "astronomer-space-scientist", "biotechnologist", "astronaut"
    ],
    "independence": [
        "graphic-designer", "entrepreneur", "software-developer", "clinical-psychologist",
        "ux-ui-designer", "marketing-specialist", "video-editor-media-producer", "music-producer-audio",
        "animator-visual-artist", "choreographer-performer"
    ],
    "entrepreneurship": [
        "entrepreneur", "business-analyst", "software-developer", "graphic-designer",
        "sports-event-manager", "product-manager", "marketing-specialist", "video-editor-media-producer", "music-producer-audio"
    ]
}

SUBJECT_AFFINITY_MAP = {
    "computer science": [
        "software-developer", "data-analyst", "cybersecurity-analyst", "ux-ui-designer",
        "sports-analyst", "product-manager", "robotics-engineer", "animator-visual-artist"
    ],
    "mathematics": [
        "data-analyst", "software-developer", "chartered-accountant", "electronics-engineer",
        "mechanical-engineer", "civil-engineer", "sports-analyst", "supply-chain-manager",
        "astronomer-space-scientist", "robotics-engineer", "electrical-engineer", "aerospace-engineer"
    ],
    "physics": [
        "electronics-engineer", "mechanical-engineer", "environmental-scientist", "civil-engineer",
        "sports-science-specialist", "astronomer-space-scientist", "astronaut", "robotics-engineer",
        "electrical-engineer", "aerospace-engineer"
    ],
    "biology": [
        "healthcare-professional", "environmental-scientist", "clinical-psychologist",
        "sports-physiotherapist", "sports-science-specialist", "pharmacist", "biotechnologist"
    ],
    "chemistry": [
        "environmental-scientist", "healthcare-professional", "sports-science-specialist",
        "pharmacist", "biotechnologist"
    ],
    "economics": [
        "business-analyst", "data-analyst", "chartered-accountant", "entrepreneur",
        "marketing-specialist", "supply-chain-manager", "product-manager"
    ],
    "accountancy": [
        "chartered-accountant", "business-analyst", "supply-chain-manager"
    ],
    "art": [
        "graphic-designer", "ux-ui-designer", "animator-visual-artist", "video-editor-media-producer"
    ],
    "design": [
        "ux-ui-designer", "graphic-designer", "civil-engineer", "product-manager",
        "animator-visual-artist", "video-editor-media-producer"
    ],
    "music": [
        "music-producer-audio", "choreographer-performer"
    ],
    "psychology": [
        "clinical-psychologist", "ux-ui-designer", "teacher-educator", "hr-specialist", "marketing-specialist"
    ],
    "english": [
        "teacher-educator", "business-analyst", "ux-ui-designer", "marketing-specialist", "hr-specialist"
    ],
    "social studies": [
        "teacher-educator", "environmental-scientist", "public service", "sports-event-manager",
        "public-policy-civil-services"
    ],
    "physical education": [
        "sports-coach", "sports-analyst", "sports-physiotherapist", "sports-event-manager",
        "sports-science-specialist", "choreographer-performer", "astronaut"
    ],
    "sports": [
        "sports-coach", "sports-analyst", "sports-physiotherapist", "sports-event-manager",
        "sports-science-specialist", "choreographer-performer", "astronaut"
    ]
}


def calculate_match(student_profile, career):
    """
    Computes transparent multi-factor matching score between student and a career.
    Total maximum raw score = 100 points.

    Factors:
    - Interests (35 pts max)
    - Strengths (25 pts max)
    - Work Style (15 pts max)
    - Career Goals (15 pts max)
    - Educational / Stream alignment (10 pts max)
    """
    reasons = []
    trade_offs = list(career.get("challenges", []))
    alternative_routes = [career.get("low_cost_routes", "Self-study and open resources available.")]

    # 1. Interests (35 pts)
    user_interests = [i.strip().lower() for i in student_profile.get("interests", [])]
    career_interests = [i.strip().lower() for i in career.get("relevant_interests", [])]
    matched_interests = [i for i in user_interests if i in career_interests]

    if career_interests:
        interest_ratio = len(matched_interests) / len(career_interests)
        # Cap ratio at 1.0
        interest_ratio = min(1.0, interest_ratio)
        interest_score = interest_ratio * 30
    else:
        interest_score = 15

    # Subject affinity bonus (up to 5 pts)
    user_subjects = [s.strip().lower() for s in student_profile.get("favorite_subjects", [])]
    matched_subjects = []
    for sub in user_subjects:
        for mapped_sub, slugs in SUBJECT_AFFINITY_MAP.items():
            if mapped_sub in sub and career.get("slug") in slugs:
                matched_subjects.append(sub)
                break
    subject_bonus = min(5.0, len(matched_subjects) * 2.5)
    interest_score += subject_bonus

    if matched_interests:
        reasons.append(f"Strongly aligns with your interest in {', '.join(matched_interests)}.")
    if matched_subjects:
        reasons.append(f"Builds on your favorite subjects ({', '.join(matched_subjects)}).")

    # 2. Strengths (25 pts)
    user_strengths = [s.strip().lower() for s in student_profile.get("strengths", [])]
    career_strengths = [s.strip().lower() for s in career.get("relevant_strengths", [])]
    matched_strengths = [s for s in user_strengths if s in career_strengths]

    if career_strengths:
        strength_ratio = len(matched_strengths) / len(career_strengths)
        strength_score = min(1.0, strength_ratio) * 25
    else:
        strength_score = 12.5

    if matched_strengths:
        reasons.append(f"Leverages your natural strengths in {', '.join(matched_strengths)}.")

    # 3. Work Style (15 pts)
    user_style = (student_profile.get("preferred_work_style") or "").strip().lower()
    style_matches = WORK_STYLE_MAP.get(user_style, [])
    if career.get("slug") in style_matches:
        work_style_score = 15.0
        reasons.append(f"Fits your preferred work style of '{user_style}'.")
    elif any(career.get("slug") in slugs for key, slugs in WORK_STYLE_MAP.items() if key in user_style):
        work_style_score = 10.0
        reasons.append(f"Compatible with your preference for '{user_style}'.")
    else:
        work_style_score = 6.0

    # 4. Goals (15 pts)
    user_goal = (student_profile.get("career_goals") or "").strip().lower()
    goal_matches = GOAL_MAP.get(user_goal, [])
    if career.get("slug") in goal_matches:
        goal_score = 15.0
        reasons.append(f"Supports your core aspiration for {user_goal.replace('_', ' ')}.")
    elif any(career.get("slug") in slugs for key, slugs in GOAL_MAP.items() if key in user_goal):
        goal_score = 10.0
        reasons.append(f"Provides good pathways toward {user_goal.replace('_', ' ')}.")
    else:
        goal_score = 6.0

    # 5. Education & Stream Compatibility (10 pts)
    edu_score = 7.0
    user_stream = (student_profile.get("current_stream") or "").strip().lower()
    suitable_streams = [s.lower() for s in career.get("suitable_streams", [])]

    is_stream_compatible = (
        any("any" in s for s in suitable_streams) or
        any(user_stream in s or s in user_stream for s in suitable_streams) or
        not user_stream
    )

    if is_stream_compatible:
        edu_score += 3.0
    else:
        # If stream isn't a direct match, explain educational transition
        edu_score += 1.0
        reasons.append(f"Note: Standard entry typically recommends {career.get('suitable_streams', ['relevant'])[0]}; bridge courses or self-taught prep may be required.")

    # Budget check - DO NOT eliminate low budget users!
    user_budget = (student_profile.get("budget_range") or "").strip().lower()
    if "low" in user_budget or "free" in user_budget:
        if career.get("cost_category") == "Low / Free Accessible":
            reasons.append("Highly budget-friendly: extensive free resources and low-cost degrees exist.")
        elif career.get("regulated"):
            alternative_routes.append(
                f"For low-budget learners: target government merit-based colleges ({career.get('cost_estimate_detail', '')}) "
                "or state scholarships to waive tuition."
            )

    # 6. Missing Skills Analysis
    existing_skills = [sk.strip().lower() for sk in student_profile.get("existing_skills", [])]
    important_skills = career.get("important_skills", [])
    missing_skills = []
    for sk in important_skills:
        sk_lower = sk.lower()
        if not any(ex in sk_lower or sk_lower in ex for ex in existing_skills):
            missing_skills.append(sk)

    # Calculate total match percentage (capped at 98% because no prediction is guaranteed 100%)
    raw_total = interest_score + strength_score + work_style_score + goal_score + edu_score
    match_percentage = min(98.0, max(25.0, round(raw_total, 1)))

    if not reasons:
        reasons.append(f"Offers broad exploration opportunities aligned with your overall profile.")

    return {
        "career_id": career["id"],
        "title": career["title"],
        "slug": career["slug"],
        "category": career["category"],
        "short_description": career["short_description"],
        "match_score": match_percentage,
        "match_reasons": reasons,
        "missing_skills": missing_skills[:4],
        "trade_offs": trade_offs[:3],
        "alternative_routes": alternative_routes,
        "cost_category": career.get("cost_category"),
        "regulated": career.get("regulated", 0),
        "min_education_level": career.get("min_education_level")
    }


def generate_recommendations(student_profile, db_path=None, top_n=6):
    """
    Evaluates all careers in the database against the student's profile.
    Returns ranked recommendations, ensuring at least 3 high-quality options.
    """
    all_careers = get_all_careers(db_path=db_path)
    if not all_careers:
        return []

    scored_recs = []
    for career in all_careers:
        rec = calculate_match(student_profile, career)
        scored_recs.append(rec)

    # Sort descending by match score
    scored_recs.sort(key=lambda x: x["match_score"], reverse=True)

    # Return top N (at least 3 if available)
    top_results = scored_recs[:max(3, min(top_n, len(scored_recs)))]

    # Attach ranks
    for idx, r in enumerate(top_results, start=1):
        r["rank"] = idx

    return top_results


# ============================================================================
# Career Reality Simulator: Extensions & Comparison Engine
# ============================================================================

# Documented configuration weights for the Reality Simulator
# Stored in one clearly documented configuration as required
SIMULATOR_WEIGHTS = {
    "work_style": 0.30,       # 30% Work-style compatibility
    "priority": 0.25,         # 25% Career-priority compatibility
    "interest": 0.25,         # 25% Interest compatibility
    "skills_strengths": 0.20  # 20% Existing skills & strengths
}

DEFAULT_DEMO_PROFILE = {
    "education_budget": "moderate",
    "work_style": "analytical",
    "priority": "growth"
}

ALLOWED_BUDGETS = {
    "very_limited": "Very limited",
    "low": "Low",
    "moderate": "Moderate",
    "flexible": "Flexible"
}

ALLOWED_WORK_STYLES = {
    "analytical": "Analytical and problem-solving",
    "creative": "Creative and design-focused",
    "people": "People-oriented and collaborative",
    "hands_on": "Hands-on and practical"
}

ALLOWED_PRIORITIES = {
    "growth": "Learning and growth",
    "stability": "Stability",
    "social_impact": "Social impact",
    "independence": "Flexibility and independence"
}

BUDGET_ALIASES = {
    "very limited": "very_limited",
    "very_limited": "very_limited",
    "very-limited": "very_limited",
    "limited": "very_limited",
    "low": "low",
    "moderate": "moderate",
    "medium": "moderate",
    "flexible": "flexible",
    "high": "flexible"
}

WORK_STYLE_ALIASES = {
    "analytical and problem-solving": "analytical",
    "analytical and problem solving": "analytical",
    "analytical": "analytical",
    "problem-solving": "analytical",
    "creative and design-focused": "creative",
    "creative and design focused": "creative",
    "creative": "creative",
    "design": "creative",
    "people-oriented and collaborative": "people",
    "people-oriented": "people",
    "people oriented": "people",
    "collaborative": "people",
    "people": "people",
    "hands-on and practical": "hands_on",
    "hands on and practical": "hands_on",
    "hands-on": "hands_on",
    "hands on": "hands_on",
    "hands_on": "hands_on",
    "practical": "hands_on"
}

PRIORITY_ALIASES = {
    "learning and growth": "growth",
    "learning & growth": "growth",
    "learning": "growth",
    "growth": "growth",
    "stability": "stability",
    "social impact": "social_impact",
    "social_impact": "social_impact",
    "impact": "social_impact",
    "flexibility and independence": "independence",
    "flexibility & independence": "independence",
    "flexibility": "independence",
    "independence": "independence"
}

# Structured affinities for all 14 career pathways
CAREER_SIMULATOR_AFFINITIES = {
    "software-developer": {
        "work_style": {"analytical": 1.0, "hands_on": 0.85, "creative": 0.65, "people": 0.50},
        "priority": {"growth": 1.0, "independence": 0.85, "stability": 0.65, "social_impact": 0.50}
    },
    "data-analyst": {
        "work_style": {"analytical": 1.0, "people": 0.60, "hands_on": 0.40, "creative": 0.35},
        "priority": {"growth": 0.95, "stability": 0.90, "independence": 0.60, "social_impact": 0.50}
    },
    "cybersecurity-analyst": {
        "work_style": {"analytical": 1.0, "hands_on": 0.70, "people": 0.45, "creative": 0.30},
        "priority": {"stability": 1.0, "growth": 0.85, "social_impact": 0.65, "independence": 0.45}
    },
    "electronics-engineer": {
        "work_style": {"hands_on": 1.0, "analytical": 0.90, "creative": 0.50, "people": 0.35},
        "priority": {"growth": 0.95, "stability": 0.80, "independence": 0.50, "social_impact": 0.55}
    },
    "mechanical-engineer": {
        "work_style": {"hands_on": 1.0, "analytical": 0.90, "creative": 0.50, "people": 0.35},
        "priority": {"growth": 0.90, "stability": 0.85, "independence": 0.40, "social_impact": 0.55}
    },
    "ux-ui-designer": {
        "work_style": {"creative": 1.0, "people": 0.85, "analytical": 0.60, "hands_on": 0.35},
        "priority": {"growth": 0.85, "independence": 0.85, "social_impact": 0.65, "stability": 0.55}
    },
    "graphic-designer": {
        "work_style": {"creative": 1.0, "hands_on": 0.50, "analytical": 0.35, "people": 0.40},
        "priority": {"independence": 1.0, "growth": 0.65, "social_impact": 0.50, "stability": 0.35}
    },
    "healthcare-professional": {
        "work_style": {"people": 1.0, "hands_on": 0.80, "analytical": 0.60, "creative": 0.25},
        "priority": {"social_impact": 1.0, "stability": 0.95, "growth": 0.70, "independence": 0.30}
    },
    "teacher-educator": {
        "work_style": {"people": 1.0, "creative": 0.60, "analytical": 0.45, "hands_on": 0.30},
        "priority": {"social_impact": 1.0, "stability": 0.90, "growth": 0.65, "independence": 0.35}
    },
    "business-analyst": {
        "work_style": {"analytical": 0.95, "people": 0.85, "creative": 0.55, "hands_on": 0.30},
        "priority": {"growth": 0.90, "stability": 0.80, "independence": 0.60, "social_impact": 0.50}
    },
    "entrepreneur": {
        "work_style": {"creative": 0.90, "people": 0.90, "analytical": 0.70, "hands_on": 0.65},
        "priority": {"growth": 1.0, "independence": 1.0, "social_impact": 0.70, "stability": 0.25}
    },
    "environmental-scientist": {
        "work_style": {"hands_on": 0.95, "analytical": 0.85, "people": 0.55, "creative": 0.30},
        "priority": {"social_impact": 1.0, "growth": 0.80, "stability": 0.60, "independence": 0.50}
    },
    "clinical-psychologist": {
        "work_style": {"people": 1.0, "analytical": 0.80, "creative": 0.50, "hands_on": 0.25},
        "priority": {"social_impact": 1.0, "independence": 0.80, "stability": 0.70, "growth": 0.75}
    },
    "chartered-accountant": {
        "work_style": {"analytical": 1.0, "people": 0.55, "hands_on": 0.25, "creative": 0.20},
        "priority": {"stability": 1.0, "growth": 0.80, "independence": 0.75, "social_impact": 0.35}
    },
    "civil-engineer": {
        "work_style": {"hands_on": 1.0, "analytical": 0.90, "people": 0.50, "creative": 0.40},
        "priority": {"stability": 0.95, "growth": 0.85, "social_impact": 0.70, "independence": 0.40}
    },
    "sports-analyst": {
        "work_style": {"analytical": 1.0, "people": 0.60, "hands_on": 0.40, "creative": 0.35},
        "priority": {"growth": 0.95, "stability": 0.85, "independence": 0.60, "social_impact": 0.50}
    },
    "sports-physiotherapist": {
        "work_style": {"people": 1.0, "hands_on": 0.95, "analytical": 0.65, "creative": 0.25},
        "priority": {"social_impact": 1.0, "stability": 0.90, "growth": 0.80, "independence": 0.45}
    },
    "sports-coach": {
        "work_style": {"people": 1.0, "hands_on": 0.90, "analytical": 0.60, "creative": 0.45},
        "priority": {"social_impact": 1.0, "growth": 0.85, "independence": 0.60, "stability": 0.50}
    },
    "sports-event-manager": {
        "work_style": {"people": 0.95, "hands_on": 0.85, "analytical": 0.65, "creative": 0.60},
        "priority": {"growth": 0.90, "independence": 0.75, "stability": 0.60, "social_impact": 0.50}
    },
    "sports-science-specialist": {
        "work_style": {"analytical": 1.0, "hands_on": 0.85, "people": 0.60, "creative": 0.30},
        "priority": {"growth": 0.95, "social_impact": 0.80, "stability": 0.70, "independence": 0.50}
    },
    "marketing-specialist": {
        "work_style": {"creative": 0.95, "people": 0.85, "analytical": 0.75, "hands_on": 0.35},
        "priority": {"growth": 0.95, "independence": 0.85, "stability": 0.55, "social_impact": 0.45}
    },
    "hr-specialist": {
        "work_style": {"people": 1.0, "analytical": 0.70, "creative": 0.45, "hands_on": 0.30},
        "priority": {"stability": 0.95, "social_impact": 0.85, "growth": 0.75, "independence": 0.40}
    },
    "supply-chain-manager": {
        "work_style": {"analytical": 0.95, "hands_on": 0.80, "people": 0.75, "creative": 0.35},
        "priority": {"stability": 0.95, "growth": 0.85, "social_impact": 0.55, "independence": 0.40}
    },
    "product-manager": {
        "work_style": {"people": 0.95, "analytical": 0.90, "creative": 0.85, "hands_on": 0.40},
        "priority": {"growth": 1.0, "independence": 0.85, "social_impact": 0.70, "stability": 0.55}
    },
    "pharmacist": {
        "work_style": {"analytical": 0.95, "people": 0.80, "hands_on": 0.60, "creative": 0.20},
        "priority": {"stability": 1.0, "social_impact": 0.90, "growth": 0.75, "independence": 0.40}
    },
    "biotechnologist": {
        "work_style": {"analytical": 1.0, "hands_on": 0.85, "people": 0.45, "creative": 0.40},
        "priority": {"social_impact": 0.95, "growth": 0.90, "stability": 0.70, "independence": 0.50}
    },
    "astronomer-space-scientist": {
        "work_style": {"analytical": 1.0, "hands_on": 0.50, "people": 0.35, "creative": 0.45},
        "priority": {"growth": 1.0, "independence": 0.70, "stability": 0.65, "social_impact": 0.55}
    },
    "astronaut": {
        "work_style": {"hands_on": 1.0, "analytical": 0.95, "people": 0.75, "creative": 0.40},
        "priority": {"growth": 1.0, "social_impact": 0.90, "stability": 0.60, "independence": 0.40}
    },
    "robotics-engineer": {
        "work_style": {"hands_on": 1.0, "analytical": 0.95, "creative": 0.60, "people": 0.45},
        "priority": {"growth": 1.0, "independence": 0.70, "stability": 0.70, "social_impact": 0.60}
    },
    "electrical-engineer": {
        "work_style": {"hands_on": 0.95, "analytical": 0.90, "people": 0.45, "creative": 0.35},
        "priority": {"stability": 0.95, "growth": 0.85, "social_impact": 0.70, "independence": 0.45}
    },
    "aerospace-engineer": {
        "work_style": {"analytical": 0.95, "hands_on": 0.90, "creative": 0.55, "people": 0.45},
        "priority": {"growth": 1.0, "stability": 0.80, "social_impact": 0.65, "independence": 0.45}
    },
    "video-editor-media-producer": {
        "work_style": {"creative": 1.0, "hands_on": 0.65, "analytical": 0.50, "people": 0.50},
        "priority": {"independence": 1.0, "growth": 0.80, "social_impact": 0.50, "stability": 0.40}
    },
    "music-producer-audio": {
        "work_style": {"creative": 1.0, "hands_on": 0.70, "analytical": 0.50, "people": 0.45},
        "priority": {"independence": 1.0, "growth": 0.80, "social_impact": 0.50, "stability": 0.35}
    },
    "animator-visual-artist": {
        "work_style": {"creative": 1.0, "hands_on": 0.60, "analytical": 0.55, "people": 0.35},
        "priority": {"independence": 0.95, "growth": 0.85, "social_impact": 0.50, "stability": 0.45}
    },
    "choreographer-performer": {
        "work_style": {"creative": 1.0, "people": 0.85, "hands_on": 0.80, "analytical": 0.30},
        "priority": {"independence": 1.0, "social_impact": 0.70, "growth": 0.75, "stability": 0.35}
    },
    "public-policy-civil-services": {
        "work_style": {"people": 0.95, "analytical": 0.90, "hands_on": 0.45, "creative": 0.40},
        "priority": {"social_impact": 1.0, "stability": 1.0, "growth": 0.75, "independence": 0.30}
    }
}


def normalize_simulator_profile(profile):
    """
    Validates and normalizes simulator profile keys and values.
    Raises ValueError with descriptive feedback on missing or invalid fields.
    """
    if not isinstance(profile, dict):
        raise ValueError("Profile must be a JSON object")

    raw_budget = str(profile.get("education_budget") or "").strip().lower()
    raw_style = str(profile.get("work_style") or "").strip().lower()
    raw_priority = str(profile.get("priority") or "").strip().lower()

    if not raw_budget:
        raise ValueError("Education budget is required (education_budget)")
    if not raw_style:
        raise ValueError("Preferred work style is required (work_style)")
    if not raw_priority:
        raise ValueError("Career priority is required (priority)")

    budget = BUDGET_ALIASES.get(raw_budget)
    if not budget:
        raise ValueError(
            f"Invalid education_budget '{raw_budget}'. Allowed values: {list(ALLOWED_BUDGETS.keys())}"
        )

    work_style = WORK_STYLE_ALIASES.get(raw_style)
    if not work_style:
        raise ValueError(
            f"Invalid work_style '{raw_style}'. Allowed values: {list(ALLOWED_WORK_STYLES.keys())}"
        )

    priority = PRIORITY_ALIASES.get(raw_priority)
    if not priority:
        raise ValueError(
            f"Invalid priority '{raw_priority}'. Allowed values: {list(ALLOWED_PRIORITIES.keys())}"
        )

    return {
        "education_budget": budget,
        "work_style": work_style,
        "priority": priority,
        "education_budget_label": ALLOWED_BUDGETS[budget],
        "work_style_label": ALLOWED_WORK_STYLES[work_style],
        "priority_label": ALLOWED_PRIORITIES[priority]
    }


def get_budget_adapted_route(career, budget_level):
    """
    Returns practical learning route options and financial considerations
    adapted to the user's budget, clearly distinguishing verified estimates
    from institution-dependent variables.
    """
    cost_cat = career.get("cost_category", "Moderate")
    estimate_detail = career.get("cost_estimate_detail", "Education costs need to be verified for your institution and location.")
    low_cost = career.get("low_cost_routes", "Self-study and open resources available.")
    is_regulated = bool(career.get("regulated", 0))

    if budget_level == "very_limited":
        feasibility = (
            "Requires state merit seat or scholarship for formal degrees; self-study and portfolio pathways are highly recommended."
            if is_regulated else
            "Highly viable via open-source tools, free documentation, and community project portfolios."
        )
        return {
            "budget_tier": "Very limited",
            "suggested_route": "Open Educational Resources & Government Fee Waivers",
            "specific_pathway": low_cost,
            "cost_notes": "Aim for near-zero tuition through open platforms (e.g. NPTEL, freeCodeCamp) or merit-based fee concessions.",
            "feasibility": feasibility,
            "verification_status": "Approximate estimate — verify specific institutional waiver criteria."
        }
    elif budget_level == "low":
        return {
            "budget_tier": "Low",
            "suggested_route": "Public / State Colleges & Subsidized Distance Learning",
            "specific_pathway": f"{low_cost}. Consider state universities or subsidized diploma institutes.",
            "cost_notes": estimate_detail,
            "feasibility": "Good accessibility through public universities, state entrance exams, and need-based financial aid.",
            "verification_status": "Approximate estimate based on public college fee guidelines."
        }
    elif budget_level == "moderate":
        return {
            "budget_tier": "Moderate",
            "suggested_route": "Standard Regional / University Degree",
            "specific_pathway": career.get("educational_requirements", "Undergraduate degree program"),
            "cost_notes": estimate_detail,
            "feasibility": "Balanced access to recognized public and regional collegiate programs.",
            "verification_status": "Verified range for public institutions; private colleges may cost more."
        }
    else:  # flexible
        return {
            "budget_tier": "Flexible",
            "suggested_route": "Comprehensive Collegiate & Specialized Accelerator Route",
            "specific_pathway": f"{career.get('educational_requirements', 'Undergraduate degree')}. Can incorporate specialized private academies, premium software suites, and studio residencies.",
            "cost_notes": "Unconstrained by basic tuition; evaluate return on investment and placement track records.",
            "feasibility": "Broadest pathway flexibility across premier institutions and global certifications.",
            "verification_status": "Variable — tuition and residency costs depend on specific chosen institution."
        }


def calculate_simulator_match(profile, career):
    """
    Calculates deterministic multi-factor compatibility score for a simulator profile.
    
    Weights (100% total):
    - Work-style compatibility: 30%
    - Career-priority compatibility: 25%
    - Interest compatibility: 25%
    - Skills and strengths: 20%
    
    CRITICAL RULE:
    Education budget does NOT artificially lower a career's intrinsic compatibility score.
    Instead, budget governs the practical learning routes and financial feasibility advice.
    """
    slug = career.get("slug", "")
    work_style = profile["work_style"]
    priority = profile["priority"]
    budget = profile["education_budget"]

    # 1. Work Style Compatibility (30 pts max)
    affinities = CAREER_SIMULATOR_AFFINITIES.get(slug, {})
    ws_ratings = affinities.get("work_style", {})
    if work_style in ws_ratings:
        ws_ratio = ws_ratings[work_style]
    else:
        # Graceful fallback for custom or unmapped career metadata
        rel_strengths = [s.lower() for s in career.get("relevant_strengths", [])]
        if work_style == "analytical":
            ws_ratio = 0.9 if "analytical thinking" in rel_strengths or "practical problem-solving" in rel_strengths else 0.5
        elif work_style == "creative":
            ws_ratio = 0.9 if "creativity" in rel_strengths else 0.5
        elif work_style == "people":
            ws_ratio = 0.9 if "empathy" in rel_strengths or "communication" in rel_strengths else 0.5
        elif work_style == "hands_on":
            ws_ratio = 0.9 if "practical problem-solving" in rel_strengths else 0.5
        else:
            ws_ratio = 0.5
    ws_score = ws_ratio * 30.0

    # 2. Priority Compatibility (25 pts max)
    pr_ratings = affinities.get("priority", {})
    if priority in pr_ratings:
        pr_ratio = pr_ratings[priority]
    else:
        # Fallback based on career category & characteristics
        cat = career.get("category", "").lower()
        if priority == "growth":
            pr_ratio = 0.9 if "tech" in cat or "data" in cat or "business" in cat else 0.6
        elif priority == "stability":
            pr_ratio = 0.95 if career.get("regulated") or "health" in cat or "education" in cat else 0.5
        elif priority == "social_impact":
            pr_ratio = 0.95 if "health" in cat or "education" in cat or "environment" in cat else 0.5
        elif priority == "independence":
            pr_ratio = 0.9 if "creative" in cat or "entrepreneur" in slug else 0.5
        else:
            pr_ratio = 0.5
    pr_score = pr_ratio * 25.0

    # 3. Interest Compatibility (25 pts max)
    # Map simulator inputs to representative interest domains
    target_interests = []
    if work_style == "analytical":
        target_interests.extend(["technology", "science", "business"])
    elif work_style == "creative":
        target_interests.extend(["creativity", "technology", "business"])
    elif work_style == "people":
        target_interests.extend(["healthcare", "education", "public service", "people-oriented work"])
    elif work_style == "hands_on":
        target_interests.extend(["technology", "science", "hands-on work"])

    if priority == "growth":
        target_interests.extend(["technology", "science"])
    elif priority == "stability":
        target_interests.extend(["stability", "business", "education"])
    elif priority == "social_impact":
        target_interests.extend(["healthcare", "education", "public service"])
    elif priority == "independence":
        target_interests.extend(["creativity", "business"])

    career_interests = [i.lower() for i in career.get("relevant_interests", [])]
    if career_interests and target_interests:
        matched = set(target_interests).intersection(set(career_interests))
        interest_ratio = len(matched) / max(1, len(set(career_interests)))
        interest_ratio = min(1.0, interest_ratio + 0.3)  # Base relevance boost
    else:
        interest_ratio = 0.6
    interest_score = min(1.0, interest_ratio) * 25.0

    # 4. Strengths & Skills Compatibility (20 pts max)
    target_strengths = []
    if work_style == "analytical":
        target_strengths.extend(["analytical thinking", "practical problem-solving"])
    elif work_style == "creative":
        target_strengths.extend(["creativity", "communication"])
    elif work_style == "people":
        target_strengths.extend(["empathy", "communication", "leadership"])
    elif work_style == "hands_on":
        target_strengths.extend(["practical problem-solving", "analytical thinking"])

    career_strengths = [s.lower() for s in career.get("relevant_strengths", [])]
    if career_strengths and target_strengths:
        matched_str = set(target_strengths).intersection(set(career_strengths))
        str_ratio = len(matched_str) / max(1, len(set(career_strengths)))
        str_ratio = min(1.0, str_ratio + 0.35)
    else:
        str_ratio = 0.6
    skills_score = min(1.0, str_ratio) * 20.0

    raw_total = ws_score + pr_score + interest_score + skills_score
    match_percentage = min(98.0, max(25.0, round(raw_total, 1)))

    # Qualitative label
    if match_percentage >= 80.0:
        match_label = "High Alignment"
    elif match_percentage >= 65.0:
        match_label = "Moderate Alignment"
    else:
        match_label = "Exploratory Alignment"

    # Specific explanation reasons grounded in facts
    reasons = []
    if ws_ratio >= 0.8:
        reasons.append(f"Strongly complements your preferred '{ALLOWED_WORK_STYLES[work_style]}' working style.")
    elif ws_ratio >= 0.6:
        reasons.append(f"Partially incorporates elements of '{ALLOWED_WORK_STYLES[work_style]}' tasks.")

    if pr_ratio >= 0.8:
        reasons.append(f"Directly supports your core priority of '{ALLOWED_PRIORITIES[priority]}'.")

    # Trade-offs & missing skills
    trade_offs = list(career.get("challenges", []))[:2]
    skills_to_learn = list(career.get("important_skills", []))[:4]
    starter_projects = list(career.get("suggested_beginner_projects", []))[:1]

    route_info = get_budget_adapted_route(career, budget)

    return {
        "career_id": career.get("id"),
        "title": career.get("title", "Career Pathway"),
        "slug": slug,
        "category": career.get("category", "General"),
        "short_description": career.get("short_description", ""),
        "match_score": match_percentage,
        "match_label": match_label,
        "matching_factors": {
            "work_style_score": round(ws_score, 1),
            "priority_score": round(pr_score, 1),
            "interest_score": round(interest_score, 1),
            "skills_score": round(skills_score, 1)
        },
        "reasons": reasons,
        "trade_offs": trade_offs,
        "missing_skills": skills_to_learn,
        "starter_project": starter_projects[0] if starter_projects else "Introductory exploratory project",
        "route_info": route_info,
        "regulated": bool(career.get("regulated", 0)),
        "educational_prerequisites": career.get("educational_requirements", "Formal degree or equivalent portfolio")
    }


def simulate_scenario(profile, db_path=None, top_n=3):
    """
    Executes a scenario simulation using real career records from SQLite.
    Returns ranked recommendations (top N) deterministically.
    """
    normalized = normalize_simulator_profile(profile)
    all_careers = get_all_careers(db_path=db_path)
    if not all_careers:
        return []

    scored = []
    for career in all_careers:
        rec = calculate_simulator_match(normalized, career)
        scored.append(rec)

    # Deterministic sort: descending by match_score, tie-break by career_id
    scored.sort(key=lambda x: (x["match_score"], -(x["career_id"] or 0)), reverse=True)

    results = scored[:max(1, min(top_n, len(scored)))]
    for idx, r in enumerate(results, start=1):
        r["rank"] = idx

    return results


def compare_scenarios(baseline_raw, alternative_raw, db_path=None):
    """
    Compares two scenarios (Baseline vs Alternative / What-If).
    Produces side-by-side career comparison, explains score shifts using
    actual attribute differences, and details budget learning-route trade-offs.
    """
    baseline_profile = normalize_simulator_profile(baseline_raw)
    alternative_profile = normalize_simulator_profile(alternative_raw)

    all_careers = get_all_careers(db_path=db_path)
    if not all_careers:
        return {
            "baseline_profile": baseline_profile,
            "alternative_profile": alternative_profile,
            "baseline_recommendations": [],
            "alternative_recommendations": [],
            "comparison": [],
            "explanations": ["No career pathways available in database."],
            "budget_route_changes": [],
            "disclaimer": DISCLAIMER_TEXT
        }

    # Calculate scores for both scenarios across all careers
    baseline_all = [calculate_simulator_match(baseline_profile, c) for c in all_careers]
    alternative_all = [calculate_simulator_match(alternative_profile, c) for c in all_careers]

    # Deterministic sort
    baseline_all.sort(key=lambda x: (x["match_score"], -(x["career_id"] or 0)), reverse=True)
    alternative_all.sort(key=lambda x: (x["match_score"], -(x["career_id"] or 0)), reverse=True)

    for idx, r in enumerate(baseline_all, start=1):
        r["rank"] = idx
    for idx, r in enumerate(alternative_all, start=1):
        r["rank"] = idx

    baseline_top3 = baseline_all[:3]
    alternative_top3 = alternative_all[:3]

    base_map = {r["career_id"]: r for r in baseline_all}
    alt_map = {r["career_id"]: r for r in alternative_all}

    base_top3_ids = {r["career_id"] for r in baseline_top3}
    alt_top3_ids = {r["career_id"] for r in alternative_top3}
    union_top_ids = sorted(list(base_top3_ids.union(alt_top3_ids)))

    # Detect attribute changes
    ws_changed = baseline_profile["work_style"] != alternative_profile["work_style"]
    pr_changed = baseline_profile["priority"] != alternative_profile["priority"]
    bd_changed = baseline_profile["education_budget"] != alternative_profile["education_budget"]

    overall_explanations = []
    if ws_changed:
        overall_explanations.append(
            f"Work Style Shift: You transitioned from '{baseline_profile['work_style_label']}' to '{alternative_profile['work_style_label']}'. "
            f"Pathways demanding this work style gained ranking compatibility."
        )
    if pr_changed:
        overall_explanations.append(
            f"Career Priority Shift: Your focus changed from '{baseline_profile['priority_label']}' to '{alternative_profile['priority_label']}'. "
            f"Roles offering direct alignment with this priority moved up in suitability."
        )
    if bd_changed:
        overall_explanations.append(
            f"Education Budget Shift: Your budget shifted from '{baseline_profile['education_budget_label']}' to '{alternative_profile['education_budget_label']}'. "
            f"Intrinsic compatibility scores were preserved, but learning routes and funding feasibility adapted accordingly."
        )
    if not (ws_changed or pr_changed or bd_changed):
        overall_explanations.append(
            "Identical Scenarios: The baseline and what-if parameters are identical. Scores and rankings remain completely stable."
        )

    # Build side-by-side comparison items
    comparison_items = []
    for cid in union_top_ids:
        b_rec = base_map[cid]
        a_rec = alt_map[cid]

        b_score = b_rec["match_score"]
        a_score = a_rec["match_score"]
        diff = round(a_score - b_score, 1)

        in_base = cid in base_top3_ids
        in_alt = cid in alt_top3_ids

        if in_base and in_alt:
            status = "remained"
            status_label = "Maintained in Top 3"
        elif in_alt and not in_base:
            status = "entered"
            status_label = "Entered Top 3"
        else:
            status = "left"
            status_label = "Left Top 3"

        is_close = abs(diff) <= 2.0

        # Detailed change explanation for this specific career
        reasons_list = []
        if diff > 0.0:
            reasons_list.append(f"Compatibility increased by +{diff}% due to stronger alignment with updated preferences.")
        elif diff < 0.0:
            reasons_list.append(f"Compatibility decreased by {diff}% as other fields align more strongly with the updated criteria.")
        else:
            reasons_list.append("Intrinsic compatibility score remained unchanged.")

        if is_close and (ws_changed or pr_changed):
            reasons_list.append("Note: The score difference is small; this career remains similarly compatible.")

        if bd_changed:
            reasons_list.append(
                f"Budget changed to '{alternative_profile['education_budget_label']}': {a_rec['route_info']['suggested_route']}."
            )

        comparison_items.append({
            "career_id": cid,
            "title": a_rec["title"],
            "slug": a_rec["slug"],
            "category": a_rec["category"],
            "baseline_score": b_score,
            "baseline_label": b_rec["match_label"],
            "baseline_rank": b_rec["rank"],
            "alternative_score": a_score,
            "alternative_label": a_rec["match_label"],
            "alternative_rank": a_rec["rank"],
            "score_difference": diff,
            "status": status,
            "status_label": status_label,
            "is_close": is_close,
            "change_explanation": " ".join(reasons_list),
            "skills_to_consider": a_rec["missing_skills"],
            "educational_prerequisites": a_rec["educational_prerequisites"],
            "baseline_route": b_rec["route_info"],
            "alternative_route": a_rec["route_info"]
        })

    # Sort comparison items by alternative score descending
    comparison_items.sort(key=lambda x: x["alternative_score"], reverse=True)

    # Budget route changes summary
    budget_route_changes = []
    if bd_changed:
        for item in comparison_items[:3]:
            budget_route_changes.append({
                "career_title": item["title"],
                "baseline_route": item["baseline_route"]["suggested_route"],
                "alternative_route": item["alternative_route"]["suggested_route"],
                "cost_notes": item["alternative_route"]["cost_notes"],
                "feasibility": item["alternative_route"]["feasibility"]
            })

    return {
        "baseline_profile": baseline_profile,
        "alternative_profile": alternative_profile,
        "baseline_recommendations": baseline_top3,
        "alternative_recommendations": alternative_top3,
        "comparison": comparison_items,
        "explanations": overall_explanations,
        "budget_route_changes": budget_route_changes,
        "disclaimer": DISCLAIMER_TEXT
    }
