"""
CareerCompass Database Layer
Handles SQLite database connection, schema migration, seed data, and data access methods.
"""

import os
import sqlite3
import json
from datetime import datetime, timezone
from flask import has_app_context, g, current_app
from database_seeds import (
    ADDITIONAL_CAREERS, INITIAL_OPPORTUNITIES, INITIAL_CAREER_QUOTES, STAGE_GROUPS,
    INITIAL_APPOINTMENT_PROVIDERS, INITIAL_APPOINTMENT_TYPES, generate_seed_appointment_slots
)

DEFAULT_DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "instance", "careercompass.db"
)


def get_db(db_path=None):
    """
    Get a thread-safe database connection.
    Enables SQLite foreign key enforcement and row factory dictionary access.
    """
    if db_path is None and has_app_context():
        target_path = getattr(g, "db_path", None) or current_app.config.get("DATABASE") or DEFAULT_DB_PATH
    else:
        target_path = db_path or DEFAULT_DB_PATH

    os.makedirs(os.path.dirname(target_path), exist_ok=True)

    # Check if g is available (inside Flask request context)
    if has_app_context():
        if hasattr(g, "db_conn") and g.db_conn is not None and getattr(g, "db_conn_path", None) == target_path:
            return g.db_conn

    conn = sqlite3.connect(target_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")

    if has_app_context():
        g.db_conn = conn
        g.db_conn_path = target_path

    return conn


def close_db(e=None):
    """Closes database connection at the end of Flask request context."""
    if has_app_context():
        db = getattr(g, "db_conn", None)
        if db is not None:
            db.close()
            g.db_conn = None


def init_db(db_path=None, reset=False):
    """
    Initializes database schema and populates seed career dataset.
    """
    target_path = db_path or DEFAULT_DB_PATH
    os.makedirs(os.path.dirname(target_path), exist_ok=True)

    if reset and os.path.exists(target_path):
        try:
            os.remove(target_path)
        except PermissionError:
            pass

    conn = sqlite3.connect(target_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")

    schema_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")
    with open(schema_file, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    # Check if seed careers exist
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as count FROM careers")
    count = cur.fetchone()["count"]

    if count == 0:
        seed_careers(conn)

    # Always ensure additional careers (civil engineering, sports, business, expanded), opportunities, quotes, and appointments are seeded
    seed_additional_careers(conn)
    seed_opportunities(conn)
    seed_career_quotes(conn)
    seed_appointments(conn)

    conn.commit()
    conn.close()


def seed_careers(conn):
    """
    Populates 14 high-quality, comprehensive career pathways across multiple sectors.
    Includes explicit qualification requirements, low-cost routes, trade-offs, and citations.
    """
    careers = [
        {
            "slug": "software-developer",
            "title": "Software Developer",
            "category": "Technology & Engineering",
            "short_description": "Designs, builds, tests, and maintains software applications, web systems, and mobile apps using programming languages and frameworks.",
            "typical_responsibilities": json.dumps([
                "Write clean, maintainable, and efficient code in modern programming languages",
                "Collaborate with product designers and backend engineers to define feature specs",
                "Debug production issues and write automated unit/integration tests",
                "Participate in code reviews, sprint planning, and architectural discussions"
            ]),
            "relevant_interests": json.dumps(["technology", "science", "creativity"]),
            "relevant_strengths": json.dumps(["analytical thinking", "practical problem-solving", "creativity"]),
            "educational_requirements": "Bachelor's degree in Computer Science, IT, Engineering, or demonstrable equivalent portfolio from accredited open/polytechnic pathways.",
            "min_education_level": "Class 11–12",
            "suitable_streams": json.dumps(["Science - PCM", "Computer Science", "Diploma in IT / CS", "Any stream with coding portfolio"]),
            "important_skills": json.dumps(["Python / JavaScript", "Data Structures & Algorithms", "Git & Version Control", "SQL & Database Design", "Problem Solving", "Web APIs"]),
            "suggested_beginner_projects": json.dumps([
                "Personal Task & Expense Manager Web App with SQLite and Flask/Node.js",
                "Interactive Quiz Application with progress tracking in Vanilla JS",
                "Automated CLI Script for file sorting or data scraping"
            ]),
            "learning_roadmap": json.dumps([
                {"step": 1, "title": "Understand prerequisites", "explanation": "Learn computer fundamentals, binary logic, and command line basics.", "action": "Complete free CS50 or freeCodeCamp computing foundations.", "duration": "2–4 weeks"},
                {"step": 2, "title": "Learn foundational concepts", "explanation": "Master programming fundamentals: variables, loops, data structures, and OOP in Python/JS.", "action": "Solve 30 beginner coding problems on LeetCode/HackerRank.", "duration": "4–6 weeks"},
                {"step": 3, "title": "Practice relevant skills", "explanation": "Build relational databases, API endpoints, and responsive frontends.", "action": "Create a full CRUD web app connected to SQLite.", "duration": "4–6 weeks"},
                {"step": 4, "title": "Build a beginner project", "explanation": "Develop a capstone project solving a real problem for friends or a community group.", "action": "Deploy project on a free tier host (Render/Vercel) and publish GitHub repository.", "duration": "3–4 weeks"},
                {"step": 5, "title": "Research courses and qualifications", "explanation": "Evaluate BCA, B.Tech, or recognized open-source certifications (e.g. AWS Cloud Practitioner).", "action": "Shortlist accredited colleges and state admission exams (JEE/CET).", "duration": "2–3 weeks"},
                {"step": 6, "title": "Explore scholarships or affordable resources", "explanation": "Leverage open educational resources: SWAYAM/NPTEL, Harvard CS50, GitHub Student Pack.", "action": "Apply for merit/need-based scholarships or zero-cost bootcamps.", "duration": "Ongoing"},
                {"step": 7, "title": "Review progress and decide next step", "explanation": "Conduct self-assessment of GitHub portfolio, resume, and mock technical interview readiness.", "action": "Apply for summer internships or contribute to open-source software.", "duration": "2 weeks"}
            ]),
            "cost_category": "Low / Free Accessible",
            "cost_estimate_detail": "Govt Colleges: ₹30,000–₹1,50,000 total; Self-taught/Open: ₹0–₹15,000 for exam fees & certifications.",
            "low_cost_routes": "Government polytechnics, SWAYAM/NPTEL university-accredited free courses, freeCodeCamp, The Odin Project, and public library computers.",
            "entrance_exams": json.dumps(["JEE Main", "State CETs", "NIMCET (for MCA)"]),
            "advantages": json.dumps([
                "Strong global market demand and remote work flexibility",
                "High portfolio transparency: proof of work often outweighs brand pedigree",
                "Rapid learning feedback loop through instant code execution"
            ]),
            "challenges": json.dumps([
                "Fast-moving technology stack requiring lifelong self-directed learning",
                "Prolonged screen time and potential sedentary fatigue",
                "Initial entry-level competition is high for candidates without demonstrable projects"
            ]),
            "geographic_considerations": "Abundant remote and hybrid jobs globally; major hubs in metro technology corridors.",
            "regulated": 0,
            "source_urls": json.dumps([
                {"title": "US Bureau of Labor Statistics - Software Developers", "url": "https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm"},
                {"title": "National Career Service India - Software Engineer", "url": "https://www.ncs.gov.in"}
            ]),
            "last_verified": "2025-02-15"
        },
        {
            "slug": "data-analyst",
            "title": "Data Analyst",
            "category": "Data & Analytics",
            "short_description": "Collects, cleans, processes, and visualizes structured data to help organizations discover patterns and make data-driven decisions.",
            "typical_responsibilities": json.dumps([
                "Query relational databases using SQL to extract and validate business metrics",
                "Clean messy datasets using Python (Pandas) or spreadsheet tools",
                "Build interactive executive dashboards in Power BI, Tableau, or Metabase",
                "Translate complex numerical metrics into plain-language business insights"
            ]),
            "relevant_interests": json.dumps(["technology", "science", "business"]),
            "relevant_strengths": json.dumps(["analytical thinking", "practical problem-solving", "communication"]),
            "educational_requirements": "Bachelor's degree in Statistics, Mathematics, Economics, Computer Applications, or Business; strong quantitative self-study portfolios accepted.",
            "min_education_level": "Class 11–12",
            "suitable_streams": json.dumps(["Commerce with Maths", "Science - PCM", "Economics / Statistics", "Computer Science"]),
            "important_skills": json.dumps(["Advanced SQL", "Python / R (Pandas, Matplotlib)", "Spreadsheets (Excel/Sheets)", "Data Visualization & Dashboards", "Statistical Analysis", "Business Storytelling"]),
            "suggested_beginner_projects": json.dumps([
                "Exploratory Data Analysis (EDA) on World Bank education/health indicators using Python",
                "Sales & Churn Dashboard built in open-source Superset or Google Looker Studio",
                "SQL Query Case Study solving fictional e-commerce revenue queries"
            ]),
            "learning_roadmap": json.dumps([
                {"step": 1, "title": "Understand prerequisites", "explanation": "Refresh core math: descriptive statistics, percentages, variance, and probability.", "action": "Watch Khan Academy college statistics playlist.", "duration": "2–3 weeks"},
                {"step": 2, "title": "Learn foundational concepts", "explanation": "Master spreadsheet analytics: VLOOKUP/XLOOKUP, Pivot tables, and charts.", "action": "Clean and summarize a 10,000-row sample dataset.", "duration": "2–3 weeks"},
                {"step": 3, "title": "Practice relevant skills", "explanation": "Learn SQL queries: JOINs, GROUP BY, aggregations, and subqueries.", "action": "Complete SQLBolt and 50 SQL queries on HackerRank.", "duration": "4 weeks"},
                {"step": 4, "title": "Build a beginner project", "explanation": "Analyze public dataset using Python Pandas and generate visual charts.", "action": "Publish an EDA notebook on Kaggle or GitHub with written findings.", "duration": "3 weeks"},
                {"step": 5, "title": "Research courses and qualifications", "explanation": "Explore degrees in Data Science, Statistics, or Google Data Analytics Professional Certificate.", "action": "Review syllabus and financial aid options on Coursera.", "duration": "2 weeks"},
                {"step": 6, "title": "Explore scholarships or affordable resources", "explanation": "Use free open datasets from Kaggle, government portals (data.gov), and Kaggle Learn.", "action": "Enroll in free Kaggle Micro-courses.", "duration": "Ongoing"},
                {"step": 7, "title": "Review progress and decide next step", "explanation": "Present an end-to-end data story to a peer or mentor and refine communication clarity.", "action": "Assemble 3 dashboard case studies into a personal portfolio.", "duration": "2 weeks"}
            ]),
            "cost_category": "Low / Free Accessible",
            "cost_estimate_detail": "Govt/Public Degree: ₹25,000–₹1,20,000 total; Online certification routes: ₹0–₹25,000.",
            "low_cost_routes": "Google Data Analytics Certificate (Coursera financial aid), Kaggle Learn, freeCodeCamp Data Analysis with Python.",
            "entrance_exams": json.dumps(["CUET (UG/PG for Stats/Math)", "State University Entrances"]),
            "advantages": json.dumps([
                "High relevance across every industry (finance, healthcare, retail, non-profits)",
                "Clear career ladder into Data Engineering, Business Intelligence, or Machine Learning",
                "Emphasis on logical reasoning over deep theoretical software engineering"
            ]),
            "challenges": json.dumps([
                "Real-world data is often chaotic, incomplete, and undocumented",
                "Requires patience for data cleaning, which often takes 70%+ of project time",
                "Need to continually translate technical findings to non-technical stakeholders"
            ]),
            "geographic_considerations": "Widespread remote, corporate, and public policy analytics positions worldwide.",
            "regulated": 0,
            "source_urls": json.dumps([
                {"title": "BLS Occupational Outlook - Operations Research & Data Analysts", "url": "https://www.bls.gov/ooh/math/operations-research-analysts.htm"}
            ]),
            "last_verified": "2025-01-20"
        },
        {
            "slug": "cybersecurity-analyst",
            "title": "Cybersecurity Analyst",
            "category": "Technology & Engineering",
            "short_description": "Protects computer systems, networks, and confidential data from cyber threats, unauthorized intrusion, malware, and digital espionage.",
            "typical_responsibilities": json.dumps([
                "Monitor network traffic and security logs for suspicious activities and anomalies",
                "Perform vulnerability assessments, threat modeling, and security audits",
                "Respond immediately to incident alerts and contain potential data breaches",
                "Formulate security policies, password standards, and educate employees on phishing"
            ]),
            "relevant_interests": json.dumps(["technology", "public service", "science"]),
            "relevant_strengths": json.dumps(["analytical thinking", "practical problem-solving", "leadership"]),
            "educational_requirements": "Bachelor's degree in Information Security, Computer Science, or equivalent industry certifications (CompTIA Security+, CEH, TryHackMe achievements).",
            "min_education_level": "Class 11–12",
            "suitable_streams": json.dumps(["Science - PCM", "Information Technology", "Computer Science"]),
            "important_skills": json.dumps(["Networking Fundamentals (TCP/IP, DNS)", "Linux Administration", "SIEM Tools & Log Analysis", "Vulnerability Scanning", "Scripting (Python/Bash)", "Ethical Hacking Foundations"]),
            "suggested_beginner_projects": json.dumps([
                "Home Virtual Security Lab with Wireshark packet capture & analysis",
                "Vulnerability scan report on an intentionally vulnerable VM (Metasploitable)",
                "Automated Python Port Scanner & Log Auditor script"
            ]),
            "learning_roadmap": json.dumps([
                {"step": 1, "title": "Understand prerequisites", "explanation": "Understand how computers and the internet talk: OSI model, TCP/IP, IP addressing.", "action": "Complete Professor Messer's free Network+ video series.", "duration": "3–4 weeks"},
                {"step": 2, "title": "Learn foundational concepts", "explanation": "Master Linux command line commands, file permissions, and process management.", "action": "Practice Linux Journey or OverTheWire Bandit challenges.", "duration": "3–4 weeks"},
                {"step": 3, "title": "Practice relevant skills", "explanation": "Understand common web vulnerabilities: SQL injection, XSS, CSRF, and authentication flaws.", "action": "Solve PortSwigger Web Security Academy free starter labs.", "duration": "4–6 weeks"},
                {"step": 4, "title": "Build a beginner project", "explanation": "Set up a virtual home lab with pfSense firewall and Snort intrusion detection.", "action": "Write a structured incident response report based on simulated attacks.", "duration": "3–4 weeks"},
                {"step": 5, "title": "Research courses and qualifications", "explanation": "Study for entry certifications: CompTIA Security+ or ISC2 Certified in Cybersecurity (CC).", "action": "Check ISC2 'One Million Certified in Cybersecurity' free voucher program.", "duration": "4 weeks"},
                {"step": 6, "title": "Explore scholarships or affordable resources", "explanation": "Utilize TryHackMe free rooms, Hack The Box, and CyberSeek career pathways.", "action": "Earn top 10% ranking on TryHackMe pre-security pathway.", "duration": "Ongoing"},
                {"step": 7, "title": "Review progress and decide next step", "explanation": "Network with local OWASP student chapters and participate in ethical CTF events.", "action": "Compete in an entry-level Capture The Flag (CTF) tournament.", "duration": "2 weeks"}
            ]),
            "cost_category": "Moderate",
            "cost_estimate_detail": "Degrees: ₹50,000–₹2,50,000; Certifications: ₹0 (ISC2 free CC initiative) to ₹30,000 (Security+ exam fee).",
            "low_cost_routes": "ISC2 free '1 Million Certified in Cybersecurity' exams, TryHackMe free tier, OWASP community materials.",
            "entrance_exams": json.dumps(["JEE Main", "State CETs", "Industry cert exams"]),
            "advantages": json.dumps([
                "Critical global shortage of qualified cybersecurity talent",
                "High job stability and strong compensation progression",
                "Intellectually stimulating cat-and-mouse problem-solving"
            ]),
            "challenges": json.dumps([
                "On-call rotations and emergency incident response pressure",
                "High stress when managing active breach attempts",
                "Must adhere strictly to legal, regulatory, and ethical boundaries"
            ]),
            "geographic_considerations": "High demand in banking, defense, healthcare, government, and multinational enterprise centres.",
            "regulated": 0,
            "source_urls": json.dumps([
                {"title": "CISA Cybersecurity Workforce Development", "url": "https://www.cisa.gov/cybersecurity-career-pathways"},
                {"title": "BLS Information Security Analysts", "url": "https://www.bls.gov/ooh/computer-and-information-technology/information-security-analysts.htm"}
            ]),
            "last_verified": "2025-01-18"
        },
        {
            "slug": "electronics-engineer",
            "title": "Electronics Engineer",
            "category": "Technology & Engineering",
            "short_description": "Designs, develops, tests, and supervises the manufacture of electronic equipment such as microprocessors, IoT devices, embedded systems, and communication hardware.",
            "typical_responsibilities": json.dumps([
                "Design and simulate circuit schematics and printed circuit boards (PCBs)",
                "Write low-level firmware in C/C++ for microcontrollers (ARM, ESP32, STM32)",
                "Test electronic prototypes using oscilloscopes, multimeters, and logic analyzers",
                "Ensure electromagnetic compliance (EMC) and thermal stability standards"
            ]),
            "relevant_interests": json.dumps(["technology", "science", "hands-on work"]),
            "relevant_strengths": json.dumps(["analytical thinking", "practical problem-solving"]),
            "educational_requirements": "B.Tech / B.E. / B.S. in Electronics & Communication, Electrical Engineering, or accredited Polytechnic Diploma in Electronics.",
            "min_education_level": "Class 11–12",
            "suitable_streams": json.dumps(["Science - PCM", "Polytechnic Diploma in ECE / EEE"]),
            "important_skills": json.dumps(["Circuit Design & PCB Layout (KiCad)", "Embedded C / C++", "Microcontroller Architectures", "Oscilloscopes & Lab Testing", "Digital Signal Processing", "IoT Communication Protocols (MQTT, I2C, SPI)"]),
            "suggested_beginner_projects": json.dumps([
                "IoT Environmental Weather Station with ESP32 reporting to a cloud dashboard",
                "Custom 2-layer PCB designed in KiCad for an automated plant watering system",
                "Digital Frequency Counter or Audio Synthesizer built with discrete components"
            ]),
            "learning_roadmap": json.dumps([
                {"step": 1, "title": "Understand prerequisites", "explanation": "Review Ohm's Law, Kirchhoff's laws, AC/DC circuit analysis, and semiconductor physics.", "action": "Solve classic circuit analysis problems on AllAboutCircuits.com.", "duration": "3–4 weeks"},
                {"step": 2, "title": "Learn foundational concepts", "explanation": "Understand operational amplifiers, transistors (BJT, MOSFET), and digital logic gates.", "action": "Simulate basic analog & digital circuits in Falstad or LTspice.", "duration": "4 weeks"},
                {"step": 3, "title": "Practice relevant skills", "explanation": "Program an Arduino or ESP32 microcontroller in C++ reading various digital sensors.", "action": "Interface 3 sensors and an OLED display via I2C/SPI.", "duration": "4 weeks"},
                {"step": 4, "title": "Build a beginner project", "explanation": "Design schematic and route a PCB in KiCad, generate Gerber files for production.", "action": "Order a budget prototype PCB from an educational fab house.", "duration": "4 weeks"},
                {"step": 5, "title": "Research courses and qualifications", "explanation": "Target AICTE-approved engineering programs in ECE or VLSI / Embedded Systems.", "action": "Prepare for national/state engineering entrance exams.", "duration": "2–4 months"},
                {"step": 6, "title": "Explore scholarships or affordable resources", "explanation": "Leverage NPTEL IIT video courses on Basic Electrical & Digital Electronics.", "action": "Enroll in free NPTEL certification course.", "duration": "Ongoing"},
                {"step": 7, "title": "Review progress and decide next step", "explanation": "Choose specialization track: VLSI / Semiconductor design vs Embedded IoT vs Robotics.", "action": "Contribute a hardware project to Hackster.io or Arduino Hub.", "duration": "2 weeks"}
            ]),
            "cost_category": "Moderate",
            "cost_estimate_detail": "Govt Engineering College: ₹40,000–₹2,00,000 total; Hardware lab starter kit: ₹3,000–₹8,000.",
            "low_cost_routes": "Government polytechnic diploma (3 years), open maker spaces, virtual circuit simulators (Wokwi, Tinkercad, LTspice).",
            "entrance_exams": json.dumps(["JEE Main", "JEE Advanced", "State CET", "GATE (for M.Tech/PSUs)"]),
            "advantages": json.dumps([
                "Key pillar of modern hardware, semiconductor, EV, and robotics revolutions",
                "Tangible satisfaction of holding and seeing physical hardware operate",
                "Strong government incentives for domestic semiconductor manufacturing"
            ]),
            "challenges": json.dumps([
                "Requires access to physical components, test tools, and fabrication cycles",
                "Hardware bugs cannot simply be patched overnight with an over-the-air script",
                "Steep mathematical learning curve in electromagnetic theory and signal math"
            ]),
            "geographic_considerations": "Manufacturing hubs, semiconductor design centres, aerospace, and robotics clusters.",
            "regulated": 0,
            "source_urls": json.dumps([
                {"title": "IEEE Electronics Engineering Resource", "url": "https://www.ieee.org"},
                {"title": "BLS Electrical and Electronics Engineers", "url": "https://www.bls.gov/ooh/architecture-and-engineering/electrical-and-electronics-engineers.htm"}
            ]),
            "last_verified": "2025-01-10"
        },
        {
            "slug": "mechanical-engineer",
            "title": "Mechanical Engineer",
            "category": "Technology & Engineering",
            "short_description": "Researches, designs, develops, and tests mechanical and thermal sensors and devices, including tools, engines, automated machines, and manufacturing systems.",
            "typical_responsibilities": json.dumps([
                "Design mechanical parts and assemblies using 3D CAD modeling software",
                "Perform finite element analysis (FEA) and computational fluid dynamics (CFD)",
                "Supervise fabrication, prototyping, and assembly line manufacturing",
                "Analyze material fatigue, stress tolerances, and thermal dissipation"
            ]),
            "relevant_interests": json.dumps(["science", "technology", "hands-on work"]),
            "relevant_strengths": json.dumps(["practical problem-solving", "analytical thinking"]),
            "educational_requirements": "Bachelor's degree in Mechanical Engineering (B.E. / B.Tech / B.S.) or Polytechnic Diploma in Mechanical Engineering.",
            "min_education_level": "Class 11–12",
            "suitable_streams": json.dumps(["Science - PCM", "Polytechnic Diploma in Mechanical / Automobile"]),
            "important_skills": json.dumps(["3D CAD Modeling (SolidWorks/Fusion 360)", "Engineering Mechanics & Statics", "Thermodynamics & Fluid Mechanics", "Materials Science", "DFM (Design for Manufacturing)", "Prototyping & CNC/3D Printing"]),
            "suggested_beginner_projects": json.dumps([
                "Parametric 3D printable mechanical gear train or linkage designed in Fusion 360",
                "Thermal dissipation analysis for a laptop cooler or battery enclosure",
                "Scale working model of a hydraulic arm or wind turbine generator"
            ]),
            "learning_roadmap": json.dumps([
                {"step": 1, "title": "Understand prerequisites", "explanation": "Master Newtonian mechanics, vector physics, free body diagrams, and calculus.", "action": "Study MIT OpenCourseWare Physics I mechanics lectures.", "duration": "3–4 weeks"},
                {"step": 2, "title": "Learn foundational concepts", "explanation": "Learn strength of materials, stress-strain curves, beam deflection, and torque.", "action": "Work through engineering textbook practice problems.", "duration": "4 weeks"},
                {"step": 3, "title": "Practice relevant skills", "explanation": "Learn parametric 3D CAD design in Autodesk Fusion 360 or FreeCAD.", "action": "Model 5 complex mechanical components from blueprint drawings.", "duration": "4 weeks"},
                {"step": 4, "title": "Build a beginner project", "explanation": "Design an automated mechanism and 3D print or machine the parts in a makerspace.", "action": "Assemble physical prototype and document mechanical tolerances.", "duration": "3–4 weeks"},
                {"step": 5, "title": "Research courses and qualifications", "explanation": "Explore accredited universities and state engineering admission exams.", "action": "Review JEE / CET counseling criteria.", "duration": "2 months"},
                {"step": 6, "title": "Explore scholarships or affordable resources", "explanation": "Use FreeCAD (100% free open-source), SimScale community edition, and NPTEL.", "action": "Complete NPTEL Engineering Mechanics online course.", "duration": "Ongoing"},
                {"step": 7, "title": "Review progress and decide next step", "explanation": "Join student automotive/robotics teams (SAE Baja, Formula Student, Robocon).", "action": "Participate in an engineering design challenge.", "duration": "1 month"}
            ]),
            "cost_category": "Moderate",
            "cost_estimate_detail": "Govt Engineering College: ₹40,000–₹2,00,000 total; FreeCAD software is free; university labs provide heavy machinery access.",
            "low_cost_routes": "Polytechnic diplomas, open-source FreeCAD, university makerspaces, public polytechnic workshops.",
            "entrance_exams": json.dumps(["JEE Main", "JEE Advanced", "State Engineering CETs", "GATE"]),
            "advantages": json.dumps([
                "Foundational engineering discipline applicable to EV, aerospace, robotics, and energy",
                "High real-world tangibility and physical product impact",
                "Broad career versatility across design, manufacturing, and operations"
            ]),
            "challenges": json.dumps([
                "Requires physical shop floor or laboratory access for practical mastery",
                "Prototyping physical tooling entails manufacturing cycle times and material expenses",
                "Heavy industrial roles may require plant relocation away from urban centres"
            ]),
            "geographic_considerations": "Automotive corridors, aerospace clusters, heavy manufacturing zones, and energy plants.",
            "regulated": 0,
            "source_urls": json.dumps([
                {"title": "American Society of Mechanical Engineers (ASME)", "url": "https://www.asme.org"},
                {"title": "BLS Mechanical Engineers", "url": "https://www.bls.gov/ooh/architecture-and-engineering/mechanical-engineers.htm"}
            ]),
            "last_verified": "2025-01-12"
        },
        {
            "slug": "ux-ui-designer",
            "title": "UX/UI Designer",
            "category": "Creative & Design",
            "short_description": "Crafts intuitive, user-friendly digital experiences, wireframes, prototypes, and visual interfaces for websites, mobile applications, and software products.",
            "typical_responsibilities": json.dumps([
                "Conduct user research interviews and synthesize user journey maps and personas",
                "Design low-fidelity wireframes, high-fidelity mockups, and interactive prototypes",
                "Establish and maintain coherent design systems, typography scales, and UI components",
                "Collaborate with developers to ensure faithful implementation and accessibility standards"
            ]),
            "relevant_interests": json.dumps(["creativity", "technology", "people-oriented work"]),
            "relevant_strengths": json.dumps(["empathy", "creativity", "communication"]),
            "educational_requirements": "Bachelor's in Design (B.Des), Human-Computer Interaction, Fine Arts, or demonstrable self-taught case-study portfolio.",
            "min_education_level": "Class 10",
            "suitable_streams": json.dumps(["Any stream", "Arts / Humanities", "Commerce", "Science", "Design Diploma"]),
            "important_skills": json.dumps(["Figma / UI Design Tools", "User Research & Usability Testing", "Information Architecture", "Wireframing & Prototyping", "Design Systems & Tokens", "Accessibility (WCAG) Standards"]),
            "suggested_beginner_projects": json.dumps([
                "Mobile App Redesign Case Study for a local municipal public library or transit pass",
                "Fintech micro-savings mobile app wireframes and interactive Figma prototype",
                "Accessibility audit and redesigned onboarding flow for a healthcare clinic website"
            ]),
            "learning_roadmap": json.dumps([
                {"step": 1, "title": "Understand prerequisites", "explanation": "Learn design principles: contrast, hierarchy, white space, alignment, and color harmony.", "action": "Read 'Refactoring UI' concepts and LawsofUX.com principles.", "duration": "2–3 weeks"},
                {"step": 2, "title": "Learn foundational concepts", "explanation": "Master industry-standard tool Figma: components, auto-layout, variants, and prototyping.", "action": "Recreate 5 popular web & mobile screens pixel-for-pixel in Figma.", "duration": "3–4 weeks"},
                {"step": 3, "title": "Practice relevant skills", "explanation": "Learn user research methodologies: user interviews, empathy maps, and usability testing.", "action": "Interview 5 people regarding a common app frustration.", "duration": "2–3 weeks"},
                {"step": 4, "title": "Build a beginner project", "explanation": "Produce an end-to-end case study: problem discovery, wireframes, testing, and final UI.", "action": "Publish the case study on Notion, Medium, or personal portfolio.", "duration": "4 weeks"},
                {"step": 5, "title": "Research courses and qualifications", "explanation": "Review National Institute of Design (NID), UCEED, or Google UX Design Certificate.", "action": "Evaluate design entrance exams (UCEED/CEED/NID DAT) or online certifications.", "duration": "3 weeks"},
                {"step": 6, "title": "Explore scholarships or affordable resources", "explanation": "Figma is free for students; use Nielsen Norman Group free research articles.", "action": "Sign up for Figma free student education plan.", "duration": "Ongoing"},
                {"step": 7, "title": "Review progress and decide next step", "explanation": "Seek portfolio critique from senior designers on ADPList or design communities.", "action": "Book 2 free mentor review sessions on ADPList.org.", "duration": "2 weeks"}
            ]),
            "cost_category": "Low / Free Accessible",
            "cost_estimate_detail": "Govt Design Colleges (NID): ₹1,50,000–₹4,00,000 total; Self-taught portfolio route: ₹0–₹10,000 with free student Figma.",
            "low_cost_routes": "Figma Student Plan (free), ADPList (free mentorship), Coursera Google UX certificate with financial aid.",
            "entrance_exams": json.dumps(["UCEED", "NID DAT", "CEED (for PG)"]),
            "advantages": json.dumps([
                "Blends artistic creativity with psychological empathy and tech strategy",
                "No rigid degree restriction: strong portfolios consistently win job offers",
                "High remote work and freelance flexibility across global products"
            ]),
            "challenges": json.dumps([
                "Design feedback is often subjective and requires balancing stakeholder opinions",
                "Requires continuous empathy to avoid imposing personal biases over user needs",
                "Need to communicate design rationale persuasively to developers and business leads"
            ]),
            "geographic_considerations": "Widespread remote opportunities, creative agencies, tech scale-ups, and global consultancies.",
            "regulated": 0,
            "source_urls": json.dumps([
                {"title": "Nielsen Norman Group - UX Careers", "url": "https://www.nngroup.com/articles/user-experience-careers/"},
                {"title": "Interaction Design Foundation", "url": "https://www.interaction-design.org"}
            ]),
            "last_verified": "2025-01-25"
        },
        {
            "slug": "graphic-designer",
            "title": "Graphic Designer",
            "category": "Creative & Design",
            "short_description": "Creates visual concepts and illustrations using computer software or by hand to communicate ideas that inspire, inform, and captivate consumers.",
            "typical_responsibilities": json.dumps([
                "Develop brand identities, logos, marketing collateral, and packaging designs",
                "Design digital social media graphics, editorial layouts, and vector illustrations",
                "Prepare print-ready files adhering to CMYK color profiles, bleeds, and DPI standards",
                "Present design concepts and mood boards to clients and marketing directors"
            ]),
            "relevant_interests": json.dumps(["creativity", "business"]),
            "relevant_strengths": json.dumps(["creativity", "communication"]),
            "educational_requirements": "Bachelor's degree in Graphic Design, Fine Arts (BFA), Visual Communication, or strong creative portfolio.",
            "min_education_level": "Class 10",
            "suitable_streams": json.dumps(["Any stream", "Arts / Humanities", "Commerce", "Vocational Design"]),
            "important_skills": json.dumps(["Adobe Illustrator / Inkscape", "Photoshop / GIMP", "Typography & Layout Hierarchy", "Color Theory & Print Standards", "Brand Identity Strategy", "Motion Graphics Basics"]),
            "suggested_beginner_projects": json.dumps([
                "Complete brand visual identity kit (logo, stationery, color palette, style guide) for a local bakery",
                "Event poster series combining expressive typography and vector illustrations",
                "Editorial magazine cover and 4-page spread layout"
            ]),
            "learning_roadmap": json.dumps([
                {"step": 1, "title": "Understand prerequisites", "explanation": "Learn visual design core: grid systems, balance, typography anatomy, and color wheels.", "action": "Complete free visual design fundamentals guides on Canva Design School.", "duration": "2–3 weeks"},
                {"step": 2, "title": "Learn foundational concepts", "explanation": "Master vector drawing and raster editing in Inkscape/Illustrator and GIMP/Photoshop.", "action": "Draw 10 vector logos and edit 10 photo compositions.", "duration": "3–4 weeks"},
                {"step": 3, "title": "Practice relevant skills", "explanation": "Learn print vs web constraints: RGB vs CMYK, raster vs vector, resolution standards.", "action": "Design and print a physical trifold brochure mockup.", "duration": "2–3 weeks"},
                {"step": 4, "title": "Build a beginner project", "explanation": "Create a complete fictional or non-profit branding package with mockups.", "action": "Publish a polished Behance presentation with 10+ slides.", "duration": "3 weeks"},
                {"step": 5, "title": "Research courses and qualifications", "explanation": "Explore BFA / Visual Arts colleges or private design schools.", "action": "Check BFA admission guidelines at state universities.", "duration": "2 weeks"},
                {"step": 6, "title": "Explore scholarships or affordable resources", "explanation": "Use free open-source tools: Inkscape, GIMP, Krita, and Blender for 3D elements.", "action": "Master open-source Inkscape tutorials.", "duration": "Ongoing"},
                {"step": 7, "title": "Review progress and decide next step", "explanation": "Build a Behance or Dribbble showcase and begin taking freelance client briefs.", "action": "Pitch pro-bono design work for a community cause to gain real client proof.", "duration": "2 weeks"}
            ]),
            "cost_category": "Low / Free Accessible",
            "cost_estimate_detail": "Govt Fine Arts College: ₹15,000–₹80,000 total; Free software (Inkscape, GIMP) = ₹0.",
            "low_cost_routes": "Government arts colleges, open-source graphic suites (Inkscape, Krita, Scribus), Behance community tutorials.",
            "entrance_exams": json.dumps(["State Fine Arts Entrances", "NIFT Entrances"]),
            "advantages": json.dumps([
                "High visual autonomy and creative self-expression",
                "Immediate ability to freelance or take client commissions worldwide",
                "Low technical barrier to entry compared to software programming"
            ]),
            "challenges": json.dumps([
                "Subjective feedback and frequent revision requests from clients",
                "Crowded junior freelance market requires clear niche positioning",
                "Rapid emergence of generative AI image tools requires upskilling into strategic branding"
            ]),
            "geographic_considerations": "Work anywhere with a computer; advertising agencies and publication studios in metro cities.",
            "regulated": 0,
            "source_urls": json.dumps([
                {"title": "AIGA Professional Association for Design", "url": "https://www.aiga.org"},
                {"title": "BLS Graphic Designers", "url": "https://www.bls.gov/ooh/arts-and-design/graphic-designers.htm"}
            ]),
            "last_verified": "2025-01-20"
        },
        {
            "slug": "healthcare-professional",
            "title": "Healthcare Professional (Nursing / Medicine)",
            "category": "Healthcare & Life Sciences",
            "short_description": "Diagnoses, treats, cares for, and promotes health in individuals and communities through clinical practice, patient care, and medical science.",
            "typical_responsibilities": json.dumps([
                "Examine patients, take medical histories, and administer prescribed treatments",
                "Monitor vital signs, administer medications, and assist in clinical procedures",
                "Educate patients and families on disease management and preventive wellness",
                "Maintain confidential electronic health records and adhere to medical protocols"
            ]),
            "relevant_interests": json.dumps(["healthcare", "science", "people-oriented work"]),
            "relevant_strengths": json.dumps(["empathy", "practical problem-solving", "communication"]),
            "educational_requirements": "B.Sc Nursing, MBBS, BAMS, or accredited Allied Health Sciences degree. Mandatory government licensing and clinical registration.",
            "min_education_level": "Class 11–12",
            "suitable_streams": json.dumps(["Science - PCB (Physics, Chemistry, Biology)"]),
            "important_skills": json.dumps(["Human Anatomy & Physiology", "Patient Empathy & Bedside Manner", "Emergency Clinical Care", "Infection Control Protocols", "Medical Ethics & Compliance", "Diagnostic Thinking"]),
            "suggested_beginner_projects": json.dumps([
                "Community Health Awareness Campaign plan on diabetes/hypertension screening",
                "Volunteer log and patient assistance reflections from a local hospital or clinic",
                "Certified First Aid and Basic Life Support (BLS) training completion"
            ]),
            "learning_roadmap": json.dumps([
                {"step": 1, "title": "Understand prerequisites", "explanation": "Excel in senior secondary Biology, Chemistry, and Physics (PCB).", "action": "Review NCERT/state biology textbooks with emphasis on human systems.", "duration": "School years"},
                {"step": 2, "title": "Learn foundational concepts", "explanation": "Understand cellular biology, biochemistry, pharmacology basics, and disease transmission.", "action": "Watch Khan Academy Health and Medicine lectures.", "duration": "4–6 weeks"},
                {"step": 3, "title": "Practice relevant skills", "explanation": "Earn certification in CPR, Basic Life Support (BLS), and first aid through Red Cross.", "action": "Attend a certified weekend First Aid workshop.", "duration": "1–2 weeks"},
                {"step": 4, "title": "Build a beginner project", "explanation": "Volunteer at a community dispensary, blood donation camp, or elderly care facility.", "action": "Complete 40 hours of supervised healthcare volunteering.", "duration": "1–2 months"},
                {"step": 5, "title": "Research courses and qualifications", "explanation": "Prepare for national medical / nursing entrance exams (NEET-UG, AIIMS Nursing).", "action": "Solve 5 years of past entrance question papers.", "duration": "6–12 months"},
                {"step": 6, "title": "Explore scholarships or affordable resources", "explanation": "Government medical and nursing colleges have highly subsidized tuition fees.", "action": "Target state government medical/nursing colleges with merit scholarships.", "duration": "Ongoing"},
                {"step": 7, "title": "Review progress and decide next step", "explanation": "Enroll in accredited degree program, complete mandatory rotating clinical internship.", "action": "Register with state medical/nursing council upon graduation.", "duration": "Degree years"}
            ]),
            "cost_category": "High / Regulated",
            "cost_estimate_detail": "Govt Colleges: ₹10,000–₹1,50,000 total (highly subsidized); Private Colleges: ₹10,00,000–₹60,00,000+.",
            "low_cost_routes": "Government medical colleges (NEET merit), Government B.Sc Nursing & GNM diplomas, Armed Forces Medical Services.",
            "entrance_exams": json.dumps(["NEET-UG", "AIIMS Nursing Entrance", "State Paramedical Entrances"]),
            "advantages": json.dumps([
                "Profound social impact and unmatched emotional fulfillment",
                "Recession-proof demand and worldwide healthcare workforce mobility",
                "High community respect and trusted professional standing"
            ]),
            "challenges": json.dumps([
                "Strict statutory licensing requirement; cannot practice without formal credentials",
                "Demanding shift work, night duties, and emotional exposure to illness and loss",
                "Rigorous, competitive entrance examinations with long training periods"
            ]),
            "geographic_considerations": "Essential worldwide in hospitals, primary health centres, clinics, and emergency services.",
            "regulated": 1,
            "source_urls": json.dumps([
                {"title": "National Medical Commission (NMC)", "url": "https://www.nmc.org.in"},
                {"title": "Indian Nursing Council", "url": "https://indiannursingcouncil.org"},
                {"title": "World Health Organization - Health Workforce", "url": "https://www.who.int/teams/health-workforce"}
            ]),
            "last_verified": "2025-02-01"
        },
        {
            "slug": "teacher-educator",
            "title": "Teacher or Educator",
            "category": "Education & Social",
            "short_description": "Instructs, mentors, inspires, and evaluates students across schools, colleges, or digital learning platforms, fostering critical thinking and subject mastery.",
            "typical_responsibilities": json.dumps([
                "Plan and deliver engaging lesson plans aligned with curriculum frameworks",
                "Assess student comprehension through quizzes, assignments, and practical projects",
                "Provide individualized guidance, mentorship, and encouragement to diverse learners",
                "Maintain classroom engagement and communicate progress to parents"
            ]),
            "relevant_interests": json.dumps(["education", "people-oriented work", "public service"]),
            "relevant_strengths": json.dumps(["communication", "empathy", "leadership"]),
            "educational_requirements": "Bachelor's / Master's degree in subject area plus Bachelor of Education (B.Ed) or Teacher Eligibility Test (TET/CTET) for school positions; NET/Ph.D for collegiate lecturing.",
            "min_education_level": "Undergraduate",
            "suitable_streams": json.dumps(["Any stream (Arts, Science, Commerce) followed by B.Ed / D.El.Ed"]),
            "important_skills": json.dumps(["Curriculum Design & Lesson Planning", "Public Speaking & Clear Communication", "Patience & Empathy", "Classroom Management", "EdTech Tools & Visual Aids", "Formative Assessment"]),
            "suggested_beginner_projects": json.dumps([
                "3-part interactive lesson plan with slides, worksheets, and formative quiz on a complex topic",
                "Pro-bono peer tutoring program documented with pre-and-post student performance improvements",
                "Educational explanatory video or interactive worksheet published on YouTube or open educational repository"
            ]),
            "learning_roadmap": json.dumps([
                {"step": 1, "title": "Understand prerequisites", "explanation": "Deepen mastery in chosen subject field (Languages, Math, Science, or Social Studies).", "action": "Earn strong undergraduate degree marks in your core subject.", "duration": "Undergraduate"},
                {"step": 2, "title": "Learn foundational concepts", "explanation": "Study educational psychology, child development, and pedagogy theory.", "action": "Read pedagogical foundations and learning style models.", "duration": "4 weeks"},
                {"step": 3, "title": "Practice relevant skills", "explanation": "Gain practical teaching experience through volunteering or home tutoring.", "action": "Tutor 2–3 younger students for 3 months.", "duration": "3 months"},
                {"step": 4, "title": "Build a beginner project", "explanation": "Design an innovative module using interactive digital tools (Kahoot, Canva, PhET).", "action": "Deliver a 45-minute guest lesson and solicit student feedback.", "duration": "2 weeks"},
                {"step": 5, "title": "Research courses and qualifications", "explanation": "Enroll in accredited B.Ed program or state teacher training diploma.", "action": "Apply for state B.Ed entrance exams.", "duration": "Degree years"},
                {"step": 6, "title": "Explore scholarships or affordable resources", "explanation": "Central/State government colleges offer very low B.Ed tuition with stipend schemes.", "action": "Prepare for Central Teacher Eligibility Test (CTET).", "duration": "4–6 months"},
                {"step": 7, "title": "Review progress and decide next step", "explanation": "Apply to government or private schools or explore EdTech instructional design roles.", "action": "Clear CTET / State TET examination.", "duration": "Ongoing"}
            ]),
            "cost_category": "Low / Free Accessible",
            "cost_estimate_detail": "Govt B.Ed Colleges: ₹10,000–₹50,000 total; CTET examination fee: ~₹1,200.",
            "low_cost_routes": "Government teacher training colleges, DIET institutes, Open Universities (IGNOU) B.Ed / M.Ed.",
            "entrance_exams": json.dumps(["B.Ed CET", "CTET / State TET", "UGC NET (for higher education)"]),
            "advantages": json.dumps([
                "Direct, generational impact on shaping minds, values, and futures",
                "Stable work schedules, predictable academic calendars, and holidays",
                "Opportunity to master and continuously share passions in beloved subjects"
            ]),
            "challenges": json.dumps([
                "Substantial administrative, grading, and curriculum compliance workload outside class",
                "Salary levels vary widely between underfunded institutions and elite schools",
                "Requires immense patience when dealing with varied student attention spans and behavioral challenges"
            ]),
            "geographic_considerations": "Needed in every village, town, city, and internationally across all demographics.",
            "regulated": 1,
            "source_urls": json.dumps([
                {"title": "National Council for Teacher Education (NCTE)", "url": "https://ncte.gov.in"},
                {"title": "Central Board of Secondary Education - CTET", "url": "https://ctet.nic.in"}
            ]),
            "last_verified": "2025-01-28"
        },
        {
            "slug": "business-analyst",
            "title": "Business Analyst",
            "category": "Business & Finance",
            "short_description": "Analyzes business processes, identifies organizational needs, and bridges the gap between commercial stakeholders and technical product teams.",
            "typical_responsibilities": json.dumps([
                "Elicit business requirements from executive stakeholders and customers",
                "Create Business Requirement Documents (BRDs), user stories, and process flows",
                "Conduct cost-benefit, ROI, and feasibility analyses for strategic initiatives",
                "Facilitate sprint ceremonies and validate that delivered software meets business goals"
            ]),
            "relevant_interests": json.dumps(["business", "technology", "people-oriented work"]),
            "relevant_strengths": json.dumps(["communication", "analytical thinking", "leadership"]),
            "educational_requirements": "Bachelor's degree in Business Administration (BBA/B.Com), Computer Applications, Economics, or Engineering; MBA is common for seniority.",
            "min_education_level": "Undergraduate",
            "suitable_streams": json.dumps(["Commerce", "Management", "Science / Engineering", "Economics"]),
            "important_skills": json.dumps(["Requirements Gathering & User Stories", "Process Modeling (BPMN, Flowcharts)", "SQL & Excel Data Validation", "Stakeholder Communication & Negotiation", "Agile & Scrum Methodologies", "Jira & Confluence"]),
            "suggested_beginner_projects": json.dumps([
                "Complete BRD and User Story breakdown for an online grocery delivery optimization",
                "As-Is vs To-Be business process flowchart modeled in Draw.io or Lucidchart",
                "Market competition analysis and financial feasibility pitch deck for a new SaaS tool"
            ]),
            "learning_roadmap": json.dumps([
                {"step": 1, "title": "Understand prerequisites", "explanation": "Learn business fundamentals: revenue models, operations, organizational hierarchies.", "action": "Read 'The Personal MBA' by Josh Kaufman summary notes.", "duration": "2–3 weeks"},
                {"step": 2, "title": "Learn foundational concepts", "explanation": "Learn Agile principles, Scrum roles, sprint cycles, and user story mapping.", "action": "Complete free Scrum guide reading and online Scrum assessment.", "duration": "2 weeks"},
                {"step": 3, "title": "Practice relevant skills", "explanation": "Practice drawing BPMN flowcharts and writing unambiguous user stories with acceptance criteria.", "action": "Draft 15 user stories with INVEST criteria in Jira/Notion.", "duration": "3 weeks"},
                {"step": 4, "title": "Build a beginner project", "explanation": "Document an existing messy real-world process (e.g. college admissions) and propose optimized flow.", "action": "Create comprehensive As-Is vs To-Be documentation.", "duration": "3 weeks"},
                {"step": 5, "title": "Research courses and qualifications", "explanation": "Explore IIBA certifications (ECBA - Entry Certificate in Business Analysis).", "action": "Review IIBA BABOK guide summaries.", "duration": "4 weeks"},
                {"step": 6, "title": "Explore scholarships or affordable resources", "explanation": "Free tools: Miro, Lucidchart free tier, open business case studies from Harvard/MIT.", "action": "Study open case studies on business strategy.", "duration": "Ongoing"},
                {"step": 7, "title": "Review progress and decide next step", "explanation": "Prepare for case-study based interviews and behavioral stakeholder alignment scenarios.", "action": "Practice 5 mock business case interviews.", "duration": "2 weeks"}
            ]),
            "cost_category": "Low / Free Accessible",
            "cost_estimate_detail": "Govt/State University Degree: ₹30,000–₹1,50,000 total; IIBA ECBA exam: ~$150–$300.",
            "low_cost_routes": "State university BBA/B.Com degrees, free Scrum Master guides, Coursera business strategy courses with financial aid.",
            "entrance_exams": json.dumps(["CUET (UG)", "CAT / CMAT (for MBA)"]),
            "advantages": json.dumps([
                "High corporate visibility and collaboration with senior leaders",
                "Natural launching pad into Product Management or Executive Leadership",
                "Balanced blend of human interpersonal psychology and quantitative rigor"
            ]),
            "challenges": json.dumps([
                "Frequent conflict resolution required between stubborn technical and commercial viewpoints",
                "Often held accountable for project scope creep without direct managerial authority",
                "Must learn new domain jargon quickly when shifting between industry sectors"
            ]),
            "geographic_considerations": "Corporate headquarters, financial centres, consulting firms, and technology hubs.",
            "regulated": 0,
            "source_urls": json.dumps([
                {"title": "International Institute of Business Analysis (IIBA)", "url": "https://www.iiba.org"},
                {"title": "BLS Management Analysts", "url": "https://www.bls.gov/ooh/business-and-financial/management-analysts.htm"}
            ]),
            "last_verified": "2025-01-30"
        },
        {
            "slug": "entrepreneur",
            "title": "Entrepreneur / Startup Founder",
            "category": "Business & Finance",
            "short_description": "Identifies unmet market opportunities, develops innovative solutions, secures resources, takes calculated financial risks, and builds viable business ventures.",
            "typical_responsibilities": json.dumps([
                "Validate customer problems, value propositions, and unit economics",
                "Build early prototypes (MVP) and iterate rapidly on user feedback",
                "Recruit founding teammates, pitch to angel investors, or bootstrap revenue",
                "Manage cash runway, marketing funnels, legal compliance, and daily operations"
            ]),
            "relevant_interests": json.dumps(["business", "creativity", "technology"]),
            "relevant_strengths": json.dumps(["leadership", "practical problem-solving", "analytical thinking"]),
            "educational_requirements": "No mandatory degree required. Passion, market insight, sales capability, and resilience are paramount.",
            "min_education_level": "Class 10",
            "suitable_streams": json.dumps(["Any stream", "Commerce", "Engineering", "Arts"]),
            "important_skills": json.dumps(["Customer Discovery & Sales", "Financial Literacy & Cash Flow", "Product Sense & Prototyping", "Resilience & Risk Management", "Persuasive Storytelling & Pitching", "Team Building & Hiring"]),
            "suggested_beginner_projects": json.dumps([
                "Launch a small service or e-commerce shop and generate the first ₹5,000 / $100 in legitimate customer revenue",
                "Conduct 25 structured customer problem discovery interviews using 'The Mom Test' methodology",
                "Publish a Lean Canvas and financial runway projection spreadsheet for an innovative startup idea"
            ]),
            "learning_roadmap": json.dumps([
                {"step": 1, "title": "Understand prerequisites", "explanation": "Read 'The Lean Startup' and 'The Mom Test' to learn how to ask questions without biased validation.", "action": "Formulate a one-sentence problem hypothesis.", "duration": "2 weeks"},
                {"step": 2, "title": "Learn foundational concepts", "explanation": "Learn business models, gross margins, customer acquisition cost (CAC), and lifetime value (LTV).", "action": "Fill out a Lean Business Model Canvas.", "duration": "1–2 weeks"},
                {"step": 3, "title": "Practice relevant skills", "explanation": "Build a zero-code landing page (Carrd/Notion) collecting email signups to test real demand.", "action": "Collect 50 genuine waitlist signups before building.", "duration": "2–3 weeks"},
                {"step": 4, "title": "Build a beginner project", "explanation": "Deliver a simple MVP manually ('concierge' or 'Wizard of Oz' prototype) to 5 paying users.", "action": "Transact first customer payment and deliver the service.", "duration": "3–4 weeks"},
                {"step": 5, "title": "Research courses and qualifications", "explanation": "Study Y Combinator's free Startup School lectures and incubator criteria.", "action": "Complete Y Combinator Startup School free curriculum.", "duration": "4 weeks"},
                {"step": 6, "title": "Explore scholarships or affordable resources", "explanation": "Leverage government startup grants (Startup India Seed Fund), college incubators.", "action": "Register on official government startup portal for tax exemptions and grants.", "duration": "Ongoing"},
                {"step": 7, "title": "Review progress and decide next step", "explanation": "Decide whether to bootstrap sustainably to profitability or pitch angel investors.", "action": "Prepare 10-slide pitch deck backed by real initial traction data.", "duration": "2 weeks"}
            ]),
            "cost_category": "Low / Free Accessible",
            "cost_estimate_detail": "Zero-degree requirement; Starting cost: ₹0–₹10,000 for domain, hosting, and prototype testing.",
            "low_cost_routes": "Y Combinator Startup School (100% free), Startup India schemes, college incubation centres, no-code tools.",
            "entrance_exams": json.dumps(["None required"]),
            "advantages": json.dumps([
                "Complete autonomy to pursue vision, build culture, and solve problems you care about",
                "Unlimited financial upside and equity value creation",
                "Deepest possible crash course in human psychology, finance, and leadership"
            ]),
            "challenges": json.dumps([
                "High probability of early failure and unpredictable income stability",
                "Extreme emotional weight and psychological resilience required during tough months",
                "Long hours where you are responsible for everything from strategy to cleaning up"
            ]),
            "geographic_considerations": "Can be launched anywhere; access to startup ecosystems and customer density helps early scaling.",
            "regulated": 0,
            "source_urls": json.dumps([
                {"title": "Y Combinator Startup School", "url": "https://www.startupschool.org"},
                {"title": "Startup India Official Portal", "url": "https://www.startupindia.gov.in"}
            ]),
            "last_verified": "2025-02-10"
        },
        {
            "slug": "environmental-scientist",
            "title": "Environmental Scientist",
            "category": "Sciences & Environment",
            "short_description": "Uses knowledge of natural sciences to protect the environment and human health, analyzing pollution data, assessing biodiversity, and guiding sustainability policy.",
            "typical_responsibilities": json.dumps([
                "Collect soil, air, water, and biological field samples for laboratory analysis",
                "Analyze environmental impact data using GIS mapping and statistical software",
                "Prepare Environmental Impact Assessment (EIA) reports for government and industry",
                "Advise corporations and public agencies on compliance, waste reduction, and conservation"
            ]),
            "relevant_interests": json.dumps(["science", "public service", "hands-on work"]),
            "relevant_strengths": json.dumps(["analytical thinking", "practical problem-solving", "communication"]),
            "educational_requirements": "Bachelor's degree in Environmental Science, Ecology, Geology, or Chemistry; Master's degree (M.Sc) strongly recommended for research roles.",
            "min_education_level": "Undergraduate",
            "suitable_streams": json.dumps(["Science - PCB", "Science - PCM", "Earth Sciences"]),
            "important_skills": json.dumps(["Field Sampling & Lab Chemistry", "GIS & Spatial Mapping (QGIS/ArcGIS)", "Data Analysis & Statistics", "Environmental Regulations & Law", "Scientific Report Writing", "Climate & Carbon Accounting"]),
            "suggested_beginner_projects": json.dumps([
                "Local groundwater or tap water quality testing study comparing pH and dissolved solids",
                "Open-source QGIS map of urban tree canopy cover vs surface heat islands in your city",
                "Campus carbon footprint assessment and waste audit proposal"
            ]),
            "learning_roadmap": json.dumps([
                {"step": 1, "title": "Understand prerequisites", "explanation": "Study earth sciences, chemistry cycles, ecosystems, and atmospheric science.", "action": "Review basic chemistry and ecology college textbooks.", "duration": "3–4 weeks"},
                {"step": 2, "title": "Learn foundational concepts", "explanation": "Learn spatial mapping and geographic information systems using free open-source QGIS.", "action": "Complete QGIS beginner mapping tutorials on QGIS.org.", "duration": "4 weeks"},
                {"step": 3, "title": "Practice relevant skills", "explanation": "Learn laboratory safety, water testing kit protocols, and statistical graphing.", "action": "Conduct field tests on 5 water samples from diverse localities.", "duration": "3 weeks"},
                {"step": 4, "title": "Build a beginner project", "explanation": "Conduct an environmental audit of a local park or residential neighborhood.", "action": "Write a 10-page formatted environmental report with maps and mitigation proposals.", "duration": "4 weeks"},
                {"step": 5, "title": "Research courses and qualifications", "explanation": "Explore accredited B.Sc / M.Sc Environmental Science degrees at public universities.", "action": "Check CUET PG / state university entrance requirements.", "duration": "2 months"},
                {"step": 6, "title": "Explore scholarships or affordable resources", "explanation": "QGIS is free; open satellite data from USGS Landsat and ESA Copernicus is publicly available.", "action": "Download free Copernicus satellite imagery for environmental monitoring.", "duration": "Ongoing"},
                {"step": 7, "title": "Review progress and decide next step", "explanation": "Intern with non-profit conservation groups, state pollution control boards, or ESG consulting firms.", "action": "Apply for summer research internships with certified labs.", "duration": "1 month"}
            ]),
            "cost_category": "Low / Free Accessible",
            "cost_estimate_detail": "Govt University B.Sc/M.Sc: ₹15,000–₹80,000 total; Open satellite data and QGIS = ₹0.",
            "low_cost_routes": "Government science colleges, open-source QGIS tutorials, ESA/NASA free satellite datasets, state forestry internships.",
            "entrance_exams": json.dumps(["CUET (UG & PG)", "State University Entrances", "GATE (Environmental Science)"]),
            "advantages": json.dumps([
                "Direct contribution to solving planetary climate and biodiversity crises",
                "Healthy balance of outdoor field investigations and indoor laboratory/data analytics",
                "Growing corporate ESG (Environmental, Social, Governance) compliance careers"
            ]),
            "challenges": json.dumps([
                "Field work in remote, harsh weather conditions or contaminated environments",
                "Government environmental policy changes can affect research grant funding",
                "Scientific findings can encounter resistance from commercial interest groups"
            ]),
            "geographic_considerations": "Research institutes, conservation sanctuaries, pollution control boards, and corporate sustainability offices.",
            "regulated": 0,
            "source_urls": json.dumps([
                {"title": "UN Environment Programme (UNEP)", "url": "https://www.unep.org"},
                {"title": "BLS Environmental Scientists and Specialists", "url": "https://www.bls.gov/ooh/life-physical-and-social-science/environmental-scientists-and-specialists.htm"}
            ]),
            "last_verified": "2025-01-16"
        },
        {
            "slug": "clinical-psychologist",
            "title": "Clinical Psychologist / Counselor",
            "category": "Healthcare & Life Sciences",
            "short_description": "Assesses, diagnoses, and treats mental health disorders, emotional struggles, and behavioral issues through evidence-based psychotherapy and counseling.",
            "typical_responsibilities": json.dumps([
                "Conduct diagnostic clinical interviews and psychometric assessments",
                "Deliver evidence-based psychotherapy (Cognitive Behavioral Therapy, ACT)",
                "Develop personalized treatment plans for anxiety, depression, and trauma",
                "Collaborate with psychiatrists, social workers, and families to support patient well-being"
            ]),
            "relevant_interests": json.dumps(["healthcare", "education", "people-oriented work"]),
            "relevant_strengths": json.dumps(["empathy", "communication", "analytical thinking"]),
            "educational_requirements": "B.A./B.Sc in Psychology followed by M.A./M.Sc in Clinical Psychology and mandatory M.Phil / Psy.D / Licensing from statutory body (e.g. RCI in India, APA / State Board in US).",
            "min_education_level": "Undergraduate",
            "suitable_streams": json.dumps(["Arts / Humanities with Psychology", "Science - PCB", "Any undergraduate stream with psychology prerequisites"]),
            "important_skills": json.dumps(["Active Listening & Empathetic Presence", "Psychological Assessment & Diagnostic Criteria (DSM-5 / ICD-11)", "Cognitive Behavioral Therapy (CBT)", "Crisis Intervention & Risk Assessment", "Ethical Boundaries & Confidentiality", "Reflective Self-Care"]),
            "suggested_beginner_projects": json.dumps([
                "Peer listening support volunteer log with certified helpline training",
                "Research review paper on the efficacy of digital mental health interventions for youth",
                "Psychoeducational workshop outline addressing adolescent exam stress and resilience"
            ]),
            "learning_roadmap": json.dumps([
                {"step": 1, "title": "Understand prerequisites", "explanation": "Study foundations of general psychology, cognitive science, and neuroanatomy.", "action": "Read introductory college psychology textbook.", "duration": "4 weeks"},
                {"step": 2, "title": "Learn foundational concepts", "explanation": "Understand abnormal psychology, developmental milestones, and social psychology.", "action": "Watch Yale OpenCourseWare 'Introduction to Psychology'.", "duration": "4–6 weeks"},
                {"step": 3, "title": "Practice relevant skills", "explanation": "Volunteer on a crisis suicide helpline after completing their rigorous training.", "action": "Complete helpline volunteer training and supervised calling shifts.", "duration": "3 months"},
                {"step": 4, "title": "Build a beginner project", "explanation": "Design an evidence-based psychoeducation module on stress management for students.", "action": "Host a supervised workshop and gather feedback.", "duration": "3 weeks"},
                {"step": 5, "title": "Research courses and qualifications", "explanation": "Apply for Master's programs in Clinical / Counseling Psychology at accredited universities.", "action": "Prepare for university PG entrance examinations.", "duration": "6 months"},
                {"step": 6, "title": "Explore scholarships or affordable resources", "explanation": "Central universities and government hospitals offer low tuition and clinical stipends.", "action": "Apply to public university M.Phil / Psy.D programs.", "duration": "Degree years"},
                {"step": 7, "title": "Review progress and decide next step", "explanation": "Complete mandatory clinical internship hours under licensed supervisors and register with licensing council.", "action": "Obtain statutory license to practice independently.", "duration": "Licensure"}
            ]),
            "cost_category": "Moderate",
            "cost_estimate_detail": "Govt Universities: ₹30,000–₹1,20,000 total; Private Universities: ₹2,50,000–₹8,00,000.",
            "low_cost_routes": "Central/State universities (DU, BHU, Jamia, Mumbai Univ), government mental health institutes (NIMHANS, CIP) with government stipends.",
            "entrance_exams": json.dumps(["CUET (UG & PG)", "NIMHANS Entrance", "National / State Council Licensure Exams"]),
            "advantages": json.dumps([
                "Deep human connection and profound ability to alleviate psychological suffering",
                "Rapidly expanding destigmatization of mental healthcare worldwide",
                "High independence in establishing private practice or tele-therapy consultations"
            ]),
            "challenges": json.dumps([
                "Strict licensing requirements: cannot legally practice clinical therapy without statutory accreditation",
                "Risk of emotional burnout and compassion fatigue requiring strict personal boundaries",
                "Long educational qualification pathway (Undergrad + Master's + Clinical Licensure)"
            ]),
            "geographic_considerations": "Hospitals, private clinics, schools, universities, rehabilitation centres, and remote tele-health.",
            "regulated": 1,
            "source_urls": json.dumps([
                {"title": "Rehabilitation Council of India (RCI)", "url": "https://rehabcouncil.nic.in"},
                {"title": "American Psychological Association (APA)", "url": "https://www.apa.org"},
                {"title": "BLS Psychologists", "url": "https://www.bls.gov/ooh/life-physical-and-social-science/psychologists.htm"}
            ]),
            "last_verified": "2025-01-22"
        },
        {
            "slug": "chartered-accountant",
            "title": "Chartered Accountant / Financial Analyst",
            "category": "Business & Finance",
            "short_description": "Manages financial auditing, taxation, corporate reporting, and investment valuation to ensure legal fiscal compliance and financial sustainability.",
            "typical_responsibilities": json.dumps([
                "Audit financial statements to verify accuracy and compliance with accounting standards",
                "Advise corporations and individuals on tax planning, GST, and legal filing",
                "Perform financial modeling, discounted cash flow (DCF) analysis, and valuation",
                "Guide strategic capital allocation, debt management, and corporate restructuring"
            ]),
            "relevant_interests": json.dumps(["business", "science", "stability"]),
            "relevant_strengths": json.dumps(["analytical thinking", "practical problem-solving"]),
            "educational_requirements": "Chartered Accountancy qualification (ICAI / ACCA / CPA) or Bachelor's in Finance/Commerce followed by CFA (Chartered Financial Analyst).",
            "min_education_level": "Class 11–12",
            "suitable_streams": json.dumps(["Commerce with Accountancy/Maths", "Science PCM", "Any stream with strong numerical aptitude"]),
            "important_skills": json.dumps(["Financial Accounting & IFRS / GAAP", "Auditing & Internal Controls", "Corporate & Direct/Indirect Taxation", "Financial Modeling in Excel", "Statutory Compliance", "Critical Attention to Detail"]),
            "suggested_beginner_projects": json.dumps([
                "Personal and family income tax computation & optimization model in Excel",
                "Comprehensive financial ratio analysis comparing two publicly traded companies",
                "3-statement integrated financial model for a retail business"
            ]),
            "learning_roadmap": json.dumps([
                {"step": 1, "title": "Understand prerequisites", "explanation": "Master double-entry bookkeeping, debit/credit rules, balance sheets, and P&L.", "action": "Score high in Class 11–12 Accountancy or college fundamentals.", "duration": "School / College"},
                {"step": 2, "title": "Learn foundational concepts", "explanation": "Register with statutory accountancy body (ICAI Foundation / ACCA Knowledge Level).", "action": "Clear Foundation exam.", "duration": "4–6 months"},
                {"step": 3, "title": "Practice relevant skills", "explanation": "Learn Intermediate subjects: corporate law, cost accounting, taxation, and advanced auditing.", "action": "Clear Intermediate Group exams.", "duration": "9–12 months"},
                {"step": 4, "title": "Build a beginner project", "explanation": "Complete mandatory practical articleship training at a chartered accountancy firm.", "action": "Complete articleship / audit engagements under licensed principal.", "duration": "2–3 years"},
                {"step": 5, "title": "Research courses and qualifications", "explanation": "Prepare for CA Final examination or CFA Level 1.", "action": "Intensive revision and mock tests for Final examinations.", "duration": "6–12 months"},
                {"step": 6, "title": "Explore scholarships or affordable resources", "explanation": "ICAI fee structure is heavily subsidized by the statutory institute; open study modules provided.", "action": "Study official ICAI Board of Studies study material.", "duration": "Ongoing"},
                {"step": 7, "title": "Review progress and decide next step", "explanation": "Obtain Certificate of Practice (COP) for independent auditing or join corporate finance.", "action": "Register as an Associate Member of the Institute.", "duration": "Post-qualification"}
            ]),
            "cost_category": "Low / Free Accessible",
            "cost_estimate_detail": "Statutory Registration & Exam Fees total: ₹30,000–₹80,000 over entire course (students earn articleship stipend during training).",
            "low_cost_routes": "Direct self-study using official ICAI BoS material, free YouTube concept marathons, articleship stipend helps offset exam costs.",
            "entrance_exams": json.dumps(["CA Foundation", "CA Intermediate", "CA Final", "ACCA Exams", "CFA Level 1"]),
            "advantages": json.dumps([
                "Extremely high financial stability and statutory monopoly over company audit signing",
                "Highly meritocratic: no college campus brand required; open to any dedicated student",
                "Comprehensive understanding of every dimension of business, cash, and law"
            ]),
            "challenges": json.dumps([
                "Statutory pass rates are notoriously demanding requiring extraordinary discipline",
                "Intense tax audit filing deadlines and prolonged working hours in peak seasons",
                "High legal and personal liability for verified audit sign-offs"
            ]),
            "geographic_considerations": "Needed in every business community, banking centre, corporate office, and audit practice globally.",
            "regulated": 1,
            "source_urls": json.dumps([
                {"title": "Institute of Chartered Accountants of India (ICAI)", "url": "https://www.icai.org"},
                {"title": "Association of Chartered Certified Accountants (ACCA)", "url": "https://www.accaglobal.com"},
                {"title": "BLS Accountants and Auditors", "url": "https://www.bls.gov/ooh/business-and-financial/accountants-and-auditors.htm"}
            ]),
            "last_verified": "2025-02-05"
        }
    ]

    cur = conn.cursor()
    for c in careers:
        cur.execute("""
            INSERT INTO careers (
                slug, title, category, short_description, typical_responsibilities,
                relevant_interests, relevant_strengths, educational_requirements,
                min_education_level, suitable_streams, important_skills,
                suggested_beginner_projects, learning_roadmap, cost_category,
                cost_estimate_detail, low_cost_routes, entrance_exams,
                advantages, challenges, geographic_considerations, regulated,
                source_urls, last_verified
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c["slug"], c["title"], c["category"], c["short_description"],
            c["typical_responsibilities"], c["relevant_interests"], c["relevant_strengths"],
            c["educational_requirements"], c["min_education_level"], c["suitable_streams"],
            c["important_skills"], c["suggested_beginner_projects"], c["learning_roadmap"],
            c["cost_category"], c["cost_estimate_detail"], c["low_cost_routes"],
            c["entrance_exams"], c["advantages"], c["challenges"],
            c["geographic_considerations"], c["regulated"], c["source_urls"],
            c["last_verified"]
        ))


# ============================================================================
# Query Helpers
# ============================================================================

def format_career_row(row):
    """Converts a SQLite row for a career into a JSON-friendly dictionary."""
    if not row:
        return None
    d = dict(row)
    for field in [
        "typical_responsibilities", "relevant_interests", "relevant_strengths",
        "suitable_streams", "important_skills", "suggested_beginner_projects",
        "learning_roadmap", "entrance_exams", "advantages", "challenges", "source_urls"
    ]:
        if d.get(field) and isinstance(d[field], str):
            try:
                d[field] = json.loads(d[field])
            except Exception:
                pass
    return d


def get_all_careers(category=None, db_path=None):
    """Retrieve all careers, optionally filtered by category."""
    conn = get_db(db_path)
    cur = conn.cursor()
    if category:
        cur.execute("SELECT * FROM careers WHERE category = ? ORDER BY title ASC", (category,))
    else:
        cur.execute("SELECT * FROM careers ORDER BY category ASC, title ASC")
    rows = cur.fetchall()
    return [format_career_row(r) for r in rows]


def get_career_by_id(career_id, db_path=None):
    """Retrieve a single career by its integer ID."""
    conn = get_db(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM careers WHERE id = ?", (career_id,))
    row = cur.fetchone()
    return format_career_row(row)


def get_career_by_slug(slug, db_path=None):
    """Retrieve a single career by its slug."""
    conn = get_db(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM careers WHERE slug = ?", (slug,))
    row = cur.fetchone()
    return format_career_row(row)


def save_assessment(data, db_path=None):
    """Saves assessment quiz responses and returns the created assessment ID."""
    conn = get_db(db_path)
    cur = conn.cursor()

    favorite_subjects = json.dumps(data.get("favorite_subjects", []))
    interests = json.dumps(data.get("interests", []))
    strengths = json.dumps(data.get("strengths", []))
    existing_skills = json.dumps(data.get("existing_skills", []))

    cur.execute("""
        INSERT INTO assessments (
            education_level, current_stream, favorite_subjects,
            interests, strengths, preferred_work_style, career_goals,
            budget_range, location_preference, existing_skills, constraints
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("education_level", "Undergraduate"),
        data.get("current_stream", ""),
        favorite_subjects,
        interests,
        strengths,
        data.get("preferred_work_style", "teamwork"),
        data.get("career_goals", "learning"),
        data.get("budget_range", "moderate"),
        data.get("location_preference", "flexible_relocate"),
        existing_skills,
        data.get("constraints", "")
    ))
    conn.commit()
    return cur.lastrowid


def get_assessment(assessment_id, db_path=None):
    """Retrieves assessment details by ID."""
    conn = get_db(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM assessments WHERE id = ?", (assessment_id,))
    row = cur.fetchone()
    if not row:
        return None
    d = dict(row)
    for field in ["favorite_subjects", "interests", "strengths", "existing_skills"]:
        if d.get(field) and isinstance(d[field], str):
            try:
                d[field] = json.loads(d[field])
            except Exception:
                pass
    return d


def save_recommendations(assessment_id, recs_list, db_path=None):
    """Saves generated recommendation objects linked to an assessment."""
    conn = get_db(db_path)
    cur = conn.cursor()
    # Remove existing recommendations for this assessment if any
    cur.execute("DELETE FROM recommendations WHERE assessment_id = ?", (assessment_id,))
    for idx, rec in enumerate(recs_list, start=1):
        cur.execute("""
            INSERT INTO recommendations (
                assessment_id, career_id, rank, match_score,
                match_reasons, missing_skills, trade_offs, alternative_routes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            assessment_id,
            rec["career_id"],
            idx,
            rec["match_score"],
            json.dumps(rec.get("match_reasons", [])),
            json.dumps(rec.get("missing_skills", [])),
            json.dumps(rec.get("trade_offs", [])),
            json.dumps(rec.get("alternative_routes", []))
        ))
    conn.commit()


def get_recommendations_by_assessment(assessment_id, db_path=None):
    """Retrieves saved recommendations with career details."""
    conn = get_db(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT r.*, c.title, c.slug, c.category, c.short_description,
               c.cost_category, c.regulated, c.min_education_level
        FROM recommendations r
        JOIN careers c ON r.career_id = c.id
        WHERE r.assessment_id = ?
        ORDER BY r.rank ASC
    """, (assessment_id,))
    rows = cur.fetchall()
    results = []
    for r in rows:
        item = dict(r)
        for field in ["match_reasons", "missing_skills", "trade_offs", "alternative_routes"]:
            if item.get(field) and isinstance(item[field], str):
                try:
                    item[field] = json.loads(item[field])
                except Exception:
                    pass
        results.append(item)
    return results


def save_career_plan(career_id, assessment_id=None, student_name="Student", notes="", db_path=None):
    """
    Creates a new persistent career plan and clones the career's roadmap milestones.
    """
    conn = get_db(db_path)
    cur = conn.cursor()

    career = get_career_by_id(career_id, db_path=db_path)
    if not career:
        return None

    title = f"{career['title']} Pathway Plan"

    cur.execute("""
        INSERT INTO career_plans (assessment_id, career_id, student_name, title, notes, status)
        VALUES (?, ?, ?, ?, ?, 'active')
    """, (assessment_id, career_id, student_name, title, notes))
    plan_id = cur.lastrowid

    # Populate milestones from career roadmap
    roadmap = career.get("learning_roadmap", [])
    if isinstance(roadmap, str):
        try:
            roadmap = json.loads(roadmap)
        except Exception:
            roadmap = []

    for step in roadmap:
        cur.execute("""
            INSERT INTO roadmap_milestones (
                plan_id, step_number, title, explanation, suggested_action, estimated_duration, is_completed
            ) VALUES (?, ?, ?, ?, ?, ?, 0)
        """, (
            plan_id,
            step.get("step", 1),
            step.get("title", ""),
            step.get("explanation", ""),
            step.get("action", ""),
            step.get("duration", "2-4 weeks")
        ))

    conn.commit()
    return plan_id


def get_career_plan(plan_id, db_path=None):
    """Retrieves a career plan along with its milestones and career details."""
    conn = get_db(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT p.*, c.title as career_title, c.slug as career_slug, c.category,
               c.cost_category, c.cost_estimate_detail, c.low_cost_routes, c.regulated
        FROM career_plans p
        JOIN careers c ON p.career_id = c.id
        WHERE p.id = ?
    """, (plan_id,))
    plan_row = cur.fetchone()
    if not plan_row:
        return None

    plan = dict(plan_row)

    cur.execute("""
        SELECT * FROM roadmap_milestones
        WHERE plan_id = ?
        ORDER BY step_number ASC
    """, (plan_id,))
    milestones = [dict(m) for m in cur.fetchall()]

    completed_count = sum(1 for m in milestones if m["is_completed"])
    total_count = len(milestones)
    progress_pct = round((completed_count / total_count * 100), 1) if total_count > 0 else 0

    plan["milestones"] = milestones
    plan["completed_count"] = completed_count
    plan["total_count"] = total_count
    plan["progress_percentage"] = progress_pct
    return plan


def get_all_plans(db_path=None):
    """Returns list of all saved career plans with progress statistics."""
    conn = get_db(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT p.*, c.title as career_title, c.slug as career_slug, c.category,
               (SELECT COUNT(*) FROM roadmap_milestones WHERE plan_id = p.id) as total_milestones,
               (SELECT COUNT(*) FROM roadmap_milestones WHERE plan_id = p.id AND is_completed = 1) as completed_milestones
        FROM career_plans p
        JOIN careers c ON p.career_id = c.id
        ORDER BY p.updated_at DESC
    """)
    rows = cur.fetchall()
    plans = []
    for r in rows:
        d = dict(r)
        tot = d.get("total_milestones", 0)
        comp = d.get("completed_milestones", 0)
        d["progress_percentage"] = round((comp / tot * 100), 1) if tot > 0 else 0
        plans.append(d)
    return plans


def update_milestone_status(plan_id, milestone_id, is_completed, db_path=None):
    """Updates completion status of a roadmap milestone."""
    conn = get_db(db_path)
    cur = conn.cursor()

    completed_at = datetime.now(timezone.utc).isoformat() if is_completed else None
    cur.execute("""
        UPDATE roadmap_milestones
        SET is_completed = ?, completed_at = ?
        WHERE id = ? AND plan_id = ?
    """, (1 if is_completed else 0, completed_at, milestone_id, plan_id))

    if cur.rowcount == 0:
        return False

    # Also touch the plan's updated_at timestamp
    cur.execute("""
        UPDATE career_plans
        SET updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (plan_id,))

    conn.commit()
    return True


def save_career_comparison(data, db_path=None):
    """Saves a student–parent career bridge comparison."""
    conn = get_db(db_path)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO parent_student_comparisons (
            assessment_id, student_career_id, alternative_career_id,
            student_reasons, alternative_reasons,
            education_comparison, cost_comparison, challenges_comparison,
            discussion_questions, shared_decision_summary, alignment_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("assessment_id"),
        data["student_career_id"],
        data["alternative_career_id"],
        data.get("student_reasons", ""),
        data.get("alternative_reasons", ""),
        json.dumps(data.get("education_comparison", {})),
        json.dumps(data.get("cost_comparison", {})),
        json.dumps(data.get("challenges_comparison", {})),
        json.dumps(data.get("discussion_questions", [])),
        data.get("shared_decision_summary", ""),
        data.get("alignment_status", "exploring")
    ))
    conn.commit()
    return cur.lastrowid


def get_career_comparison(comparison_id, db_path=None):
    """Retrieves a comparison by ID including details of both careers."""
    conn = get_db(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT comp.*,
               c1.title as student_career_title, c1.category as student_career_category,
               c1.educational_requirements as student_career_education,
               c1.cost_category as student_career_cost_cat, c1.cost_estimate_detail as student_career_cost,
               c1.challenges as student_career_challenges, c1.advantages as student_career_advantages,
               c2.title as alternative_career_title, c2.category as alternative_career_category,
               c2.educational_requirements as alternative_career_education,
               c2.cost_category as alternative_career_cost_cat, c2.cost_estimate_detail as alternative_career_cost,
               c2.challenges as alternative_career_challenges, c2.advantages as alternative_career_advantages
        FROM parent_student_comparisons comp
        JOIN careers c1 ON comp.student_career_id = c1.id
        JOIN careers c2 ON comp.alternative_career_id = c2.id
        WHERE comp.id = ?
    """, (comparison_id,))
    row = cur.fetchone()
    if not row:
        return None

    d = dict(row)
    for field in [
        "education_comparison", "cost_comparison", "challenges_comparison",
        "discussion_questions", "student_career_challenges", "student_career_advantages",
        "alternative_career_challenges", "alternative_career_advantages"
    ]:
        if d.get(field) and isinstance(d[field], str):
            try:
                d[field] = json.loads(d[field])
            except Exception:
                pass
    return d


def save_scenario_comparison(baseline_profile, alternative_profile, comparison_results, db_path=None):
    """
    Saves a Career Reality Simulator scenario comparison to SQLite.
    Returns the newly inserted comparison ID.
    """
    conn = get_db(db_path)
    cur = conn.cursor()

    b_json = json.dumps(baseline_profile) if not isinstance(baseline_profile, str) else baseline_profile
    a_json = json.dumps(alternative_profile) if not isinstance(alternative_profile, str) else alternative_profile
    r_json = json.dumps(comparison_results) if not isinstance(comparison_results, str) else comparison_results

    cur.execute("""
        INSERT INTO scenario_comparisons (baseline_profile, alternative_profile, comparison_results)
        VALUES (?, ?, ?)
    """, (b_json, a_json, r_json))
    conn.commit()
    return cur.lastrowid


def get_scenario_comparison(comparison_id, db_path=None):
    """Retrieves a saved scenario comparison by ID."""
    conn = get_db(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM scenario_comparisons WHERE id = ?", (comparison_id,))
    row = cur.fetchone()
    if not row:
        return None

    d = dict(row)
    for field in ["baseline_profile", "alternative_profile", "comparison_results"]:
        if d.get(field) and isinstance(d[field], str):
            try:
                d[field] = json.loads(d[field])
            except Exception:
                pass
    return d


# ============================================================================
# Additional Seeders & Helpers for Opportunities, Quotes & Custom Roadmaps
# ============================================================================

def seed_additional_careers(conn):
    """
    Seeds additional careers (Civil Engineer, Sports pathways, Business pathways) if not already present.
    """
    cur = conn.cursor()
    for c in ADDITIONAL_CAREERS:
        cur.execute("SELECT id FROM careers WHERE slug = ?", (c["slug"],))
        if cur.fetchone() is None:
            cur.execute("""
                INSERT INTO careers (
                    slug, title, category, short_description, typical_responsibilities,
                    relevant_interests, relevant_strengths, educational_requirements,
                    min_education_level, suitable_streams, important_skills,
                    suggested_beginner_projects, learning_roadmap, cost_category,
                    cost_estimate_detail, low_cost_routes, entrance_exams,
                    advantages, challenges, geographic_considerations, regulated,
                    source_urls, last_verified
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                c["slug"], c["title"], c["category"], c["short_description"],
                c["typical_responsibilities"], c["relevant_interests"], c["relevant_strengths"],
                c["educational_requirements"], c["min_education_level"], c["suitable_streams"],
                c["important_skills"], c["suggested_beginner_projects"], c["learning_roadmap"],
                c["cost_category"], c["cost_estimate_detail"], c["low_cost_routes"],
                c["entrance_exams"], c["advantages"], c["challenges"],
                c["geographic_considerations"], c["regulated"], c["source_urls"],
                c["last_verified"]
            ))


def seed_opportunities(conn):
    """
    Seeds curated entry-level, internship, apprenticeship, and campus opportunities if table is empty.
    """
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as count FROM opportunities")
    if cur.fetchone()["count"] == 0:
        for opp in INITIAL_OPPORTUNITIES:
            cur.execute("""
                INSERT INTO opportunities (
                    title, employer_or_source, category, opportunity_type,
                    location_city, work_mode, eligibility, skills_required,
                    schedule_type, stipend_or_compensation, is_verified,
                    verification_status, last_verified, application_deadline,
                    official_url, description, source_portal, career_slug, milestone_tag
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                opp["title"], opp["employer_or_source"], opp["category"], opp["opportunity_type"],
                opp["location_city"], opp["work_mode"], opp["eligibility"], opp["skills_required"],
                opp["schedule_type"], opp.get("stipend_or_compensation"), opp.get("is_verified", 1),
                opp.get("verification_status", "Verified Official Portal Framework"),
                opp.get("last_verified", "2026-10-10"), opp.get("application_deadline", "Ongoing"),
                opp["official_url"], opp["description"], opp["source_portal"],
                opp.get("career_slug"), opp.get("milestone_tag")
            ))


def seed_career_quotes(conn):
    """
    Seeds authentic Career Inspiration guidance quotes and practical tips.
    """
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as count FROM career_quotes")
    if cur.fetchone()["count"] == 0:
        for q in INITIAL_CAREER_QUOTES:
            cur.execute("""
                INSERT INTO career_quotes (quote, author, category, practical_tip, suggested_action)
                VALUES (?, ?, ?, ?, ?)
            """, (q["quote"], q["author"], q["category"], q["practical_tip"], q["suggested_action"]))


def seed_appointments(conn):
    """
    Seeds verified appointment providers, session types, and upcoming slots if empty.
    """
    cur = conn.cursor()
    # 1. Providers
    cur.execute("SELECT COUNT(*) as count FROM appointment_providers")
    if cur.fetchone()["count"] == 0:
        for p in INITIAL_APPOINTMENT_PROVIDERS:
            cur.execute("""
                INSERT INTO appointment_providers (
                    name, title, organization, is_verified, badge_label, rating, bio, initials, avatar_bg
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p["name"], p["title"], p["organization"], p.get("is_verified", 1),
                p.get("badge_label", "Verified Guidance Counsellor"), p.get("rating", 4.9),
                p["bio"], p["initials"], p.get("avatar_bg", "#2563EB")
            ))

    # 2. Types
    cur.execute("SELECT COUNT(*) as count FROM appointment_types")
    if cur.fetchone()["count"] == 0:
        for t in INITIAL_APPOINTMENT_TYPES:
            cur.execute("""
                INSERT INTO appointment_types (
                    category, title, format, duration_minutes, cost_label,
                    short_description, full_description, preparation_notes, target_audience, icon
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                t["category"], t["title"], t.get("format", "Virtual Video Call"),
                t.get("duration_minutes", 45), t.get("cost_label", "Free / Institutional Subsidy"),
                t["short_description"], t["full_description"], t["preparation_notes"],
                t["target_audience"], t.get("icon", "📅")
            ))

    # 3. Slots
    cur.execute("SELECT COUNT(*) as count FROM appointment_slots")
    if cur.fetchone()["count"] == 0:
        slots = generate_seed_appointment_slots()
        for s in slots:
            cur.execute("""
                INSERT INTO appointment_slots (
                    type_id, provider_id, slot_date, start_time, end_time,
                    is_booked, status, meeting_mode
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                s["type_id"], s["provider_id"], s["slot_date"], s["start_time"], s["end_time"],
                s.get("is_booked", 0), s.get("status", "available"), s.get("meeting_mode", "Google Meet (Encrypted Video Link)")
            ))


def format_opportunity_row(row):
    """Converts a SQLite row for an opportunity into a JSON-friendly dict."""
    if not row:
        return None
    d = dict(row)
    if "skills_required" in d and isinstance(d["skills_required"], str):
        try:
            d["skills_required"] = json.loads(d["skills_required"])
        except Exception:
            d["skills_required"] = []
    d["is_verified"] = bool(d.get("is_verified", 1))
    return d


def get_opportunities(category=None, location_city=None, work_mode=None, opportunity_type=None, query=None, limit=60, db_path=None):
    """
    Retrieves filtered opportunities with parameterized SQL query.
    Supports location-awareness, category filtering, work mode, and search keyword.
    """
    conn = get_db(db_path)
    cur = conn.cursor()
    conditions = []
    params = []

    if category and category.lower() != "all":
        conditions.append("category = ?")
        params.append(category)

    if location_city and location_city.lower() not in ["all", "all cities", ""]:
        conditions.append("(location_city LIKE ? OR work_mode = 'remote')")
        params.append(f"%{location_city}%")

    if work_mode and work_mode.lower() != "all":
        conditions.append("work_mode = ?")
        params.append(work_mode.lower())

    if opportunity_type and opportunity_type.lower() != "all":
        conditions.append("opportunity_type = ?")
        params.append(opportunity_type)

    if query and query.strip():
        q_term = f"%{query.strip()}%"
        conditions.append("(title LIKE ? OR employer_or_source LIKE ? OR description LIKE ? OR eligibility LIKE ?)")
        params.extend([q_term, q_term, q_term, q_term])

    where_sql = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    sql = f"SELECT * FROM opportunities {where_sql} ORDER BY id ASC LIMIT ?"
    params.append(limit)

    cur.execute(sql, params)
    return [format_opportunity_row(r) for r in cur.fetchall()]


def get_opportunity_by_id(opportunity_id, db_path=None):
    """Retrieves a single opportunity by its ID."""
    conn = get_db(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM opportunities WHERE id = ?", (opportunity_id,))
    row = cur.fetchone()
    return format_opportunity_row(row) if row else None


def get_career_quotes(category=None, db_path=None):
    """
    Retrieves career inspiration guidance quotes.
    If category is provided, prioritizes matching category and includes General quotes.
    """
    conn = get_db(db_path)
    cur = conn.cursor()
    if category and category.lower() != "all":
        cur.execute("""
            SELECT * FROM career_quotes 
            WHERE category = ? OR category = 'General'
            ORDER BY CASE WHEN category = ? THEN 0 ELSE 1 END, id ASC
        """, (category, category))
    else:
        cur.execute("SELECT * FROM career_quotes ORDER BY id ASC")
    return [dict(r) for r in cur.fetchall()]


def get_custom_roadmap(career_identifier, education_level="Undergraduate", db_path=None):
    """
    Returns an interactive snake roadmap for the given career, tailored to the student's education level.
    Maps milestones to stage groups (Stage A to Stage G), attaches relevant opportunities,
    free/affordable resources, and beginner projects.
    """
    if isinstance(career_identifier, int) or (isinstance(career_identifier, str) and career_identifier.isdigit()):
        career = get_career_by_id(int(career_identifier), db_path=db_path)
    else:
        career = get_career_by_slug(career_identifier, db_path=db_path)

    if not career:
        return None

    raw_roadmap = career.get("learning_roadmap") or []
    if isinstance(raw_roadmap, str):
        try:
            raw_roadmap = json.loads(raw_roadmap)
        except Exception:
            raw_roadmap = []

    total_steps = len(raw_roadmap)
    custom_milestones = []

    for idx, m in enumerate(raw_roadmap):
        step_num = m.get("step", idx + 1)
        if total_steps >= 10:
            # 11-step roadmap (e.g. Civil Engineering)
            if step_num in [1]:
                stage_code = "C"
            elif step_num in [2, 3]:
                stage_code = "C"
            elif step_num in [4, 5, 6]:
                stage_code = "D"
            elif step_num in [7]:
                stage_code = "E"
            elif step_num in [8, 9, 10]:
                stage_code = "F"
            else:
                stage_code = "G"
        else:
            # 7-step standard roadmap
            if step_num == 1:
                stage_code = "A" if education_level in ["Class 10", "High School"] else "C"
            elif step_num == 2:
                stage_code = "B" if education_level in ["Class 10", "Class 11-12"] else "C"
            elif step_num in [3, 4]:
                stage_code = "D"
            elif step_num in [5]:
                stage_code = "E"
            elif step_num in [6]:
                stage_code = "F"
            else:
                stage_code = "G"

        stage_meta = STAGE_GROUPS.get(stage_code, STAGE_GROUPS["C"])

        conn = get_db(db_path)
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM opportunities 
            WHERE career_slug = ? OR category = ? OR milestone_tag = ?
            LIMIT 2
        """, (career.get("slug"), career.get("category"), f"step-{step_num}"))
        milestone_opps = [format_opportunity_row(r) for r in cur.fetchall()]

        custom_milestones.append({
            "step_number": step_num,
            "title": m.get("title", f"Step {step_num}"),
            "explanation": m.get("explanation", ""),
            "suggested_action": m.get("action", m.get("suggested_action", "")),
            "estimated_duration": m.get("duration", m.get("estimated_duration", "2–4 weeks")),
            "stage_code": stage_code,
            "stage_name": stage_meta["name"],
            "stage_icon": stage_meta["icon"],
            "stage_description": stage_meta["description"],
            "prerequisites": career.get("min_education_level", "Class 11–12"),
            "skills": career.get("important_skills", [])[:4],
            "beginner_projects": career.get("suggested_beginner_projects", [])[:2],
            "low_cost_route": career.get("low_cost_routes", "Open-source and government learning resources available."),
            "verification_source": career.get("source_urls", [])[:2],
            "opportunities": milestone_opps,
            "is_completed": False
        })

    return {
        "career_id": career["id"],
        "career_title": career["title"],
        "career_slug": career["slug"],
        "category": career["category"],
        "education_level": education_level,
        "total_milestones": len(custom_milestones),
        "milestones": custom_milestones,
        "stages": [STAGE_GROUPS[k] for k in ["A", "B", "C", "D", "E", "F", "G"]]
    }


# ============================================================================
# Appointments Data Access Layer
# Atomic double-booking prevention, cancellation, rescheduling & status lookup
# ============================================================================

def get_appointment_types(category=None, format_filter=None, db_path=None):
    """
    Retrieves appointment session types, optionally filtered by category or delivery format.
    """
    conn = get_db(db_path)
    cur = conn.cursor()
    sql = "SELECT * FROM appointment_types WHERE 1=1"
    params = []
    if category and category.lower() != "all":
        sql += " AND category = ?"
        params.append(category)
    if format_filter and format_filter.lower() != "all":
        sql += " AND format = ?"
        params.append(format_filter)
    sql += " ORDER BY category ASC, id ASC"
    cur.execute(sql, params)
    return [dict(r) for r in cur.fetchall()]


def get_appointment_type_by_id(type_id, db_path=None):
    """Retrieves a single appointment type by ID."""
    conn = get_db(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM appointment_types WHERE id = ?", (type_id,))
    row = cur.fetchone()
    return dict(row) if row else None


def get_appointment_providers(is_verified=None, db_path=None):
    """Retrieves appointment mentors and counsellors."""
    conn = get_db(db_path)
    cur = conn.cursor()
    sql = "SELECT * FROM appointment_providers WHERE 1=1"
    params = []
    if is_verified is not None:
        sql += " AND is_verified = ?"
        params.append(1 if is_verified else 0)
    sql += " ORDER BY rating DESC, id ASC"
    cur.execute(sql, params)
    return [dict(r) for r in cur.fetchall()]


def get_available_slots(type_id=None, slot_date=None, category=None, provider_id=None, include_booked=False, db_path=None):
    """
    Fetches real-time appointment slots with joined type and provider details.
    By default returns only available slots (is_booked = 0).
    """
    conn = get_db(db_path)
    cur = conn.cursor()
    sql = """
        SELECT s.id, s.type_id, s.provider_id, s.slot_date, s.start_time, s.end_time,
               s.is_booked, s.status, s.meeting_mode,
               t.category as type_category, t.title as type_title, t.format as type_format,
               t.duration_minutes, t.cost_label, t.icon as type_icon, t.short_description as type_short_desc,
               p.name as provider_name, p.title as provider_title, p.organization as provider_org,
               p.is_verified as provider_verified, p.badge_label as provider_badge, p.rating as provider_rating,
               p.initials as provider_initials, p.avatar_bg as provider_avatar_bg
        FROM appointment_slots s
        JOIN appointment_types t ON s.type_id = t.id
        JOIN appointment_providers p ON s.provider_id = p.id
        WHERE 1=1
    """
    params = []

    if not include_booked:
        sql += " AND s.is_booked = 0 AND s.status = 'available'"

    if type_id:
        sql += " AND s.type_id = ?"
        params.append(type_id)

    if slot_date and slot_date.lower() not in ["all", "any", ""]:
        sql += " AND s.slot_date = ?"
        params.append(slot_date)

    if category and category.lower() not in ["all", ""]:
        sql += " AND t.category = ?"
        params.append(category)

    if provider_id:
        sql += " AND s.provider_id = ?"
        params.append(provider_id)

    sql += " ORDER BY s.slot_date ASC, s.start_time ASC"
    cur.execute(sql, params)
    rows = cur.fetchall()
    return [dict(r) for r in rows]


def get_booking_by_ref(booking_ref, db_path=None):
    """
    Retrieves full booking details by unique reference code.
    """
    conn = get_db(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT b.*, 
               s.slot_date, s.start_time, s.end_time, s.meeting_mode,
               t.category as type_category, t.title as type_title, t.format as type_format,
               t.duration_minutes, t.cost_label, t.icon as type_icon, t.preparation_notes,
               p.name as provider_name, p.title as provider_title, p.organization as provider_org,
               p.is_verified as provider_verified, p.badge_label as provider_badge,
               p.initials as provider_initials, p.avatar_bg as provider_avatar_bg
        FROM appointment_bookings b
        JOIN appointment_slots s ON b.slot_id = s.id
        JOIN appointment_types t ON s.type_id = t.id
        JOIN appointment_providers p ON s.provider_id = p.id
        WHERE b.booking_ref = ?
    """, (booking_ref,))
    row = cur.fetchone()
    return dict(row) if row else None


def get_bookings_by_email(email, db_path=None):
    """
    Retrieves all bookings made under a given student email address.
    """
    conn = get_db(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT b.*, 
               s.slot_date, s.start_time, s.end_time, s.meeting_mode,
               t.category as type_category, t.title as type_title, t.format as type_format,
               t.duration_minutes, t.cost_label, t.icon as type_icon,
               p.name as provider_name, p.title as provider_title, p.badge_label as provider_badge
        FROM appointment_bookings b
        JOIN appointment_slots s ON b.slot_id = s.id
        JOIN appointment_types t ON s.type_id = t.id
        JOIN appointment_providers p ON s.provider_id = p.id
        WHERE LOWER(b.student_email) = LOWER(?)
        ORDER BY s.slot_date DESC, s.start_time DESC
    """, (email.strip(),))
    return [dict(r) for r in cur.fetchall()]


def book_appointment_slot(slot_id, student_name, student_email, student_phone, education_level,
                          current_career_interest=None, notes_or_questions=None, db_path=None):
    """
    Atomically books an appointment slot with double-booking prevention.
    Uses atomic conditional UPDATE (`is_booked = 0 AND status = 'available'`).
    Returns (booking_dict, None) on success, or (None, error_message) on failure.
    """
    import random
    conn = get_db(db_path)
    cur = conn.cursor()

    # 1. ATOMIC LOCK: Update slot ONLY IF not currently booked
    cur.execute("""
        UPDATE appointment_slots
        SET is_booked = 1, status = 'booked'
        WHERE id = ? AND is_booked = 0 AND status = 'available'
    """, (slot_id,))

    if cur.rowcount == 0:
        return None, "This slot was just booked by another user or is no longer available. Please select another slot."

    # 2. Generate unique booking reference: CC-APT-XXXX
    ref_num = random.randint(1000, 9999)
    booking_ref = f"CC-APT-{ref_num}"
    cur.execute("SELECT id FROM appointment_bookings WHERE booking_ref = ?", (booking_ref,))
    if cur.fetchone():
        booking_ref = f"CC-APT-{random.randint(10000, 99999)}"

    cur.execute("""
        INSERT INTO appointment_bookings (
            booking_ref, slot_id, student_name, student_email, student_phone,
            education_level, current_career_interest, notes_or_questions, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'confirmed')
    """, (
        booking_ref, slot_id, student_name.strip(), student_email.strip(),
        (student_phone or "").strip(), education_level or "Undergraduate",
        (current_career_interest or "").strip(), (notes_or_questions or "").strip()
    ))

    conn.commit()
    booking = get_booking_by_ref(booking_ref, db_path=db_path)
    return booking, None


def cancel_appointment_booking(booking_ref, reason="Cancelled by student", db_path=None):
    """
    Cancels an active booking and atomically releases the appointment slot for rebooking.
    """
    conn = get_db(db_path)
    cur = conn.cursor()

    cur.execute("SELECT * FROM appointment_bookings WHERE booking_ref = ?", (booking_ref,))
    booking = cur.fetchone()
    if not booking:
        return None, "Booking reference not found."

    if booking["status"] == "cancelled":
        return None, "This booking has already been cancelled."

    slot_id = booking["slot_id"]
    now_iso = datetime.now(timezone.utc).isoformat()

    # Mark booking cancelled
    cur.execute("""
        UPDATE appointment_bookings
        SET status = 'cancelled', cancelled_at = ?, cancellation_reason = ?
        WHERE booking_ref = ?
    """, (now_iso, reason or "Cancelled by student", booking_ref))

    # Atomically release slot back to available
    cur.execute("""
        UPDATE appointment_slots
        SET is_booked = 0, status = 'available'
        WHERE id = ?
    """, (slot_id,))

    conn.commit()
    updated_booking = get_booking_by_ref(booking_ref, db_path=db_path)
    return updated_booking, None


def reschedule_appointment_booking(booking_ref, new_slot_id, db_path=None):
    """
    Reschedules an existing booking to a new slot atomically.
    Releases the old slot and reserves the new slot.
    """
    conn = get_db(db_path)
    cur = conn.cursor()

    cur.execute("SELECT * FROM appointment_bookings WHERE booking_ref = ?", (booking_ref,))
    booking = cur.fetchone()
    if not booking:
        return None, "Booking reference not found."

    if booking["status"] == "cancelled":
        return None, "Cannot reschedule a cancelled booking. Please book a new slot."

    old_slot_id = booking["slot_id"]
    if old_slot_id == new_slot_id:
        return None, "The selected slot is already your currently scheduled slot."

    # Attempt atomic lock on new slot
    cur.execute("""
        UPDATE appointment_slots
        SET is_booked = 1, status = 'booked'
        WHERE id = ? AND is_booked = 0 AND status = 'available'
    """, (new_slot_id,))

    if cur.rowcount == 0:
        return None, "The requested new slot is no longer available. Please select another slot."

    # Release old slot
    cur.execute("""
        UPDATE appointment_slots
        SET is_booked = 0, status = 'available'
        WHERE id = ?
    """, (old_slot_id,))

    # Update booking record
    cur.execute("""
        UPDATE appointment_bookings
        SET slot_id = ?, status = 'rescheduled'
        WHERE booking_ref = ?
    """, (new_slot_id, booking_ref))

    conn.commit()
    updated_booking = get_booking_by_ref(booking_ref, db_path=db_path)
    return updated_booking, None


# ============================================================================
# AI Career Chat Conversations Persistence
# ============================================================================

def save_ai_conversation(conv_id, session_id, provider, model, title, profile_shared=False, db_path=None):
    """Creates or updates an AI conversation header."""
    conn = get_db(db_path)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ai_conversations (id, session_id, provider, model, title, profile_shared, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(id) DO UPDATE SET
            provider = excluded.provider,
            model = excluded.model,
            title = excluded.title,
            profile_shared = excluded.profile_shared,
            updated_at = CURRENT_TIMESTAMP
    """, (conv_id, session_id, provider, model, title[:100], 1 if profile_shared else 0))
    conn.commit()
    return conv_id


def add_ai_message(conv_id, role, content, action_chips=None, db_path=None):
    """Appends a message to an AI conversation."""
    conn = get_db(db_path)
    cur = conn.cursor()
    chips_json = json.dumps(action_chips) if action_chips else None
    cur.execute("""
        INSERT INTO ai_messages (conversation_id, role, content, action_chips)
        VALUES (?, ?, ?, ?)
    """, (conv_id, role, content, chips_json))
    
    # Update conversation updated_at
    cur.execute("""
        UPDATE ai_conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?
    """, (conv_id,))
    conn.commit()
    return cur.lastrowid


def get_ai_conversations(session_id, limit=30, db_path=None):
    """Retrieves all conversation summaries for a specific session."""
    conn = get_db(db_path)
    cur = conn.cursor()
    rows = cur.execute("""
        SELECT id, session_id, provider, model, title, profile_shared, created_at, updated_at
        FROM ai_conversations
        WHERE session_id = ?
        ORDER BY updated_at DESC
        LIMIT ?
    """, (session_id, limit)).fetchall()
    return [dict(r) for r in rows]


def get_ai_messages(conv_id, session_id=None, db_path=None):
    """Retrieves all messages for a specific conversation with optional session verification."""
    conn = get_db(db_path)
    cur = conn.cursor()
    if session_id:
        conv = cur.execute("""
            SELECT id FROM ai_conversations WHERE id = ? AND session_id = ?
        """, (conv_id, session_id)).fetchone()
        if not conv:
            return None

    rows = cur.execute("""
        SELECT id, conversation_id, role, content, action_chips, created_at
        FROM ai_messages
        WHERE conversation_id = ?
        ORDER BY id ASC
    """, (conv_id,)).fetchall()

    result = []
    for r in rows:
        d = dict(r)
        if d.get("action_chips"):
            try:
                d["action_chips"] = json.loads(d["action_chips"])
            except Exception:
                d["action_chips"] = []
        else:
            d["action_chips"] = []
        result.append(d)
    return result


def delete_ai_conversation(conv_id, session_id, db_path=None):
    """Deletes an AI conversation and its messages belonging to a session."""
    conn = get_db(db_path)
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM ai_conversations WHERE id = ? AND session_id = ?
    """, (conv_id, session_id))
    deleted = cur.rowcount > 0
    conn.commit()
    return deleted


def clear_all_ai_conversations(session_id, db_path=None):
    """Clears all AI conversations for a session."""
    conn = get_db(db_path)
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM ai_conversations WHERE session_id = ?
    """, (session_id,))
    count = cur.rowcount
    conn.commit()
    return count



