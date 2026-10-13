"""
CareerCompass - Multi-AI Service Layer
Supports Google Gemini and ChatGPT (OpenAI) using official Python SDKs:
- google-genai (official Google Gen AI SDK)
- openai (official OpenAI SDK)
Features safe request validation, normalized responses, CareerCompass ethical guidance,
and career action chips navigation.
"""

import os
import re
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dotenv import load_dotenv

logger = logging.getLogger("careercompass.ai")

# ---------------------------------------------------------------------------
# Environment Variable Loader (.env)
# ---------------------------------------------------------------------------
def load_env_file():
    """Loads environment variables from .env located at project root or parent."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base_dir, ".env"),
        os.path.join(base_dir, "..", ".env"),
        ".env"
    ]
    for candidate in candidates:
        if os.path.isfile(candidate):
            try:
                load_dotenv(dotenv_path=candidate, override=True)
                break
            except Exception as e:
                logger.warning("Failed to parse .env file at %s: %s", candidate, e)
    load_dotenv(override=False)

load_env_file()

# ---------------------------------------------------------------------------
# Provider Registry & Model Configurations (Gemini & OpenAI only)
# ---------------------------------------------------------------------------
def get_providers_config() -> Dict[str, Any]:
    """Returns dynamic provider configuration with environment model overrides."""
    load_env_file()
    gemini_default_model = os.environ.get("GEMINI_MODEL", "gemini-flash-latest").strip() or "gemini-flash-latest"
    openai_default_model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"

    # Build OpenAI model list, ensuring server-configured model is included
    openai_models = [
    {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "default": True},
    {"id": "gpt-4o", "name": "GPT-4o", "default": False}
]
    if openai_default_model not in [m["id"] for m in openai_models]:
        openai_models.insert(0, {
            "id": openai_default_model,
            "name": f"{openai_default_model} (Configured Model)",
            "default": True
        })

    gemini_models = [
        {"id": "gemini-flash-latest", "name": "Gemini Flash (Latest)", "default": True},
        {"id": "gemini-2.5-flash", "name": "Gemini 2.5 Flash", "default": False}
    ]

    openai_models = [
        {"id": "gpt-4o-mini", "name": "GPT-4o Mini (Fast & Affordable)", "default": True},
        {"id": "gpt-4o", "name": "GPT-4o (High Intelligence)", "default": False}
    ]

    if gemini_default_model not in [m["id"] for m in gemini_models]:
        gemini_models.insert(0, {
            "id": gemini_default_model,
            "name": f"{gemini_default_model} (Configured Model)",
            "default": True
        })

    return {
        "gemini": {
            "id": "gemini",
            "name": "Google Gemini",
            "env_key": "GEMINI_API_KEY",
            "icon": "✨",
            "badge_color": "blue",
            "description": "Google's high-speed multimodal frontier model specialized in STEM, analysis & education.",
            "default_model": gemini_default_model,
            "models": gemini_models
        },
        "openai": {
            "id": "openai",
            "name": "ChatGPT (OpenAI)",
            "env_key": "OPENAI_API_KEY",
            "icon": "🧠",
            "badge_color": "navy",
            "description": "Official OpenAI GPT models for structured planning, synthesis, and nuanced guidance.",
            "default_model": openai_default_model,
            "models": openai_models
        }
    }

PROVIDERS_CONFIG = get_providers_config()

# ---------------------------------------------------------------------------
# CareerCompass Ethical System Prompt
# ---------------------------------------------------------------------------
CAREERCOMPASS_SYSTEM_INSTRUCTION = """You are CareerCompass AI, an ethical, supportive, and practical career advisor for students and parents.
Your mission is to empower informed, realistic career exploration and educational planning.

