-- ============================================================================
-- CareerCompass Database Schema
-- SQLite 3 with Foreign Key Enforcement
-- ============================================================================

PRAGMA foreign_keys = ON;

-- Table: careers
-- Stores comprehensive catalog of seed and verified career pathways
CREATE TABLE IF NOT EXISTS careers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    short_description TEXT NOT NULL,
    typical_responsibilities TEXT NOT NULL, -- JSON array of strings
    relevant_interests TEXT NOT NULL,       -- JSON array of strings
    relevant_strengths TEXT NOT NULL,       -- JSON array of strings
    educational_requirements TEXT NOT NULL,
    min_education_level TEXT NOT NULL,      -- "Class 10", "Class 11-12", "Diploma", "Undergraduate"
    suitable_streams TEXT NOT NULL,         -- JSON array of stream names
    important_skills TEXT NOT NULL,         -- JSON array of strings
    suggested_beginner_projects TEXT NOT NULL, -- JSON array of strings
    learning_roadmap TEXT NOT NULL,         -- JSON array of milestones
    cost_category TEXT NOT NULL,            -- "Low / Free Accessible", "Moderate", "High / Regulated"
    cost_estimate_detail TEXT NOT NULL,
    low_cost_routes TEXT NOT NULL,          -- Open learning, govt scholarships, MOOCs
    entrance_exams TEXT,                    -- JSON array of exams if any
    advantages TEXT NOT NULL,               -- JSON array of strings
    challenges TEXT NOT NULL,               -- JSON array of strings
    geographic_considerations TEXT,
    regulated BOOLEAN NOT NULL DEFAULT 0,   -- 1 = statutory licensure/degree required
    source_urls TEXT,                       -- JSON array of {title, url}
    last_verified TEXT,                     -- ISO date string
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: assessments
-- Stores individual quiz submissions
CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    education_level TEXT NOT NULL,
    current_stream TEXT,
    favorite_subjects TEXT NOT NULL,        -- JSON array
    interests TEXT NOT NULL,                -- JSON array
    strengths TEXT NOT NULL,                -- JSON array
    preferred_work_style TEXT NOT NULL,
    career_goals TEXT NOT NULL,
    budget_range TEXT NOT NULL,
    location_preference TEXT NOT NULL,
    existing_skills TEXT NOT NULL,          -- JSON array
    constraints TEXT                        -- Optional accessibility/resource constraint note
);

-- Table: recommendations
-- Stores computed recommendation records linked to an assessment
CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id INTEGER NOT NULL,
    career_id INTEGER NOT NULL,
    rank INTEGER NOT NULL,
    match_score REAL NOT NULL,
    match_reasons TEXT NOT NULL,            -- JSON array of human-readable reasons
    missing_skills TEXT NOT NULL,           -- JSON array of skills to develop
    trade_offs TEXT NOT NULL,               -- JSON array of trade-offs
    alternative_routes TEXT NOT NULL,       -- JSON array of alternative routes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assessment_id) REFERENCES assessments (id) ON DELETE CASCADE,
    FOREIGN KEY (career_id) REFERENCES careers (id) ON DELETE CASCADE
);

-- Table: career_plans
-- Student's saved career action plans
CREATE TABLE IF NOT EXISTS career_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id INTEGER,
    career_id INTEGER NOT NULL,
    student_name TEXT DEFAULT 'Student',
    title TEXT NOT NULL,
    notes TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assessment_id) REFERENCES assessments (id) ON DELETE SET NULL,
    FOREIGN KEY (career_id) REFERENCES careers (id) ON DELETE CASCADE
);

-- Table: roadmap_milestones
-- Persistent milestone checklists for each career plan
CREATE TABLE IF NOT EXISTS roadmap_milestones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id INTEGER NOT NULL,
    step_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    explanation TEXT NOT NULL,
    suggested_action TEXT NOT NULL,
    estimated_duration TEXT NOT NULL,
    is_completed BOOLEAN NOT NULL DEFAULT 0,
    completed_at TIMESTAMP,
    FOREIGN KEY (plan_id) REFERENCES career_plans (id) ON DELETE CASCADE
);

-- Table: parent_student_comparisons
-- Student–Parent Career Bridge comparison entries
CREATE TABLE IF NOT EXISTS parent_student_comparisons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id INTEGER,
    student_career_id INTEGER NOT NULL,
    alternative_career_id INTEGER NOT NULL,
    student_reasons TEXT NOT NULL,
    alternative_reasons TEXT NOT NULL,
    education_comparison TEXT,              -- JSON object
    cost_comparison TEXT,                   -- JSON object
    challenges_comparison TEXT,             -- JSON object
    discussion_questions TEXT NOT NULL,     -- JSON array
    shared_decision_summary TEXT,
    alignment_status TEXT DEFAULT 'exploring',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assessment_id) REFERENCES assessments (id) ON DELETE SET NULL,
    FOREIGN KEY (student_career_id) REFERENCES careers (id) ON DELETE CASCADE,
    FOREIGN KEY (alternative_career_id) REFERENCES careers (id) ON DELETE CASCADE
);

