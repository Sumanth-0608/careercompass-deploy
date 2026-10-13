# 🧭 CareerCompass

> **"Your future, your choice."**  
> *A full-stack, transparent, and explainable career guidance platform built for students and parents.*

---

## 🌟 Table of Contents
1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Architecture & Tech Stack](#architecture--tech-stack)
4. [Folder Structure](#folder-structure)
5. [Prerequisites](#prerequisites)
6. [Quickstart & Local Installation](#quickstart--local-installation)
   - [Windows (PowerShell / CMD)](#windows-setup)
   - [macOS / Linux](#macos--linux-setup)
7. [Running the Server & Accessing the App](#running-the-server)
8. [Running Automated Tests](#running-automated-tests)
9. [REST API Documentation](#rest-api-documentation)
10. [How the Transparent Matching Engine Works](#how-the-matching-engine-works)
11. [Student–Parent Career Bridge](#studentparent-career-bridge)
12. [Known Limitations & Ethical Disclaimers](#known-limitations--ethical-disclaimers)
13. [Troubleshooting Common Errors](#troubleshooting-common-errors)
14. [2-Minute Hackathon Demo Script](#2-minute-hackathon-demo-script)

---

## 1. Project Overview

Students frequently make high-stakes educational and career decisions influenced by peer pressure, family anxiety, coaching institute marketing, or incomplete career information. 

**CareerCompass** provides an objective, transparent, and empathetic alternative:
- **No Black-Box AI Hallucinations**: Uses an explainable, auditable 100-point rule-based matching engine that works completely offline.
- **Deep Reality Checks**: Details the day-to-day duties, trade-offs, licensure regulations, and real educational costs for 14+ pathways.
- **Equity-Focused**: Never eliminates a student from exploring a career due to a low budget; surfaces government colleges, open-source resources, and scholarship options.
- **Student–Parent Bridge**: Facilitates respectful, side-by-side family conversations with guided dinner-table discussion prompts.
- **Personalized Roadmaps**: 7-step actionable milestones with interactive progress tracking saved persistently in SQLite.

---

## 2. Key Features

- **Multi-Step Career Discovery Assessment**: 4-stage guided quiz evaluating education, streams, favorite subjects, interests, natural strengths, work style, and budget preferences.
- **Transparent Recommendation Engine**: Returns at least 3 ranked recommendations explaining *why* each matched, which skills the student already has, and which skills to build next.
- **Career Reality Simulator ("What-If" Explorer)**: Dynamic simulation answering "What if my budget changes?", "What if I switch from analytical to creative work?", and "What if my priority shifts from growth to stability?" with explainable score movements and budget-adapted learning routes.
- **14+ Verified Career Pathways**: Software Developer, Data Analyst, Cybersecurity Analyst, Electronics Engineer, Mechanical Engineer, UX/UI Designer, Graphic Designer, Healthcare Professional, Teacher/Educator, Business Analyst, Entrepreneur, Environmental Scientist, Clinical Psychologist, and Chartered Accountant.
- **Reality Check & Trade-offs**: Side-by-side advantages vs. challenges (e.g. screen fatigue, statutory exam pass rates, on-call shifts).
- **Personalized Action Roadmaps**: 7 milestones per career (prerequisites, foundations, hands-on practice, starter project, formal degrees, scholarships, progress review) with interactive checkbox persistence.
- **Student–Parent Career Bridge**: Compares the student's dream career against a parent's alternative, outlining costs, requirements, and guided family discussion questions.
- **Persistent Plans Dashboard**: Revisit saved roadmaps with real-time progress percentages retained across server reboots.

---

## 3. Architecture & Tech Stack

- **Frontend**: HTML5, Modern CSS3 (Navy Blue & Mint Green theme, responsive grid/flexbox, accessible contrast), Vanilla JavaScript (ES6+), Fetch API. Zero heavy node_modules or front-end build pipelines required.
- **Backend**: Python 3.10+, Flask 3.x, REST API, JSON serialization, server-side validation, HTTP status codes.
- **Database**: SQLite 3 (Python built-in `sqlite3`), `PRAGMA foreign_keys = ON;`, parameterized SQL queries, automatic schema migration and seed data loading.
- **Testing**: `pytest` test suite with 100% pass rate covering API routes, matching logic, edge cases, and SQLite persistence.

---

## 4. Folder Structure

```text
careercompass/
├── app.py                     # Flask application & REST API controllers
├── database.py                # SQLite database helper, migrations & 14 seed careers
├── recommender.py             # Rule-based transparent matching engine
├── schema.sql                 # Relational SQL schema definitions with foreign keys
├── requirements.txt           # Minimal Python dependencies (Flask, pytest)
├── .gitignore                 # Ignores __pycache__, .pytest_cache, instance/*.db
├── README.md                  # Comprehensive setup, API guide, and demo script
├── instance/
│   └── careercompass.db       # Persistent SQLite database (auto-created on startup)
├── templates/                 # Jinja2 HTML templates
│   ├── base.html              # Core layout (navbar, footer, toast notifications)
│   ├── index.html             # Landing page with hero & feature cards
│   ├── quiz.html              # Multi-step assessment with progress bar
│   ├── recommendations.html   # Ranked recommendations with match explanations
│   ├── careers.html           # Full career catalog with category filtering
│   ├── career_detail.html     # Reality checks, pros/cons, costs & citations
│   ├── roadmap.html           # Interactive 7-milestone roadmap checklist
│   ├── compare.html           # Student–Parent Career Bridge comparison
│   ├── plans.html             # Saved career plans dashboard
│   ├── about.html             # Platform mission, scoring formula & disclaimers
│   └── error.html             # Safe, user-friendly error page
├── static/
│   ├── css/
│   │   └── style.css          # Design system, accessible palette & responsive layouts
│   └── js/
│       ├── app.js             # Global utilities, toast alerts, HTML escaping
│       ├── quiz.js            # Multi-step form controller & validation
│       ├── recommendations.js # Client-side recommendations renderer
│       ├── roadmap.js         # Milestone checkbox PATCH handler & progress tracker
│       └── compare.js         # Side-by-side comparison bridge generator
└── tests/
    ├── test_api.py            # API route integration tests & SQLite persistence
    ├── test_recommender.py    # Unit tests for matching engine & profile distinctiveness
    └── test_demo_flow.py      # End-to-end 10-step hackathon demo acceptance test
```

---

## 5. Prerequisites

- **Python 3.10, 3.11, or 3.12+**
- **pip** (Python package installer)
- Modern web browser (Chrome, Edge, Firefox, Safari)
- No external paid APIs, no node.js, no Docker, and no cloud dependencies required.

---

## 6. Quickstart & Local Installation

### Windows Setup

1. Open PowerShell or Command Prompt.
2. Navigate to the project directory:
   ```powershell
   cd C:\Users\summa\.gemini\antigravity\scratch\careercompass
   ```
3. (Optional but recommended) Create and activate a Python virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   *If using Command Prompt (cmd.exe):*
   ```cmd
   .\venv\Scripts\activate.bat
   ```
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
5. Initialize the database (automatically seeds 14 careers):
   ```powershell
   python -c "from database import init_db; init_db()"
   ```

### macOS / Linux Setup

1. Open Terminal and navigate to the project directory:
   ```bash
   cd careercompass
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize the database:
   ```bash
   python3 -c "from database import init_db; init_db()"
   ```

---

## 7. Running the Server

Start the Flask application:

**Windows:**
```powershell
python app.py
```

**macOS / Linux:**
```bash
python3 app.py
```

You should see:
```text
Starting CareerCompass Web Application on http://127.0.0.1:5000
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 8. Running Automated Tests

Run the full automated test suite with pytest:

```powershell
pytest -v
```

Expected output:
```text
tests/test_api.py::test_health_check PASSED                              [  5%]
tests/test_api.py::test_careers_list_and_category_filter PASSED          [ 11%]
tests/test_api.py::test_career_details_valid_and_invalid PASSED          [ 17%]
tests/test_api.py::test_assessment_validation_failures PASSED            [ 23%]
tests/test_api.py::test_assessment_submission_and_recommendations PASSED [ 29%]
tests/test_api.py::test_recommendations_post_endpoint PASSED             [ 35%]
tests/test_api.py::test_career_roadmap_endpoint PASSED                   [ 41%]
tests/test_api.py::test_plan_lifecycle_and_milestone_patch PASSED        [ 47%]
tests/test_api.py::test_student_parent_comparison PASSED                 [ 52%]
tests/test_api.py::test_sqlite_persistence_after_reconnection PASSED     [ 58%]
tests/test_demo_flow.py::test_full_hackathon_demo_flow PASSED            [ 64%]
tests/test_recommender.py::test_tech_profile_recommendations PASSED      [ 70%]
tests/test_recommender.py::test_healthcare_profile_recommendations PASSED [ 76%]
tests/test_recommender.py::test_creative_design_profile_recommendations PASSED [ 82%]
tests/test_recommender.py::test_different_profiles_produce_different_rankings PASSED [ 88%]
tests/test_recommender.py::test_missing_skills_identification PASSED     [ 94%]
tests/test_recommender.py::test_low_budget_does_not_eliminate_careers PASSED [100%]

============================= 17 passed in 0.55s ==============================
```

---

## 9. REST API Documentation

All API responses return JSON with standardized status codes (`200`, `201`, `400`, `404`, `500`).

### 1. `GET /api/health`
- **Description**: Returns server and database health status.
- **Response `200`**:
  ```json
  {
    "status": "healthy",
    "service": "CareerCompass API",
    "version": "1.0.0",
    "database": "connected"
  }
  ```

### 2. `GET /api/careers`
- **Query Params**: `?category=<category_name>` (optional)
- **Description**: Returns catalog of careers.
- **Response `200`**:
  ```json
  {
    "success": true,
    "count": 14,
    "category_filter": null,
    "careers": [ ... ]
  }
  ```

### 3. `GET /api/careers/<id>`
- **Description**: Returns detailed specifications, reality check data, entrance exams, and source citations for a single career.
- **Response `200`** or `404` if not found.

### 4. `POST /api/assessments`
- **Description**: Validates and stores a student's assessment submission in SQLite, immediately computing recommendations.
- **Request Body**:
  ```json
  {
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
    "constraints": "Prefer self-paced study"
  }
  ```
- **Response `201`**:
  ```json
  {
    "success": true,
    "assessment_id": 1,
    "message": "Assessment recorded successfully.",
    "recommendations_count": 6
  }
  ```

### 5. `POST /api/recommendations`
- **Description**: Computes recommendations on-the-fly for a submitted profile, or fetches for an existing `assessment_id`.
- **Response `200`**:
  ```json
  {
    "success": true,
    "count": 6,
    "disclaimer": "CareerCompass match scores are reflective guidance...",
    "recommendations": [
      {
        "career_id": 1,
        "title": "Software Developer",
        "rank": 1,
        "match_score": 88.5,
        "match_reasons": ["Strongly aligns with your interest in technology, science."],
        "missing_skills": ["Data Structures & Algorithms", "SQL & Database Design"],
        "trade_offs": ["Fast-moving technology stack requiring lifelong self-directed learning"],
        "alternative_routes": ["Government polytechnics, SWAYAM/NPTEL, freeCodeCamp"]
      }
    ]
  }
  ```

### 6. `GET /api/assessments/<id>/recommendations`
- **Description**: Retrieves saved recommendations for an assessment record.

### 7. `GET /api/careers/<id>/roadmap`
- **Description**: Returns template roadmap containing 7 sequential learning milestones.

### 8. `POST /api/plans`
- **Description**: Saves an active career plan for a student, instantiating persistent milestone checklist items.
- **Request Body**:
  ```json
  {
    "career_id": 1,
    "student_name": "Aarav",
    "assessment_id": 1,
    "notes": "Targeting open source internships"
  }
  ```
- **Response `201`**: Returns `plan_id` and initial 0% progress.

### 9. `GET /api/plans/<id>`
- **Description**: Retrieves saved plan, list of milestones, and completion percentage.

### 10. `PATCH /api/plans/<id>/milestones/<milestone_id>`
- **Description**: Toggles milestone completion status (`is_completed: true/false`).
- **Request Body**: `{ "is_completed": true }`
- **Response `200`**: Returns updated `plan_progress` percentage.

### 11. `POST /api/comparisons`
- **Description**: Saves a Student–Parent Career Bridge entry comparing two choices.
- **Request Body**:
  ```json
  {
    "student_career_id": 1,
    "alternative_career_id": 8,
    "student_reasons": "Passion for programming and modern software",
    "alternative_reasons": "Parent concern for healthcare job security",
    "shared_decision_summary": "Student will build 1 starter project; parents explore state college fees."
  }
  ```
- **Response `201`**: Returns `comparison_id`, side-by-side matrices, and 5 guided discussion questions.

### 12. `GET /api/comparisons/<id>`
- **Description**: Retrieves saved comparison record for family revisit.

### 13. `POST /api/simulator/compare`
- **Description**: Evaluates and compares two scenarios (Baseline vs Alternative) in the Career Reality Simulator.
- **Request Body**:
  ```json
  {
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
  ```
- **Response `200`**:
  ```json
  {
    "success": true,
    "baseline_profile": { ... },
    "alternative_profile": { ... },
    "baseline_recommendations": [ ... ],
    "alternative_recommendations": [ ... ],
    "comparison": [
      {
        "career_id": 1,
        "title": "Software Developer",
        "baseline_score": 98.0,
        "alternative_score": 75.0,
        "score_difference": -23.0,
        "status": "left",
        "status_label": "Left Top 3",
        "change_explanation": "Compatibility decreased by -23.0% as other fields align more strongly with creative preferences.",
        "skills_to_consider": [ ... ],
        "alternative_route": { ... }
      }
    ],
    "explanations": [ "Work Style Shift: ...", "Career Priority Shift: ..." ],
    "budget_route_changes": [ ... ]
  }
  ```

### 14. `POST /api/simulator/save`
- **Description**: Evaluates and persistently saves a scenario comparison to the `scenario_comparisons` SQLite table.
- **Response `201`**: Returns `comparison_id` and structured results.

### 15. `GET /api/simulator/saved/<id>`
- **Description**: Retrieves a previously saved scenario comparison from SQLite.
- **Response `200`** or `404` if not found.

---

## 10. How the Matching Engine Works

CareerCompass avoids black-box neural networks in favor of an **auditable, deterministic scoring formula (100 points maximum)**:

### Assessment Matching Formula
$$\text{Total Score} = \text{Interests} (35) + \text{Strengths} (25) + \text{Work Style} (15) + \text{Goals} (15) + \text{Education Fit} (10)$$

### Career Reality Simulator ("What-If") Formula
Stored in `SIMULATOR_WEIGHTS` configuration (`recommender.py`):
$$\text{Simulator Score} = \text{Work Style} (30\%) + \text{Priority} (25\%) + \text{Interests} (25\%) + \text{Skills/Strengths} (20\%)$$

- **Budget Invariance Rule**: A student's intrinsic compatibility score is **never penalized** for having a lower education budget. Instead, budget shifts alter the practical learning route suggestions (e.g. self-learning & government fee waivers vs. standard public degrees vs. flexible academies).
- **Transparent Attribute Grounding**: When a career enters or leaves top recommendations, the simulator attributes the exact preference shift (e.g. analytical to creative, or growth to stability) without fabricating reasons.

---

## 11. Student–Parent Career Bridge

The Student–Parent Bridge is designed to replace stressful arguments with structured empathy:
- **Preserving Student Agency**: The student's preference remains primary; a parent's viewpoint is presented alongside, never overwriting the student's choices.
- **Side-by-Side Fact Matrices**: Directly contrasts tuition costs, examination requirements, and daily work challenges.
- **Constructive Dinner-Table Prompts**: Generates 5 neutral, collaborative questions to explore shared values before making financial commitments.

---

## 12. Known Limitations & Ethical Disclaimers

1. **No Psychometric Claim**: This tool is an educational orientation compass, not a clinical diagnostic or psychometric evaluation.
2. **No Admission or Placement Guarantees**: Completing roadmaps or high match scores does not guarantee admission or job placement.
3. **Illustrative Estimates**: Tuition figures and timelines are based on publicly available estimates from national occupational databases (e.g. BLS, NCS, AICTE, NMC, ICAI) and may fluctuate by institution.
4. **Offline Prototype**: No live real-time job-market scraper is utilized; data is updated via verified catalog seed updates.

---

## 13. Troubleshooting Common Errors

### "Python was not found" or "Execution alias" on Windows
- Ensure Python 3.10+ is installed with "Add Python to PATH" checked.
- Disable Windows App Execution Aliases:
  `Settings > Apps > Advanced app settings > App execution aliases > Turn off 'App Installer: python.exe'`.

### "Port 5000 is already in use"
Run on an alternate port:
```powershell
$env:PORT="5050"; python app.py
```
Or on macOS/Linux:
```bash
PORT=5050 python3 app.py
```

### Database Lock or Permission Error
If `instance/careercompass.db` is locked by another process:
```powershell
Remove-Item -Force .\instance\careercompass.db*
python -c "from database import init_db; init_db()"
```

---

## 14. 2-Minute Hackathon Demo Script

Follow this script for a flawless judge demonstration:

1. **Start & Context (0:00 – 0:20)**:
   - Open `http://127.0.0.1:5000` on the browser.
   - Point out the headline: *"Your future starts with understanding yourself."*
   - Mention the core problem: Students choosing careers due to peer pressure and lack of transparent reality checks.
2. **Discovery Assessment (0:20 – 0:45)**:
   - Click **"Discover My Career"**.
   - Walk through the 4 steps: select Undergraduate, Science, Computer Science & Math, Technology & Science interests, Analytical Thinking strength, Hands-on work style, and Low-cost budget.
   - Click **"Generate My Recommendations"**.
3. **Career Reality Simulator ("What-If") (0:45 – 1:15)**:
   - Click **"Reality Simulator"** in the top navigation bar.
   - Show the pre-loaded **Demo Profile** (Moderate Budget, Analytical, Growth).
   - Change Scenario B to: Creative work style and Stability priority.
   - Click **"Compare Scenarios"**.
   - Show how Data/Software careers shift while Design careers enter Top 3 with explicit reasons.
   - Toggle Budget to "Very limited" and demonstrate that compatibility scores remain invariant while learning routes adapt to zero-cost open platforms and fee waivers!
4. **Reality Check & Roadmap (1:15 – 1:35)**:
   - Open Software Developer reality check. Show the side-by-side Pros & Cons and the suggested beginner project.
   - Click **"Start Personalized Roadmap"**, save the active plan for "Demo Student", and check off Milestone 1. Show the dynamic progress percentage update.
5. **Parent–Student Bridge (1:35 – 2:00)**:
   - Navigate to **"Parent–Student Bridge"**.
   - Select Software Developer (Student) vs. Healthcare Professional (Parent).
   - Click **"Generate Side-by-Side Comparison"**.
   - Highlight the side-by-side costs, challenges, and the 5 guided conversation questions for the family dinner table.
   - Conclude with the tagline: *"CareerCompass: Your future, your choice."*

#   c a r e e r c o m p a s s - d e p l o y  
 