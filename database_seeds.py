"""
CareerCompass Database Seeds
Comprehensive, authentic datasets for:
- Additional careers: B.Tech Civil Engineering, Sports Careers, Business & Commerce Careers
- Curated opportunities: Internships, Apprenticeships, Part-time, Campus roles
- Career Inspiration Quotes with field-specific guidance
- Custom stage-grouped Roadmaps including B.Tech Civil Engineering 11-step journey
"""

import json

# ============================================================================
# Additional Seed Careers
# ============================================================================

ADDITIONAL_CAREERS = [
    {
        "slug": "civil-engineer",
        "title": "Civil Engineer",
        "category": "Technology & Engineering",
        "short_description": "Plans, designs, constructs, and oversees vital infrastructure systems including buildings, transport networks, bridges, water supply, and smart urban structures.",
        "typical_responsibilities": json.dumps([
            "Prepare engineering drawings, structural blueprints, and site layouts using AutoCAD and BIM software",
            "Calculate structural load capacities, material takeoff quantities, and project cost estimates",
            "Supervise on-site construction operations in strict adherence to National Building Code (NBC) and IS codes",
            "Coordinate with structural consultants, geotechnical surveyors, municipal authorities, and project contractors",
            "Perform soil mechanics evaluation, surveying checks, and quality assurance testing of construction materials"
        ]),
        "relevant_interests": json.dumps(["engineering", "practical problem-solving", "design", "infrastructure", "construction"]),
        "relevant_strengths": json.dumps(["spatial reasoning", "analytical thinking", "project management", "practical problem-solving"]),
        "educational_requirements": "Bachelor's degree (B.Tech / B.E.) in Civil Engineering, or a 3-year State Polytechnic Diploma in Civil Engineering with lateral entry to B.Tech. Statutory municipal/chartered license required for signing structural blueprints.",
        "min_education_level": "Class 11–12",
        "suitable_streams": json.dumps(["Science - PCM", "Diploma in Civil Engineering", "Vocational Building Construction"]),
        "important_skills": json.dumps([
            "AutoCAD & 2D/3D Drafting",
            "Structural Analysis (STAAD.Pro / ETABS)",
            "Surveying & Total Station Operation",
            "Quantity Surveying & Estimation",
            "IS Codes (IS 456, IS 800) & NBC 2016",
            "Construction Project Planning (Primavera / MS Project)",
            "Site Safety Standards (OSHA / Safety Management)"
        ]),
        "suggested_beginner_projects": json.dumps([
            "Draft a 2BHK Residential Floor Plan and Structural Column Grid in AutoCAD or FreeCAD",
            "Create a Detailed Material Quantity Takeoff & Cost Estimation Sheet for a G+1 Building",
            "Conduct a Rainwater Harvesting & Stormwater Drainage Feasibility Study for Your Campus or Locality",
            "Evaluate a Local Construction Site's Safety Signage and PPE Compliance Against NBC 2016 Norms"
        ]),
        "learning_roadmap": json.dumps([
            {
                "step": 1,
                "title": "Understand Core Civil Engineering Subjects",
                "explanation": "Master fundamental physics, engineering mechanics, strength of materials, fluid mechanics, and plane surveying principles.",
                "action": "Complete NPTEL Strength of Materials or MIT OpenCourseWare mechanics lectures; solve 20 beam bending moment problems.",
                "duration": "4–6 weeks"
            },
            {
                "step": 2,
                "title": "Learn Engineering Drawing and CAD Fundamentals",
                "explanation": "Develop precision technical drafting skills in AutoCAD (or open-source FreeCAD/LibreCAD), understanding scale, layers, and orthographic projections.",
                "action": "Draft 5 floor plans and structural cross-sections with dimensioning and municipal title blocks.",
                "duration": "3–5 weeks"
            },
            {
                "step": 3,
                "title": "Practice Surveying and Site Measurement Basics",
                "explanation": "Understand leveling instruments, total station electronic measurement, GPS coordinates, and contour map interpretation.",
                "action": "Perform a closed traverse survey exercise on campus using a Dumpy level or digital measuring tool.",
                "duration": "3–4 weeks"
            },
            {
                "step": 4,
                "title": "Explore Core Disciplines & Sub-Fields",
                "explanation": "Survey structural engineering, geotechnical/soil mechanics, transportation & highway design, environmental hydrology, and construction management.",
                "action": "Read introductory case studies on bridge engineering, highway alignment, and soil bearing capacity.",
                "duration": "2–3 weeks"
            },
            {
                "step": 5,
                "title": "Complete a Beginner Civil Design Project",
                "explanation": "Apply theoretical knowledge to design a small residential building layout, calculate approximate column loads, and prepare a bill of quantities.",
                "action": "Produce an AutoCAD layout with structural grid and a complete material quantity schedule in Excel.",
                "duration": "4–6 weeks"
            },
            {
                "step": 6,
                "title": "Master Structural & BIM Software Tools",
                "explanation": "Learn modern industry computational tools: STAAD.Pro or ETABS for frame analysis, and Revit/BIM for 3D building information modeling using student licenses.",
                "action": "Model a 2-storey reinforced concrete portal frame in STAAD.Pro / ETABS under dead and live load combinations.",
                "duration": "4–6 weeks"
            },
            {
                "step": 7,
                "title": "Site Visits, Supervised Practical Experience & Internships",
                "explanation": "Gain first-hand field exposure through structured site visits, contractor internships, or government apprentice portals (NATS / AICTE).",
                "action": "Apply for a 4–8 week summer site internship via the NATS (MHRD) portal or state PWD approved contractor.",
                "duration": "6–8 weeks"
            },
            {
                "step": 8,
                "title": "Research Building Codes, Safety Regulations & Licensure",
                "explanation": "Study the National Building Code of India (NBC 2016), IS 456 (Plain & Reinforced Concrete), IS 800 (Steel), and site environmental/safety norms.",
                "action": "Download free public excerpts from the Bureau of Indian Standards (BIS) and review bar bending schedule standards.",
                "duration": "2–3 weeks"
            },
            {
                "step": 9,
                "title": "Prepare a Technical Resume and Project Portfolio",
                "explanation": "Synthesize your academic project reports, AutoCAD blueprints, structural calculation sheets, and internship certifications into an engineering portfolio.",
                "action": "Build a clean PDF engineering portfolio showcasing 2 design projects, site photos, and verified software proficiencies.",
                "duration": "2 weeks"
            },
            {
                "step": 10,
                "title": "Explore Entry-Level Pathways & Competitive Opportunities",
                "explanation": "Examine graduate engineer trainee (GET), site engineer, junior quantity surveyor, and public sector exam tracks (GATE, SSC-JE, State PSC-AE).",
                "action": "Map eligibility criteria for top infrastructure employers (L&T, Tata Projects, Afcons) and national competitive exams.",
                "duration": "3–4 weeks"
            },
            {
                "step": 11,
                "title": "Review Progress and Choose a Specialization",
                "explanation": "Decide on your long-term focus area: Structural Engineering, Transportation Systems, Geotechnical Engineering, or Project Management (NICMAR / MBA).",
                "action": "Consult faculty mentors and industry engineers; outline applications for higher study or specialized industry roles.",
                "duration": "Ongoing"
            }
        ]),
        "cost_category": "Moderate",
        "cost_estimate_detail": "State Govt Colleges / NITs: ₹1,50,000–₹4,50,000 total tuition; State Polytechnics: ₹20,000–₹60,000; Private Universities: ₹4,00,000–₹10,00,000.",
        "low_cost_routes": "Government polytechnics with 2nd-year lateral entry to B.Tech, NPTEL/SWAYAM free certified courses by IIT faculty, open educational drawing standards, and public library access to IS codes.",
        "entrance_exams": json.dumps(["JEE Main", "JEE Advanced", "State Engineering CETs (MHT CET, KCET, WBJEE, TANCET)", "GATE (for PSUs & M.Tech)", "SSC JE"]),
        "advantages": json.dumps([
            "Tangible, lasting societal impact creating vital physical infrastructure",
            "Diverse employment across public works departments, central PSUs (NHAI, BHEL, Railways), and leading private construction firms",
            "Global mobility opportunities in infrastructure development, smart cities, and sustainable urban renewal"
        ]),
        "challenges": json.dumps([
            "Demanding outdoor site working conditions with exposure to variable weather and dust",
            "Strict legal and safety liability for structural stability and human safety",
            "Starting entry-level stipends can be modest compared to the physical demands before gaining field experience"
        ]),
        "geographic_considerations": "High demand across metro construction corridors, developing tier-2/tier-3 cities, smart city initiatives, and national highway/railway projects.",
        "regulated": 1,
        "source_urls": json.dumps([
            {"title": "All India Council for Technical Education (AICTE)", "url": "https://www.aicte-india.org"},
            {"title": "National Apprenticeship Training Scheme (NATS)", "url": "http://mhrdnats.gov.in"},
            {"title": "Bureau of Indian Standards (BIS) Civil Codes", "url": "https://www.bis.gov.in"},
            {"title": "National Career Service (NCS) - Civil Engineering", "url": "https://www.ncs.gov.in"}
        ]),
        "last_verified": "2026-10-10"
    },
    {
        "slug": "sports-analyst",
        "title": "Sports Analyst & Performance Data Specialist",
        "category": "Sports & Fitness",
        "short_description": "Collects, processes, and evaluates athletic data, video footage, and match statistics to help coaches, athletes, and teams optimize performance and tactics.",
        "typical_responsibilities": json.dumps([
            "Tag match video footage to record tactical events, player movements, and scoring patterns",
            "Analyze GPS tracking metrics, heart-rate zones, and physical load data from wearable sensors",
            "Build visual dashboards and tactical reports for coaching staff and team management",
            "Conduct opposition scouting and predictive trend analysis before competitive matches"
        ]),
        "relevant_interests": json.dumps(["sports", "data analysis", "technology", "tactics"]),
        "relevant_strengths": json.dumps(["analytical thinking", "pattern recognition", "attention to detail", "communication"]),
        "educational_requirements": "Bachelor's in Sports Science, Data Analytics, Statistics, Computer Science, or Physical Education with proven video-tagging and data visualization proficiency.",
        "min_education_level": "Undergraduate",
        "suitable_streams": json.dumps(["Science - PCM", "Computer Science", "Physical Education", "Statistics / Economics"]),
        "important_skills": json.dumps(["Python / R", "Excel & Tableau / PowerBI", "Video Tagging Software (Hudl, Dartfish, Kinovea)", "Sports Tactics", "Data Storytelling"]),
        "suggested_beginner_projects": json.dumps([
            "Analyze a full football or cricket match using Kinovea (free video analysis tool) and generate an event map",
            "Create a public Tableau dashboard analyzing public IPL or Premier League player stats",
            "Draft a tactical scouting report on your school or college sports team's upcoming opponent"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Understand the Rules and Tactical Fundamentals", "explanation": "Deepen tactical awareness in your sport of interest beyond casual viewership.", "action": "Study official coaching manuals and tactical playbooks.", "duration": "3–4 weeks"},
            {"step": 2, "title": "Master Basic Video Analysis Tools", "explanation": "Learn open-source video annotation tools like Kinovea or OpenBroadcaster.", "action": "Tag 3 matches for key metrics (pass completion, pressure zones).", "duration": "4 weeks"},
            {"step": 3, "title": "Learn Sports Analytics in Python/R", "explanation": "Use pandas, seaborn, and matplotlib to analyze public match tracking datasets.", "action": "Complete a sports data project using Kaggle or StatsBomb open data.", "duration": "6 weeks"},
            {"step": 4, "title": "Build a Public Analysis Portfolio", "explanation": "Share tactical breakdowns on LinkedIn, Substack, or GitHub.", "action": "Publish 3 visual analytical breakdowns of recent matches.", "duration": "4 weeks"},
            {"step": 5, "title": "Pursue Internships with Academies or Teams", "explanation": "Offer video-analysis assistance to local sports academies, college teams, or grassroots clubs.", "action": "Apply to sports analytics internships at clubs or sports media outlets.", "duration": "Ongoing"}
        ]),
        "cost_category": "Low / Free Accessible",
        "cost_estimate_detail": "State Universities: ₹30,000–₹1,20,000; Open data & self-taught portfolio: ₹0–₹15,000 for software certifications.",
        "low_cost_routes": "StatsBomb open data, Coursera/edX audited courses, Kaggle sports datasets, free Kinovea software.",
        "entrance_exams": json.dumps(["University Entrance Tests (CUET)", "NIMCET / General Data Science entrance"]),
        "advantages": json.dumps([
            "Allows passionate sports enthusiasts to work directly in professional sports environments",
            "High demand as franchises and national federations increasingly rely on data-driven coaching",
            "Transferable data science and visualization skills applicable to tech and finance"
        ]),
        "challenges": json.dumps([
            "Irregular hours including weekend matches, late-night video tagging, and heavy travel schedules",
            "Requires ability to communicate technical numbers simply to athletes and traditional coaches",
            "Niche entry-level hiring with reliance on demonstrable portfolio proof-of-work"
        ]),
        "geographic_considerations": "Centred around sports franchises (IPL, ISL, PKL), national sports institutes, sports media hubs, and high-performance academies.",
        "regulated": 0,
        "source_urls": json.dumps([
            {"title": "Sports Authority of India (SAI)", "url": "https://sportsauthorityofindia.nic.in"},
            {"title": "StatsBomb Open Football Data", "url": "https://statsbomb.com/what-we-do/hub/free-data/"},
            {"title": "National Institute of Sports (NIS Patiala)", "url": "https://nsnis.org"}
        ]),
        "last_verified": "2026-10-10"
    },
    {
        "slug": "sports-physiotherapist",
        "title": "Sports Physiotherapist",
        "category": "Sports & Fitness",
        "short_description": "Specializes in injury prevention, on-field emergency care, rehabilitation, and biomechanical optimization for athletes and active individuals.",
        "typical_responsibilities": json.dumps([
            "Assess acute athletic injuries and administer on-field emergency treatment (taping, splinting, cryotherapy)",
            "Design tailored rehabilitation and conditioning protocols to restore athletic function",
            "Conduct musculoskeletal screenings and biomechanical gait analysis to mitigate injury risk",
            "Collaborate with strength & conditioning coaches, orthopaedic surgeons, and team nutritionists"
        ]),
        "relevant_interests": json.dumps(["sports", "biology", "human anatomy", "healthcare", "rehabilitation"]),
        "relevant_strengths": json.dumps(["empathy", "anatomical understanding", "hands-on clinical skill", "quick decision-making under pressure"]),
        "educational_requirements": "MANDATORY STATUTORY REQUIREMENT: Bachelor of Physiotherapy (BPT - 4.5 years including clinical internship), followed by Master of Physiotherapy (MPT in Sports) and registration with the National Commission for Allied and Healthcare Professions (NCAHP) / State Physiotherapy Council.",
        "min_education_level": "Undergraduate",
        "suitable_streams": json.dumps(["Science - PCB (Physics, Chemistry, Biology)"]),
        "important_skills": json.dumps(["Musculoskeletal Assessment", "Manual Therapy & Taping", "Exercise Physiology", "Emergency Field Care", "Biomechanics & Gait Analysis"]),
        "suggested_beginner_projects": json.dumps([
            "Shadow a licensed physiotherapist at a local sports clinic or hospital for 10 hours",
            "Create an illustrated guide to common sports injuries (ACL sprains, rotator cuff strains) and preventative warmups",
            "Complete a certified Red Cross or St. John Ambulance Sports First Aid & CPR training workshop"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Complete Class 12 with PCB", "explanation": "Secure eligibility in Physics, Chemistry, and Biology with minimum 50% marks.", "action": "Prepare for university entrance exams (NEET / State Allied Health CETs).", "duration": "High school"},
            {"step": 2, "title": "Enroll in Accredited BPT Degree", "explanation": "Complete 4 years of academic study covering anatomy, physiology, biomechanics, and pathology.", "action": "Maintain high clinical scores across orthopaedic and neurological modules.", "duration": "4 years"},
            {"step": 3, "title": "Complete Mandatory 6-Month Rotational Internship", "explanation": "Gain hands-on clinical exposure in orthopaedics, ICU, sports outpatient, and general medicine.", "action": "Obtain provisional clinical registration upon degree completion.", "duration": "6 months"},
            {"step": 4, "title": "Pursue MPT in Sports / Fellowship", "explanation": "Specialize in athletic injury management, on-field emergency care, and return-to-play protocols.", "action": "Gain experience with university or district athletic teams.", "duration": "2 years"},
            {"step": 5, "title": "Obtain Official Council Registration & Team Role", "explanation": "Register with State Allied Health Council and apply for sports academy or franchise positions.", "action": "Build network with sports clubs and national federation academies.", "duration": "Ongoing"}
        ]),
        "cost_category": "High / Regulated",
        "cost_estimate_detail": "Govt Medical Colleges: ₹40,000–₹1,50,000 total BPT tuition; Private Institutions: ₹4,00,000–₹9,00,000 total.",
        "low_cost_routes": "Government medical colleges and state university physiotherapy departments offer highly subsidized education through competitive merit exams.",
        "entrance_exams": json.dumps(["NEET-UG (in select states/universities)", "State Allied Health Sciences CETs", "Institutional BPT Entrance Exams"]),
        "advantages": json.dumps([
            "Direct clinical contribution to athlete wellness and high-performance recovery",
            "Statutory licensed profession with dual opportunities in sports teams and private clinical practice",
            "Evergreen demand across private sports clinics, gyms, fitness centres, and hospital orthopaedics"
        ]),
        "challenges": json.dumps([
            "Strict qualification requirements: interest in sports alone cannot bypass mandatory 4.5-year clinical degree",
            "Physical stamina required for long standing hours, manual therapy, and on-field emergency sprints",
            "High emotional pressure when managing star athletes before crucial tournament fixtures"
        ]),
        "geographic_considerations": "Widespread across all major cities, district sports complexes, SAI training centres, and private rehabilitation clinics.",
        "regulated": 1,
        "source_urls": json.dumps([
            {"title": "National Commission for Allied and Healthcare Professions (NCAHP)", "url": "https://ncahp.gov.in"},
            {"title": "Indian Association of Physiotherapists (IAP)", "url": "https://www.iapindia.org"},
            {"title": "World Physiotherapy - Sports Specialty", "url": "https://world.physio"}
        ]),
        "last_verified": "2026-10-10"
    },
    {
        "slug": "sports-coach",
        "title": "Athletic Coach & Sports Trainer",
        "category": "Sports & Fitness",
        "short_description": "Guides athletes and teams in skill development, tactical play, physical conditioning, and mental resilience across grassroots, school, or elite competitive levels.",
        "typical_responsibilities": json.dumps([
            "Plan and conduct structured training sessions focusing on athletic technique, tactics, and team strategy",
            "Assess individual athlete strengths, weaknesses, and fitness benchmarks to personalize coaching plans",
            "Promote athlete safety, fair play, injury prevention, and positive sportsmanship",
            "Manage tournament logistics, match rosters, and post-game performance evaluations"
        ]),
        "relevant_interests": json.dumps(["sports", "teaching", "leadership", "mentoring", "fitness"]),
        "relevant_strengths": json.dumps(["communication", "leadership", "motivation", "patience", "strategic thinking"]),
        "educational_requirements": "Bachelor's in Physical Education (B.P.Ed) or sports degree, combined with accredited National Sports Federation / SAI / Netaji Subhas National Institute of Sports (NSNIS) coaching certification (Certificate/Diploma in Sports Coaching).",
        "min_education_level": "Undergraduate",
        "suitable_streams": json.dumps(["Physical Education", "Any stream with competitive playing credentials", "Sports Science"]),
        "important_skills": json.dumps(["Tactical Instruction", "Drill Design", "Motivation & Psychology", "First Aid & CPR", "Performance Review"]),
        "suggested_beginner_projects": json.dumps([
            "Volunteer as an assistant coach for a junior team in your school, college, or neighborhood club",
            "Design a 4-week fitness and skill progression plan for beginners in your sport of choice",
            "Complete an introductory Level 1 grassroot coaching certification from your state or national federation"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Build Competitive Playing Experience", "explanation": "Active participation at district, state, or university level establishes practical game insight.", "action": "Compete actively in recognized school or club tournaments.", "duration": "Ongoing"},
            {"step": 2, "title": "Obtain First Aid and Grassroots Certification", "explanation": "Learn emergency safety protocols and complete grassroots federation coaching modules.", "action": "Complete Red Cross CPR and state sports federation Level 1 course.", "duration": "2–4 weeks"},
            {"step": 3, "title": "Complete B.P.Ed or NIS Diploma", "explanation": "Enroll in an NCTE-approved Bachelor of Physical Education (B.P.Ed) or NSNIS Diploma in Coaching.", "action": "Study sports pedagogy, training methodology, and biomechanics.", "duration": "1–2 years"},
            {"step": 4, "title": "Gain Supervised Assistant Coaching Experience", "explanation": "Work under senior licensed coaches in sports academies, schools, or university teams.", "action": "Log 100+ hours of supervised coaching time.", "duration": "6 months"},
            {"step": 5, "title": "Advance Coaching Licenses & Lead Programs", "explanation": "Pursue higher license grades (e.g., AFC/FIFA licenses in football, BCCI levels in cricket).", "action": "Take head coaching responsibility for academy or competitive school squads.", "duration": "Ongoing"}
        ]),
        "cost_category": "Low / Free Accessible",
        "cost_estimate_detail": "Govt Universities (B.P.Ed / NSNIS): ₹25,000–₹80,000 total; Federation courses: ₹5,000–₹35,000 per license level.",
        "low_cost_routes": "Government Physical Education colleges (LNIPE Gwalior, NSNIS Patiala), state university departments, and subsidized SAI scholarships.",
        "entrance_exams": json.dumps(["B.P.Ed Physical Fitness Test & Entrance", "NSNIS Coaching Admission Aptitude Test"]),
        "advantages": json.dumps([
            "Mentoring next-generation youth and seeing direct personal growth and athletic achievement",
            "High personal job satisfaction working in active, outdoor, and competitive settings",
            "Steady opportunities across private academies, K-12 schools, universities, and government sports hostels"
        ]),
        "challenges": json.dumps([
            "Early mornings, late evenings, and heavy weekend match commitments",
            "Seasonal competition pressures and parent/management performance expectations",
            "Requires ongoing physical fitness and personal demonstrations"
        ]),
        "geographic_considerations": "Abundant across all districts in schools, private sports complexes, residential academies, and SAI training centres.",
        "regulated": 0,
        "source_urls": json.dumps([
            {"title": "Netaji Subhas National Institute of Sports (NSNIS Patiala)", "url": "https://nsnis.org"},
            {"title": "Lakshmibai National Institute of Physical Education (LNIPE)", "url": "https://www.lnipe.edu.in"},
            {"title": "Khelo India Portal", "url": "https://kheloindia.gov.in"}
        ]),
        "last_verified": "2026-10-10"
    },
    {
        "slug": "sports-event-manager",
        "title": "Sports Event & Facility Manager",
        "category": "Sports & Fitness",
        "short_description": "Organizes, promotes, and executes sports tournaments, marathon events, school leagues, and stadium operations with focus on logistics, safety, and spectator experience.",
        "typical_responsibilities": json.dumps([
            "Coordinate tournament logistics: venue booking, playing equipment, referee scheduling, and team hospitality",
            "Manage tournament budgets, vendor contracts, ticketing, and brand sponsorship deliverables",
            "Ensure participant safety, emergency medical support, security protocols, and crowd management",
            "Oversee sports facility maintenance, turf care, and booking management systems"
        ]),
        "relevant_interests": json.dumps(["sports", "event planning", "business", "operations", "communication"]),
        "relevant_strengths": json.dumps(["organization", "multitasking", "negotiation", "problem-solving under pressure"]),
        "educational_requirements": "Bachelor's degree in Event Management, Sports Management, Business Administration (BBA), or Physical Education with demonstrable tournament coordination experience.",
        "min_education_level": "Undergraduate",
        "suitable_streams": json.dumps(["Commerce", "Humanities / Arts", "Business Administration", "Physical Education"]),
        "important_skills": json.dumps(["Logistics & Operations", "Budgeting & Vendor Management", "Sponsorship & Marketing", "Risk Management", "Public Relations"]),
        "suggested_beginner_projects": json.dumps([
            "Coordinate logistics for an inter-college or neighborhood 8-team cricket/football tournament",
            "Prepare a comprehensive budget, fixture schedule, and safety checklist for a 5K community run",
            "Audit a local sports facility or gym's booking efficiency and propose an online scheduling improvement"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Understand Tournament Operations", "explanation": "Learn bracket structures (knockout, round-robin, Swiss) and scheduling guidelines.", "action": "Organize a small school or campus tournament using free bracket software.", "duration": "3 weeks"},
            {"step": 2, "title": "Volunteer at Major Sporting Events", "explanation": "Gain frontline exposure to ticketing, accreditation, and athlete hospitality.", "action": "Volunteer for marathon, state championship, or franchise league games.", "duration": "Ongoing"},
            {"step": 3, "title": "Study Sports Management / Business Fundamentals", "explanation": "Learn vendor contracting, sponsorship fulfillment, and facility operations.", "action": "Complete a course in sports management or event logistics.", "duration": "4–6 months"},
            {"step": 4, "title": "Master Health, Safety & Permitting Protocols", "explanation": "Understand municipal permissions, crowd control, and emergency medical protocols.", "action": "Shadow event coordinators at a district sports complex.", "duration": "4 weeks"},
            {"step": 5, "title": "Lead Operations for Commercial or Federation Events", "explanation": "Take full responsibility for venue management, sponsor activations, or league operations.", "action": "Apply to sports management agencies, leagues, or facility operators.", "duration": "Ongoing"}
        ]),
        "cost_category": "Moderate",
        "cost_estimate_detail": "State Universities (BBA / B.Com): ₹40,000–₹1,50,000 total; Specialized Private Sports Management Institutes: ₹2,50,000–₹7,00,000.",
        "low_cost_routes": "General BBA / B.Com degrees in public universities, combined with active volunteer credentials at grassroots and municipal sports meets.",
        "entrance_exams": json.dumps(["CUET (UG)", "State Management CETs", "Institutional BBA Entrance Exams"]),
        "advantages": json.dumps([
            "Vibrant, energetic work atmosphere surrounded by live competitive action",
            "Rapid expansion of franchise leagues, marathon circuits, and corporate sports leagues across India",
            "Broadly transferable project management, vendor negotiation, and marketing skill set"
        ]),
        "challenges": json.dumps([
            "High-stress execution days with unpredictable weather, delays, and last-minute emergencies",
            "Extended physical hours on event days with early morning setups and late breakdowns",
            "Requires diplomatic handling of competing demands from sponsors, referees, and team managers"
        ]),
        "geographic_considerations": "Major metropolitan centres, state capital sports hubs, stadium facilities, and recreational marathon destination circuits.",
        "regulated": 0,
        "source_urls": json.dumps([
            {"title": "International Institute of Sports & Management (IISM)", "url": "https://www.iismworld.com"},
            {"title": "Fit India Movement", "url": "https://fitindia.gov.in"},
            {"title": "National Career Service - Event Management", "url": "https://www.ncs.gov.in"}
        ]),
        "last_verified": "2026-10-10"
    },
    {
        "slug": "sports-science-specialist",
        "title": "Sports Science Specialist & Exercise Physiologist",
        "category": "Sports & Fitness",
        "short_description": "Applies scientific principles of physiology, biomechanics, psychology, and nutrition to enhance human athletic performance and recovery.",
        "typical_responsibilities": json.dumps([
            "Conduct VO2 max, lactate threshold, and metabolic testing on competitive athletes",
            "Analyze movement biomechanics using force plates, high-speed cameras, and motion sensors",
            "Develop periodized strength, conditioning, and recovery regimens with coaching staff",
            "Monitor hydration, sleep metrics, and fatigue biomarkers to prevent overtraining syndrome"
        ]),
        "relevant_interests": json.dumps(["science", "sports", "biology", "human physiology", "research"]),
        "relevant_strengths": json.dumps(["analytical thinking", "scientific method", "precision measurement", "communication"]),
        "educational_requirements": "B.Sc. in Sports Science, Exercise Physiology, or Physical Education, ideally followed by M.Sc. in Sports Science or Human Performance.",
        "min_education_level": "Undergraduate",
        "suitable_streams": json.dumps(["Science - PCB / PCM", "Physical Education with Science electives"]),
        "important_skills": json.dumps(["Exercise Physiology", "Biomechanics Lab Equipment", "Strength & Conditioning (CSCS)", "Data Analysis in Sports", "Fatigue Monitoring"]),
        "suggested_beginner_projects": json.dumps([
            "Conduct a structured 4-week resting heart-rate and recovery tracking experiment on yourself or friends",
            "Analyze vertical jump biomechanics using high-speed smartphone video and Kinovea angle measurements",
            "Review a published sports science study on hydration strategies and write a 2-page student summary"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Build Strong Foundation in Biology & Physics", "explanation": "Master muscle anatomy, cardiovascular systems, and Newton's laws applied to motion.", "action": "Complete high school biology and physics with emphasis on mechanics and human body.", "duration": "High school"},
            {"step": 2, "title": "Pursue B.Sc. in Sports Science or Human Kinetics", "explanation": "Study exercise physiology, biomechanics, motor control, and sports nutrition.", "action": "Maintain active laboratory research participation during college.", "duration": "3 years"},
            {"step": 3, "title": "Obtain Strength & Conditioning Certifications", "explanation": "Pursue recognized certifications such as NSCA CSCS (Certified Strength and Conditioning Specialist).", "action": "Study periodization and Olympic lifting safety guidelines.", "duration": "3–6 months"},
            {"step": 4, "title": "Gain Clinical / High-Performance Lab Experience", "explanation": "Intern at sports institutes (SAI centres, Olympic training hubs, cricket state associations).", "action": "Assist with VO2 max testing, force-plate assessments, and GPS telemetry.", "duration": "6 months"},
            {"step": 5, "title": "Advance to Team Science or Research Roles", "explanation": "Lead sports science departments at franchise teams, state academies, or universities.", "action": "Publish applied findings or present at sports science conferences.", "duration": "Ongoing"}
        ]),
        "cost_category": "Moderate",
        "cost_estimate_detail": "State Universities & Central Sports Universities: ₹35,000–₹1,20,000 total; Private specialized colleges: ₹2,00,000–₹6,00,000.",
        "low_cost_routes": "National Sports University (Manipur), LNIPE Gwalior, state central universities, and free research papers via PubMed Central / Google Scholar.",
        "entrance_exams": json.dumps(["CUET (UG)", "National Sports University Entrance Examination (NSU EE)"]),
        "advantages": json.dumps([
            "Combines passion for sports with rigorous empirical laboratory and field science",
            "Growing demand as national sports programs invest in modern performance labs",
            "Opportunity to directly impact national and international athletic achievements"
        ]),
        "challenges": json.dumps([
            "High-level roles typically require Master's degree (M.Sc.) or doctoral qualification",
            "Limited number of advanced high-performance labs in tier-2/3 regions",
            "Must navigate traditional coaching cultures that may initially resist scientific intervention"
        ]),
        "geographic_considerations": "Centred around national sports hubs (SAI centres, NIS Patiala, National Sports University), elite private academies, and metro medical universities.",
        "regulated": 0,
        "source_urls": json.dumps([
            {"title": "National Sports University (NSU Manipur)", "url": "https://www.nsu.ac.in"},
            {"title": "Sports Authority of India - High Performance Labs", "url": "https://sportsauthorityofindia.nic.in"},
            {"title": "National Strength and Conditioning Association (NSCA)", "url": "https://www.nsca.com"}
        ]),
        "last_verified": "2026-10-10"
    },
    {
        "slug": "marketing-specialist",
        "title": "Marketing Specialist & Brand Strategist",
        "category": "Business & Finance",
        "short_description": "Develops and executes marketing campaigns, brand messaging, customer acquisition strategies, and market research to connect products with target audiences.",
        "typical_responsibilities": json.dumps([
            "Conduct audience research and competitor benchmarking to identify customer personas",
            "Plan and execute multichannel campaigns across digital, content, email, and social media",
            "Analyze campaign metrics: cost per acquisition (CPA), conversion rates, and return on ad spend (ROAS)",
            "Collaborate with graphic designers, copywriters, and product managers to launch brand initiatives"
        ]),
        "relevant_interests": json.dumps(["business", "creativity", "communication", "psychology", "writing"]),
        "relevant_strengths": json.dumps(["creativity", "storytelling", "analytical thinking", "empathy", "adaptability"]),
        "educational_requirements": "Bachelor's degree in Business Administration (BBA), Commerce (B.Com), Mass Communication, or any undergraduate degree with demonstrable campaign portfolio or certifications.",
        "min_education_level": "Undergraduate",
        "suitable_streams": json.dumps(["Commerce", "Humanities / Arts", "Science", "Any stream with digital portfolio"]),
        "important_skills": json.dumps(["Digital Marketing & SEO", "Content Creation & Copywriting", "Data Analytics (Google Analytics / Meta)", "Brand Strategy", "Customer Psychology"]),
        "suggested_beginner_projects": json.dumps([
            "Create a mock marketing launch strategy for an eco-friendly student product with Instagram & email copy",
            "Audit a local small business's social media presence and suggest 5 measurable improvements",
            "Complete free Google Digital Garage certification and launch a test blog with basic SEO"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Understand Marketing Fundamentals", "explanation": "Study the 4 Ps (Product, Price, Place, Promotion), positioning, and consumer decision journey.", "action": "Complete free Google Digital Garage Fundamentals of Digital Marketing.", "duration": "3–4 weeks"},
            {"step": 2, "title": "Learn Content and Copywriting", "explanation": "Master persuasive writing, headline formulas, and content structuring.", "action": "Write 5 sample campaign landing page copy drafts for different industries.", "duration": "3 weeks"},
            {"step": 3, "title": "Master Analytics and Paid Channels", "explanation": "Learn Google Analytics 4, Meta Ads Manager basics, and email marketing tools (Mailchimp).", "action": "Set up a test analytics dashboard and track mock campaign funnels.", "duration": "4 weeks"},
            {"step": 4, "title": "Execute a Practical Campaign or Internship", "explanation": "Manage social media or marketing for a college club, local business, or startup internship.", "action": "Apply to marketing internships via university placement or AICTE portals.", "duration": "6–8 weeks"},
            {"step": 5, "title": "Build a Measurable Portfolio", "explanation": "Document results with metrics: reach generated, engagement lift, or leads delivered.", "action": "Publish a visual case study PDF detailing your campaign results.", "duration": "Ongoing"}
        ]),
        "cost_category": "Low / Free Accessible",
        "cost_estimate_detail": "State Universities: ₹30,000–₹1,20,000 total degree tuition; Free certifications from Google, HubSpot, Meta.",
        "low_cost_routes": "HubSpot Academy free certifications, Google Digital Garage, open educational marketing case studies, public library business books.",
        "entrance_exams": json.dumps(["CUET (UG)", "State University Management CETs"]),
        "advantages": json.dumps([
            "Strong versatility: every enterprise, startup, non-profit, and institution requires marketing",
            "High creative freedom combined with data-driven feedback",
            "Abundant remote and freelance opportunities alongside corporate agency careers"
        ]),
        "challenges": json.dumps([
            "Rapid algorithm shifts across digital platforms requiring continuous upskilling",
            "Constant pressure to demonstrate direct commercial return on marketing investment",
            "Creative burnout during high-volume campaign cycles"
        ]),
        "geographic_considerations": "Widespread across all business centres, agency hubs, startup corridors, with widespread remote work availability.",
        "regulated": 0,
        "source_urls": json.dumps([
            {"title": "HubSpot Academy Free Certifications", "url": "https://academy.hubspot.com"},
            {"title": "Google Digital Garage", "url": "https://learndigital.withgoogle.com"},
            {"title": "National Career Service - Marketing", "url": "https://www.ncs.gov.in"}
        ]),
        "last_verified": "2026-10-10"
    },
    {
        "slug": "hr-specialist",
        "title": "Human Resources (HR) & Talent Specialist",
        "category": "Business & Finance",
        "short_description": "Manages talent recruitment, employee relations, workplace culture, onboarding, training, and statutory compliance within organizations.",
        "typical_responsibilities": json.dumps([
            "Source, screen, and interview candidates for open job positions",
            "Facilitate employee onboarding, performance appraisal cycles, and team training workshops",
            "Address employee grievances and mediate workplace conflict to foster an inclusive culture",
            "Ensure adherence to statutory labour regulations, employment contracts, and workplace safety norms"
        ]),
        "relevant_interests": json.dumps(["people", "psychology", "organization", "business", "communication"]),
        "relevant_strengths": json.dumps(["empathy", "communication", "conflict resolution", "organization", "discretion"]),
        "educational_requirements": "Bachelor's degree in Business Administration (BBA), Psychology, Commerce, or Humanities; followed by MBA in Human Resources or Postgraduate Diploma in HR (PGDM).",
        "min_education_level": "Undergraduate",
        "suitable_streams": json.dumps(["Commerce", "Humanities / Arts", "Psychology", "Business Administration"]),
        "important_skills": json.dumps(["Talent Acquisition", "Employee Relations", "HR Information Systems (HRIS)", "Labour Law & Compliance", "Conflict Mediation", "Performance Management"]),
        "suggested_beginner_projects": json.dumps([
            "Draft a comprehensive job description, interview rubric, and onboarding checklist for a campus club role",
            "Conduct an employee well-being and engagement survey for a team or student body",
            "Review key statutory labour welfare provisions in India (Factories Act, POSH Act) and prepare a summary guide"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Understand Organizational Behaviour & Psychology", "explanation": "Study motivation theories, team dynamics, and workplace culture.", "action": "Read foundational texts on organizational behaviour.", "duration": "4 weeks"},
            {"step": 2, "title": "Learn Recruitment and Interviewing Techniques", "explanation": "Master competency-based interviewing, boolean search sourcing, and applicant tracking systems (ATS).", "action": "Conduct 3 mock behavioural interviews with structured rubrics.", "duration": "3 weeks"},
            {"step": 3, "title": "Study Labour Laws and Workplace Compliance", "explanation": "Understand POSH compliance, minimum wages, leave policies, and employment contracts.", "action": "Complete a certified online module in Indian labour compliance.", "duration": "4 weeks"},
            {"step": 4, "title": "Gain Practical HR Internship Experience", "explanation": "Work in recruitment sourcing, campus hiring coordination, or HR operations.", "action": "Apply to HR internships via college placement or official portals.", "duration": "6–8 weeks"},
            {"step": 5, "title": "Pursue Advanced HR Certifications or MBA", "explanation": "Evaluate MBA in HR or SHRM/HRCI recognized certifications to access strategic HR partner roles.", "action": "Prepare for national management entrance exams (CAT, XAT, CMAT).", "duration": "Ongoing"}
        ]),
        "cost_category": "Moderate",
        "cost_estimate_detail": "State Universities: ₹30,000–₹1,50,000 total; Top Management Institutes: ₹4,00,000–₹18,00,000.",
        "low_cost_routes": "Government university BBA / Psychology degrees, free Coursera audited HR courses, and direct entry via recruitment agency roles.",
        "entrance_exams": json.dumps(["CUET (UG)", "CAT / CMAT / MAT (for Postgraduate MBA)"]),
        "advantages": json.dumps([
            "Central role in shaping workplace culture, supporting human careers, and fostering fair environments",
            "Stable corporate demand across IT, manufacturing, healthcare, education, and retail",
            "Clear career progression from recruiter to HR Business Partner to Chief People Officer"
        ]),
        "challenges": json.dumps([
            "Delicate responsibility of balancing employee welfare with company business targets",
            "Challenging situations during organizational restructuring, layoffs, or disciplinary investigations",
            "Requires high emotional resilience and neutrality in conflict mediation"
        ]),
        "geographic_considerations": "Present in every corporate office, manufacturing plant, hospital, university, and multinational branch.",
        "regulated": 0,
        "source_urls": json.dumps([
            {"title": "Society for Human Resource Management (SHRM India)", "url": "https://www.shrm.org/in"},
            {"title": "National Institute of Personnel Management (NIPM India)", "url": "https://nipm.in"},
            {"title": "Ministry of Labour & Employment", "url": "https://labour.gov.in"}
        ]),
        "last_verified": "2026-10-10"
    },
    {
        "slug": "supply-chain-manager",
        "title": "Operations & Supply Chain Manager",
        "category": "Business & Finance",
        "short_description": "Oversees the end-to-end flow of goods, raw materials, inventory, and logistics from suppliers to end customers with focus on speed, cost, and reliability.",
        "typical_responsibilities": json.dumps([
            "Coordinate procurement, vendor supplier management, and purchase order fulfillment",
            "Manage warehouse inventory levels, demand forecasting, and storage logistics",
            "Optimize transportation routes, freight costs, and customs/transit compliance",
            "Implement lean operations and quality assurance to minimize waste and bottlenecks"
        ]),
        "relevant_interests": json.dumps(["business", "logistics", "problem-solving", "efficiency", "operations"]),
        "relevant_strengths": json.dumps(["analytical thinking", "organization", "process optimization", "negotiation", "calm under pressure"]),
        "educational_requirements": "Bachelor's in Engineering, Commerce (B.Com), Business Administration (BBA), or Logistics & Supply Chain Management; followed by MBA in Operations / SCM.",
        "min_education_level": "Undergraduate",
        "suitable_streams": json.dumps(["Commerce", "Science / Engineering", "Business Administration"]),
        "important_skills": json.dumps(["Logistics & Freight Management", "Inventory Control (ERP / SAP)", "Demand Forecasting & Excel", "Vendor Negotiation", "Lean / Six Sigma Principles"]),
        "suggested_beginner_projects": json.dumps([
            "Map the supply chain journey of a daily item (e.g., your smartphone or milk) from raw material to shelf",
            "Build an Excel inventory tracker with automatic reorder triggers and safety stock calculations",
            "Audit a local retail store or warehouse's shelf-restocking process and propose an efficiency improvement"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Understand Supply Chain Fundamentals", "explanation": "Learn procurement, inventory holding costs, logistics modes, and bullwhip effect.", "action": "Complete MIT OpenCourseWare or Coursera Supply Chain Fundamentals course.", "duration": "4 weeks"},
            {"step": 2, "title": "Master Inventory & Logistics Modeling in Excel", "explanation": "Build models for Economic Order Quantity (EOQ), safety stock, and transportation routing.", "action": "Complete 3 spreadsheet inventory simulations with fluctuating demand.", "duration": "4 weeks"},
            {"step": 3, "title": "Learn ERP Systems and Quality Principles", "explanation": "Understand Enterprise Resource Planning (SAP / Oracle) and Lean Six Sigma methodologies.", "action": "Earn an introductory Lean Six Sigma White/Yellow belt certification.", "duration": "3 weeks"},
            {"step": 4, "title": "Gain Practical Operations or Warehouse Internship", "explanation": "Work in warehouse operations, dispatch tracking, or vendor coordination.", "action": "Apply to supply chain internships at e-commerce, retail, or FMCG firms.", "duration": "6–8 weeks"},
            {"step": 5, "title": "Advance to Operations Management Roles", "explanation": "Lead end-to-end supply chain planning or logistics operations.", "action": "Prepare for APICS CSCP (Certified Supply Chain Professional) certification.", "duration": "Ongoing"}
        ]),
        "cost_category": "Moderate",
        "cost_estimate_detail": "State Universities: ₹30,000–₹1,50,000 total; Specialized Operations MBA: ₹3,00,000–₹12,00,000.",
        "low_cost_routes": "Government university B.Com/BBA degrees, free MIT SCM OpenCourseWare lectures, and entry via logistics trainee positions.",
        "entrance_exams": json.dumps(["CUET (UG)", "CAT / CMAT (for MBA in Operations)"]),
        "advantages": json.dumps([
            "Massive expansion driven by e-commerce, quick commerce, global manufacturing, and infrastructure corridors",
            "Highly tangible, visible impact keeping commerce, medicines, and consumer goods moving seamlessly",
            "High demand across retail, automotive, pharmaceutical, technology, and export sectors"
        ]),
        "challenges": json.dumps([
            "High vulnerability to external disruptions (weather, geopolitical conflicts, fuel price spikes)",
            "demanding pressure when supply bottlenecks threaten factory production or customer delivery dates",
            "May involve shifts across 24/7 operating distribution hubs and fulfillment centres"
        ]),
        "geographic_considerations": "Centered around major logistics hubs, port cities, industrial manufacturing clusters, and e-commerce fulfillment hubs.",
        "regulated": 0,
        "source_urls": json.dumps([
            {"title": "National Logistics Portal (Marine & Trade)", "url": "https://www.nlp.gov.in"},
            {"title": "Association for Supply Chain Management (ASCM / APICS)", "url": "https://www.ascm.org"},
            {"title": "National Career Service - Logistics", "url": "https://www.ncs.gov.in"}
        ]),
        "last_verified": "2026-10-10"
    },
    {
        "slug": "product-manager",
        "title": "Product Manager",
        "category": "Business & Finance",
        "short_description": "Guides the success of a product and leads the cross-functional team responsible for improving it, balancing user needs, technical feasibility, and business viability.",
        "typical_responsibilities": json.dumps([
            "Define the product vision, roadmap, and feature requirements based on user research and analytics",
            "Collaborate cross-functionally with software engineers, UX designers, marketing, and executives",
            "Analyze user metrics, feature adoption, churn rates, and feedback to prioritize backlog sprints",
            "Conduct customer discovery interviews and usability tests to validate product hypotheses"
        ]),
        "relevant_interests": json.dumps(["technology", "business", "design", "problem-solving", "psychology"]),
        "relevant_strengths": json.dumps(["strategic thinking", "prioritization", "communication", "empathy", "data literacy"]),
        "educational_requirements": "Bachelor's degree in Computer Science, Engineering, Business, or Design; often complemented by MBA or demonstrable experience transitioning from engineering, design, or business analysis.",
        "min_education_level": "Undergraduate",
        "suitable_streams": json.dumps(["Computer Science", "Engineering", "Commerce / Business", "Design"]),
        "important_skills": json.dumps(["User Research & Wireframing", "Product Analytics (Mixpanel / GA)", "Agile / Scrum Methodology", "Roadmap Strategy (Jira / Linear)", "SQL & Business Modeling"]),
        "suggested_beginner_projects": json.dumps([
            "Write a complete Product Requirement Document (PRD) for a new feature on a tool you use daily (e.g., Spotify, WhatsApp)",
            "Conduct 5 customer discovery interviews about an annoying student problem and draft a solution concept",
            "Create a visual wireframe prototype in Figma demonstrating an onboarding flow for a student study app"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Understand Product Thinking and User Discovery", "explanation": "Learn the triad of Product: User Experience, Technology feasibility, and Business viability.", "action": "Read 'Inspired' by Marty Cagan and complete free product teardowns.", "duration": "4 weeks"},
            {"step": 2, "title": "Master Product Documentation (PRDs & Wireframing)", "explanation": "Learn to write clear problem statements, user stories, acceptance criteria, and Figma wireframes.", "action": "Draft 2 detailed PRDs for hypothetical features with user flow diagrams.", "duration": "4 weeks"},
            {"step": 3, "title": "Learn Product Analytics & Metrics", "explanation": "Understand North Star metrics, acquisition, activation, retention, and churn funnels.", "action": "Analyze mock usage data in SQL/Excel and recommend 3 sprint priorities.", "duration": "4 weeks"},
            {"step": 4, "title": "Build a Real Digital Product or Project", "explanation": "Lead a team of student developers and designers to build and launch an open web application.", "action": "Launch a live project on Product Hunt or college community with measurable users.", "duration": "6–8 weeks"},
            {"step": 5, "title": "Apply for Associate Product Manager (APM) Programs", "explanation": "Target dedicated APM rotational programs at tech firms or early-stage startups.", "action": "Prepare for product design, analytical, and execution interview questions.", "duration": "Ongoing"}
        ]),
        "cost_category": "Moderate",
        "cost_estimate_detail": "Undergraduate degrees in engineering/commerce: ₹40,000–₹4,00,000; Open product management learning resources are widely free.",
        "low_cost_routes": "Lenny's Newsletter free guides, Mind the Product community resources, YouTube APM interview prep, building free student side-projects.",
        "entrance_exams": json.dumps(["Engineering CETs", "CUET (UG)", "CAT (for MBA transition)"]),
        "advantages": json.dumps([
            "High strategic impact shaping real software, mobile apps, and services used by millions",
            "High market demand and strong career trajectory towards executive leadership (CPO / CEO)",
            "Fascinating blend of human empathy, technical craft, and commercial business acumen"
        ]),
        "challenges": json.dumps([
            "High accountability with no direct authority: must influence cross-functional peers through persuasion and data",
            "Constant pressure to balance engineering debt, design quality, and urgent business revenue demands",
            "Requires saying 'no' to good ideas to protect product focus and sprint capacity"
        ]),
        "geographic_considerations": "Centered around technology hubs (Bengaluru, Hyderabad, NCR, Pune), corporate tech centers, and distributed remote tech startups.",
        "regulated": 0,
        "source_urls": json.dumps([
            {"title": "Product School Open Resources", "url": "https://productschool.com"},
            {"title": "Mind the Product Global Community", "url": "https://www.mindtheproduct.com"},
            {"title": "National Career Service - Tech Products", "url": "https://www.ncs.gov.in"}
        ]),
        "last_verified": "2026-10-10"
    }
,
    {
        "slug": 'pharmacist',
        "title": 'Pharmacist & Clinical Medication Specialist',
        "category": 'Healthcare & Life Sciences',
        "short_description": ('Dispenses prescription medications, counsels patients on drug interactions and dosage, monitors therapeutic '
 'regimens, and oversees pharmaceutical compounding and quality control.'),
        "typical_responsibilities": json.dumps([           'Dispense prescribed pharmaceutical formulations with strict dosage and contraindication checks',
            'Counsel patients and caregivers on medication adherence, side-effects, and dietary interactions',
            'Monitor adverse drug reactions (ADR) and maintain pharmacovigilance records in hospital settings',
            'Manage medication inventory, cold-chain biological storage, and regulatory compounding protocols',
            'Collaborate with physicians and healthcare teams on evidence-based medication therapy management']),
        "relevant_interests": json.dumps(['science', 'healthcare', 'chemistry', 'public service', 'patient care']),
        "relevant_strengths": json.dumps(['attention to detail', 'empathy', 'analytical thinking', 'communication', 'scientific method']),
        "educational_requirements": ('Statutory 4-year Bachelor of Pharmacy (B.Pharm) or 6-year Doctor of Pharmacy (Pharm.D) from an institution approved '
 'by the Pharmacy Council of India (PCI). Mandatory statutory registration as a Registered Pharmacist with the State '
 'Pharmacy Council is legally required to dispense medications.'),
        "min_education_level": 'Undergraduate',
        "suitable_streams": json.dumps(['Science - PCB', 'Science - PCMB', 'Diploma in Pharmacy (D.Pharm) with lateral entry']),
        "important_skills": json.dumps([           'Pharmacology & Pharmacokinetics',
            'Medicinal Chemistry & Drug Formulation',
            'Patient Counseling & Drug Interaction Monitoring',
            'Good Dispensing Practice (GDP)',
            'Pharmacovigilance & Drug Safety',
            'Inventory & Cold-Chain Management']),
        "suggested_beginner_projects": json.dumps([           'Compare active pharmaceutical ingredients (APIs), mechanisms of action, and contraindications for common '
            'OTC analgesics',
            'Create a patient medication leaflet in clear language explaining drug interactions between hypertension '
            'medicines and common foods',
            'Audit storage temperature logs and inventory batch tracking protocols in a local community or college '
            'dispensary']),
        "learning_roadmap": json.dumps([           {           'action': 'Score high in 10+2 PCB subjects and review medicinal chemistry basics.',
                        'duration': 'School',
                        'explanation': 'Build deep foundation in organic chemistry reactions, cell biology, and '
                                       'biochemistry.',
                        'step': 1,
                        'title': 'Master High School Chemistry & Biology'},
            {           'action': 'Enrol in a Pharmacy Council of India (PCI) recognized college.',
                        'duration': '4 years',
                        'explanation': 'Complete 4-year curriculum in pharmacology, pharmaceutics, pharmaceutical '
                                       'chemistry, and pharmacognosy.',
                        'step': 2,
                        'title': 'Complete PCI-Approved B.Pharm Degree'},
            {           'action': 'Complete practical training in a recognized multi-specialty hospital pharmacy.',
                        'duration': '3–6 months',
                        'explanation': 'Gain practical clinical dispensing and manufacturing exposure during mandatory '
                                       'clinical rotation.',
                        'step': 3,
                        'title': 'Undergo Hospital & Industrial Pharmacy Internship'},
            {           'action': 'Submit verification documents to State Pharmacy Council.',
                        'duration': 'Post-graduation',
                        'explanation': 'Register with the State Pharmacy Council to receive official Pharmacist '
                                       'Registration Certificate and number.',
                        'step': 4,
                        'title': 'Obtain State Pharmacy Council Registration'},
            {           'action': 'Apply to healthcare systems or pharmaceutical research firms.',
                        'duration': 'Ongoing',
                        'explanation': 'Pursue clinical pharmacy, pharmaceutical R&D, regulatory affairs, or community '
                                       'pharmacy practice.',
                        'step': 5,
                        'title': 'Specialization or Clinical Practice (Pharm.D / M.Pharm)'}]),
        "cost_category": 'Moderate',
        "cost_estimate_detail": 'Govt / State University B.Pharm: ₹30,000–₹1,20,000 total; PCI-Approved Private Colleges: ₹2,00,000–₹6,00,000.',
        "low_cost_routes": ('Government pharmacy colleges, state central universities, state post-matric scholarships, and open NPTEL / Swayam '
 'pharmaceutical chemistry lectures.'),
        "entrance_exams": json.dumps(['State Pharmacy CETs (MHT-CET, KCET, WBJEE)', 'CUET (UG)', 'GPAT (for Postgraduate M.Pharm)']),
        "advantages": json.dumps([           'High career stability with essential healthcare provider status across public and private sectors',
            'Diverse career branches across clinical hospitals, retail community practice, drug regulatory affairs, '
            'and pharma R&D',
            'Growing global demand driven by biopharmaceuticals, clinical trials, and expanding healthcare coverage']),
        "challenges": json.dumps([           'Strict legal liability and zero-tolerance for dispensing errors requiring extreme precision',
            'Continuous learning required as new drug molecules, biological therapies, and safety warnings emerge',
            'Shift schedules and extended standing hours in busy hospital or community dispensaries']),
        "geographic_considerations": ('Every hospital, clinic, community neighborhood, and major pharmaceutical manufacturing corridors (Hyderabad, '
 'Ahmedabad, Baddi, Goa).'),
        "regulated": 1,
        "source_urls": json.dumps([           {'title': 'Pharmacy Council of India (PCI)', 'url': 'https://www.pci.nic.in'},
            {'title': 'Central Drugs Standard Control Organisation (CDSCO)', 'url': 'https://cdsco.gov.in'},
            {'title': 'National Career Service - Pharmacist', 'url': 'https://www.ncs.gov.in'}]),
        "last_verified": '2026-10-10',
    },
    {
        "slug": 'biotechnologist',
        "title": 'Biotechnologist & Genomic Researcher',
        "category": 'Healthcare & Life Sciences',
        "short_description": ('Applies biological systems, cellular genetics, and molecular biology to develop therapeutic biologics, vaccines, '
 'diagnostic test kits, and sustainable bio-agricultural innovations.'),
        "typical_responsibilities": json.dumps([           'Culture mammalian cells, microbial strains, and recombinant expression vectors in bioreactors',
            'Conduct DNA/RNA extraction, PCR amplification, gel electrophoresis, and next-generation sequencing',
            'Analyze genomic, proteomic, and biochemical data using bioinformatics pipelines (BLAST, Biopython)',
            'Validate therapeutic candidates through enzyme assays, ELISA, and high-throughput screening',
            'Adhere to Good Laboratory Practice (GLP) and biosafety level (BSL) containment protocols']),
        "relevant_interests": json.dumps(['science', 'biology', 'genetics', 'research', 'healthcare']),
        "relevant_strengths": json.dumps(['analytical thinking', 'precision', 'scientific method', 'curiosity', 'problem-solving']),
        "educational_requirements": ('B.Tech in Biotechnology or B.Sc. in Biotechnology / Biochemistry / Molecular Biology, followed by M.Tech / M.Sc. in '
 'Biotechnology, Bioinformatics, or Ph.D. for independent research.'),
        "min_education_level": 'Undergraduate',
        "suitable_streams": json.dumps(['Science - PCB', 'Science - PCMB', 'Biotechnology vocational']),
        "important_skills": json.dumps([           'Cell Culture & Bioreactor Operations',
            'Molecular Biology (PCR, Cloning, CRISPR basics)',
            'Bioinformatics (BLAST, NCBI, Biopython)',
            'Protein Purification & Chromatography (HPLC, FPLC)',
            'Good Laboratory Practice (GLP) & Bio-Safety (BSL-2)',
            'Assay Development (ELISA, Western Blot)']),
        "suggested_beginner_projects": json.dumps([           'Analyze real SARS-CoV-2 or insulin gene variants using NCBI nucleotide databases and phylogenetic trees',
            'Conduct an enzyme reaction rate experiment using household catalase (yeast/potato) across varying pH and '
            'temperatures',
            'Write a student research synthesis on recombinant human insulin manufacturing and scale-up bioreactors']),
        "learning_roadmap": json.dumps([           {           'action': 'Complete AP Biology / high school genetics curriculum.',
                        'duration': 'High school',
                        'explanation': 'Master molecular biology, genetics, organic chemistry, and cellular '
                                       'respiration.',
                        'step': 1,
                        'title': 'Build Strong Foundation in Biology & Chemistry'},
            {           'action': 'Actively participate in wet-lab college practicals.',
                        'duration': '3–4 years',
                        'explanation': 'Study microbiology, immunology, genetic engineering, bioprocess engineering, '
                                       'and bioinformatics.',
                        'step': 2,
                        'title': 'Pursue B.Tech / B.Sc in Biotechnology'},
            {           'action': 'Complete Rosalind.info bioinformatics problem tracks.',
                        'duration': '3–4 months',
                        'explanation': 'Learn Python for bioinformatics, sequence alignment, and molecular modeling in '
                                       'PyMOL.',
                        'step': 3,
                        'title': 'Master Computational Biology & Tools'},
            {           'action': 'Apply for DBT Summer Training or CSIR-SRTP fellowship.',
                        'duration': '2–6 months',
                        'explanation': 'Intern in academic labs (CSIR, DBT, ICMR) or biopharma production facilities.',
                        'step': 4,
                        'title': 'Gain Research Lab or Industry Internship'},
            {           'action': 'Take GATE / GAT-B entrance exams.',
                        'duration': 'Ongoing',
                        'explanation': 'Pursue M.Sc / M.Tech in Molecular Medicine, Industrial Biotech, or Ph.D.',
                        'step': 5,
                        'title': 'Advance to Specialization or Graduate Studies'}]),
        "cost_category": 'Moderate',
        "cost_estimate_detail": 'Govt Universities (B.Sc / B.Tech): ₹25,000–₹1,50,000 total; Private Biotech Institutes: ₹3,00,000–₹8,00,000.',
        "low_cost_routes": ('DBT-funded public central universities, NPTEL Biotechnology free lecture tracks, open bioinformatics databases '
 '(NCBI, PDB, UniProt).'),
        "entrance_exams": json.dumps(['CUET (UG)', 'JEE Main (for B.Tech Biotech)', 'GATE / GAT-B (Postgraduate)']),
        "advantages": json.dumps([           'Frontier science directly developing cures for diseases, cancer therapies, and climate-resilient crops',
            'Rapid industry growth fueled by vaccine manufacturing, biotherapeutics, and precision medicine',
            'Strong international collaboration and global research fellowship opportunities']),
        "challenges": json.dumps([           'Substantial scientific leadership roles typically require postgraduate (M.Sc/M.Tech) or doctoral degree',
            'Lengthy developmental cycles before laboratory discoveries achieve clinical approval',
            'Requires absolute rigor and sterility; a minor contamination can invalidate weeks of cell culture']),
        "geographic_considerations": ('Major biotech corridors in Bengaluru, Hyderabad, Pune, NCR, Ahmedabad, and national research institutes (CSIR, DBT, '
 'ICMR).'),
        "regulated": 0,
        "source_urls": json.dumps([           {'title': 'Department of Biotechnology (DBT India)', 'url': 'https://dbtindia.gov.in'},
            {'title': 'Biotechnology Industry Research Assistance Council (BIRAC)', 'url': 'https://birac.nic.in'},
            {'title': 'National Center for Biotechnology Information (NCBI)', 'url': 'https://www.ncbi.nlm.nih.gov'}]),
        "last_verified": '2026-10-10',
    },
    {
        "slug": 'astronomer-space-scientist',
        "title": 'Astronomer & Space Scientist',
        "category": 'Sciences & Environment',
        "short_description": ('Investigates celestial objects, stellar physics, planetary geology, observational astrophysics, and cosmological '
 'phenomena using ground-based radio/optical observatories and space satellites.'),
        "typical_responsibilities": json.dumps([           'Analyze observational telemetry and photometric data from optical, radio, and space-based telescopes',
            'Develop computational models of stellar evolution, galactic dynamics, and high-energy radiation',
            'Write reduction pipelines in Python (Astropy, SciPy) to clean atmospheric noise and instrument bias',
            'Publish peer-reviewed observational papers and draft observing proposals for major telescope time',
            'Collaborate with international research consortia on deep-space exploration and space satellite payloads']),
        "relevant_interests": json.dumps(['science', 'astronomy', 'physics', 'mathematics', 'space']),
        "relevant_strengths": json.dumps(['analytical thinking', 'mathematical modeling', 'curiosity', 'programming', 'patience']),
        "educational_requirements": ('B.Sc. in Physics or B.Tech in Engineering Physics / Aerospace, followed by M.Sc. in Astronomy / Astrophysics and '
 'Ph.D. in Astrophysics for research observatory and university faculty positions.'),
        "min_education_level": 'Undergraduate',
        "suitable_streams": json.dumps(['Science - PCM']),
        "important_skills": json.dumps([           'Astrophysics & Classical/Quantum Mechanics',
            'Data Reduction & Pipeline Scripting (Python, Astropy)',
            'Electromagnetic Radiation & Astronomical Spectroscopy',
            'Numerical Simulation & Differential Equations',
            'Telescope Instrumentation & Optics',
            'Scientific Writing & LaTeX']),
        "suggested_beginner_projects": json.dumps([           'Analyze public Kepler / TESS space telescope light curves in Python to detect exoplanet orbital transits',
            'Simulate gravitational multi-body planetary orbits using Runge-Kutta numerical integration in Python',
            'Analyze variable star pulsation periods using free citizen-science photometric data from AAVSO']),
        "learning_roadmap": json.dumps([           {           'action': 'Score high in high school physics and math.',
                        'duration': 'High school',
                        'explanation': 'Master Newtonian mechanics, optics, thermodynamics, and differential '
                                       'equations.',
                        'step': 1,
                        'title': 'Build Mastery in Advanced Calculus & Physics'},
            {           'action': 'Enroll at a reputable university physics department.',
                        'duration': '3–4 years',
                        'explanation': 'Study quantum physics, electromagnetic theory, statistical mechanics, and '
                                       'scientific programming.',
                        'step': 2,
                        'title': 'Pursue B.Sc in Physics or B.Tech Engineering Physics'},
            {           'action': 'Complete online tutorials using real Hubble or James Webb telescope public archive '
                                  'data.',
                        'duration': '3–6 months',
                        'explanation': 'Master Astropy, FITS image handling, aperture photometry, and spectroscopy '
                                       'data reduction.',
                        'step': 3,
                        'title': 'Learn Observational Data Reduction in Python'},
            {           'action': 'Clear JEST or CSIR-UGC NET JRF.',
                        'duration': '4–5 years',
                        'explanation': 'Join premier astrophysics institutes (IIA, IUCAA, TIFR, ISRO URSC) with '
                                       'research fellowship stipend.',
                        'step': 4,
                        'title': 'Pursue M.Sc and Doctoral Research (Ph.D)'},
            {           'action': 'Publish high-impact papers and secure observatory grants.',
                        'duration': 'Ongoing',
                        'explanation': 'Conduct specialized research on black holes, cosmic microwave background, or '
                                       'exoplanets.',
                        'step': 5,
                        'title': 'Postdoctoral Research Fellowships & Observatory Science'}]),
        "cost_category": 'Low / Free Accessible',
        "cost_estimate_detail": ('Govt Central Universities: ₹15,000–₹60,000 total tuition; Ph.D. programs are fully funded with CSIR-JRF / INSPIRE '
 'fellowships (₹37,000+/month stipend + HRA).'),
        "low_cost_routes": ('Public central universities, open astronomical datasets from NASA/ESA/ISRO archives, Astropy open tutorials, IIA and '
 'IUCAA public summer schools.'),
        "entrance_exams": json.dumps(['CUET (UG)', 'IIT JAM (Physics)', 'JEST (Joint Entrance Screening Test)', 'CSIR NET Physical Sciences']),
        "advantages": json.dumps([           'Direct pursuit of fundamental questions about the birth, evolution, and future of the universe',
            'Fully funded Ph.D. and postdoctoral fellowships with international telescope collaborations',
            'Highly transferable computational physics, big-data modeling, and image processing skill set']),
        "challenges": json.dumps([           'Long educational commitment typically requiring 7–10 years to reach independent tenure',
            'Extremely competitive permanent academic and observatory research positions worldwide',
            'Demands continuous mathematical endurance and complex statistical error analysis']),
        "geographic_considerations": ('National observatories (Hanle, Kavalur, Nainital, Pune GMRT, Udaipur Solar Observatory) and premier research centers '
 '(IUCAA, IIA, TIFR, ISRO).'),
        "regulated": 0,
        "source_urls": json.dumps([           {'title': 'Inter-University Centre for Astronomy and Astrophysics (IUCAA)', 'url': 'https://www.iucaa.in'},
            {'title': 'Indian Institute of Astrophysics (IIA Bengaluru)', 'url': 'https://www.iiap.res.in'},
            {'title': 'ISRO Space Science Data Centre (ISSDC)', 'url': 'https://www.issdc.gov.in'}]),
        "last_verified": '2026-10-10',
    },
    {
        "slug": 'astronaut',
        "title": 'Astronaut & Spaceflight Mission Specialist',
        "category": 'Technology & Engineering',
        "short_description": ('Undergoes rigorous technical, physical, and physiological training to command or operate spacecraft missions, '
 'execute orbital microgravity experiments, and conduct space exploration operations.'),
        "typical_responsibilities": json.dumps([           'Pilot or operate crewed spacecraft systems, guidance navigation controls, and docking hardware',
            'Execute scheduled scientific experiments in microgravity biology, materials physics, and astronomy',
            'Conduct Extravehicular Activities (EVAs / spacewalks) for spacecraft inspection, repair, and assembly',
            'Maintain extreme physical conditioning, vestibular adaptation, and emergency survival readiness',
            'Communicate mission milestones, telemetry reports, and educational broadcasts with ground control']),
        "relevant_interests": json.dumps(['space', 'aviation', 'engineering', 'science', 'adventure', 'technology']),
        "relevant_strengths": json.dumps(['physical fitness', 'crisis composure', 'leadership', 'technical mastery', 'team resilience']),
        "educational_requirements": ("Extremely selective and physically demanding. Requires advanced Master's or Ph.D. in STEM (Engineering, Computer "
 "Science, Physics, Medicine) or Bachelor's in Engineering with at least 1,000 hours of high-performance military jet "
 'flight experience. Candidates must pass rigorous physiological screening (G-force tolerance, cardiovascular '
 'endurance, visual acuity) and selection by national space agencies (ISRO Gaganyaan Astronaut Selection / NASA '
 'Astronaut Candidate).'),
        "min_education_level": 'Undergraduate',
        "suitable_streams": json.dumps(['Science - PCM', 'Aeronautical / Mechanical / Computer Engineering', 'Military Aviation Cadet']),
        "important_skills": json.dumps([           'Spacecraft Flight Mechanics & Telemetry Systems',
            'Extreme Physiological Stress Tolerance (G-load, Hypoxia)',
            'Neutral Buoyancy & EVA Spacewalk Simulation',
            'Crisis Communication & Tactical Decision-Making',
            'Microgravity Experimental Protocols',
            'Wilderness & Oceanic Survival Operations']),
        "suggested_beginner_projects": json.dumps([           'Simulate orbital rendezvous and docking maneuvers using open-source Orbiter Space Simulator or Kerbal '
            'Space Program',
            'Participate in the NASA Space Apps Challenge or national student sounding rocket competition',
            'Complete certified open-water scuba diving certification to understand neutral buoyancy movement '
            'principles']),
        "learning_roadmap": json.dumps([           {           'action': 'Commit to daily physical training, competitive athletics, and STEM Olympiads.',
                        'duration': 'High school',
                        'explanation': 'Maintain top marks in math and physics while achieving peak cardiovascular '
                                       'conditioning and swimming agility.',
                        'step': 1,
                        'title': 'Excel in STEM Academics and Peak Physical Fitness'},
            {           'action': 'Graduate at the top of your class with leadership credentials.',
                        'duration': '4 years',
                        'explanation': 'Pursue aerospace, mechanical, or computer engineering at premier institutions '
                                       'or National Defence Academy (NDA).',
                        'step': 2,
                        'title': 'Earn Degree in Engineering, Physics, or Aviation'},
            {           'action': 'Serve as experimental test pilot or lead aerospace systems engineer at ISRO/DRDO.',
                        'duration': '5–8 years',
                        'explanation': 'Accumulate jet test pilot flight hours or earn a doctoral degree with '
                                       'groundbreaking aerospace/physics research.',
                        'step': 3,
                        'title': 'Gain Advanced Operational or Research Experience'},
            {           'action': 'Complete national astronaut candidate application and medical clearance.',
                        'duration': '1–2 years',
                        'explanation': 'Pass grueling psychological, physiological, centrifuge, and multi-axis trainer '
                                       'selection tests.',
                        'step': 4,
                        'title': 'Apply for National Astronaut Candidate Selection'},
            {           'action': 'Certify on mission command and EVA spacewalk protocols.',
                        'duration': '2–3 years',
                        'explanation': 'Train in centrifuge simulators, zero-G parabolic flights, Russian/NASA partner '
                                       'training centers, and survival skills.',
                        'step': 5,
                        'title': 'Intensive Mission-Specific Astronaut Training'}]),
        "cost_category": 'Low / Free Accessible',
        "cost_estimate_detail": ('Military flight pathway: 100% government-funded via National Defence Academy (NDA) / Air Force Academy; STEM '
 'scientist pathway: Public university B.Tech/M.Tech + research appointments.'),
        "low_cost_routes": ('Indian Air Force flight cadet entry, public IITs/NITs aerospace programs, ISRO student internships, open space '
 'education resources via ISRO IIRS / NASA Open Science.'),
        "entrance_exams": json.dumps(['NDA / CDS (Aviation Cadet)', 'JEE Advanced (Aerospace / Engineering Physics)', 'GATE (ISRO Scientist Entry)']),
        "advantages": json.dumps([           'Pinnacle human exploration achievement contributing directly to national and global space history',
            'World-class physical, cognitive, and flight training alongside premier scientific minds',
            'Inspires millions of students worldwide to pursue science, engineering, and exploration']),
        "challenges": json.dumps([           'Extremely demanding selection criteria: fewer than a few dozen individuals worldwide selected per decade',
            'Severe physical strain including high G-forces, radiation exposure, muscle atrophy, and mission risks',
            'Prolonged confinement, intense training schedules, and unpredictable mission launch delays']),
        "geographic_considerations": ('ISRO Astronaut Training Facility (Bengaluru), Human Space Flight Centre (HSFC), Gaganyaan launch sites '
 '(Sriharikota), IAF Institute of Aerospace Medicine, and partner space facilities.'),
        "regulated": 1,
        "source_urls": json.dumps([           {'title': 'ISRO Human Space Flight Centre (HSFC / Gaganyaan)', 'url': 'https://www.isro.gov.in'},
            {'title': 'Institute of Aerospace Medicine (IAM IAF)', 'url': 'https://indianairforce.nic.in'},
            {'title': 'NASA Astronaut Selection Standards', 'url': 'https://www.nasa.gov/astronauts'}]),
        "last_verified": '2026-10-10',
    },
    {
        "slug": 'robotics-engineer',
        "title": 'Robotics & Mechatronics Engineer',
        "category": 'Technology & Engineering',
        "short_description": ('Designs, programs, and integrates autonomous robots, multi-axis robotic arms, mobile AGVs, sensors, '
 'microcontrollers, and computer vision systems for manufacturing, surgery, and exploration.'),
        "typical_responsibilities": json.dumps([           'Develop robot kinematics, trajectory planning, and motor motion control algorithms',
            'Program embedded microcontrollers and Single Board Computers (ROS 2, C++, Python, Arduino, STM32)',
            'Integrate computer vision, LiDAR sensors, and IMUs for autonomous localization and mapping (SLAM)',
            'Design 3D mechanical linkages, gearboxes, and end-effectors in CAD with rapid 3D printing',
            'Conduct safety integration tests according to ISO 10218 industrial robot safety standards']),
        "relevant_interests": json.dumps(['robotics', 'technology', 'engineering', 'machinery', 'programming']),
        "relevant_strengths": json.dumps(['practical problem-solving', 'analytical thinking', 'spatial reasoning', 'creativity', 'systems integration']),
        "educational_requirements": ('B.Tech in Mechatronics, Mechanical Engineering, Electrical & Electronics, or Computer Science with demonstrable '
 'hands-on robotics projects and ROS proficiency.'),
        "min_education_level": 'Class 11–12',
        "suitable_streams": json.dumps(['Science - PCM', 'Diploma in Mechatronics / Mechanical', 'Computer Science']),
        "important_skills": json.dumps([           'Robot Operating System (ROS 2 / Gazebo)',
            'Forward & Inverse Kinematics',
            'C++ and Python for Embedded Systems',
            'Computer Vision & SLAM (OpenCV)',
            'Motor Drivers, Actuators & Sensors',
            'CAD Modeling & 3D Prototyping (Fusion 360 / SolidWorks)']),
        "suggested_beginner_projects": json.dumps([           'Build an autonomous 2-wheeled obstacle-avoiding mobile robot using Arduino, ultrasonic sensors, and motor '
            'shields',
            'Simulate a 3-DOF robotic arm in ROS 2 and Gazebo, calculating inverse kinematics in Python',
            'Build a smart color-sorting conveyor belt using an open-source USB webcam and OpenCV shape recognition']),
        "learning_roadmap": json.dumps([           {           'action': 'Build 5 basic breadboard circuits with Arduino.',
                        'duration': '4 weeks',
                        'explanation': "Understand DC motors, servos, Ohm's law, torque calculations, and "
                                       'microcontroller basics.',
                        'step': 1,
                        'title': 'Learn Mechanics & Circuit Fundamentals'},
            {           'action': 'Solve embedded coding challenges and read sensor data over UART/I2C.',
                        'duration': '6 weeks',
                        'explanation': 'Learn object-oriented programming, data structures, and serial communication '
                                       'protocols.',
                        'step': 2,
                        'title': 'Master C++ and Python Programming'},
            {           'action': 'Simulate an autonomous wheeled mobile robot navigating a virtual maze.',
                        'duration': '6–8 weeks',
                        'explanation': 'Study publisher-subscriber nodes, URDF robot modeling, and simulation in '
                                       'Gazebo.',
                        'step': 3,
                        'title': 'Learn ROS 2 & Robot Simulation'},
            {           'action': 'Document robot hardware and open-source GitHub code.',
                        'duration': '8 weeks',
                        'explanation': 'Design 3D printed chassis, integrate motor encoders, LiDAR or camera, and '
                                       'implement SLAM mapping.',
                        'step': 4,
                        'title': 'Build a Physical Multi-Sensor Robot'},
            {           'action': 'Apply to robotics startups or manufacturing automation firms.',
                        'duration': 'Ongoing',
                        'explanation': 'Work with industrial robotic arms, automated guided vehicles (AGVs), or '
                                       'medical robotics teams.',
                        'step': 5,
                        'title': 'Internship in Industrial Automation or Agritech'}]),
        "cost_category": 'Moderate',
        "cost_estimate_detail": 'Govt Engineering Colleges: ₹60,000–₹2,50,000 total; Starter robot kit / electronics for learning: ₹3,000–₹12,000.',
        "low_cost_routes": ('Open-source ROS 2 and Gazebo simulators requiring zero physical hardware, NPTEL robotics courses, community tinker '
 'labs / Atal Tinkering Labs.'),
        "entrance_exams": json.dumps(['JEE Main', 'JEE Advanced', 'State Engineering CETs', 'GATE (Mechanical / Electronics)']),
        "advantages": json.dumps([           'At the convergence of AI, mechanical hardware, and embedded electronics with explosive future demand',
            'Hands-on creative thrill of seeing physical machines think, move, and solve real tasks in the physical '
            'world',
            'High versatility across warehouse automation, defense drones, agricultural robots, and surgical robotics']),
        "challenges": json.dumps([           'Must debug both hardware issues (loose wiring, sensor noise, gear backlash) and software code bugs '
            'simultaneously',
            'Advanced industrial components, sensors, and servos can be costly for home projects',
            'Requires multidisciplinary competence across physics, mathematics, electronics, and coding']),
        "geographic_considerations": ('Major manufacturing corridors (Pune, Chennai, NCR, Bengaluru, Ahmedabad), robotics research labs, and automated '
 'fulfillment hubs.'),
        "regulated": 0,
        "source_urls": json.dumps([           {'title': 'Open Source Robotics Foundation (ROS 2)', 'url': 'https://www.ros.org'},
            {'title': 'IEEE Robotics and Automation Society', 'url': 'https://www.ieee-ras.org'},
            {'title': 'NPTEL Robotics Certification', 'url': 'https://nptel.ac.in'}]),
        "last_verified": '2026-10-10',
    },
    {
        "slug": 'electrical-engineer',
        "title": 'Electrical & Power Systems Engineer',
        "category": 'Technology & Engineering',
        "short_description": ('Designs, simulates, and manages electrical power grids, renewable energy generation (solar/wind), electric vehicle '
 'powertrains, switchgear, and high-voltage transmission networks.'),
        "typical_responsibilities": json.dumps([           'Design electrical schematics, single-line diagrams (SLDs), and switchgear specifications',
            'Model power grid load flows, short-circuit faults, and voltage stability in MATLAB/ETAP',
            'Supervise installation and commissioning of transformers, protection relays, and solar inverters',
            'Ensure adherence to Central Electricity Authority (CEA) regulations and IEEE/IS safety standards',
            'Perform energy audits, power factor correction, and harmonic distortion mitigations in industrial plants']),
        "relevant_interests": json.dumps(['engineering', 'electricity', 'machinery', 'renewable energy', 'problem-solving']),
        "relevant_strengths": json.dumps(['analytical thinking', 'mathematical calculation', 'safety orientation', 'practical troubleshooting']),
        "educational_requirements": ('B.Tech / B.E. in Electrical Engineering (EE) or Electrical & Electronics Engineering (EEE), or 3-year State '
 'Polytechnic Diploma in Electrical Engineering with lateral entry to B.Tech.'),
        "min_education_level": 'Class 11–12',
        "suitable_streams": json.dumps(['Science - PCM', 'Diploma in Electrical Engineering', 'Vocational Electrical Maintenance']),
        "important_skills": json.dumps([           'Power System Simulation (MATLAB / Simulink / ETAP)',
            'Single Line Diagrams & Electrical CAD (AutoCAD Electrical)',
            'Switchgear & Protective Relay Coordination',
            'Solar PV & Wind Renewable Integration',
            'PLC & SCADA Industrial Automation',
            'Electrical Safety Standards (CEA / IS 732 / NFPA 70E)']),
        "suggested_beginner_projects": json.dumps([           'Design and calculate sizing for an off-grid 1kW rooftop solar photovoltaic system with battery backup',
            'Simulate a 3-phase induction motor speed controller and power factor improvement circuit in '
            'MATLAB/Simulink',
            'Build an IoT smart energy meter using an ESP32 and non-invasive current transformer (CT) sensor to log '
            'household power usage']),
        "learning_roadmap": json.dumps([           {           'action': 'Solve 50 complex AC network analysis problems.',
                        'duration': 'High school / Sem 1',
                        'explanation': "Master Kirchhoff's laws, AC circuits, phasors, magnetic circuits, and "
                                       "Maxwell's equations.",
                        'step': 1,
                        'title': 'Master Circuit Theory & Electromagnetism'},
            {           'action': 'Complete laboratory experiments on transformer load tests and DC motors.',
                        'duration': '1 year',
                        'explanation': 'Learn transformers, induction motors, synchronous generators, and transmission '
                                       'line models.',
                        'step': 2,
                        'title': 'Study Electrical Machines & Power Systems'},
            {           'action': 'Simulate a 5-bus industrial power distribution network in ETAP.',
                        'duration': '2–3 months',
                        'explanation': 'Model load flow, symmetrical faults, and renewable grid integration.',
                        'step': 3,
                        'title': 'Learn Power Simulation Software (ETAP / Simulink)'},
            {           'action': 'Apply for summer training at state electricity transmission boards '
                                  '(DISCOMs/TRANSCOs).',
                        'duration': '4–6 weeks',
                        'explanation': 'Visit 33kV/132kV substations, study switchgear, circuit breakers, and relay '
                                       'protection panels.',
                        'step': 4,
                        'title': 'Substation Visits & Practical Site Exposure'},
            {           'action': 'Prepare for GATE (EE) or state PSU technical selection.',
                        'duration': 'Ongoing',
                        'explanation': 'Join power utilities (PGCIL, NTPC), renewable developers, EV manufacturers, or '
                                       'consulting firms.',
                        'step': 5,
                        'title': 'Target Graduate Engineering Trainee Roles or PSUs'}]),
        "cost_category": 'Moderate',
        "cost_estimate_detail": 'Govt Engineering Colleges: ₹40,000–₹2,00,000 total; State Polytechnic: ₹15,000–₹50,000 total.',
        "low_cost_routes": ('Government polytechnic colleges, central state universities, NPTEL Electrical Engineering courses, open circuit '
 'simulation software (Qucs / LTspice).'),
        "entrance_exams": json.dumps(['JEE Main', 'State Engineering CETs', 'GATE (for PSU recruitment: PGCIL, NTPC, BHEL)']),
        "advantages": json.dumps([           'Perennial foundational engineering discipline essential to all modern civilization and clean energy '
            'transition',
            'Substantial recruitment across prestigious public sector undertakings (PSUs: Power Grid, NTPC, BHEL, '
            'Metro Rail)',
            'Rapidly expanding opportunities in electric vehicles (EV), battery storage, and solar/wind megaprojects']),
        "challenges": json.dumps([           'Strict safety requirements: working around high voltage lines involves inherent electrical flash hazards',
            'Heavy theoretical mathematics in differential equations, Laplace transforms, and complex power flow '
            'vectors',
            'Site engineer roles frequently require field travel to remote substations and industrial facilities in '
            'harsh weather']),
        "geographic_considerations": ('Every electricity distribution board (DISCOM), thermal/hydro/solar plants, industrial manufacturing corridors, and '
 'metro railway systems.'),
        "regulated": 0,
        "source_urls": json.dumps([           {'title': 'Central Electricity Authority (CEA)', 'url': 'https://cea.nic.in'},
            {'title': 'Power Grid Corporation of India (POWERGRID)', 'url': 'https://www.powergrid.in'},
            {'title': 'IEEE Power & Energy Society', 'url': 'https://www.ieee-pes.org'}]),
        "last_verified": '2026-10-10',
    },
    {
        "slug": 'aerospace-engineer',
        "title": 'Aerospace & Aeronautical Engineer',
        "category": 'Technology & Engineering',
        "short_description": ('Researches, designs, and manufactures fixed-wing aircraft, drones, helicopters, launch vehicles, and spacecraft '
 'propulsion systems with emphasis on aerodynamics and structures.'),
        "typical_responsibilities": json.dumps([           'Calculate aircraft aerodynamic lift, drag, and stability characteristics using Computational Fluid '
            'Dynamics (CFD)',
            'Design lightweight airframe composite structures, wing spars, and landing gear in 3D CAD',
            'Perform structural finite element analysis (FEA) under extreme flight load and flutter conditions',
            'Design and test propulsion systems including gas turbines, ramjets, and solid/liquid rocket engines',
            'Coordinate with flight test crews and airworthiness certification authorities (DGCA / FAA)']),
        "relevant_interests": json.dumps(['aviation', 'space', 'aerodynamics', 'engineering', 'physics']),
        "relevant_strengths": json.dumps(['analytical thinking', 'advanced mathematics', 'simulation', 'attention to precision']),
        "educational_requirements": ('B.Tech / B.E. in Aerospace Engineering, Aeronautical Engineering, or Mechanical Engineering with aerospace '
 'specialization.'),
        "min_education_level": 'Class 11–12',
        "suitable_streams": json.dumps(['Science - PCM']),
        "important_skills": json.dumps([           'Computational Fluid Dynamics (CFD / OpenFOAM / ANSYS Fluent)',
            'Aerodynamics & High-Speed Flight Mechanics',
            'Propulsion Systems (Gas Turbines / Rocket Engines)',
            'Finite Element Analysis (FEA / Nastran / Abaqus)',
            'Avionics & Flight Control Systems',
            'Airworthiness Standards & Certification (FAR / CS-25)']),
        "suggested_beginner_projects": json.dumps([           'Simulate aerodynamic lift and drag curves for an NACA 4412 airfoil in OpenFOAM or XFLR5',
            'Design, construct, and test-fly a custom RC fixed-wing glider or quadcopter drone',
            'Calculate payload capability and delta-V budget for a two-stage suborbital sounding rocket in Python']),
        "learning_roadmap": json.dumps([           {           'action': 'Score high in high school physics and math.',
                        'duration': 'High school',
                        'explanation': 'Master vector calculus, differential equations, thermodynamics, and fluid '
                                       'mechanics.',
                        'step': 1,
                        'title': 'Build Mastery in Advanced Mathematics & Physics'},
            {           'action': 'Enroll in an accredited aerospace engineering program.',
                        'duration': '4 years',
                        'explanation': 'Study compressible aerodynamics, aircraft structures, flight mechanics, and '
                                       'propulsion.',
                        'step': 2,
                        'title': 'Pursue B.Tech in Aerospace or Mechanical Engineering'},
            {           'action': 'Complete aerodynamic wing simulation case study.',
                        'duration': '4–6 months',
                        'explanation': 'Learn CFD modeling in open-source OpenFOAM or XFLR5, and CAD modeling in '
                                       'SolidWorks.',
                        'step': 3,
                        'title': 'Master Computational Aerodynamics Tools'},
            {           'action': 'Build and fly a team drone or sounding rocket.',
                        'duration': 'College year',
                        'explanation': 'Join SAE Aero Design, AIAA Design/Build/Fly, or CanSat satellite student '
                                       'teams.',
                        'step': 4,
                        'title': 'Participate in UAV / Rocketry Student Competitions'},
            {           'action': 'Apply to graduate engineering programs or take GATE (AE).',
                        'duration': 'Ongoing',
                        'explanation': 'Work with aerospace defense companies, drone startups, or space agencies (HAL, '
                                       'ISRO, DRDO, Boeing, Airbus).',
                        'step': 5,
                        'title': 'Join Aerospace R&D, Defense, or Space Organizations'}]),
        "cost_category": 'Moderate',
        "cost_estimate_detail": 'IITs / NITs: ₹1,50,000–₹8,00,000 total; Private Aerospace Institutes: ₹4,00,000–₹12,00,000.',
        "low_cost_routes": ('Government IITs/NITs with merit/means fee concessions, open CFD tools (OpenFOAM, NASA OpenVSP), open flight '
 'mechanics lectures on NPTEL.'),
        "entrance_exams": json.dumps(['JEE Advanced', 'JEE Main', 'GATE Aerospace (AE)']),
        "advantages": json.dumps([           'Frontier engineering pushing physical limits of speed, altitude, and deep space exploration',
            'Surging domestic defense aerospace and commercial drone manufacturing under Make in India initiatives',
            'Deeply respected, intellectually elite technical discipline with global career mobility']),
        "challenges": json.dumps([           'Strict aviation and defense regulatory oversight resulting in long certification cycles before flight',
            'High capital intensity limits the number of primary aircraft manufacturers',
            'Requires relentless mathematical discipline in compressible flows, supersonic shocks, and nonlinear '
            'elasticity']),
        "geographic_considerations": 'Aviation hubs in Bengaluru (HAL, ISRO, NAL, Boeing/Airbus R&D), Hyderabad, Kanpur, and defense manufacturing nodes.',
        "regulated": 0,
        "source_urls": json.dumps([           {'title': 'Directorate General of Civil Aviation (DGCA India)', 'url': 'https://www.dgca.gov.in'},
            {'title': 'Hindustan Aeronautics Limited (HAL)', 'url': 'https://hal-india.co.in'},
            {'title': 'Aeronautical Society of India (AeSI)', 'url': 'https://aesi.org.in'}]),
        "last_verified": '2026-10-10',
    },
    {
        "slug": 'video-editor-media-producer',
        "title": 'Video Editor & Digital Media Producer',
        "category": 'Creative & Design',
        "short_description": ('Assembles raw recorded footage, dialogue, sound effects, motion graphics, and color grading into polished visual '
 'stories for documentaries, streaming series, commercials, and digital education.'),
        "typical_responsibilities": json.dumps([           'Ingest, organize, and log multi-camera video footage, audio tracks, and production metadata',
            'Assemble assembly cuts, rough cuts, and fine cuts balancing narrative pacing and emotional arc',
            'Perform primary and secondary color correction and cinematic color grading (DaVinci Resolve)',
            'Design motion graphic title cards, lower thirds, and animated overlays (After Effects)',
            'Mix and master multi-track audio dialogue, ambient soundscapes, and musical scores']),
        "relevant_interests": json.dumps(['creativity', 'video editing', 'storytelling', 'film', 'visual arts', 'technology']),
        "relevant_strengths": json.dumps(['visual storytelling', 'attention to detail', 'rhythm and pacing', 'creativity', 'patience']),
        "educational_requirements": ('Degree or diploma in Film Editing, Mass Communication, or Visual Arts, or proven demonstrable editing showreel (many '
 'successful editors are self-taught or enter via apprenticeship).'),
        "min_education_level": 'Class 10',
        "suitable_streams": json.dumps(['Any stream with visual portfolio', 'Humanities / Arts', 'Commerce', 'Vocational Media']),
        "important_skills": json.dumps([           'Non-Linear Editing (DaVinci Resolve / Premiere Pro / Final Cut)',
            'Color Correction & Grading (Color Wheels, Waveforms, LUTs)',
            'Audio Post-Production (Dialogue EQ, Noise Reduction, Audio Ducking)',
            'Motion Graphics & Keyframing (After Effects)',
            'Video Codecs, Bitrates & Export Compression',
            'Narrative Pacing & Visual Rhythm']),
        "suggested_beginner_projects": json.dumps([           'Edit a 90-second dynamic documentary trailer from open-source stock footage with sound design and title '
            'cards',
            'Complete a cinematic color grading breakdown in free DaVinci Resolve using raw camera test clips',
            'Produce a 3-minute educational video explaining a complex science topic with synced motion graphics']),
        "learning_roadmap": json.dumps([           {           'action': 'Watch classic film editing breakdowns and analyze pacing.',
                        'duration': '3 weeks',
                        'explanation': 'Understand shot types (wide, medium, close-up), match cuts, J-cuts, L-cuts, '
                                       'and the 180-degree rule.',
                        'step': 1,
                        'title': 'Learn Video Foundations & Grammar of the Edit'},
            {           'action': "Complete Blackmagic Design's free certified DaVinci Resolve beginner training.",
                        'duration': '4–6 weeks',
                        'explanation': 'Learn DaVinci Resolve (free) or Premiere Pro: keyboard shortcuts, timeline '
                                       'trimming, and multi-cam sync.',
                        'step': 2,
                        'title': 'Master Professional NLE Software'},
            {           'action': 'Edit the sound design for a 60-second silent film scene.',
                        'duration': '3 weeks',
                        'explanation': 'Master dialogue noise cleanup, room tone, Foley sound effects, and music '
                                       'synchronization.',
                        'step': 3,
                        'title': 'Learn Sound Design and Audio Mixing'},
            {           'action': 'Grade a 5-shot sequence for day-for-night and sunset moods.',
                        'duration': '4 weeks',
                        'explanation': 'Understand color temperature, lift/gamma/gain curves, shot matching, and '
                                       'keyframing title animations.',
                        'step': 4,
                        'title': 'Study Color Grading and Motion Graphics'},
            {           'action': 'Publish showreel and pitch to YouTube channels, advertising agencies, or production '
                                  'houses.',
                        'duration': 'Ongoing',
                        'explanation': 'Assemble a 60-second fast-paced showreel showcasing diversity in documentary, '
                                       'commercial, and narrative cuts.',
                        'step': 5,
                        'title': 'Build a Public Showreel and Freelance / Studio Work'}]),
        "cost_category": 'Low / Free Accessible',
        "cost_estimate_detail": 'Free DaVinci Resolve software; Decent editing computer: ₹40,000–₹90,000; Film institute degrees: ₹1,00,000–₹6,00,000.',
        "low_cost_routes": ('Free full version of DaVinci Resolve, YouTube tutorials, public domain archive footage (Internet Archive), freelance '
 'student projects.'),
        "entrance_exams": json.dumps(['FTII / SRFTI JET (Film Editing)', 'CUET (UG) Mass Communication', 'Institutional Portfolio Review']),
        "advantages": json.dumps([           'Extremely high demand across streaming platforms (Netflix, Hotstar), YouTube creators, advertising, and '
            'corporate media',
            'Strong global freelance earning potential and location-independent remote work',
            'Deep creative fulfillment transforming raw fragmented footage into compelling emotional stories']),
        "challenges": json.dumps([           'Tight turnaround deadlines and repetitive client revision cycles',
            'Extended sitting hours in dark edit suites causing eye fatigue and ergonomic strain',
            'Heavy computer rendering demands and large external hard drive storage overheads']),
        "geographic_considerations": 'Major media hubs (Mumbai, Hyderabad, Chennai, NCR, Bengaluru) and completely distributed global remote contracts.',
        "regulated": 0,
        "source_urls": json.dumps([           {           'title': 'Blackmagic Design DaVinci Resolve Free Training',
                        'url': 'https://www.blackmagicdesign.com/products/davinciresolve/training'},
            {'title': 'Film and Television Institute of India (FTII)', 'url': 'https://www.ftiindia.com'},
            {'title': 'National Career Service - Video Editing', 'url': 'https://www.ncs.gov.in'}]),
        "last_verified": '2026-10-10',
    },
    {
        "slug": 'music-producer-audio',
        "title": 'Music Producer & Audio Engineer',
        "category": 'Creative & Design',
        "short_description": ('Composes, arranges, records, mixes, and masters music tracks, cinematic scores, podcast audio, and game soundscapes '
 'using modern Digital Audio Workstations (DAWs) and studio outboard equipment.'),
        "typical_responsibilities": json.dumps([           'Compose melodies, harmonic chord progressions, basslines, and rhythmic drum patterns in DAWs',
            'Record live acoustic instruments, vocals, and synthesizers with optimal microphone placement',
            'Perform audio mixing: surgical EQ, dynamic compression, spatial reverb, and stereo imaging',
            'Master finished tracks to international loudness streaming standards (LUFS / true peak limits)',
            'Collaborate with songwriters, film directors, and game developers on sonic branding and soundtracks']),
        "relevant_interests": json.dumps(['music', 'singing', 'audio engineering', 'creativity', 'technology', 'sound design']),
        "relevant_strengths": json.dumps(['musical ear', 'creativity', 'attention to audio detail', 'rhythm', 'technical patience']),
        "educational_requirements": ('Diploma or degree in Audio Engineering, Music Production, or Sound Design, or extensive practical studio '
 'apprenticeship and demonstrable audio portfolio.'),
        "min_education_level": 'Class 10',
        "suitable_streams": json.dumps(['Any stream with musical aptitude', 'Humanities / Arts', 'Vocational Sound Engineering']),
        "important_skills": json.dumps([           'Digital Audio Workstation (Ableton Live / Logic Pro / FL Studio / Pro Tools)',
            'Audio Mixing (Subtractive EQ, Multiband Compression, Saturation)',
            'Audio Mastering & Loudness Standards (LUFS / True Peak)',
            'MIDI Programming & Synthesizer Sound Design',
            'Studio Acoustics, Microphone Polar Patterns & Gain Staging',
            'Music Theory Fundamentals (Chords, Scales, Arrangements)']),
        "suggested_beginner_projects": json.dumps([           'Produce a complete 2-minute original musical beat or soundtrack using free DAW (Reaper / BandLab / '
            'GarageBand)',
            'Record a live acoustic instrument or vocal track and clean background noise using spectral editing',
            'Create a custom sound design pack (50 sound effects) for a short indie video game trailer']),
        "learning_roadmap": json.dumps([           {           'action': 'Complete free interactive music theory tutorials (e.g. Ableton Learning Music).',
                        'duration': '4 weeks',
                        'explanation': 'Learn scales, chord progressions, tempo, audio frequencies (20Hz–20kHz), and '
                                       'decibels.',
                        'step': 1,
                        'title': 'Understand Music Theory and Acoustic Physics'},
            {           'action': 'Recreate the arrangement of a favorite song in your DAW.',
                        'duration': '6 weeks',
                        'explanation': 'Learn audio recording, MIDI sequencing, virtual instruments, and audio '
                                       'slicing.',
                        'step': 2,
                        'title': 'Master a Digital Audio Workstation (DAW)'},
            {           'action': 'Mix a multi-track stem session downloaded from free Cambridge Music Technology '
                                  'library.',
                        'duration': '8 weeks',
                        'explanation': 'Learn high-pass filtering, dynamic range compression, sidechaining, and stereo '
                                       'panning.',
                        'step': 3,
                        'title': 'Master Audio Mixing Fundamentals'},
            {           'action': 'Master 3 tracks to -14 LUFS with dynamic preservation.',
                        'duration': '4 weeks',
                        'explanation': 'Learn bus limiting, multiband saturation, and streaming normalization '
                                       'standards (Spotify, Apple Music).',
                        'step': 4,
                        'title': 'Study Audio Mastering & Delivery Standards'},
            {           'action': 'Upload portfolio to SoundCloud/Spotify and freelance platforms.',
                        'duration': 'Ongoing',
                        'explanation': 'Distribute original tracks, pitch for indie games, web series, or offer audio '
                                       'mixing services.',
                        'step': 5,
                        'title': 'Publish Music & Pitch for Sync Licensing / Games'}]),
        "cost_category": 'Low / Free Accessible',
        "cost_estimate_detail": ('Affordable home setup (Budget studio headphones, USB audio interface, condenser mic, DAW): ₹25,000–₹60,000; Sound '
 'engineering colleges: ₹80,000–₹4,50,000.'),
        "low_cost_routes": ('Free DAWs (Reaper free trial, Cakewalk, BandLab), open audio sample packs, free acoustic tutorials, community church '
 'or campus audio volunteering.'),
        "entrance_exams": json.dumps(['FTII JET (Sound Recording & Design)', 'Institutional Music Production Auditions']),
        "advantages": json.dumps([           'Turn personal passion for music, melody, and rhythm into a sustainable professional craft',
            'Diverse avenues in film scoring, gaming, streaming podcasts, advertising jingles, and indie artist '
            'releases',
            'Global digital streaming allows publishing directly to worldwide audiences without traditional label '
            'gatekeepers']),
        "challenges": json.dumps([           'Initial freelance income can be unpredictable while establishing an industry reputation',
            'Requires continuous critical ear training to discern subtle phase cancellations and frequency masking',
            'Late night studio sessions and highly subjective client revisions']),
        "geographic_considerations": 'Major film and music capitals (Mumbai, Chennai, Hyderabad, Kolkata, Punjab, NCR) and home studios worldwide.',
        "regulated": 0,
        "source_urls": json.dumps([           {'title': 'Ableton Learning Music & Synths', 'url': 'https://learningmusic.ableton.com'},
            {           'title': 'Cambridge Music Technology Free Multitrack Library',
                        'url': 'https://www.cambridge-mt.com/ms/mtk'},
            {'title': 'Audio Engineering Society (AES India)', 'url': 'https://aes.org'}]),
        "last_verified": '2026-10-10',
    },
    {
        "slug": 'animator-visual-artist',
        "title": '3D Animator & Visual Development Artist',
        "category": 'Creative & Design',
        "short_description": ('Brings virtual characters, objects, and environments to life through keyframe animation, 3D modeling, texturing, '
 'character rigging, and lighting for films, games, and VR experiences.'),
        "typical_responsibilities": json.dumps([           'Animate stylized and realistic character movement applying the 12 Principles of Animation',
            'Construct skeletal character armatures, inverse kinematics (IK), and skinning weights for rigging',
            'Model 3D hard-surface and organic assets in polygonal modeling software (Blender / Maya)',
            'Paint PBR (Physically Based Rendering) texture maps for roughness, metallic, and normal maps',
            'Set up cinematic three-point lighting, ambient occlusion, and camera focal lengths for final rendering']),
        "relevant_interests": json.dumps(['animation', '3d art', 'creativity', 'fine arts', 'gaming', 'visual storytelling']),
        "relevant_strengths": json.dumps(['visual imagination', 'attention to weight and timing', 'patience', 'spatial reasoning', 'creativity']),
        "educational_requirements": ("Bachelor's degree in Animation, Visual Effects, Fine Arts (BFA), or diploma in 3D Animation with an outstanding "
 'showreel demonstrating body mechanics and acting.'),
        "min_education_level": 'Class 10',
        "suitable_streams": json.dumps(['Any stream with drawing / 3D aptitude', 'Fine Arts', 'Humanities', 'Computer Science']),
        "important_skills": json.dumps([           '12 Principles of Animation (Timing, Spacing, Squash & Stretch, Anticipation)',
            '3D Animation Software (Blender / Maya / 3ds Max)',
            'Character Rigging & Weight Painting',
            'Texturing & UV Unwrapping (Substance 3D Painter / Blender)',
            'Lighting, Rendering & Compositing (Cycles / Eevee / Arnold)',
            'Real-Time Engines (Unreal Engine 5 basics)']),
        "suggested_beginner_projects": json.dumps([           'Animate a classic bouncing ball with realistic weight, squash, and decay in free open-source Blender',
            'Model, texture, and rig a low-poly stylized character suitable for a mobile game in Blender',
            'Animate a dynamic 5-second character walk-cycle and jump obstacle in 3D']),
        "learning_roadmap": json.dumps([           {           'action': 'Complete bouncing ball, pendulum, and flour sack exercises in 2D or 3D.',
                        'duration': '4 weeks',
                        'explanation': "Read 'The Animator's Survival Kit' by Richard Williams and study timing, "
                                       'spacing, and arcs.',
                        'step': 1,
                        'title': 'Study the 12 Principles of Animation'},
            {           'action': 'Complete Blender Foundation official beginner Donut and Animation tutorials.',
                        'duration': '6 weeks',
                        'explanation': "Learn Blender's interface, viewport navigation, keyframing, graph editor, and "
                                       'dope sheet.',
                        'step': 2,
                        'title': 'Master Free 3D Software (Blender)'},
            {           'action': 'Animate 3 distinct character locomotion cycles.',
                        'duration': '8 weeks',
                        'explanation': 'Use free character rigs to animate walk cycles, run cycles, heavy lifting, and '
                                       'athletic jumps.',
                        'step': 3,
                        'title': 'Master Body Mechanics Animation'},
            {           'action': 'Animate a 10-second character acting sequence to an audio dialogue clip.',
                        'duration': '6 weeks',
                        'explanation': 'Animate dialogue lip-sync, subtle eye darts, emotional gestures, and subtext.',
                        'step': 4,
                        'title': 'Study Character Acting and Facial Animation'},
            {           'action': 'Apply to gaming, VFX, and animation studios.',
                        'duration': 'Ongoing',
                        'explanation': 'Compile your best 45–60 seconds of character animation showing clean arcs and '
                                       'strong weight.',
                        'step': 5,
                        'title': 'Assemble Animation Showreel & Apply to Studios'}]),
        "cost_category": 'Low / Free Accessible',
        "cost_estimate_detail": ('Blender is 100% free and open-source; Mid-tier graphics workstation: ₹50,000–₹1,00,000; Private animation diplomas: '
 '₹1,50,000–₹5,00,000.'),
        "low_cost_routes": ('Blender Foundation free official tutorials, open 3D rigs from Animation Mentor / Blender Studio, community art '
 'challenges.'),
        "entrance_exams": json.dumps(['UCEED', 'NID DAT', 'Institutional Animation Entrance Tests']),
        "advantages": json.dumps([           'Massive global demand driven by video games, VFX blockbuster films, animated series, and virtual '
            'simulations',
            'Blender allows anyone with a computer to learn world-class 3D craft with zero software licensing costs',
            'Deep satisfaction bringing imaginary characters and fantasy worlds to vivid life']),
        "challenges": json.dumps([           'Requires immense patience: a polished 5-second character animation can take days of meticulous '
            'fine-tuning',
            'Hardware intensive: requires capable GPU for smooth viewport playback and rendering',
            'Must keep pace with rapidly evolving real-time rendering pipelines (Unreal Engine 5) and AI procedural '
            'tools']),
        "geographic_considerations": ('Major animation and VFX clusters in Mumbai, Hyderabad, Pune, Bengaluru, Chennai, and remote international studio '
 'contracts.'),
        "regulated": 0,
        "source_urls": json.dumps([           {'title': 'Blender Foundation Open Source 3D', 'url': 'https://www.blender.org'},
            {'title': 'National Institute of Design (NID Animation)', 'url': 'https://www.nid.edu'},
            {'title': 'Animation Guild Open Resources', 'url': 'https://animationguild.org'}]),
        "last_verified": '2026-10-10',
    },
    {
        "slug": 'choreographer-performer',
        "title": 'Choreographer & Movement Director',
        "category": 'Creative & Design',
        "short_description": ('Designs original movement sequences, stage blocking, and expressive dance choreography for films, music videos, '
 'theatrical productions, dance academies, and competitive athletic routines.'),
        "typical_responsibilities": json.dumps([           'Conceive and structure thematic dance routines matching musical tempo, lyrics, and emotional narrative',
            'Teach complex choreography, footwork, and movement dynamics to dancers of varying experience levels',
            'Coordinate stage blocking, spatial formations, and camera angles with directors and lighting crews',
            'Design physical warm-ups, conditioning routines, and injury prevention exercises for performers',
            'Direct live dance rehearsals, audition casting, and stage performances under production deadlines']),
        "relevant_interests": json.dumps(['dance', 'choreography', 'performing arts', 'music', 'fitness', 'creativity']),
        "relevant_strengths": json.dumps(['physical agility', 'musical rhythm', 'creativity', 'spatial awareness', 'leadership', 'communication']),
        "educational_requirements": ('Degree or diploma in Performing Arts (Dance / Choreography) or extensive professional training under accredited '
 'dance masters (Gurus) and dance academies with proven performance credits.'),
        "min_education_level": 'Class 10',
        "suitable_streams": json.dumps(['Any stream with physical agility and musical rhythm', 'Humanities / Arts', 'Performing Arts']),
        "important_skills": json.dumps([           'Dance Technique & Movement Vocabulary (Classical, Contemporary, Urban/Hip-hop)',
            'Choreographic Composition & Spatial Formations',
            'Rhythm, Musicality & Tempo Counting',
            'Dancer Coaching & Rehearsal Leadership',
            'Stage Staging & Camera Framing Awareness',
            'Physical Conditioning & Injury Prevention']),
        "suggested_beginner_projects": json.dumps([           'Choreograph and record a 60-second original dance piece interpreting a musical piece with a clear '
            'emotional arc',
            'Design a synchronized group routine for a 5-member campus or local dance team and conduct rehearsals',
            'Create an instructional video breaking down fundamental movement techniques and warm-up safety for '
            'beginners']),
        "learning_roadmap": json.dumps([           {           'action': 'Enroll in structured dance training with daily practice.',
                        'duration': '2–4 years',
                        'explanation': 'Train extensively in classical, contemporary, folk, or street dance '
                                       'foundations.',
                        'step': 1,
                        'title': 'Build Rigorous Physical Technique in a Dance Form'},
            {           'action': 'Choreograph a short solo piece and seek peer critique.',
                        'duration': '6 months',
                        'explanation': 'Learn spatial pathways, canon, unison, contrast, levels (high/low), and '
                                       'musical counts.',
                        'step': 2,
                        'title': 'Study Choreographic Principles and Composition'},
            {           'action': 'Audition for dance ensembles or collegiate performance teams.',
                        'duration': '1–2 years',
                        'explanation': 'Perform in professional dance troupes, theatrical musicals, or assist senior '
                                       'choreographers on set.',
                        'step': 3,
                        'title': 'Gain Assistant Choreographer / Troupe Experience'},
            {           'action': 'Direct and film 2 dance concept videos with multicam coverage.',
                        'duration': '4 months',
                        'explanation': 'Understand camera angles, movement tracking, and theatrical lighting to '
                                       'enhance movement visual impact.',
                        'step': 4,
                        'title': 'Learn Video Staging and Lighting Design'},
            {           'action': 'Build a client portfolio and social media video showreel.',
                        'duration': 'Ongoing',
                        'explanation': 'Direct routines for films, commercials, music videos, or found a professional '
                                       'dance training academy.',
                        'step': 5,
                        'title': 'Establish Independent Choreography Practice or Academy'}]),
        "cost_category": 'Low / Free Accessible',
        "cost_estimate_detail": 'State Performing Arts Universities (BPA): ₹15,000–₹50,000 total; Specialized private academies: ₹50,000–₹2,00,000.',
        "low_cost_routes": ('Government performing arts academies (Sangeet Natak Akademi affiliates, university dance departments), cultural '
 'scholarships, and community performance troupes.'),
        "entrance_exams": json.dumps(['CUET (UG) Performing Arts', 'Institutional Dance Auditions']),
        "advantages": json.dumps([           'Deep personal expression through visceral, energetic physical artistry',
            'Expanding commercial opportunities across film production, weddings, corporate events, reality '
            'television, and fitness dance academies',
            'Lifelong community building and mentorship of upcoming dance and movement talent']),
        "challenges": json.dumps([           'High physical demands on joints and muscles; requires disciplined injury prevention and recovery regimens',
            'Income can be project-based and seasonal, requiring self-promotion and networking',
            'Requires patience and communication to train dancers of varying skill levels']),
        "geographic_considerations": ('Entertainment centers (Mumbai, Chennai, Hyderabad, Kolkata), national cultural hubs, and dance studios across tier-1 '
 'and tier-2 cities.'),
        "regulated": 0,
        "source_urls": json.dumps([           {           'title': 'Sangeet Natak Akademi (National Academy of Music, Dance and Drama)',
                        'url': 'https://sangeetnatak.gov.in'},
            {'title': 'Kathak Kendra / Kalakshetra Foundation', 'url': 'https://www.kalakshetra.in'},
            {'title': 'International Dance Council (CID UNESCO)', 'url': 'https://www.cid-world.org'}]),
        "last_verified": '2026-10-10',
    },
    {
        "slug": 'public-policy-civil-services',
        "title": 'Civil Services Officer & Public Policy Administrator',
        "category": 'Education & Social',
        "short_description": ('Directs administrative governance, policy implementation, law and order enforcement, socio-economic welfare schemes, '
 'and public revenue systems through constitutional and statutory authorities.'),
        "typical_responsibilities": json.dumps([           'Administer district governance, public revenue collection, and land administration',
            'Oversee execution of government welfare programs (rural employment, healthcare, public education)',
            'Coordinate emergency disaster response, humanitarian relief, and law-and-order maintenance',
            'Draft policy recommendations, cabinet briefing notes, and statutory regulatory notifications',
            'Address citizen grievances and ensure transparent delivery of public municipal services']),
        "relevant_interests": json.dumps(['public service', 'governance', 'law', 'social impact', 'leadership', 'policy']),
        "relevant_strengths": json.dumps(['leadership', 'ethical integrity', 'decision-making under pressure', 'communication', 'analytical thinking']),
        "educational_requirements": ("Bachelor's degree in any discipline from a recognized university. Mandatory qualification through competitive civil "
 'service examinations (UPSC Civil Services Examination for IAS/IPS/IFS or State Public Service Commission exams). '
 'Nonpartisan statutory administration.'),
        "min_education_level": 'Undergraduate',
        "suitable_streams": json.dumps(['Any stream', 'Humanities / Arts (History, Pol Science, Geography)', 'Commerce', 'Science / Engineering']),
        "important_skills": json.dumps([           'Public Administration & District Governance',
            'Constitutional Law & Statutory Regulations',
            'Policy Analysis & Socio-Economic Assessment',
            'Disaster Management & Crisis Leadership',
            'Public Budgeting & Financial Allocation',
            'Empathetic Citizen Grievance Redressal']),
        "suggested_beginner_projects": json.dumps([           'Conduct an empirical audit of a local municipal grievance redressal system or public distribution scheme',
            'Write a structured 5-page policy brief proposing solutions to urban solid waste management in your '
            'municipality',
            'Participate in a Model United Nations (MUN) or Youth Parliament debating public welfare legislation']),
        "learning_roadmap": json.dumps([           {           'action': 'Read NCERT Class 6–12 textbooks and daily national newspapers.',
                        'duration': '1–2 years',
                        'explanation': 'Master NCERT fundamentals in history, geography, polity, economics, and '
                                       'environment.',
                        'step': 1,
                        'title': 'Build Broad General Studies & Current Affairs Awareness'},
            {           'action': 'Complete undergraduate degree in arts, science, or engineering.',
                        'duration': '3–4 years',
                        'explanation': 'Maintain strong graduation record while developing critical analytical and '
                                       'essay writing skills.',
                        'step': 2,
                        'title': "Earn Bachelor's Degree in Any Discipline"},
            {           'action': 'Solve 30 full-length prelims previous-year question papers.',
                        'duration': '9–12 months',
                        'explanation': 'Master General Studies Paper I and Civil Services Aptitude Test (CSAT) with '
                                       'extensive mock tests.',
                        'step': 3,
                        'title': 'Prepare for UPSC / State PSC Preliminary Exam'},
            {           'action': 'Write 50 practice answers and participate in evaluation test series.',
                        'duration': '6–9 months',
                        'explanation': 'Practice intensive answer writing across 9 descriptive papers including Essay, '
                                       'GS I–IV, and Optional Subject.',
                        'step': 4,
                        'title': 'UPSC Main Written Examination Prep'},
            {           'action': 'Attend mock interviews and complete foundational civil service induction.',
                        'duration': 'Post-selection',
                        'explanation': 'Clear interview panel on personality, ethics, and current issues; undergo '
                                       'training at LBSNAA.',
                        'step': 5,
                        'title': 'Personality Test (Interview) & Academy Foundation Training'}]),
        "cost_category": 'Low / Free Accessible',
        "cost_estimate_detail": ('Govt University degree: ₹10,000–₹50,000 total; Exam fee: ₹100 (free for female/SC/ST candidates); NCERT textbooks: '
 '₹1,500.'),
        "low_cost_routes": ('NCERT books (available free online), Press Information Bureau (PIB), Rajya Sabha / Sansad TV debates, public '
 'libraries, free civil services study initiatives.'),
        "entrance_exams": json.dumps([           'UPSC Civil Services Examination (Prelims, Mains, Interview)',
            'State Public Service Commission Examinations (State PSC)']),
        "advantages": json.dumps([           'Unmatched institutional scale to positively impact millions of lives and public welfare',
            'High constitutional status, security of tenure, and respect in society',
            'Diverse administrative exposure spanning rural development, health, transport, and finance']),
        "challenges": json.dumps([           'Extremely competitive examination with acceptance rate below 0.1% among over 1 million applicants',
            'Demanding 24/7 public accountability during emergencies, natural disasters, and administrative crises',
            'Regular transfers across districts and remote administrative postings']),
        "geographic_considerations": ('District collectorates, state secretariats, central government ministries (New Delhi), and diplomatic missions '
 'worldwide.'),
        "regulated": 1,
        "source_urls": json.dumps([           {'title': 'Union Public Service Commission (UPSC)', 'url': 'https://www.upsc.gov.in'},
            {           'title': 'Lal Bahadur Shastri National Academy of Administration (LBSNAA)',
                        'url': 'https://www.lbsnaa.gov.in'},
            {'title': 'National Portal of India - Governance', 'url': 'https://www.india.gov.in'}]),
        "last_verified": '2026-10-10',
    },
]