CORE ADVISORY PRINCIPLES:
1. EXPLORE MULTIPLE PATHWAYS: Never prescribe just one single 'perfect' career. Provide 2-3 suitable alternative pathways and compare their practical trade-offs.
2. EXPLAIN WHY: Clearly explain why a pathway suits the student's stated interests, natural strengths, or constraints.
3. IDENTIFY MISSING SKILLS & ACTIONS: Highlight realistic skill gaps and suggest concrete next steps (e.g., specific beginner projects, foundational textbooks, free verified platforms like NPTEL, Coursera, freeCodeCamp, official documentation).
4. RESPECT REGULATED REQUIREMENTS: When discussing professions requiring statutory licensing (such as Pharmacy under PCI, Medicine under NMC, Law under BCI, Architecture under COA, or Chartered Accountancy under ICAI), clearly note the mandatory degrees and qualifying exams.
5. RESPECT BUDGET & CONSTRAINTS: Be mindful of tuition costs and family circumstances. Highlight affordable alternatives, government colleges, and self-learning pathways when budget is sensitive.
6. NO FALSE PROMISES: Never guarantee employment, campus placements, starting salaries, or college admissions. Distinguish verified structural facts from general guidance.
7. ENCOURAGE COLLABORATION: Encourage students to discuss significant decisions with parents, teachers, and verified human career counselors.
8. ETHICAL TRANSPARENCY: State clearly that you are an AI guidance tool providing educational recommendations, not a licensed therapist or certified career examiner.

RESPONSE STRUCTURE (for career planning inquiries):
- Goal & Overview: Short empathetic summary.
- Pathways & Fit: 2-3 practical career routes and why they align.
- Skills & Qualifications: Key degrees, statutory requirements, and practical tools.
- Practical Trade-offs: Costs, timeline, work-life aspects, and uncertainties.
- Next Steps: Immediate actionable milestones for this week/month.

