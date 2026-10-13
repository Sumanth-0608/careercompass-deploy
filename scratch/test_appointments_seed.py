"""
Validate appointment seed tables and generation
"""
import json
from datetime import datetime, timedelta

INITIAL_APPOINTMENT_PROVIDERS = [
    {
        "name": "Dr. Ananya Sharma",
        "title": "Senior Career & Education Counsellor",
        "organization": "CareerCompass Certified Practitioner Network",
        "is_verified": 1,
        "badge_label": "Verified Guidance Counsellor",
        "rating": 4.95,
        "bio": "Ph.D. in Educational Psychology with 12+ years advising students on career discovery, higher education stream selection, and family consensus.",
        "initials": "AS",
        "avatar_bg": "#2563EB"
    },
    {
        "name": "Rajesh Varma, M.Tech",
        "title": "Technical & Engineering Interview Coach",
        "organization": "Technology Mentorship Guild",
        "is_verified": 1,
        "badge_label": "Verified Technical Mentor",
        "rating": 4.90,
        "bio": "Former Senior Engineering Manager with 15+ years experience in systems architecture. Conducts rigorous technical mock interviews and coding portfolio reviews.",
        "initials": "RV",
        "avatar_bg": "#1D4ED8"
    },
    {
        "name": "Priya Sundaram",
        "title": "Employment & Internship Specialist",
        "organization": "National Career Service Partner Network",
        "is_verified": 1,
        "badge_label": "Verified Employment Coach",
        "rating": 4.88,
        "bio": "Specializes in NATS statutory apprenticeships, AICTE internship applications, ATS resume optimization, and campus-to-corporate transition.",
        "initials": "PS",
        "avatar_bg": "#059669"
    },
    {
        "name": "Vikram Malhotra",
        "title": "Parent–Student Career Facilitator",
        "organization": "Family Career Dialogue Initiative",
        "is_verified": 1,
        "badge_label": "Verified Family Counsellor",
        "rating": 4.92,
        "bio": "Certified mediator facilitating empathetic, data-backed career discussions between students and parents to build mutual trust and shared plans.",
        "initials": "VM",
        "avatar_bg": "#7C3AED"
    },
    {
        "name": "Meera Sen, MFA",
        "title": "Creative Arts & Media Portfolio Advisor",
        "organization": "Creative Careers Collective",
        "is_verified": 1,
        "badge_label": "Verified Creative Mentor",
        "rating": 4.85,
        "bio": "Creative director and producer conducting showreel and portfolio critiques for students in video editing, 3D animation, choreography, and audio.",
        "initials": "MS",
        "avatar_bg": "#D97706"
    },
    {
        "name": "CareerCompass Peer Mentor Team",
        "title": "Peer Guidance & Practice Facilitator",
        "organization": "Student Ambassador Network",
        "is_verified": 0,
        "badge_label": "Demonstration Mode — Practice Session",
        "rating": 4.70,
        "bio": "Practice session hosted by senior university scholars. Ideal for getting familiar with virtual mock interviews and testing platform tools.",
        "initials": "CC",
        "avatar_bg": "#4B5563"
    }
]