# ============================================================================
# Curated & Verified Opportunities Seed Data
# ============================================================================

INITIAL_OPPORTUNITIES = [
    # --- Civil Engineering & Construction ---
    {
        "title": "Graduate & Technician Apprentice - Civil Engineering",
        "employer_or_source": "National Apprenticeship Training Scheme (NATS / MHRD)",
        "category": "Civil Engineering & Construction",
        "opportunity_type": "Apprenticeship",
        "location_city": "Delhi NCR",
        "work_mode": "on_site",
        "eligibility": "B.Tech / B.E. or Diploma in Civil Engineering (Recent Graduates)",
        "skills_required": json.dumps(["Site Measurement", "AutoCAD Basics", "Quality Checks", "IS Code Awareness"]),
        "schedule_type": "Full-Time (1 Year Statutory Apprenticeship)",
        "stipend_or_compensation": "Stipend as per Central Apprenticeship Rules (₹8,000–₹12,000/month)",
        "is_verified": 1,
        "verification_status": "Verified Official Portal Framework",
        "last_verified": "2026-10-10",
        "application_deadline": "Annual National Enrolment Cycle",
        "official_url": "http://mhrdnats.gov.in",
        "description": "Statutory apprentice positions under the Ministry of Education & National Apprenticeship Training Scheme across central/state infrastructure organizations including CPWD, NHAI, Metro Rail, and state PWDs.",
        "source_portal": "NATS Portal (MHRD)",
        "career_slug": "civil-engineer",
        "milestone_tag": "step-7"
    },
    {
        "title": "Junior CAD Drafting & Modeling Intern",
        "employer_or_source": "Infrastructure Design Consulting Hub",
        "category": "Civil Engineering & Construction",
        "opportunity_type": "Internship",
        "location_city": "Bengaluru",
        "work_mode": "hybrid",
        "eligibility": "Diploma / 2nd-4th Year B.Tech Civil Engineering Students",
        "skills_required": json.dumps(["AutoCAD 2D", "Orthographic Projections", "Dimensioning", "PDF Plotting"]),
        "schedule_type": "Study-Friendly / Flexible (20 hrs/week)",
        "stipend_or_compensation": "₹6,000–₹10,000/month stipend + Training certificate",
        "is_verified": 1,
        "verification_status": "Verified Official Portal Framework",
        "last_verified": "2026-10-10",
        "application_deadline": "Rolling Admissions / Summer Intake",
        "official_url": "https://internship.aicte-india.org",
        "description": "Hands-on drafting internship converting conceptual architectural layouts into precision engineering drawings, column grids, and municipal sanction sheets under licensed structural engineers.",
        "source_portal": "AICTE Internship Portal",
        "career_slug": "civil-engineer",
        "milestone_tag": "step-2"
    },
    {
        "title": "Smart Cities Urban Infrastructure Trainee",
        "employer_or_source": "Smart Cities Mission / AICTE Urban Internship",
        "category": "Civil Engineering & Construction",
        "opportunity_type": "Internship",
        "location_city": "Jaipur",
        "work_mode": "on_site",
        "eligibility": "B.Tech / B.Arch Students with urban interest",
        "skills_required": json.dumps(["Site Observation", "Surveying Basics", "Documentation", "Teamwork"]),
        "schedule_type": "Summer Internship (6–8 weeks)",
        "stipend_or_compensation": "Certificate of Completion + Project Allowance",
        "is_verified": 1,
        "verification_status": "Verified Official Portal Framework",
        "last_verified": "2026-10-10",
        "application_deadline": "AICTE Seasonal Cycle",
        "official_url": "https://internship.aicte-india.org",
        "description": "Government-partnered student internship observing urban drainage, transport corridor development, and municipal water supply monitoring projects.",
        "source_portal": "AICTE Internship Portal",
        "career_slug": "civil-engineer",
        "milestone_tag": "step-7"
    },
    {
        "title": "Site Quality & Safety Supervisory Assistant",
        "employer_or_source": "National Career Service (Ministry of Labour)",
        "category": "Civil Engineering & Construction",
        "opportunity_type": "Entry-Level",
        "location_city": "Mumbai",
        "work_mode": "on_site",
        "eligibility": "Diploma / B.Tech Civil or Construction Management",
        "skills_required": json.dumps(["Slump Test", "Cube Compressive Strength", "Bar Bending Checks", "Safety Protocols"]),
        "schedule_type": "Full-Time Trainee Role",
        "stipend_or_compensation": "Industry Standard Trainee Remuneration",
        "is_verified": 1,
        "verification_status": "Verified Official Portal Framework",
        "last_verified": "2026-10-10",
        "application_deadline": "Rolling Vacancy Portal",
        "official_url": "https://www.ncs.gov.in",
        "description": "Assist on-site project engineers with material testing, concrete slump verification, reinforcement inspection, and safety documentation.",
        "source_portal": "National Career Service (NCS)",
        "career_slug": "civil-engineer",
        "milestone_tag": "step-8"
    },

    # --- IT & Software Opportunities ---
    {
        "title": "AICTE Digital Skills & Open Innovation Software Intern",
        "employer_or_source": "AICTE Partner Innovation Initiative",
        "category": "IT & Software",
        "opportunity_type": "Internship",
        "location_city": "Remote",
        "work_mode": "remote",
        "eligibility": "Undergraduate Students (Any Engineering / BCA / B.Sc)",
        "skills_required": json.dumps(["Python or JavaScript", "Git & GitHub", "Problem Solving", "Web Basics"]),
        "schedule_type": "Study-Friendly / Self-Paced (12–15 hrs/week)",
        "stipend_or_compensation": "Free Certification + Industry Mentorship",
        "is_verified": 1,
        "verification_status": "Verified Official Portal Framework",
        "last_verified": "2026-10-10",
        "application_deadline": "Ongoing Batch Registrations",
        "official_url": "https://internship.aicte-india.org",
        "description": "Virtual technical internship completing open-source projects, cloud computing fundamentals, and real software modules under AICTE corporate partnership guidelines.",
        "source_portal": "AICTE Internship Portal",
        "career_slug": "software-developer",
        "milestone_tag": "step-4"
    },
    {
        "title": "Frontend Web & Accessible UI Trainee",
        "employer_or_source": "Civic Tech Innovation Lab",
        "category": "IT & Software",
        "opportunity_type": "Internship",
        "location_city": "Bengaluru",
        "work_mode": "hybrid",
        "eligibility": "Students with HTML/CSS/JS and web development portfolio",
        "skills_required": json.dumps(["HTML5", "CSS3", "Vanilla JavaScript", "Responsive Design", "Accessibility WCAG"]),
        "schedule_type": "Part-Time (18 hrs/week)",
        "stipend_or_compensation": "₹8,000–₹14,000/month",
        "is_verified": 1,
        "verification_status": "Verified Official Portal Framework",
        "last_verified": "2026-10-10",
        "application_deadline": "Rolling Applications",
        "official_url": "https://www.ncs.gov.in",
        "description": "Build responsive glassmorphic student portals, accessible interfaces, and interactive dashboards using modern web standards.",
        "source_portal": "National Career Service (NCS)",
        "career_slug": "software-developer",
        "milestone_tag": "step-3"
    },
    {
        "title": "FOSS Open Source Software Fellowship",
        "employer_or_source": "Free & Open Source Software Foundation",
        "category": "IT & Software",
        "opportunity_type": "Freelance Project",
        "location_city": "Remote",
        "work_mode": "remote",
        "eligibility": "Open to all students with active GitHub presence",
        "skills_required": json.dumps(["Git Workflow", "Python / Go / Rust / JS", "Issue Triage", "Unit Testing"]),
        "schedule_type": "Flexible / Weekend Friendly",
        "stipend_or_compensation": "Project Grant or Open Recognition",
        "is_verified": 1,
        "verification_status": "Verified Community Framework",
        "last_verified": "2026-10-10",
        "application_deadline": "Continuous Open Call",
        "official_url": "https://summerofcode.withgoogle.com",
        "description": "Contribute bug fixes, feature requests, and documentation to public open-source tools; an internationally recognized stepping stone for entry-level engineering roles.",
        "source_portal": "Open Source Community",
        "career_slug": "software-developer",
        "milestone_tag": "step-4"
    },

    # --- Business & Finance Opportunities ---
    {
        "title": "ICAI Mandatory Article Assistant / CA Trainee",
        "employer_or_source": "Institute of Chartered Accountants of India (ICAI)",
        "category": "Business & Finance",
        "opportunity_type": "Apprenticeship",
        "location_city": "Mumbai",
        "work_mode": "on_site",
        "eligibility": "Passed CA Intermediate (Either or Both Groups) + ICITSS Completed",
        "skills_required": json.dumps(["Tally / ERP", "Tax Filing Concepts", "Audit Vouching", "MS Excel"]),
        "schedule_type": "Full-Time (2 Years Practical Training under CA Regulations)",
        "stipend_or_compensation": "Stipend as mandated by ICAI regulations (₹3,000–₹10,000+/month based on city tier)",
        "is_verified": 1,
        "verification_status": "Verified Statutory Body Portal",
        "last_verified": "2026-10-10",
        "application_deadline": "Continuous Post-Intermediate Enrolment",
        "official_url": "https://www.icai.org",
        "description": "Mandatory statutory practical articleship under a practicing Chartered Accountant firm covering statutory audits, direct tax compliance, GST returns, and corporate accounting.",
        "source_portal": "ICAI Official Portal",
        "career_slug": "chartered-accountant",
        "milestone_tag": "step-5"
    },
    {
        "title": "Market Research & Business Intelligence Intern",
        "employer_or_source": "Commercial Advisory Services",
        "category": "Business & Finance",
        "opportunity_type": "Internship",
        "location_city": "Kolkata",
        "work_mode": "hybrid",
        "eligibility": "B.Com / BBA / Economics / Statistics Students",
        "skills_required": json.dumps(["Excel Modeling", "Data Analysis", "Survey Design", "PowerPoint Storytelling"]),
        "schedule_type": "Study-Friendly (15–20 hrs/week)",
        "stipend_or_compensation": "₹7,000–₹11,000/month",
        "is_verified": 1,
        "verification_status": "Verified Official Portal Framework",
        "last_verified": "2026-10-10",
        "application_deadline": "Rolling Quarter Admissions",
        "official_url": "https://www.ncs.gov.in",
        "description": "Conduct secondary industry research, evaluate pricing models across consumer goods, and prepare executive intelligence summaries for corporate decision makers.",
        "source_portal": "National Career Service (NCS)",
        "career_slug": "business-analyst",
        "milestone_tag": "step-3"
    },
    {
        "title": "Logistics & Supply Chain Operations Apprentice",
        "employer_or_source": "National Apprenticeship Promotion Scheme (NAPS)",
        "category": "Business & Finance",
        "opportunity_type": "Apprenticeship",
        "location_city": "Pune",
        "work_mode": "on_site",
        "eligibility": "Diploma / Undergraduate in Commerce, Management, or Engineering",
        "skills_required": json.dumps(["Inventory Tracking", "Dispatch Scheduling", "ERP Data Entry", "Process Audit"]),
        "schedule_type": "Full-Time Apprenticeship (1 Year)",
        "stipend_or_compensation": "Government Co-funded Stipend",
        "is_verified": 1,
        "verification_status": "Verified Official Portal Framework",
        "last_verified": "2026-10-10",
        "application_deadline": "Annual Regional Drive",
        "official_url": "https://www.apprenticeshipindia.gov.in",
        "description": "Government recognized apprenticeship program observing warehouse operations, barcode inventory handling, freight tracking, and supply chain fulfillment.",
        "source_portal": "NAPS Portal (MSDE)",
        "career_slug": "supply-chain-manager",
        "milestone_tag": "step-4"
    },

    # --- Sports & Fitness Opportunities ---
    {
        "title": "Grassroots Sports Event & Competition Trainee",
        "employer_or_source": "Sports Authority of India (SAI) / State Sports Council",
        "category": "Sports & Fitness",
        "opportunity_type": "Campus Opportunity",
        "location_city": "Delhi NCR",
        "work_mode": "on_site",
        "eligibility": "Enrolled College / University Students (Active Sports Background)",
        "skills_required": json.dumps(["Tournament Logistics", "Participant Registration", "Scorekeeping", "First Aid Basics"]),
        "schedule_type": "Weekend Tournament Cycles (Flexible)",
        "stipend_or_compensation": "Daily Match Allowance + Official SAI Certificate",
        "is_verified": 1,
        "verification_status": "Verified Official Body Portal",
        "last_verified": "2026-10-10",
        "application_deadline": "Pre-Tournament Seasonal Calls",
        "official_url": "https://sportsauthorityofindia.nic.in",
        "description": "Support grassroots athletics and school tournament operations under state and central youth sports schemes, managing participant verifications and on-field logistics.",
        "source_portal": "Sports Authority of India (SAI)",
        "career_slug": "sports-event-manager",
        "milestone_tag": "step-2"
    },
    {
        "title": "Performance Video Tagging & Sports Analytics Assistant",
        "employer_or_source": "Regional Sports High Performance Center",
        "category": "Sports & Fitness",
        "opportunity_type": "Internship",
        "location_city": "Bengaluru",
        "work_mode": "hybrid",
        "eligibility": "Students with passion for sports tactics & basic data skills",
        "skills_required": json.dumps(["Kinovea / Video Software", "Excel Data Entry", "Tactical Observation", "Patience"]),
        "schedule_type": "Study-Friendly / Part-Time (16 hrs/week)",
        "stipend_or_compensation": "₹6,000–₹10,000/month",
        "is_verified": 1,
        "verification_status": "Verified Official Body Portal",
        "last_verified": "2026-10-10",
        "application_deadline": "Rolling Academic Terms",
        "official_url": "https://kheloindia.gov.in",
        "description": "Tag match footage and generate performance stat sheets for youth development squads in football, badminton, or cricket.",
        "source_portal": "Khelo India Portal",
        "career_slug": "sports-analyst",
        "milestone_tag": "step-2"
    },
    {
        "title": "Assistant Strength & Conditioning Coach Trainee",
        "employer_or_source": "District Athletics & Fitness Academy",
        "category": "Sports & Fitness",
        "opportunity_type": "Apprenticeship",
        "location_city": "Hyderabad",
        "work_mode": "on_site",
        "eligibility": "Pursuing B.P.Ed, Sports Science, or Fitness Certification",
        "skills_required": json.dumps(["Warmup Protocols", "Exercise Technique Monitoring", "Agility Drills", "CPR"]),
        "schedule_type": "Morning / Evening Sessions (14 hrs/week)",
        "stipend_or_compensation": "Practical Mentorship + Academy Allowance",
        "is_verified": 1,
        "verification_status": "Verified Official Portal Framework",
        "last_verified": "2026-10-10",
        "application_deadline": "Ongoing Enrollment",
        "official_url": "https://nsnis.org",
        "description": "Supervised coaching apprenticeship assisting licensed head trainers with youth athlete warm-ups, speed-agility drills, and recovery protocols.",
        "source_portal": "National Institute of Sports (NSNIS)",
        "career_slug": "sports-coach",
        "milestone_tag": "step-4"
    },

    # --- Part-Time & Campus Opportunities ---
    {
        "title": "Campus Peer Academic Tutor (Mathematics & Science)",
        "employer_or_source": "University Student Learning Center",
        "category": "Part-Time & Campus",
        "opportunity_type": "Part-Time",
        "location_city": "Delhi NCR",
        "work_mode": "on_site",
        "eligibility": "Undergraduate Students with Grade A/B+ in Subject",
        "skills_required": json.dumps(["Clear Explanation", "Patience", "Subject Knowledge", "Empathy"]),
        "schedule_type": "Part-Time (8–12 hrs/week, Post-Class)",
        "stipend_or_compensation": "Hourly Student Honorarium (₹250–₹400/hour)",
        "is_verified": 1,
        "verification_status": "Verified Educational Framework",
        "last_verified": "2026-10-10",
        "application_deadline": "Semester Startup Cycle",
        "official_url": "https://www.ncs.gov.in",
        "description": "Help junior classmates and school students understand foundational algebra, calculus, physics, or coding logic during evening study circles.",
        "source_portal": "University Career Services",
        "career_slug": "teacher-educator",
        "milestone_tag": "step-3"
    },
    {
        "title": "Digital Library & Archives Student Assistant",
        "employer_or_source": "Central University Library Division",
        "category": "Part-Time & Campus",
        "opportunity_type": "Campus Opportunity",
        "location_city": "Chandigarh",
        "work_mode": "on_site",
        "eligibility": "Regular Enrolled College Students",
        "skills_required": json.dumps(["Catalogue Data Entry", "Book Indexing", "Quiet Professionalism", "Basic Computer Skills"]),
        "schedule_type": "Study-Friendly (10 hrs/week)",
        "stipend_or_compensation": "Monthly Work-Study Stipend",
        "is_verified": 1,
        "verification_status": "Verified Educational Framework",
        "last_verified": "2026-10-10",
        "application_deadline": "Annual Semester Drive",
        "official_url": "https://www.ncs.gov.in",
        "description": "Work-study opportunity assisting academic librarians with e-journal cataloguing, digital repository tagging, and student reference assistance.",
        "source_portal": "University Career Services",
        "career_slug": "general",
        "milestone_tag": "step-1"
    },
    {
        "title": "Community STEM & Coding Club Volunteer Mentor",
        "employer_or_source": "Youth Science Foundation India",
        "category": "Part-Time & Campus",
        "opportunity_type": "Freelance Project",
        "location_city": "Remote",
        "work_mode": "remote",
        "eligibility": "College Students enthusiastic about STEM education",
        "skills_required": json.dumps(["Scratch / Python Basics", "Youth Mentoring", "Creative Activities", "Public Speaking"]),
        "schedule_type": "Weekend Only (4 hrs/weekend)",
        "stipend_or_compensation": "Volunteer Certificate + Recognition Letter",
        "is_verified": 1,
        "verification_status": "Verified Community Framework",
        "last_verified": "2026-10-10",
        "application_deadline": "Rolling Batch Onboarding",
        "official_url": "https://www.ncs.gov.in",
        "description": "Conduct fun, interactive weekend online coding and science demonstrations for middle-school students in underserved communities.",
        "source_portal": "National Career Service (NCS)",
        "career_slug": "teacher-educator",
        "milestone_tag": "step-3"
    }
]