-- Indexes for optimal lookup performance
CREATE INDEX IF NOT EXISTS idx_careers_category ON careers(category);
CREATE INDEX IF NOT EXISTS idx_recommendations_assessment ON recommendations(assessment_id);
CREATE INDEX IF NOT EXISTS idx_career_plans_career ON career_plans(career_id);
CREATE INDEX IF NOT EXISTS idx_milestones_plan ON roadmap_milestones(plan_id);
CREATE INDEX IF NOT EXISTS idx_comparisons_careers ON parent_student_comparisons(student_career_id, alternative_career_id);

-- Table: scenario_comparisons
-- Persists Career Reality Simulator scenario comparison runs
CREATE TABLE IF NOT EXISTS scenario_comparisons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    baseline_profile TEXT NOT NULL,      -- JSON string
    alternative_profile TEXT NOT NULL,   -- JSON string
    comparison_results TEXT NOT NULL,    -- JSON string
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_scenario_comparisons_created ON scenario_comparisons(created_at);

-- Table: career_comparisons
-- Persists multi-career (2 or 3 careers) comparison runs from Comparison Lab
CREATE TABLE IF NOT EXISTS career_comparisons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    career_ids TEXT NOT NULL,            -- JSON array of 2 or 3 career IDs
    assessment_id INTEGER,
    comparison_data TEXT NOT NULL,       -- JSON string of comparison matrix
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assessment_id) REFERENCES assessments (id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_career_comparisons_created ON career_comparisons(created_at);

-- Table: learning_resources
-- Verified affordable learning routes, scholarships, open platforms, and certification tools
CREATE TABLE IF NOT EXISTS learning_resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    career_id INTEGER,                   -- NULL if applicable across multiple careers
    category TEXT,                       -- e.g. "Technology & Engineering", "Healthcare", "General"
    title TEXT NOT NULL,
    provider TEXT NOT NULL,
    resource_type TEXT NOT NULL,         -- 'free_course', 'degree', 'polytechnic', 'scholarship', 'portfolio_tool'
    cost_tier TEXT NOT NULL,             -- 'free', 'subsidized', 'moderate', 'flexible'
    url TEXT NOT NULL,
    eligibility TEXT,
    description TEXT NOT NULL,
    last_verified TEXT,                  -- ISO date string
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (career_id) REFERENCES careers (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_learning_resources_career ON learning_resources(career_id);
CREATE INDEX IF NOT EXISTS idx_learning_resources_tier ON learning_resources(cost_tier);

-- Table: opportunities
-- Curated, verified, and student-friendly entry-level, internship, apprenticeship, and part-time opportunities
CREATE TABLE IF NOT EXISTS opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    employer_or_source TEXT NOT NULL,
    category TEXT NOT NULL,               -- e.g. "Civil Engineering & Construction", "IT & Software", "Business & Finance", "Sports & Fitness", "Part-Time & Campus"
    opportunity_type TEXT NOT NULL,       -- "Internship", "Apprenticeship", "Part-Time", "Entry-Level", "Freelance Project", "Campus Opportunity"
    location_city TEXT NOT NULL,          -- e.g. "Delhi NCR", "Bengaluru", "Mumbai", "Pune", "Hyderabad", "Chennai", "Kolkata", "Remote", "Pan-India"
    work_mode TEXT NOT NULL DEFAULT 'on_site', -- 'remote', 'hybrid', 'on_site'
    eligibility TEXT NOT NULL,            -- e.g. "Pursuing Diploma / B.Tech Civil", "Students (Any stream)", etc.
    skills_required TEXT NOT NULL,        -- JSON array of strings
    schedule_type TEXT NOT NULL,          -- "Study-Friendly / Flexible", "Weekend", "Part-Time (15 hrs/wk)", "Full-Time Summer"
    stipend_or_compensation TEXT,         -- Educational or stipend info if verified
    is_verified BOOLEAN NOT NULL DEFAULT 1,
    verification_status TEXT NOT NULL DEFAULT 'Verified Official Portal Framework',
    last_verified TEXT,                   -- ISO date string
    application_deadline TEXT,            -- Date or "Rolling Admissions / Annual Portal Cycle"
    official_url TEXT NOT NULL,           -- Link to official portal
    description TEXT NOT NULL,
    source_portal TEXT NOT NULL,          -- e.g. "NATS Portal (MHRD)", "AICTE Internship Portal", "NCS Ministry of Labour", "SAI Portal", "ICAI Portal"
    career_slug TEXT,                     -- Links to career slug e.g. "civil-engineer", "software-developer", etc.
    milestone_tag TEXT,                   -- Tag linking to roadmap milestone step e.g. "step-7", "step-5"
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_opportunities_category ON opportunities(category);
CREATE INDEX IF NOT EXISTS idx_opportunities_city ON opportunities(location_city);
CREATE INDEX IF NOT EXISTS idx_opportunities_mode ON opportunities(work_mode);
CREATE INDEX IF NOT EXISTS idx_opportunities_type ON opportunities(opportunity_type);

-- Table: career_quotes
-- Career inspiration quotes and practical field-specific tips for students
CREATE TABLE IF NOT EXISTS career_quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote TEXT NOT NULL,
    author TEXT NOT NULL DEFAULT 'CareerCompass Guidance',
    category TEXT NOT NULL,               -- "General", "Civil Engineering", "Software & IT", "Business & Commerce", "Sports & Athletics", "Healthcare & Sciences"
    practical_tip TEXT NOT NULL,
    suggested_action TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Appointment Booking System Tables
-- Real-time scheduling with atomic double-booking prevention & provider badges
-- ============================================================================

-- Table: appointment_providers
CREATE TABLE IF NOT EXISTS appointment_providers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    title TEXT NOT NULL,
    organization TEXT NOT NULL,
    is_verified BOOLEAN NOT NULL DEFAULT 1,
    badge_label TEXT NOT NULL DEFAULT 'Verified Guidance Counsellor',
    rating REAL NOT NULL DEFAULT 4.9,
    bio TEXT NOT NULL,
    initials TEXT NOT NULL,
    avatar_bg TEXT DEFAULT '#2563EB',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: appointment_types
CREATE TABLE IF NOT EXISTS appointment_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,               -- 'Career Guidance', 'Interview Preparation', 'Employment & Internship Support', 'Educational & Professional Guidance', 'Parent–Student Discussion'
    title TEXT NOT NULL,
    format TEXT NOT NULL DEFAULT 'Virtual Video Call', -- 'Virtual Video Call', 'Phone Consultation', 'In-Person Hub'
    duration_minutes INTEGER NOT NULL DEFAULT 45,
    cost_label TEXT NOT NULL DEFAULT 'Free / Institutional Subsidy',
    short_description TEXT NOT NULL,
    full_description TEXT NOT NULL,
    preparation_notes TEXT NOT NULL,
    target_audience TEXT NOT NULL,
    icon TEXT NOT NULL DEFAULT '📅',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: appointment_slots
CREATE TABLE IF NOT EXISTS appointment_slots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_id INTEGER NOT NULL,
    provider_id INTEGER NOT NULL,
    slot_date TEXT NOT NULL,              -- YYYY-MM-DD
    start_time TEXT NOT NULL,             -- HH:MM (24h)
    end_time TEXT NOT NULL,               -- HH:MM (24h)
    is_booked BOOLEAN NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'available', -- 'available', 'booked', 'cancelled'
    meeting_mode TEXT NOT NULL DEFAULT 'Google Meet (Encrypted Video Link)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (type_id) REFERENCES appointment_types (id) ON DELETE CASCADE,
    FOREIGN KEY (provider_id) REFERENCES appointment_providers (id) ON DELETE CASCADE
);

-- Table: appointment_bookings
CREATE TABLE IF NOT EXISTS appointment_bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_ref TEXT UNIQUE NOT NULL,     -- e.g. "CC-APT-9102"
    slot_id INTEGER NOT NULL,
    student_name TEXT NOT NULL,
    student_email TEXT NOT NULL,
    student_phone TEXT,
    education_level TEXT NOT NULL,
    current_career_interest TEXT,
    notes_or_questions TEXT,
    status TEXT NOT NULL DEFAULT 'confirmed', -- 'confirmed', 'cancelled', 'rescheduled'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cancelled_at TIMESTAMP,
    cancellation_reason TEXT,
    FOREIGN KEY (slot_id) REFERENCES appointment_slots (id) ON DELETE RESTRICT
);

-- Indexes for Appointments
CREATE INDEX IF NOT EXISTS idx_appointment_slots_date ON appointment_slots(slot_date);
CREATE INDEX IF NOT EXISTS idx_appointment_slots_type ON appointment_slots(type_id);
CREATE INDEX IF NOT EXISTS idx_appointment_slots_avail ON appointment_slots(is_booked, status);
CREATE INDEX IF NOT EXISTS idx_appointment_bookings_ref ON appointment_bookings(booking_ref);
CREATE INDEX IF NOT EXISTS idx_appointment_bookings_email ON appointment_bookings(student_email);

-- Table: ai_conversations
-- Persists multi-provider AI career guidance conversations
CREATE TABLE IF NOT EXISTS ai_conversations (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    title TEXT NOT NULL,
    profile_shared BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: ai_messages
-- Persists individual messages and associated career action chips
CREATE TABLE IF NOT EXISTS ai_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT NOT NULL,
    role TEXT NOT NULL,                   -- 'user', 'assistant'
    content TEXT NOT NULL,
    action_chips TEXT,                    -- JSON array of action chips
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES ai_conversations (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_ai_conv_session ON ai_conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_ai_msg_conv ON ai_messages(conversation_id);