Keep responses readable, well-structured, encouraging, and free of unnecessary jargon."""


def get_providers_info() -> List[Dict[str, Any]]:
    """
    Returns public metadata and honest live configuration status for Gemini and OpenAI.
    Never exposes API keys or secrets.
    """
    providers_cfg = get_providers_config()
    result = []
    for pid, pdata in providers_cfg.items():
        key_val = os.environ.get(pdata["env_key"], "").strip()
        is_configured = bool(key_val)
        status = "configured" if is_configured else "not_configured"
        status_label = "Configured" if is_configured else "Not Configured"

        result.append({
            "id": pdata["id"],
            "name": pdata["name"],
            "icon": pdata["icon"],
            "badge_color": pdata["badge_color"],
            "description": pdata["description"],
            "is_configured": is_configured,
            "status": status,
            "status_label": status_label,
            "default_model": pdata["default_model"],
            "models": pdata["models"]
        })
    return result


def validate_chat_request(
    provider_id: str,
    model_id: str,
    messages: List[Dict[str, str]],
    max_history: int = 12
) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
    """
    Validates provider (gemini or openai), model allowlist, message format, length, and history limits.
    Returns (is_valid, error_message, validated_payload).
    """
    providers_cfg = get_providers_config()
    if not provider_id or provider_id not in providers_cfg:
        allowed = ", ".join(providers_cfg.keys())
        return False, f"Invalid AI provider '{provider_id}'. Supported: {allowed}.", None

    pconfig = providers_cfg[provider_id]
    allowed_models = [m["id"] for m in pconfig["models"]]

    if not model_id or model_id not in allowed_models:
        model_id = pconfig["default_model"]

    if not isinstance(messages, list) or len(messages) == 0:
        return False, "Message list cannot be empty.", None

    if len(messages) > max_history:
        messages = messages[-max_history:]

    cleaned_messages = []
    for idx, msg in enumerate(messages):
        if not isinstance(msg, dict):
            return False, f"Message #{idx} must be an object with 'role' and 'content'.", None
        
        role = msg.get("role", "").strip().lower()
        if role not in ["user", "assistant", "system"]:
            return False, f"Invalid message role '{role}' in message #{idx}.", None
        
        content = msg.get("content", "")
        if not isinstance(content, str):
            return False, f"Message content #{idx} must be a string.", None
        
        content = content.strip()
        if not content and idx == len(messages) - 1:
            return False, "The latest user message cannot be empty.", None
        
        if len(content) > 2500:
            return False, "Message exceeds maximum allowed length of 2,500 characters. Please shorten your question.", None
        
        cleaned_messages.append({"role": role, "content": content})

    return True, None, {
        "provider_id": provider_id,
        "model_id": model_id,
        "messages": cleaned_messages
    }


def build_system_prompt_with_profile(user_profile: Optional[Dict[str, Any]] = None) -> str:
    """Appends opt-in student profile context to the system prompt if provided."""
    if not user_profile or not isinstance(user_profile, dict):
        return CAREERCOMPASS_SYSTEM_INSTRUCTION

    edu_level = user_profile.get("education_level", "")
    stream = user_profile.get("current_stream", "")
    budget = user_profile.get("budget_range", "")
    work_style = user_profile.get("work_style", "")
    interests = user_profile.get("interests", [])
    strengths = user_profile.get("strengths", [])
    target_career = user_profile.get("target_career", "")

    profile_parts = ["\n\n--- OPTIONAL STUDENT CONTEXT (USER OPTED-IN) ---"]
    if edu_level:
        profile_parts.append(f"Current Education Stage: {edu_level}")
    if stream:
        profile_parts.append(f"Current Academic Stream: {stream}")
    if budget:
        profile_parts.append(f"Budget Preference: {budget}")
    if work_style:
        profile_parts.append(f"Preferred Work Style: {work_style}")
    if target_career:
        profile_parts.append(f"Interested Career Path: {target_career}")
    if interests:
        if isinstance(interests, list):
            profile_parts.append(f"Key Interests: {', '.join(interests[:6])}")
        else:
            profile_parts.append(f"Key Interests: {interests}")
    if strengths:
        if isinstance(strengths, list):
            profile_parts.append(f"Natural Strengths: {', '.join(strengths[:6])}")
        else:
            profile_parts.append(f"Natural Strengths: {strengths}")

    profile_parts.append("Use this background to tailor pathway suggestions to the student's context.")
    return CAREERCOMPASS_SYSTEM_INSTRUCTION + "\n".join(profile_parts)


# ---------------------------------------------------------------------------
# Official SDK Adapters (Google Gen AI SDK & OpenAI SDK)
# ---------------------------------------------------------------------------

def call_gemini(model: str, messages: List[Dict[str, str]], system_prompt: str, api_key: str) -> str:
    """
    Calls Google Gemini using the official Google Gen AI Python SDK (google-genai).
    Sends conversation history and returns the generated text.
    """
    try:
        from google import genai
        from google.genai import types, errors
    except ImportError as e:
        logger.error("google-genai SDK not installed: %s", e)
        raise RuntimeError("Google Gen AI Python SDK (google-genai) is not installed on the server.")

    client = genai.Client(api_key=api_key)

    contents = []
    for m in messages:
        if m["role"] == "system":
            continue
        g_role = "user" if m["role"] == "user" else "model"
        contents.append(
            types.Content(
                role=g_role,
                parts=[types.Part.from_text(text=m["content"])]
            )
        )

    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.7,
        max_output_tokens=1024,
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=config
        )
        if not response or not response.text:
            raise ValueError("Google Gemini returned an empty response. Please rephrase your question.")
        return response.text.strip()
    except errors.APIError as e:
        status_code = getattr(e, "code", 500)
        msg = getattr(e, "message", str(e))
        logger.warning("Google Gemini APIError (Status %s): %s", status_code, msg[:200])
        if status_code in (401, 403) or "API_KEY_INVALID" in msg or "PERMISSION_DENIED" in msg:
            raise PermissionError("Authentication failed for Google Gemini. Please verify that GEMINI_API_KEY is valid.")
        elif status_code == 429 or "RESOURCE_EXHAUSTED" in msg:
            raise RuntimeError("Google Gemini quota or rate limit exceeded. Please wait a minute or check your account quota.")
        elif status_code == 404 or "NOT_FOUND" in msg:
            raise ValueError(f"Google Gemini model '{model}' was not found. Please choose an active supported model.")
        elif status_code >= 500:
            raise ConnectionError("Google Gemini servers are temporarily experiencing issues. Please try again shortly.")
        else:
            clean_hint = f" ({msg[:120]})" if msg else ""
            raise RuntimeError(f"Google Gemini request failed{clean_hint}.")
    except Exception as e:
        logger.warning("Google Gemini error: %s", e)
        if isinstance(e, (PermissionError, RuntimeError, ValueError, ConnectionError)):
            raise
        raise RuntimeError(f"Google Gemini request failed: {str(e)[:150]}")


def call_openai(model: str, messages: List[Dict[str, str]], system_prompt: str, api_key: str) -> str:
    """
    Calls ChatGPT / OpenAI using the official OpenAI Python SDK.
    Sends conversation history and returns the generated text.
    """
    try:
        from openai import OpenAI, AuthenticationError, RateLimitError, APIConnectionError, APIStatusError, NotFoundError
    except ImportError as e:
        logger.error("openai SDK not installed: %s", e)
        raise RuntimeError("OpenAI Python SDK (openai) is not installed on the server.")

    client = OpenAI(api_key=api_key)

    o_messages = [{"role": "system", "content": system_prompt}]
    for m in messages:
        if m["role"] != "system":
            o_messages.append({"role": m["role"], "content": m["content"]})

    try:
        response = client.chat.completions.create(
            model=model,
            messages=o_messages,
            temperature=0.7,
            max_tokens=1024
        )
        if not response.choices or not response.choices[0].message or not response.choices[0].message.content:
            raise ValueError("ChatGPT (OpenAI) returned an empty response. Please retry with a revised query.")
        return response.choices[0].message.content.strip()
    except AuthenticationError as e:
        logger.warning("OpenAI AuthenticationError: %s", e)
        raise PermissionError("OpenAI authentication failed: The provided OPENAI_API_KEY is invalid or expired. Please check your credentials.")
    except RateLimitError as e:
        logger.warning("OpenAI RateLimitError: %s", e)
        err_msg = str(e).lower()
        if "quota" in err_msg or "insufficient_quota" in err_msg or "billing" in err_msg:
            raise RuntimeError("OpenAI quota exceeded or insufficient credit. Please check your OpenAI account billing and usage limits.")
        raise RuntimeError("OpenAI rate limit reached. The service is experiencing high demand. Please wait a moment before retrying.")
    except NotFoundError as e:
        logger.warning("OpenAI NotFoundError: %s", e)
        raise ValueError(f"The requested OpenAI model '{model}' was not found or is not accessible with your API key. Please select a supported model such as gpt-4o-mini.")
    except APIConnectionError as e:
        logger.warning("OpenAI APIConnectionError: %s", e)
        raise ConnectionError("Network error connecting to OpenAI API. Please check your internet connection or retry shortly.")
    except APIStatusError as e:
        logger.warning("OpenAI APIStatusError (Status %s): %s", e.status_code, e.message)
        if e.status_code >= 500:
            raise ConnectionError("OpenAI servers are temporarily unavailable. Please try again shortly.")
        raise RuntimeError(f"OpenAI request failed: {e.message[:150]}")
    except Exception as e:
        logger.warning("OpenAI error: %s", e)
        if isinstance(e, (PermissionError, RuntimeError, ValueError, ConnectionError)):
            raise
        raise RuntimeError(f"OpenAI request failed: {str(e)[:150]}")


# ---------------------------------------------------------------------------
# Career Action Buttons Extraction
# ---------------------------------------------------------------------------
def extract_career_action_chips(text: str, careers_catalog: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Scans the AI response text for mentions of verified CareerCompass catalog careers
    and generates safe navigation action chips (links to career details, roadmap, simulator).
    """
    if not text or not careers_catalog:
        return []

    found_careers = []
    text_lower = text.lower()

    for c in careers_catalog:
        title = c.get("title", "")
        slug = c.get("slug", "")
        if not title:
            continue
        
        pattern = r"\b" + re.escape(title.lower()) + r"\b"
        if re.search(pattern, text_lower):
            found_careers.append(c)
            if len(found_careers) >= 3:
                break

    actions = []
    for c in found_careers:
        actions.append({
            "type": "career_detail",
            "label": f"Explore {c['title']}",
            "url": f"/careers/{c['slug']}",
            "icon": "🧭"
        })
        actions.append({
            "type": "roadmap",
            "label": f"Snake Roadmap: {c['title']}",
            "url": f"/roadmap?career={c['slug']}",
            "icon": "🗺️"
        })

    if "interview" in text_lower or "counsellor" in text_lower or "guidance" in text_lower:
        actions.append({
            "type": "appointment",
            "label": "Book Live Guidance Appointment",
            "url": "/appointments",
            "icon": "📅"
        })

    if "budget" in text_lower or "simulator" in text_lower or "cost" in text_lower:
        actions.append({
            "type": "simulator",
            "label": "Run Career Reality Simulator",
            "url": "/simulator",
            "icon": "⚖️"
        })

    unique_actions = []
    seen_urls = set()
    for a in actions:
        if a["url"] not in seen_urls:
            seen_urls.add(a["url"])
            unique_actions.append(a)
            if len(unique_actions) >= 4:
                break

    return unique_actions