# ============================================================================
# Career Inspiration Quotes & Field-Specific Explanations
# ============================================================================

INITIAL_CAREER_QUOTES = [
    {
        "quote": "Your first career choice is a starting point, not a life sentence.",
        "author": "CareerCompass Guidance",
        "category": "General",
        "practical_tip": "Careers today are fluid. You can begin in one role, build transferable problem-solving skills, and transition into adjacent domains as your curiosity matures.",
        "suggested_action": "Focus on building core strengths this semester rather than stressing about where you will be 20 years from now."
    },
    {
        "quote": "Choose a path that matches your interests, then build the skills to move forward.",
        "author": "CareerCompass Guidance",
        "category": "General",
        "practical_tip": "Natural curiosity provides the energy to practice during difficult learning plateaus. Align your work style with your daily routine.",
        "suggested_action": "Pick one skill you are genuinely curious about and schedule 30 minutes of daily hands-on practice."
    },
    {
        "quote": "Your marks are one part of your story. Your curiosity, practice, and persistence matter too.",
        "author": "CareerCompass Guidance",
        "category": "General",
        "practical_tip": "Exam percentages open initial doors, but real-world capability is defined by tangible projects, reliable communication, and resilience when facing bugs or site challenges.",
        "suggested_action": "Build a tangible micro-project that proves your skills directly to employers or mentors."
    },
    {
        "quote": "Before choosing a career, try a small project that shows you what the work is actually like.",
        "author": "CareerCompass Guidance",
        "category": "General",
        "practical_tip": "A weekend micro-project reveals the reality of a field 10x faster than reading generic opinions or salary speculation online.",
        "suggested_action": "Browse the 'Suggested Beginner Projects' in any Career Detail page and spend this weekend testing one."
    },
    {
        "quote": "Progress comes from informed decisions and consistent learning, not from comparing your journey with someone else's.",
        "author": "CareerCompass Guidance",
        "category": "General",
        "practical_tip": "Every student has different family circumstances, financial constraints, and learning rhythms. Design a plan that honors your personal realities.",
        "suggested_action": "Use the Career Reality Simulator to evaluate trade-offs based on your budget, not external peer pressure."
    },
    {
        "quote": "Civil engineering transforms sketches on paper into enduring physical infrastructure for communities.",
        "author": "CareerCompass Guidance",
        "category": "Civil Engineering",
        "practical_tip": "Try sketching a simple floor plan or observing how a local building project is organized before deciding on construction pathways.",
        "suggested_action": "Download free CAD software (FreeCAD or educational AutoCAD) and draft your own room or house floor plan with accurate measurements."
    },
    {
        "quote": "Great software is not written overnight; it is built through patient debugging and curious experimentation.",
        "author": "CareerCompass Guidance",
        "category": "Software & IT",
        "practical_tip": "Build a small webpage or automate a repetitive task to test whether you enjoy solving technical problems before enrolling in expensive courses.",
        "suggested_action": "Write a 30-line Python script or create a simple interactive HTML quiz to experience the satisfaction of working code."
    },
    {
        "quote": "Business is about creating real value for people and solving bottlenecks sustainably.",
        "author": "CareerCompass Guidance",
        "category": "Business & Commerce",
        "practical_tip": "Choose a familiar process in a local shop or campus club, identify a problem, and suggest a measurable improvement in cost or speed.",
        "suggested_action": "Build an Excel model tracking your weekly budget or analyze a small business's customer acquisition funnel."
    },
    {
        "quote": "Sports careers span far beyond playing on the field into science, event management, coaching, and analytics.",
        "author": "CareerCompass Guidance",
        "category": "Sports & Athletics",
        "practical_tip": "Explore coaching, sports science, officiating, event management, and athlete development; each provides a viable, fulfilling professional career in sports.",
        "suggested_action": "Volunteer to record match statistics or help coordinate logistics at a local school or club tournament this month."
    },
    {
        "quote": "Healing and healthcare demand both precise scientific knowledge and deep human empathy.",
        "author": "CareerCompass Guidance",
        "category": "Healthcare & Sciences",
        "practical_tip": "Shadow a local healthcare clinic, community health worker, or physiotherapist to witness the real daily rhythm of patient care.",
        "suggested_action": "Complete a certified first-aid training workshop to build early emergency response confidence."
    }
]