INITIAL_APPOINTMENT_TYPES = [
    {
        "category": "Career Guidance",
        "title": "1-on-1 Comprehensive Career Pathway Exploration",
        "format": "Virtual Video Call",
        "duration_minutes": 45,
        "cost_label": "Free / Institutional Subsidy",
        "short_description": "Personalized walkthrough of your assessment results, strengths, and realistic pathways tailored to your interests.",
        "full_description": "In this 45-minute interactive video session, you will review your CareerCompass assessment matches with a certified counsellor, dissect day-to-day realities, discuss tuition alternatives, and formulate next steps.",
        "preparation_notes": "Complete the CareerCompass assessment before joining and have your top 2 career interests ready for discussion.",
        "target_audience": "Students in Class 9–12 and Undergraduates exploring career direction",
        "icon": "🧭"
    },
    {
        "category": "Career Guidance",
        "title": "Higher Education & Stream Selection Strategy",
        "format": "Virtual Video Call",
        "duration_minutes": 40,
        "cost_label": "Free / Institutional Subsidy",
        "short_description": "Data-driven advice on selecting academic streams (PCM, PCB, Commerce, Arts) and entrance exam targets.",
        "full_description": "Detailed analysis of secondary school academic streams, polytechnic diploma options, and government university prerequisites.",
        "preparation_notes": "Bring your current school marks card and a list of subjects you enjoy or struggle with.",
        "target_audience": "Class 10 and 11 students preparing for stream transition",
        "icon": "🎓"
    },
    {
        "category": "Interview Preparation",
        "title": "Technical & Coding Mock Interview",
        "format": "Virtual Video Call",
        "duration_minutes": 60,
        "cost_label": "Free / Institutional Subsidy",
        "short_description": "Simulated live technical coding problem-solving, data structures, and engineering architecture review with instant diagnostic feedback.",
        "full_description": "Simulates a genuine tier-1 software or engineering interview. Involves live shared-screen coding, algorithmic complexity analysis, and actionable diagnostic feedback.",
        "preparation_notes": "Have a browser ready for live coding. Review basic data structures (arrays, hash maps, trees).",
        "target_audience": "Engineering, Computer Science, and Data undergraduates",
        "icon": "💻"
    },
    {
        "category": "Interview Preparation",
        "title": "Behavioral, HR & Communication Mock Interview",
        "format": "Virtual Video Call",
        "duration_minutes": 45,
        "cost_label": "Free / Institutional Subsidy",
        "short_description": "Practice the STAR framework, answering tricky HR questions, body language confidence, and clear communication.",
        "full_description": "Covers storytelling frameworks (Situation, Task, Action, Result), leadership questions, conflict handling, and workplace ethics scenarios.",
        "preparation_notes": "Prepare 3 stories from your academic, team, or personal projects highlighting problem solving.",
        "target_audience": "Final-year students, job seekers, and internship applicants",
        "icon": "🗣️"
    },
    {
        "category": "Interview Preparation",
        "title": "Resume, CV & Portfolio Review",
        "format": "Virtual Video Call",
        "duration_minutes": 30,
        "cost_label": "Free / Institutional Subsidy",
        "short_description": "Live screen-share critique of your resume, GitHub, design portfolio, or LinkedIn profile for maximum employer impact.",
        "full_description": "Detailed review of bullet points, ATS readability, verifiable outcome metrics, and portfolio presentation.",
        "preparation_notes": "Have your current resume in PDF or editable format and link to your online portfolio / GitHub.",
        "target_audience": "Students and fresh graduates actively applying for jobs",
        "icon": "📄"
    },
    {
        "category": "Employment & Internship Support",
        "title": "Internship & NATS/AICTE Portal Navigation",
        "format": "Virtual Video Call",
        "duration_minutes": 40,
        "cost_label": "Free / Institutional Subsidy",
        "short_description": "Step-by-step guidance on registering, filtering, and applying on official apprentice portals and vetted opportunities.",
        "full_description": "Walks you through NATS (Ministry of Education) enrolment, AICTE internship portal verification, eligibility criteria, and stipend rules.",
        "preparation_notes": "Have your college enrollment details and student ID card handy.",
        "target_audience": "Diploma, B.Tech, and undergraduate students seeking first practical work",
        "icon": "💼"
    },
    {
        "category": "Employment & Internship Support",
        "title": "Authorized Employer Connect & Opportunity Verification",
        "format": "Virtual Video Call",
        "duration_minutes": 30,
        "cost_label": "Free / Institutional Subsidy",
        "short_description": "Guidance on vetting legitimate job opportunities, spotting placement scams, and preparing application packages.",
        "full_description": "Teaches students how to verify corporate recruitment portals, avoid unpaid fraudulent schemes, and structure professional email inquiries.",
        "preparation_notes": "Bring links to any job postings or offers you wish to verify.",
        "target_audience": "Job seekers and entry-level applicants",
        "icon": "🛡️"
    },
    {
        "category": "Parent–Student Discussion",
        "title": "Parent–Student Facilitated Career Alignment Session",
        "format": "Virtual Video Call",
        "duration_minutes": 50,
        "cost_label": "Free / Institutional Subsidy",
        "short_description": "Facilitated conversation using the CareerCompass Bridge tool to align student passion with family expectations without conflict.",
        "full_description": "A neutral, empathetic setting where parents and students compare pathways, discuss budget constraints calmly, and build a consensual career roadmap.",
        "preparation_notes": "Both the student and at least one parent/guardian must attend. Complete the Parent–Student Bridge comparison beforehand.",
        "target_audience": "Students and their parents / guardians seeking consensus",
        "icon": "🤝"
    }
]

def generate_seed_appointment_slots():
    """Generates 40+ realistic upcoming slots over the next 14 days."""
    slots = []
    base_date = datetime.now().date()
    
    # Provider mapping to type specialties:
    # 1 (Dr. Ananya): types 1, 2
    # 2 (Rajesh Varma): type 3, 5
    # 3 (Priya Sundaram): types 6, 7, 5
    # 4 (Vikram Malhotra): type 8, 1
    # 5 (Meera Sen): types 1, 5
    # 6 (CC Peer Team): types 3, 4, 6
    
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

slots = generate_seed_appointment_slots()
print(f"Generated {len(slots)} appointment slots across {len(INITIAL_APPOINTMENT_PROVIDERS)} providers and {len(INITIAL_APPOINTMENT_TYPES)} types.")