# ---------------------------------------------------------------------------
# Main AI Dispatcher
# ---------------------------------------------------------------------------
def call_ai_provider(
    provider_id: str,
    model_id: str,
    messages: List[Dict[str, str]],
    user_profile: Optional[Dict[str, Any]] = None,
    careers_catalog: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Main entry point for AI chat.
    Validates credentials, calls the provider SDK, normalizes response,
    and attaches career action chips.
    """
    load_env_file()
    providers_cfg = get_providers_config()

    if provider_id not in providers_cfg:
        allowed = ", ".join(providers_cfg.keys())
        raise ValueError(f"Invalid AI provider '{provider_id}'. Supported: {allowed}.")

    pconfig = providers_cfg[provider_id]
    api_key = os.environ.get(pconfig["env_key"], "").strip()

    # Check for Mock / Test mode for automated unit testing without live credentials
    if os.environ.get("AI_TEST_MODE") == "1" or api_key.startswith("test-mock-key"):
        model_name = model_id or pconfig["default_model"]
        query_text = messages[-1]["content"] if messages else "guidance"
        mock_response = (
            f"[Verified {pconfig['name']} ({model_name}) Career Guidance]\n\n"
            f"Based on your query '{query_text}', here are two realistic pathways:\n"
            "1. **Software & Applied Computing**: Focus on core Python, data structures, and web architecture. Strong alignment with analytical skills.\n"
            "2. **Cybersecurity Analyst**: Focus on networking, Linux fundamentals, and cryptography.\n\n"
            "**Recommended Next Actions**: Build a hands-on project and schedule a consultation with a mentor."
        )
        action_chips = extract_career_action_chips(mock_response, careers_catalog or [])
        return {
            "provider": provider_id,
            "provider_name": pconfig["name"],
            "model": model_name,
            "content": mock_response,
            "action_chips": action_chips,
            "is_mock": True
        }

    if not api_key:
        raise PermissionError(
            f"Provider '{pconfig['name']}' is not configured yet. Please add {pconfig['env_key']} to your environment variables or local .env file."
        )

    system_prompt = build_system_prompt_with_profile(user_profile)
    active_model = model_id or pconfig["default_model"]

    if provider_id == "gemini":
        response_text = call_gemini(active_model, messages, system_prompt, api_key)
    elif provider_id == "openai":
        response_text = call_openai(active_model, messages, system_prompt, api_key)
    else:
        raise ValueError(f"Unhandled provider: {provider_id}")

    action_chips = extract_career_action_chips(response_text, careers_catalog or [])

    return {
        "provider": provider_id,
        "provider_name": pconfig["name"],
        "model": active_model,
        "content": response_text,
        "action_chips": action_chips,
        "is_mock": False
    }


# ---------------------------------------------------------------------------
# Multilingual Parent Voice Canvass System Prompt & Dispatcher
# ---------------------------------------------------------------------------

PARENT_GUIDE_LANGUAGES = {
    "te": {"name": "Telugu", "native": "తెలుగు", "code": "te-IN"},
    "hi": {"name": "Hindi", "native": "हिन्दी", "code": "hi-IN"},
    "en": {"name": "English", "native": "English", "code": "en-IN"}
}


def build_parent_career_guide_prompt(language: str, student_profile: Dict[str, Any]) -> str:
    """
    Constructs a respectful, culturally empathetic system instruction for parents,
    strictly conditioned on verified student inputs from the Bridge interface.
    """
    lang_info = PARENT_GUIDE_LANGUAGES.get(language, PARENT_GUIDE_LANGUAGES["en"])
    lang_name = lang_info["name"]
    lang_native = lang_info["native"]

    preferred_career = (student_profile.get("preferred_career") or "").strip() or "Selected Career"
    reasons = (student_profile.get("reasons") or "").strip()
    goals = student_profile.get("goals", [])
    goals_str = ", ".join(goals) if isinstance(goals, list) else str(goals or "")
    
    parent_concerns = student_profile.get("parent_concerns", [])
    concerns_str = ", ".join(parent_concerns) if isinstance(parent_concerns, list) else str(parent_concerns or "")

    alternative_career = (student_profile.get("alternative_career") or "").strip()
    alternative_reasons = (student_profile.get("alternative_reasons") or "").strip()
    shared_next_step = (student_profile.get("shared_next_step") or "").strip()
    edu_level = (student_profile.get("education_level") or "").strip()
    budget = (student_profile.get("budget_limit") or "").strip()
    interests = student_profile.get("interests", [])
    strengths = student_profile.get("strengths", [])
    education_pathway = (student_profile.get("education_pathway") or "").strip()
    required_skills = student_profile.get("required_skills", [])
    estimated_costs = (student_profile.get("estimated_costs") or "").strip()
    challenges = student_profile.get("challenges", [])

    profile_text = [
        "STUDENT VERIFIED BRIDGE PROFILE:",
        f"- Student Chosen Career: {preferred_career}",
    ]
    if reasons:
        profile_text.append(f"- Student Excited Reasons: {reasons}")
    if goals_str:
        profile_text.append(f"- Student Goals & Priorities: {goals_str}")
    if concerns_str:
        profile_text.append(f"- Practical Parent Concerns Noted: {concerns_str}")
    if alternative_career:
        profile_text.append(f"- Parent Alternative Option: {alternative_career} ({alternative_reasons})")
    if shared_next_step:
        profile_text.append(f"- Agreed Next Step: {shared_next_step}")
    if edu_level:
        profile_text.append(f"- Education Stage: {edu_level}")
    if budget:
        profile_text.append(f"- Family Budget Context: {budget}")
    if interests:
        profile_text.append(f"- Stated Interests: {interests if isinstance(interests, str) else ', '.join(interests[:5])}")
    if strengths:
        profile_text.append(f"- Stated Strengths: {strengths if isinstance(strengths, str) else ', '.join(strengths[:5])}")
    if education_pathway:
        profile_text.append(f"- Education Pathway: {education_pathway}")
    if required_skills:
        skills_str = ", ".join(required_skills) if isinstance(required_skills, list) else str(required_skills)
        profile_text.append(f"- Required Skills: {skills_str}")
    if estimated_costs:
        profile_text.append(f"- Estimated Costs: {estimated_costs}")
    if challenges:
        chal_str = ", ".join(challenges) if isinstance(challenges, list) else str(challenges)
        profile_text.append(f"- Challenges & Realities: {chal_str}")

    prompt = f"""You are the CareerCompass AI Parent Career Guide (తల్లిదండ్రుల మార్గదర్శి / अभिभावक करियर गाइड).
Your role is to explain the student's career aspirations respectfully, honestly, and empathetically to their parents.

{chr(10).join(profile_text)}

CRITICAL ETHICAL & BEHAVIORAL DIRECTIVES:
1. RESPECTFUL & EMPATHETIC TONE: Address the parents with utmost dignity and warmth (use culturally respectful greetings such as 'నమస్కారం' in Telugu, 'नमस्ते' in Hindi, and polite respectful warmth in English).
2. ACCURATE TO STUDENT PROFILE: Base your explanation ONLY on the student's actual reported information above. Do NOT assume or invent unmentioned achievements, talents, or passions.
3. BALANCED & OBJECTIVE: Explain the required degrees, entrance requirements, skill learning curve, and estimated training timeline clearly.
4. ADDRESS PARENT CONCERNS: Validate worries about employment stability, education loans/tuition, and qualification recognition. Highlight affordable alternatives such as government colleges, state universities, vocational certifications, and merit scholarships.
5. NO EMOTIONAL PRESSURE OR MANIPULATION: Never shame or judge parents for wanting financial security. Never guarantee job placement, salary numbers, college admission, or future success.
6. TECHNICAL CAREER NAMES: Keep technical career names recognizable to parents (when helpful, show the original English career name alongside the translation, e.g. 'సివిల్ ఇంజనీరింగ్ (Civil Engineering)').
7. COLLABORATIVE NEXT STEP: Encourage the family to explore a low-risk next step together (e.g., a 3-week beginner micro-project, checking state scholarship portals, or talking to a practicing professional).

LANGUAGE & SCRIPT INSTRUCTIONS:
- Target Language: {lang_name} ({lang_native}).
- You MUST generate your ENTIRE response in {lang_name}.
- For Telugu ({lang_native}): Write in natural, fluent Telugu script (తెలుగు లిపి). Do NOT use English script.
- For Hindi ({lang_native}): Write in natural, fluent Hindi script (देवनागरी लिपि).
- For English: Write in warm, clear Indian English accessible to parents.
- Keep sentences clear, well-spaced, and natural for text-to-speech audio playback.

If this is the initial opening explanation:
- Respectfully greet the parents.
- Mention the career ({preferred_career}) and the reasons their child expressed excitement about it.
- Connect their child's expressed interests/strengths to what this career really involves.
- Explain the realistic educational path and qualification requirements.
- Directly discuss practical family considerations (costs, stability, alternatives).
- Recommend one concrete, low-risk step the family can try together this week.
- Warmly invite the parents to ask any question or share any worry.
"""
    return prompt


def call_parent_career_guide(
    language: str,
    student_profile: Dict[str, Any],
    message: str = "",
    history: Optional[List[Dict[str, str]]] = None,
    preferred_provider: Optional[str] = None
) -> Dict[str, Any]:
    """
    Executes multilingual parent voice career guidance via configured Gemini or OpenAI models.
    Supports Telugu ('te'), Hindi ('hi'), and English ('en').
    """
    load_env_file()
    lang = (language or "en").strip().lower()
    if lang not in PARENT_GUIDE_LANGUAGES:
        raise ValueError(f"Unsupported language '{language}'. Supported languages: {', '.join(PARENT_GUIDE_LANGUAGES.keys())}.")

    if not isinstance(student_profile, dict):
        student_profile = {}

    system_prompt = build_parent_career_guide_prompt(lang, student_profile)
    preferred_career = (student_profile.get("preferred_career") or "their selected pathway").strip()

    providers_cfg = get_providers_config()
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    openai_key = os.environ.get("OPENAI_API_KEY", "").strip()

    # Check Test / Mock Mode
    is_test_mode = os.environ.get("AI_TEST_MODE") == "1" or gemini_key.startswith("test-mock") or openai_key.startswith("test-mock")

    if is_test_mode:
        if lang == "te":
            if not message:
                reply = (
                    f"నమస్కారం! కెరీర్‌కంపాస్ తల్లిదండ్రుల మార్గదర్శికి స్వాగతం.\n\n"
                    f"మీ పిల్లలు **{preferred_career}** రంగాన్ని తమ కెరీర్‌గా ఎంచుకోవడానికి ఎంతో ఆసక్తి చూపుతున్నారు. "
                    f"వారు తెలిపిన ఆసక్తులు మరియు లక్ష్యాల ఆధారంగా, ఈ రంగంలో ముందుకు సాగడానికి అవసరమైన ముఖ్యమైన అంశాలు ఇక్కడ ఉన్నాయి:\n\n"
                    f"1. **విద్య మరియు శిక్షణ**: ఈ రంగానికి సంబంధిత గుర్తింపు పొందిన డిగ్రీ లేదా డిప్లొమా, అలాగే ప్రాక్టికల్ ప్రాజెక్ట్‌లు ఎంతో ముఖ్యం.\n"
                    f"2. **ఆచరణాత్మక అంశాలు**: ఫీజులు, ప్రభుత్వ కళాశాలలు మరియు స్కాలర్‌షిప్‌ల అవకాశాలను పరిశీలించడం ద్వారా కుటుంబ బడ్జెట్‌ను సమతుల్యం చేసుకోవచ్చు.\n"
                    f"3. **ఉమ్మడి తదుపరి అడుగు**: ఒక చిన్న 3-వారాల ప్రాథమిక ప్రాజెక్ట్ లేదా అనుభవజ్ఞుడైన మెంటార్‌తో సంభాషణ ద్వారా నిజమైన ఆసక్తిని పరీక్షించవచ్చు.\n\n"
                    f"మీకు ఫీజులు, ఉద్యోగ స్థిరత్వం లేదా ఇతర ప్రత్యామ్నాయాల గురించి ఏవైనా సందేహాలు ఉంటే దయచేసి అడగండి!"
                )
            else:
                reply = (
                    f"నమస్కారం అండి. మీ ప్రశ్న: '{message}'.\n\n"
                    f"**{preferred_career}** రంగానికి సంబంధించి ఇది ఎంతో ముఖ్యమైన ఆలోచన. "
                    f"ప్రభుత్వ గుర్తింపు పొందిన కళాశాలలు మరియు స్కాలర్‌షిప్‌ల ద్వారా నాణ్యమైన విద్యను తక్కువ ఖర్చుతో పొందవచ్చు. "
                    f"అదే సమయంలో ప్రాక్టికల్ నైపుణ్యాలు పెంచుకోవడం ద్వారా కెరీర్‌లో స్థిరత్వాన్ని సాధించవచ్చు."
                )
        elif lang == "hi":
            if not message:
                reply = (
                    f"नमस्ते! करियरकम्पास अभिभावक करियर गाइड में आपका स्वागत है।\n\n"
                    f"आपके बच्चे ने **{preferred_career}** करियर में अपनी गहरी रुचि दिखाई है। "
                    f"उनके द्वारा साझा की गई प्राथमिकताओं और लक्ष्यों के आधार पर, यह महत्वपूर्ण मार्गदर्शन आपके लिए है:\n\n"
                    f"1. **शिक्षा और योग्यता**: इस क्षेत्र में मान्यता प्राप्त डिग्री/डिप्लोमा और व्यावहारिक कौशल की आवश्यकता होती है।\n"
                    f"2. **व्यावहारिक विचार**: सरकारी संस्थानों और छात्रवृत्ति विकल्पों की जांच करके परिवार के बजट को संतुलित किया जा सकता है।\n"
                    f"3. **पारिवारिक अगला कदम**: इस सप्ताह एक बुनियादी परिचयात्मक प्रोजेक्ट या कार्यशाला साथ मिलकर देखें।\n\n"
                    f"क्या आपके मन में शिक्षा शुल्क, नौकरी की स्थिरता या किसी अन्य विकल्प को लेकर कोई प्रश्न है? कृपया पूछें!"
                )
            else:
                reply = (
                    f"नमस्ते जी। आपका सवाल: '{message}'.\n\n"
                    f"**{preferred_career}** के संदर्भ में यह एक बहुत ही समझदारी भरा सवाल है। "
                    f"मान्यता प्राप्त संस्थानों में प्रवेश और निरंतर अभ्यास से अच्छी नींव रखी जा सकती है। "
                    f"परिवार के बजट को ध्यान में रखते हुए सरकारी छात्रवृत्तियां एक बेहतरीन विकल्प हैं।"
                )
        else: # en
            if not message:
                reply = (
                    f"Warm greetings! Welcome to the CareerCompass Parent Career Guide.\n\n"
                    f"Your child has expressed strong excitement about pursuing **{preferred_career}**. "
                    f"Based on their personal excitement and shared priorities, here is a balanced overview for your family:\n\n"
                    f"1. **Educational Pathway**: Pursuing this path involves accredited degree or diploma studies along with hands-on skill practice.\n"
                    f"2. **Practical Considerations**: Managing educational expenses can be supported by exploring state institutions and merit scholarships.\n"
                    f"3. **Next Step Together**: Review a 3-week beginner micro-project together to test interest before making long-term commitments.\n\n"
                    f"Please feel free to ask questions about education costs, job stability, or alternative pathways!"
                )
            else:
                reply = (
                    f"Thank you for asking: '{message}'.\n\n"
                    f"Regarding **{preferred_career}**, this is an important consideration. "
                    f"Accredited universities and recognized certifications provide a steady foundation, while state scholarships help manage costs. "
                    f"We recommend exploring both standard and subsidized paths together as a family."
                )

        return {
            "success": True,
            "language": lang,
            "reply": reply,
            "provider": "mock",
            "model": "parent-voice-mock"
        }

    # Live Mode: require at least one provider credential
    if not gemini_key and not openai_key:
        raise PermissionError(
            "AI service credentials are required. Neither GEMINI_API_KEY nor OPENAI_API_KEY is configured in your server environment or .env file."
        )

    # Determine provider
    chosen_provider = "gemini" if gemini_key else "openai"
    if preferred_provider in ("gemini", "openai"):
        if preferred_provider == "gemini" and gemini_key:
            chosen_provider = "gemini"
        elif preferred_provider == "openai" and openai_key:
            chosen_provider = "openai"

    pconfig = providers_cfg[chosen_provider]
    active_model = pconfig["default_model"]
    api_key = gemini_key if chosen_provider == "gemini" else openai_key

    # Construct conversation history
    messages: List[Dict[str, str]] = []
    if history and isinstance(history, list):
        for h in history[-6:]:
            if isinstance(h, dict) and "role" in h and "content" in h:
                messages.append({"role": h["role"], "content": str(h["content"])[:2000]})

    lang_meta = PARENT_GUIDE_LANGUAGES[lang]
    if message:
        messages.append({"role": "user", "content": message[:2000]})
    else:
        messages.append({
            "role": "user",
            "content": f"Please provide the respectful, structured opening explanation for the parents regarding {preferred_career} in {lang_meta['name']} ({lang_meta['native']})."
        })

    if chosen_provider == "gemini":
        reply = call_gemini(active_model, messages, system_prompt, api_key)
    else:
        reply = call_openai(active_model, messages, system_prompt, api_key)

    return {
        "success": True,
        "language": lang,
        "reply": reply,
        "provider": chosen_provider,
        "model": active_model
    }