# ============================================================================
# Stage Group Definitions for Flexible Roadmap Navigation (Feature 4 & 5)
# ============================================================================

STAGE_GROUPS = {
    "A": {
        "id": "A",
        "code": "STAGE_A",
        "name": "School Exploration",
        "icon": "🎒",
        "description": "Discover genuine curiosity, school subjects you enjoy, and initial broad career awareness.",
        "education_levels": ["Class 10", "High School"]
    },
    "B": {
        "id": "B",
        "code": "STAGE_B",
        "name": "Subject & Stream Selection",
        "icon": "🧭",
        "description": "Evaluate academic streams (Science PCM/PCB, Commerce, Humanities), prerequisites, and alternative vocational routes.",
        "education_levels": ["Class 10", "Class 11-12"]
    },
    "C": {
        "id": "C",
        "code": "STAGE_C",
        "name": "College & Degree Foundations",
        "icon": "🎓",
        "description": "Master foundational concepts, core mathematics/sciences, and engineering or professional drawing.",
        "education_levels": ["Undergraduate", "Diploma", "B.Tech"]
    },
    "D": {
        "id": "D",
        "code": "STAGE_D",
        "name": "Specialization & Micro-Projects",
        "icon": "🔬",
        "description": "Select sub-disciplines, complete practical micro-projects, and master modern industry software tools.",
        "education_levels": ["Undergraduate", "Diploma", "B.Tech"]
    },
    "E": {
        "id": "E",
        "code": "STAGE_E",
        "name": "Internships & Practical Experience",
        "icon": "🏗️",
        "description": "Gain supervised field experience, site visits, apprentice programs (NATS/AICTE), and professional communication.",
        "education_levels": ["Undergraduate", "B.Tech", "Graduate"]
    },
    "F": {
        "id": "F",
        "code": "STAGE_F",
        "name": "Licensure, Portfolio & Employment",
        "icon": "💼",
        "description": "Prepare technical portfolio, understand building codes/statutory requirements, and target graduate trainee roles.",
        "education_levels": ["Undergraduate", "Graduate", "B.Tech"]
    },
    "G": {
        "id": "G",
        "code": "STAGE_G",
        "name": "Career Growth & Specialization",
        "icon": "🚀",
        "description": "Continuous professional development, postgraduate research, or specialized chartered practice.",
        "education_levels": ["Graduate", "Professional"]
    }
}


# ============================================================================
# Real-Time Appointment Booking System Seed Data
# ============================================================================

from datetime import datetime, timedelta

INITIAL_APPOINTMENT_PROVIDERS = [   {   'avatar_bg': '#2563EB',
        'badge_label': 'Verified Guidance Counsellor',
        'bio': 'Ph.D. in Educational Psychology with 12+ years advising students on career discovery, higher education '
               'stream selection, and family consensus.',
        'initials': 'AS',
        'is_verified': 1,
        'name': 'Dr. Ananya Sharma',
        'organization': 'CareerCompass Certified Practitioner Network',
        'rating': 4.95,
        'title': 'Senior Career & Education Counsellor'},
    {   'avatar_bg': '#1D4ED8',
        'badge_label': 'Verified Technical Mentor',
        'bio': 'Former Senior Engineering Manager with 15+ years experience in systems architecture. Conducts rigorous '
               'technical mock interviews and coding portfolio reviews.',
        'initials': 'RV',
        'is_verified': 1,
        'name': 'Rajesh Varma, M.Tech',
        'organization': 'Technology Mentorship Guild',
        'rating': 4.9,
        'title': 'Technical & Engineering Interview Coach'},
    {   'avatar_bg': '#059669',
        'badge_label': 'Verified Employment Coach',
        'bio': 'Specializes in NATS statutory apprenticeships, AICTE internship applications, ATS resume optimization, '
               'and campus-to-corporate transition.',
        'initials': 'PS',
        'is_verified': 1,
        'name': 'Priya Sundaram',
        'organization': 'National Career Service Partner Network',
        'rating': 4.88,
        'title': 'Employment & Internship Specialist'},
    {   'avatar_bg': '#7C3AED',
        'badge_label': 'Verified Family Counsellor',
        'bio': 'Certified mediator facilitating empathetic, data-backed career discussions between students and '
               'parents to build mutual trust and shared plans.',
        'initials': 'VM',
        'is_verified': 1,
        'name': 'Vikram Malhotra',
        'organization': 'Family Career Dialogue Initiative',
        'rating': 4.92,
        'title': 'Parent–Student Career Facilitator'},
    {   'avatar_bg': '#D97706',
        'badge_label': 'Verified Creative Mentor',
        'bio': 'Creative director and producer conducting showreel and portfolio critiques for students in video '
               'editing, 3D animation, choreography, and audio.',
        'initials': 'MS',
        'is_verified': 1,
        'name': 'Meera Sen, MFA',
        'organization': 'Creative Careers Collective',
        'rating': 4.85,
        'title': 'Creative Arts & Media Portfolio Advisor'},
    {   'avatar_bg': '#4B5563',
        'badge_label': 'Demonstration Mode — Practice Session',
        'bio': 'Practice session hosted by senior university scholars. Ideal for getting familiar with virtual mock '
               'interviews and testing platform tools.',
        'initials': 'CC',
        'is_verified': 0,
        'name': 'CareerCompass Peer Mentor Team',
        'organization': 'Student Ambassador Network',
        'rating': 4.7,
        'title': 'Peer Guidance & Practice Facilitator'}]

INITIAL_APPOINTMENT_TYPES = [   {   'category': 'Career Guidance',
        'cost_label': 'Free / Institutional Subsidy',
        'duration_minutes': 45,
        'format': 'Virtual Video Call',
        'full_description': 'In this 45-minute interactive video session, you will review your CareerCompass '
                            'assessment matches with a certified counsellor, dissect day-to-day realities, discuss '
                            'tuition alternatives, and formulate next steps.',
        'icon': '🧭',
        'preparation_notes': 'Complete the CareerCompass assessment before joining and have your top 2 career '
                             'interests ready for discussion.',
        'short_description': 'Personalized walkthrough of your assessment results, strengths, and realistic pathways '
                             'tailored to your interests.',
        'target_audience': 'Students in Class 9–12 and Undergraduates exploring career direction',
        'title': '1-on-1 Comprehensive Career Pathway Exploration'},
    {   'category': 'Career Guidance',
        'cost_label': 'Free / Institutional Subsidy',
        'duration_minutes': 40,
        'format': 'Virtual Video Call',
        'full_description': 'Detailed analysis of secondary school academic streams, polytechnic diploma options, and '
                            'government university prerequisites.',
        'icon': '🎓',
        'preparation_notes': 'Bring your current school marks card and a list of subjects you enjoy or struggle with.',
        'short_description': 'Data-driven advice on selecting academic streams (PCM, PCB, Commerce, Arts) and entrance '
                             'exam targets.',
        'target_audience': 'Class 10 and 11 students preparing for stream transition',
        'title': 'Higher Education & Stream Selection Strategy'},
    {   'category': 'Interview Preparation',
        'cost_label': 'Free / Institutional Subsidy',
        'duration_minutes': 60,
        'format': 'Virtual Video Call',
        'full_description': 'Simulates a genuine tier-1 software or engineering interview. Involves live shared-screen '
                            'coding, algorithmic complexity analysis, and actionable diagnostic feedback.',
        'icon': '💻',
        'preparation_notes': 'Have a browser ready for live coding. Review basic data structures (arrays, hash maps, '
                             'trees).',
        'short_description': 'Simulated live technical coding problem-solving, data structures, and engineering '
                             'architecture review with instant diagnostic feedback.',
        'target_audience': 'Engineering, Computer Science, and Data undergraduates',
        'title': 'Technical & Coding Mock Interview'},
    {   'category': 'Interview Preparation',
        'cost_label': 'Free / Institutional Subsidy',
        'duration_minutes': 45,
        'format': 'Virtual Video Call',
        'full_description': 'Covers storytelling frameworks (Situation, Task, Action, Result), leadership questions, '
                            'conflict handling, and workplace ethics scenarios.',
        'icon': '🗣️',
        'preparation_notes': 'Prepare 3 stories from your academic, team, or personal projects highlighting problem '
                             'solving.',
        'short_description': 'Practice the STAR framework, answering tricky HR questions, body language confidence, '
                             'and clear communication.',
        'target_audience': 'Final-year students, job seekers, and internship applicants',
        'title': 'Behavioral, HR & Communication Mock Interview'},
    {   'category': 'Interview Preparation',
        'cost_label': 'Free / Institutional Subsidy',
        'duration_minutes': 30,
        'format': 'Virtual Video Call',
        'full_description': 'Detailed review of bullet points, ATS readability, verifiable outcome metrics, and '
                            'portfolio presentation.',
        'icon': '📄',
        'preparation_notes': 'Have your current resume in PDF or editable format and link to your online portfolio / '
                             'GitHub.',
        'short_description': 'Live screen-share critique of your resume, GitHub, design portfolio, or LinkedIn profile '
                             'for maximum employer impact.',
        'target_audience': 'Students and fresh graduates actively applying for jobs',
        'title': 'Resume, CV & Portfolio Review'},
    {   'category': 'Employment & Internship Support',
        'cost_label': 'Free / Institutional Subsidy',
        'duration_minutes': 40,
        'format': 'Virtual Video Call',
        'full_description': 'Walks you through NATS (Ministry of Education) enrolment, AICTE internship portal '
                            'verification, eligibility criteria, and stipend rules.',
        'icon': '💼',
        'preparation_notes': 'Have your college enrollment details and student ID card handy.',
        'short_description': 'Step-by-step guidance on registering, filtering, and applying on official apprentice '
                             'portals and vetted opportunities.',
        'target_audience': 'Diploma, B.Tech, and undergraduate students seeking first practical work',
        'title': 'Internship & NATS/AICTE Portal Navigation'},
    {   'category': 'Employment & Internship Support',
        'cost_label': 'Free / Institutional Subsidy',
        'duration_minutes': 30,
        'format': 'Virtual Video Call',
        'full_description': 'Teaches students how to verify corporate recruitment portals, avoid unpaid fraudulent '
                            'schemes, and structure professional email inquiries.',
        'icon': '🛡️',
        'preparation_notes': 'Bring links to any job postings or offers you wish to verify.',
        'short_description': 'Guidance on vetting legitimate job opportunities, spotting placement scams, and '
                             'preparing application packages.',
        'target_audience': 'Job seekers and entry-level applicants',
        'title': 'Authorized Employer Connect & Opportunity Verification'},
    {   'category': 'Parent–Student Discussion',
        'cost_label': 'Free / Institutional Subsidy',
        'duration_minutes': 50,
        'format': 'Virtual Video Call',
        'full_description': 'A neutral, empathetic setting where parents and students compare pathways, discuss budget '
                            'constraints calmly, and build a consensual career roadmap.',
        'icon': '🤝',
        'preparation_notes': 'Both the student and at least one parent/guardian must attend. Complete the '
                             'Parent–Student Bridge comparison beforehand.',
        'short_description': 'Facilitated conversation using the CareerCompass Bridge tool to align student passion '
                             'with family expectations without conflict.',
        'target_audience': 'Students and their parents / guardians seeking consensus',
        'title': 'Parent–Student Facilitated Career Alignment Session'}]

def generate_seed_appointment_slots():
    """Generates 50+ realistic upcoming slots over the next 14 days."""
    slots = []
    base_date = datetime.now().date()
    
    schedule_pattern = [
        # (day_offset, start_time, end_time, type_id, provider_id, is_booked)
        (1, "10:00", "10:45", 1, 1, 0),
        (1, "11:30", "12:15", 2, 1, 0),
        (1, "14:00", "15:00", 3, 2, 0),
        (1, "15:30", "16:15", 4, 2, 0),
        (1, "17:00", "17:50", 8, 4, 0),
        
        (2, "10:00", "10:30", 5, 3, 1), # Pre-booked slot for demonstration
        (2, "11:00", "11:40", 6, 3, 0),
        (2, "14:00", "14:45", 1, 1, 0),
        (2, "15:30", "16:30", 3, 2, 0),
        (2, "17:00", "17:50", 8, 4, 0),
        
        (3, "09:30", "10:15", 4, 6, 0),
        (3, "11:00", "11:45", 7, 3, 0),
        (3, "14:00", "14:45", 1, 5, 0),
        (3, "15:30", "16:00", 5, 5, 0),
        (3, "17:00", "18:00", 3, 2, 0),
        
        (4, "10:00", "10:45", 2, 1, 0),
        (4, "11:30", "12:10", 6, 3, 0),
        (4, "14:00", "14:45", 4, 2, 0),
        (4, "16:00", "16:50", 8, 4, 0),
        
        (5, "10:00", "10:45", 1, 1, 0),
        (5, "11:30", "12:30", 3, 2, 0),
        (5, "14:00", "14:30", 5, 3, 0),
        (5, "16:00", "16:45", 7, 3, 0),
        
        (6, "11:00", "11:50", 8, 4, 0),
        (6, "14:00", "14:45", 1, 5, 0),
        (6, "15:30", "16:15", 4, 6, 0),
        
        (7, "10:00", "10:45", 1, 1, 0),
        (7, "11:30", "12:15", 2, 1, 0),
        (7, "14:00", "15:00", 3, 2, 0),
        (7, "16:00", "16:40", 6, 3, 0),
        
        (8, "10:00", "10:45", 4, 2, 0),
        (8, "11:30", "12:00", 5, 3, 0),
        (8, "14:00", "14:50", 8, 4, 0),
        (8, "16:00", "16:45", 1, 1, 0),
        
        (9, "10:30", "11:15", 7, 3, 0),
        (9, "14:00", "15:00", 3, 2, 0),
        (9, "16:00", "16:45", 1, 5, 0),
        
        (10, "10:00", "10:45", 2, 1, 0),
        (10, "11:30", "12:10", 6, 3, 0),
        (10, "14:00", "14:50", 8, 4, 0),
        (10, "16:00", "16:45", 4, 6, 0),
        
        (11, "10:00", "10:45", 1, 1, 0),
        (11, "14:00", "15:00", 3, 2, 0),
        (11, "16:00", "16:30", 5, 5, 0),
        
        (12, "11:00", "11:45", 7, 3, 0),
        (12, "14:00", "14:50", 8, 4, 0),
        
        (13, "10:00", "10:45", 1, 1, 0),
        (13, "14:00", "14:45", 4, 2, 0),
        
        (14, "10:00", "10:45", 2, 1, 0),
        (14, "14:00", "15:00", 3, 2, 0),
        (14, "16:00", "16:50", 8, 4, 0)
    ]
    
    for offset, st, et, tid, pid, booked in schedule_pattern:
        sdate = (base_date + timedelta(days=offset)).isoformat()
        slots.append({
            "type_id": tid,
            "provider_id": pid,
            "slot_date": sdate,
            "start_time": st,
            "end_time": et,
            "is_booked": booked,
            "status": "booked" if booked else "available",
            "meeting_mode": "Google Meet (Encrypted Video Link)" if tid != 7 else "Virtual Call & Screen Share"
        })
    return slots
