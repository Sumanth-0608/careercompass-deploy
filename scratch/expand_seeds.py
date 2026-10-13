"""
Helper to verify and validate the 12 expanded careers and appointments seed data.
"""
import json
from datetime import datetime, timedelta

EXPANDED_CAREERS = [
    {
        "slug": "pharmacist",
        "title": "Pharmacist & Clinical Medication Specialist",
        "category": "Healthcare & Life Sciences",
        "short_description": "Dispenses prescription medications, counsels patients on drug interactions and dosage, monitors therapeutic regimens, and oversees pharmaceutical compounding and quality control.",
        "typical_responsibilities": json.dumps([
            "Dispense prescribed pharmaceutical formulations with strict dosage and contraindication checks",
            "Counsel patients and caregivers on medication adherence, side-effects, and dietary interactions",
            "Monitor adverse drug reactions (ADR) and maintain pharmacovigilance records in hospital settings",
            "Manage medication inventory, cold-chain biological storage, and regulatory compounding protocols",
            "Collaborate with physicians and healthcare teams on evidence-based medication therapy management"
        ]),
        "relevant_interests": json.dumps(["science", "healthcare", "chemistry", "public service", "patient care"]),
        "relevant_strengths": json.dumps(["attention to detail", "empathy", "analytical thinking", "communication", "scientific method"]),
        "educational_requirements": "Statutory 4-year Bachelor of Pharmacy (B.Pharm) or 6-year Doctor of Pharmacy (Pharm.D) from an institution approved by the Pharmacy Council of India (PCI). Mandatory statutory registration as a Registered Pharmacist with the State Pharmacy Council is legally required to dispense medications.",
        "min_education_level": "Undergraduate",
        "suitable_streams": json.dumps(["Science - PCB", "Science - PCMB", "Diploma in Pharmacy (D.Pharm) with lateral entry"]),
        "important_skills": json.dumps([
            "Pharmacology & Pharmacokinetics",
            "Medicinal Chemistry & Drug Formulation",
            "Patient Counseling & Drug Interaction Monitoring",
            "Good Dispensing Practice (GDP)",
            "Pharmacovigilance & Drug Safety",
            "Inventory & Cold-Chain Management"
        ]),
        "suggested_beginner_projects": json.dumps([
            "Compare active pharmaceutical ingredients (APIs), mechanisms of action, and contraindications for common OTC analgesics",
            "Create a patient medication leaflet in clear language explaining drug interactions between hypertension medicines and common foods",
            "Audit storage temperature logs and inventory batch tracking protocols in a local community or college dispensary"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Master High School Chemistry & Biology", "explanation": "Build deep foundation in organic chemistry reactions, cell biology, and biochemistry.", "action": "Score high in 10+2 PCB subjects and review medicinal chemistry basics.", "duration": "School"},
            {"step": 2, "title": "Complete PCI-Approved B.Pharm Degree", "explanation": "Complete 4-year curriculum in pharmacology, pharmaceutics, pharmaceutical chemistry, and pharmacognosy.", "action": "Enrol in a Pharmacy Council of India (PCI) recognized college.", "duration": "4 years"},
            {"step": 3, "title": "Undergo Hospital & Industrial Pharmacy Internship", "explanation": "Gain practical clinical dispensing and manufacturing exposure during mandatory clinical rotation.", "action": "Complete practical training in a recognized multi-specialty hospital pharmacy.", "duration": "3–6 months"},
            {"step": 4, "title": "Obtain State Pharmacy Council Registration", "explanation": "Register with the State Pharmacy Council to receive official Pharmacist Registration Certificate and number.", "action": "Submit verification documents to State Pharmacy Council.", "duration": "Post-graduation"},
            {"step": 5, "title": "Specialization or Clinical Practice (Pharm.D / M.Pharm)", "explanation": "Pursue clinical pharmacy, pharmaceutical R&D, regulatory affairs, or community pharmacy practice.", "action": "Apply to healthcare systems or pharmaceutical research firms.", "duration": "Ongoing"}
        ]),
        "cost_category": "Moderate",
        "cost_estimate_detail": "Govt / State University B.Pharm: ₹30,000–₹1,20,000 total; PCI-Approved Private Colleges: ₹2,00,000–₹6,00,000.",
        "low_cost_routes": "Government pharmacy colleges, state central universities, state post-matric scholarships, and open NPTEL / Swayam pharmaceutical chemistry lectures.",
        "entrance_exams": json.dumps(["State Pharmacy CETs (MHT-CET, KCET, WBJEE)", "CUET (UG)", "GPAT (for Postgraduate M.Pharm)"]),
        "advantages": json.dumps([
            "High career stability with essential healthcare provider status across public and private sectors",
            "Diverse career branches across clinical hospitals, retail community practice, drug regulatory affairs, and pharma R&D",
            "Growing global demand driven by biopharmaceuticals, clinical trials, and expanding healthcare coverage"
        ]),
        "challenges": json.dumps([
            "Strict legal liability and zero-tolerance for dispensing errors requiring extreme precision",
            "Continuous learning required as new drug molecules, biological therapies, and safety warnings emerge",
            "Shift schedules and extended standing hours in busy hospital or community dispensaries"
        ]),
        "geographic_considerations": "Every hospital, clinic, community neighborhood, and major pharmaceutical manufacturing corridors (Hyderabad, Ahmedabad, Baddi, Goa).",
        "regulated": 1,
        "source_urls": json.dumps([
            {"title": "Pharmacy Council of India (PCI)", "url": "https://www.pci.nic.in"},
            {"title": "Central Drugs Standard Control Organisation (CDSCO)", "url": "https://cdsco.gov.in"},
            {"title": "National Career Service - Pharmacist", "url": "https://www.ncs.gov.in"}
        ]),
        "last_verified": "2026-10-10"
    },
    {
        "slug": "biotechnologist",
        "title": "Biotechnologist & Genomic Researcher",
        "category": "Healthcare & Life Sciences",
        "short_description": "Applies biological systems, cellular genetics, and molecular biology to develop therapeutic biologics, vaccines, diagnostic test kits, and sustainable bio-agricultural innovations.",
        "typical_responsibilities": json.dumps([
            "Culture mammalian cells, microbial strains, and recombinant expression vectors in bioreactors",
            "Conduct DNA/RNA extraction, PCR amplification, gel electrophoresis, and next-generation sequencing",
            "Analyze genomic, proteomic, and biochemical data using bioinformatics pipelines (BLAST, Biopython)",
            "Validate therapeutic candidates through enzyme assays, ELISA, and high-throughput screening",
            "Adhere to Good Laboratory Practice (GLP) and biosafety level (BSL) containment protocols"
        ]),
        "relevant_interests": json.dumps(["science", "biology", "genetics", "research", "healthcare"]),
        "relevant_strengths": json.dumps(["analytical thinking", "precision", "scientific method", "curiosity", "problem-solving"]),
        "educational_requirements": "B.Tech in Biotechnology or B.Sc. in Biotechnology / Biochemistry / Molecular Biology, followed by M.Tech / M.Sc. in Biotechnology, Bioinformatics, or Ph.D. for independent research.",
        "min_education_level": "Undergraduate",
        "suitable_streams": json.dumps(["Science - PCB", "Science - PCMB", "Biotechnology vocational"]),
        "important_skills": json.dumps([
            "Cell Culture & Bioreactor Operations",
            "Molecular Biology (PCR, Cloning, CRISPR basics)",
            "Bioinformatics (BLAST, NCBI, Biopython)",
            "Protein Purification & Chromatography (HPLC, FPLC)",
            "Good Laboratory Practice (GLP) & Bio-Safety (BSL-2)",
            "Assay Development (ELISA, Western Blot)"
        ]),
        "suggested_beginner_projects": json.dumps([
            "Analyze real SARS-CoV-2 or insulin gene variants using NCBI nucleotide databases and phylogenetic trees",
            "Conduct an enzyme reaction rate experiment using household catalase (yeast/potato) across varying pH and temperatures",
            "Write a student research synthesis on recombinant human insulin manufacturing and scale-up bioreactors"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Build Strong Foundation in Biology & Chemistry", "explanation": "Master molecular biology, genetics, organic chemistry, and cellular respiration.", "action": "Complete AP Biology / high school genetics curriculum.", "duration": "High school"},
            {"step": 2, "title": "Pursue B.Tech / B.Sc in Biotechnology", "explanation": "Study microbiology, immunology, genetic engineering, bioprocess engineering, and bioinformatics.", "action": "Actively participate in wet-lab college practicals.", "duration": "3–4 years"},
            {"step": 3, "title": "Master Computational Biology & Tools", "explanation": "Learn Python for bioinformatics, sequence alignment, and molecular modeling in PyMOL.", "action": "Complete Rosalind.info bioinformatics problem tracks.", "duration": "3–4 months"},
            {"step": 4, "title": "Gain Research Lab or Industry Internship", "explanation": "Intern in academic labs (CSIR, DBT, ICMR) or biopharma production facilities.", "action": "Apply for DBT Summer Training or CSIR-SRTP fellowship.", "duration": "2–6 months"},
            {"step": 5, "title": "Advance to Specialization or Graduate Studies", "explanation": "Pursue M.Sc / M.Tech in Molecular Medicine, Industrial Biotech, or Ph.D.", "action": "Take GATE / GAT-B entrance exams.", "duration": "Ongoing"}
        ]),
        "cost_category": "Moderate",
        "cost_estimate_detail": "Govt Universities (B.Sc / B.Tech): ₹25,000–₹1,50,000 total; Private Biotech Institutes: ₹3,00,000–₹8,00,000.",
        "low_cost_routes": "DBT-funded public central universities, NPTEL Biotechnology free lecture tracks, open bioinformatics databases (NCBI, PDB, UniProt).",
        "entrance_exams": json.dumps(["CUET (UG)", "JEE Main (for B.Tech Biotech)", "GATE / GAT-B (Postgraduate)"]),
        "advantages": json.dumps([
            "Frontier science directly developing cures for diseases, cancer therapies, and climate-resilient crops",
            "Rapid industry growth fueled by vaccine manufacturing, biotherapeutics, and precision medicine",
            "Strong international collaboration and global research fellowship opportunities"
        ]),
        "challenges": json.dumps([
            "Substantial scientific leadership roles typically require postgraduate (M.Sc/M.Tech) or doctoral degree",
            "Lengthy developmental cycles before laboratory discoveries achieve clinical approval",
            "Requires absolute rigor and sterility; a minor contamination can invalidate weeks of cell culture"
        ]),
        "geographic_considerations": "Major biotech corridors in Bengaluru, Hyderabad, Pune, NCR, Ahmedabad, and national research institutes (CSIR, DBT, ICMR).",
        "regulated": 0,
        "source_urls": json.dumps([
            {"title": "Department of Biotechnology (DBT India)", "url": "https://dbtindia.gov.in"},
            {"title": "Biotechnology Industry Research Assistance Council (BIRAC)", "url": "https://birac.nic.in"},
            {"title": "National Center for Biotechnology Information (NCBI)", "url": "https://www.ncbi.nlm.nih.gov"}
        ]),
        "last_verified": "2026-10-10"
    },
    {
        "slug": "astronomer-space-scientist",
        "title": "Astronomer & Space Scientist",
        "category": "Sciences & Environment",
        "short_description": "Investigates celestial objects, stellar physics, planetary geology, observational astrophysics, and cosmological phenomena using ground-based radio/optical observatories and space satellites.",
        "typical_responsibilities": json.dumps([
            "Analyze observational telemetry and photometric data from optical, radio, and space-based telescopes",
            "Develop computational models of stellar evolution, galactic dynamics, and high-energy radiation",
            "Write reduction pipelines in Python (Astropy, SciPy) to clean atmospheric noise and instrument bias",
            "Publish peer-reviewed observational papers and draft observing proposals for major telescope time",
            "Collaborate with international research consortia on deep-space exploration and space satellite payloads"
        ]),
        "relevant_interests": json.dumps(["science", "astronomy", "physics", "mathematics", "space"]),
        "relevant_strengths": json.dumps(["analytical thinking", "mathematical modeling", "curiosity", "programming", "patience"]),
        "educational_requirements": "B.Sc. in Physics or B.Tech in Engineering Physics / Aerospace, followed by M.Sc. in Astronomy / Astrophysics and Ph.D. in Astrophysics for research observatory and university faculty positions.",
        "min_education_level": "Undergraduate",
        "suitable_streams": json.dumps(["Science - PCM"]),
        "important_skills": json.dumps([
            "Astrophysics & Classical/Quantum Mechanics",
            "Data Reduction & Pipeline Scripting (Python, Astropy)",
            "Electromagnetic Radiation & Astronomical Spectroscopy",
            "Numerical Simulation & Differential Equations",
            "Telescope Instrumentation & Optics",
            "Scientific Writing & LaTeX"
        ]),
        "suggested_beginner_projects": json.dumps([
            "Analyze public Kepler / TESS space telescope light curves in Python to detect exoplanet orbital transits",
            "Simulate gravitational multi-body planetary orbits using Runge-Kutta numerical integration in Python",
            "Analyze variable star pulsation periods using free citizen-science photometric data from AAVSO"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Build Mastery in Advanced Calculus & Physics", "explanation": "Master Newtonian mechanics, optics, thermodynamics, and differential equations.", "action": "Score high in high school physics and math.", "duration": "High school"},
            {"step": 2, "title": "Pursue B.Sc in Physics or B.Tech Engineering Physics", "explanation": "Study quantum physics, electromagnetic theory, statistical mechanics, and scientific programming.", "action": "Enroll at a reputable university physics department.", "duration": "3–4 years"},
            {"step": 3, "title": "Learn Observational Data Reduction in Python", "explanation": "Master Astropy, FITS image handling, aperture photometry, and spectroscopy data reduction.", "action": "Complete online tutorials using real Hubble or James Webb telescope public archive data.", "duration": "3–6 months"},
            {"step": 4, "title": "Pursue M.Sc and Doctoral Research (Ph.D)", "explanation": "Join premier astrophysics institutes (IIA, IUCAA, TIFR, ISRO URSC) with research fellowship stipend.", "action": "Clear JEST or CSIR-UGC NET JRF.", "duration": "4–5 years"},
            {"step": 5, "title": "Postdoctoral Research Fellowships & Observatory Science", "explanation": "Conduct specialized research on black holes, cosmic microwave background, or exoplanets.", "action": "Publish high-impact papers and secure observatory grants.", "duration": "Ongoing"}
        ]),
        "cost_category": "Low / Free Accessible",
        "cost_estimate_detail": "Govt Central Universities: ₹15,000–₹60,000 total tuition; Ph.D. programs are fully funded with CSIR-JRF / INSPIRE fellowships (₹37,000+/month stipend + HRA).",
        "low_cost_routes": "Public central universities, open astronomical datasets from NASA/ESA/ISRO archives, Astropy open tutorials, IIA and IUCAA public summer schools.",
        "entrance_exams": json.dumps(["CUET (UG)", "IIT JAM (Physics)", "JEST (Joint Entrance Screening Test)", "CSIR NET Physical Sciences"]),
        "advantages": json.dumps([
            "Direct pursuit of fundamental questions about the birth, evolution, and future of the universe",
            "Fully funded Ph.D. and postdoctoral fellowships with international telescope collaborations",
            "Highly transferable computational physics, big-data modeling, and image processing skill set"
        ]),
        "challenges": json.dumps([
            "Long educational commitment typically requiring 7–10 years to reach independent tenure",
            "Extremely competitive permanent academic and observatory research positions worldwide",
            "Demands continuous mathematical endurance and complex statistical error analysis"
        ]),
        "geographic_considerations": "National observatories (Hanle, Kavalur, Nainital, Pune GMRT, Udaipur Solar Observatory) and premier research centers (IUCAA, IIA, TIFR, ISRO).",
        "regulated": 0,
        "source_urls": json.dumps([
            {"title": "Inter-University Centre for Astronomy and Astrophysics (IUCAA)", "url": "https://www.iucaa.in"},
            {"title": "Indian Institute of Astrophysics (IIA Bengaluru)", "url": "https://www.iiap.res.in"},
            {"title": "ISRO Space Science Data Centre (ISSDC)", "url": "https://www.issdc.gov.in"}
        ]),
        "last_verified": "2026-10-10"
    },
    {
        "slug": "astronaut",
        "title": "Astronaut & Spaceflight Mission Specialist",
        "category": "Technology & Engineering",
        "short_description": "Undergoes rigorous technical, physical, and physiological training to command or operate spacecraft missions, execute orbital microgravity experiments, and conduct space exploration operations.",
        "typical_responsibilities": json.dumps([
            "Pilot or operate crewed spacecraft systems, guidance navigation controls, and docking hardware",
            "Execute scheduled scientific experiments in microgravity biology, materials physics, and astronomy",
            "Conduct Extravehicular Activities (EVAs / spacewalks) for spacecraft inspection, repair, and assembly",
            "Maintain extreme physical conditioning, vestibular adaptation, and emergency survival readiness",
            "Communicate mission milestones, telemetry reports, and educational broadcasts with ground control"
        ]),
        "relevant_interests": json.dumps(["space", "aviation", "engineering", "science", "adventure", "technology"]),
        "relevant_strengths": json.dumps(["physical fitness", "crisis composure", "leadership", "technical mastery", "team resilience"]),
        "educational_requirements": "Extremely selective and physically demanding. Requires advanced Master's or Ph.D. in STEM (Engineering, Computer Science, Physics, Medicine) or Bachelor's in Engineering with at least 1,000 hours of high-performance military jet flight experience. Candidates must pass rigorous physiological screening (G-force tolerance, cardiovascular endurance, visual acuity) and selection by national space agencies (ISRO Gaganyaan Astronaut Selection / NASA Astronaut Candidate).",
        "min_education_level": "Undergraduate",
        "suitable_streams": json.dumps(["Science - PCM", "Aeronautical / Mechanical / Computer Engineering", "Military Aviation Cadet"]),
        "important_skills": json.dumps([
            "Spacecraft Flight Mechanics & Telemetry Systems",
            "Extreme Physiological Stress Tolerance (G-load, Hypoxia)",
            "Neutral Buoyancy & EVA Spacewalk Simulation",
            "Crisis Communication & Tactical Decision-Making",
            "Microgravity Experimental Protocols",
            "Wilderness & Oceanic Survival Operations"
        ]),
        "suggested_beginner_projects": json.dumps([
            "Simulate orbital rendezvous and docking maneuvers using open-source Orbiter Space Simulator or Kerbal Space Program",
            "Participate in the NASA Space Apps Challenge or national student sounding rocket competition",
            "Complete certified open-water scuba diving certification to understand neutral buoyancy movement principles"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Excel in STEM Academics and Peak Physical Fitness", "explanation": "Maintain top marks in math and physics while achieving peak cardiovascular conditioning and swimming agility.", "action": "Commit to daily physical training, competitive athletics, and STEM Olympiads.", "duration": "High school"},
            {"step": 2, "title": "Earn Degree in Engineering, Physics, or Aviation", "explanation": "Pursue aerospace, mechanical, or computer engineering at premier institutions or National Defence Academy (NDA).", "action": "Graduate at the top of your class with leadership credentials.", "duration": "4 years"},
            {"step": 3, "title": "Gain Advanced Operational or Research Experience", "explanation": "Accumulate jet test pilot flight hours or earn a doctoral degree with groundbreaking aerospace/physics research.", "action": "Serve as experimental test pilot or lead aerospace systems engineer at ISRO/DRDO.", "duration": "5–8 years"},
            {"step": 4, "title": "Apply for National Astronaut Candidate Selection", "explanation": "Pass grueling psychological, physiological, centrifuge, and multi-axis trainer selection tests.", "action": "Complete national astronaut candidate application and medical clearance.", "duration": "1–2 years"},
            {"step": 5, "title": "Intensive Mission-Specific Astronaut Training", "explanation": "Train in centrifuge simulators, zero-G parabolic flights, Russian/NASA partner training centers, and survival skills.", "action": "Certify on mission command and EVA spacewalk protocols.", "duration": "2–3 years"}
        ]),
        "cost_category": "Low / Free Accessible",
        "cost_estimate_detail": "Military flight pathway: 100% government-funded via National Defence Academy (NDA) / Air Force Academy; STEM scientist pathway: Public university B.Tech/M.Tech + research appointments.",
        "low_cost_routes": "Indian Air Force flight cadet entry, public IITs/NITs aerospace programs, ISRO student internships, open space education resources via ISRO IIRS / NASA Open Science.",
        "entrance_exams": json.dumps(["NDA / CDS (Aviation Cadet)", "JEE Advanced (Aerospace / Engineering Physics)", "GATE (ISRO Scientist Entry)"]),
        "advantages": json.dumps([
            "Pinnacle human exploration achievement contributing directly to national and global space history",
            "World-class physical, cognitive, and flight training alongside premier scientific minds",
            "Inspires millions of students worldwide to pursue science, engineering, and exploration"
        ]),
        "challenges": json.dumps([
            "Extremely demanding selection criteria: fewer than a few dozen individuals worldwide selected per decade",
            "Severe physical strain including high G-forces, radiation exposure, muscle atrophy, and mission risks",
            "Prolonged confinement, intense training schedules, and unpredictable mission launch delays"
        ]),
        "geographic_considerations": "ISRO Astronaut Training Facility (Bengaluru), Human Space Flight Centre (HSFC), Gaganyaan launch sites (Sriharikota), IAF Institute of Aerospace Medicine, and partner space facilities.",
        "regulated": 1,
        "source_urls": json.dumps([
            {"title": "ISRO Human Space Flight Centre (HSFC / Gaganyaan)", "url": "https://www.isro.gov.in"},
            {"title": "Institute of Aerospace Medicine (IAM IAF)", "url": "https://indianairforce.nic.in"},
            {"title": "NASA Astronaut Selection Standards", "url": "https://www.nasa.gov/astronauts"}
        ]),
        "last_verified": "2026-10-10"
    },
    {
        "slug": "robotics-engineer",
        "title": "Robotics & Mechatronics Engineer",
        "category": "Technology & Engineering",
        "short_description": "Designs, programs, and integrates autonomous robots, multi-axis robotic arms, mobile AGVs, sensors, microcontrollers, and computer vision systems for manufacturing, surgery, and exploration.",
        "typical_responsibilities": json.dumps([
            "Develop robot kinematics, trajectory planning, and motor motion control algorithms",
            "Program embedded microcontrollers and Single Board Computers (ROS 2, C++, Python, Arduino, STM32)",
            "Integrate computer vision, LiDAR sensors, and IMUs for autonomous localization and mapping (SLAM)",
            "Design 3D mechanical linkages, gearboxes, and end-effectors in CAD with rapid 3D printing",
            "Conduct safety integration tests according to ISO 10218 industrial robot safety standards"
        ]),
        "relevant_interests": json.dumps(["robotics", "technology", "engineering", "machinery", "programming"]),
        "relevant_strengths": json.dumps(["practical problem-solving", "analytical thinking", "spatial reasoning", "creativity", "systems integration"]),
        "educational_requirements": "B.Tech in Mechatronics, Mechanical Engineering, Electrical & Electronics, or Computer Science with demonstrable hands-on robotics projects and ROS proficiency.",
        "min_education_level": "Class 11–12",
        "suitable_streams": json.dumps(["Science - PCM", "Diploma in Mechatronics / Mechanical", "Computer Science"]),
        "important_skills": json.dumps([
            "Robot Operating System (ROS 2 / Gazebo)",
            "Forward & Inverse Kinematics",
            "C++ and Python for Embedded Systems",
            "Computer Vision & SLAM (OpenCV)",
            "Motor Drivers, Actuators & Sensors",
            "CAD Modeling & 3D Prototyping (Fusion 360 / SolidWorks)"
        ]),
        "suggested_beginner_projects": json.dumps([
            "Build an autonomous 2-wheeled obstacle-avoiding mobile robot using Arduino, ultrasonic sensors, and motor shields",
            "Simulate a 3-DOF robotic arm in ROS 2 and Gazebo, calculating inverse kinematics in Python",
            "Build a smart color-sorting conveyor belt using an open-source USB webcam and OpenCV shape recognition"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Learn Mechanics & Circuit Fundamentals", "explanation": "Understand DC motors, servos, Ohm's law, torque calculations, and microcontroller basics.", "action": "Build 5 basic breadboard circuits with Arduino.", "duration": "4 weeks"},
            {"step": 2, "title": "Master C++ and Python Programming", "explanation": "Learn object-oriented programming, data structures, and serial communication protocols.", "action": "Solve embedded coding challenges and read sensor data over UART/I2C.", "duration": "6 weeks"},
            {"step": 3, "title": "Learn ROS 2 & Robot Simulation", "explanation": "Study publisher-subscriber nodes, URDF robot modeling, and simulation in Gazebo.", "action": "Simulate an autonomous wheeled mobile robot navigating a virtual maze.", "duration": "6–8 weeks"},
            {"step": 4, "title": "Build a Physical Multi-Sensor Robot", "explanation": "Design 3D printed chassis, integrate motor encoders, LiDAR or camera, and implement SLAM mapping.", "action": "Document robot hardware and open-source GitHub code.", "duration": "8 weeks"},
            {"step": 5, "title": "Internship in Industrial Automation or Agritech", "explanation": "Work with industrial robotic arms, automated guided vehicles (AGVs), or medical robotics teams.", "action": "Apply to robotics startups or manufacturing automation firms.", "duration": "Ongoing"}
        ]),
        "cost_category": "Moderate",
        "cost_estimate_detail": "Govt Engineering Colleges: ₹60,000–₹2,50,000 total; Starter robot kit / electronics for learning: ₹3,000–₹12,000.",
        "low_cost_routes": "Open-source ROS 2 and Gazebo simulators requiring zero physical hardware, NPTEL robotics courses, community tinker labs / Atal Tinkering Labs.",
        "entrance_exams": json.dumps(["JEE Main", "JEE Advanced", "State Engineering CETs", "GATE (Mechanical / Electronics)"]),
        "advantages": json.dumps([
            "At the convergence of AI, mechanical hardware, and embedded electronics with explosive future demand",
            "Hands-on creative thrill of seeing physical machines think, move, and solve real tasks in the physical world",
            "High versatility across warehouse automation, defense drones, agricultural robots, and surgical robotics"
        ]),
        "challenges": json.dumps([
            "Must debug both hardware issues (loose wiring, sensor noise, gear backlash) and software code bugs simultaneously",
            "Advanced industrial components, sensors, and servos can be costly for home projects",
            "Requires multidisciplinary competence across physics, mathematics, electronics, and coding"
        ]),
        "geographic_considerations": "Major manufacturing corridors (Pune, Chennai, NCR, Bengaluru, Ahmedabad), robotics research labs, and automated fulfillment hubs.",
        "regulated": 0,
        "source_urls": json.dumps([
            {"title": "Open Source Robotics Foundation (ROS 2)", "url": "https://www.ros.org"},
            {"title": "IEEE Robotics and Automation Society", "url": "https://www.ieee-ras.org"},
            {"title": "NPTEL Robotics Certification", "url": "https://nptel.ac.in"}
        ]),
        "last_verified": "2026-10-10"
    },
    {
        "slug": "electrical-engineer",
        "title": "Electrical & Power Systems Engineer",
        "category": "Technology & Engineering",
        "short_description": "Designs, simulates, and manages electrical power grids, renewable energy generation (solar/wind), electric vehicle powertrains, switchgear, and high-voltage transmission networks.",
        "typical_responsibilities": json.dumps([
            "Design electrical schematics, single-line diagrams (SLDs), and switchgear specifications",
            "Model power grid load flows, short-circuit faults, and voltage stability in MATLAB/ETAP",
            "Supervise installation and commissioning of transformers, protection relays, and solar inverters",
            "Ensure adherence to Central Electricity Authority (CEA) regulations and IEEE/IS safety standards",
            "Perform energy audits, power factor correction, and harmonic distortion mitigations in industrial plants"
        ]),
        "relevant_interests": json.dumps(["engineering", "electricity", "machinery", "renewable energy", "problem-solving"]),
        "relevant_strengths": json.dumps(["analytical thinking", "mathematical calculation", "safety orientation", "practical troubleshooting"]),
        "educational_requirements": "B.Tech / B.E. in Electrical Engineering (EE) or Electrical & Electronics Engineering (EEE), or 3-year State Polytechnic Diploma in Electrical Engineering with lateral entry to B.Tech.",
        "min_education_level": "Class 11–12",
        "suitable_streams": json.dumps(["Science - PCM", "Diploma in Electrical Engineering", "Vocational Electrical Maintenance"]),
        "important_skills": json.dumps([
            "Power System Simulation (MATLAB / Simulink / ETAP)",
            "Single Line Diagrams & Electrical CAD (AutoCAD Electrical)",
            "Switchgear & Protective Relay Coordination",
            "Solar PV & Wind Renewable Integration",
            "PLC & SCADA Industrial Automation",
            "Electrical Safety Standards (CEA / IS 732 / NFPA 70E)"
        ]),
        "suggested_beginner_projects": json.dumps([
            "Design and calculate sizing for an off-grid 1kW rooftop solar photovoltaic system with battery backup",
            "Simulate a 3-phase induction motor speed controller and power factor improvement circuit in MATLAB/Simulink",
            "Build an IoT smart energy meter using an ESP32 and non-invasive current transformer (CT) sensor to log household power usage"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Master Circuit Theory & Electromagnetism", "explanation": "Master Kirchhoff's laws, AC circuits, phasors, magnetic circuits, and Maxwell's equations.", "action": "Solve 50 complex AC network analysis problems.", "duration": "High school / Sem 1"},
            {"step": 2, "title": "Study Electrical Machines & Power Systems", "explanation": "Learn transformers, induction motors, synchronous generators, and transmission line models.", "action": "Complete laboratory experiments on transformer load tests and DC motors.", "duration": "1 year"},
            {"step": 3, "title": "Learn Power Simulation Software (ETAP / Simulink)", "explanation": "Model load flow, symmetrical faults, and renewable grid integration.", "action": "Simulate a 5-bus industrial power distribution network in ETAP.", "duration": "2–3 months"},
            {"step": 4, "title": "Substation Visits & Practical Site Exposure", "explanation": "Visit 33kV/132kV substations, study switchgear, circuit breakers, and relay protection panels.", "action": "Apply for summer training at state electricity transmission boards (DISCOMs/TRANSCOs).", "duration": "4–6 weeks"},
            {"step": 5, "title": "Target Graduate Engineering Trainee Roles or PSUs", "explanation": "Join power utilities (PGCIL, NTPC), renewable developers, EV manufacturers, or consulting firms.", "action": "Prepare for GATE (EE) or state PSU technical selection.", "duration": "Ongoing"}
        ]),
        "cost_category": "Moderate",
        "cost_estimate_detail": "Govt Engineering Colleges: ₹40,000–₹2,00,000 total; State Polytechnic: ₹15,000–₹50,000 total.",
        "low_cost_routes": "Government polytechnic colleges, central state universities, NPTEL Electrical Engineering courses, open circuit simulation software (Qucs / LTspice).",
        "entrance_exams": json.dumps(["JEE Main", "State Engineering CETs", "GATE (for PSU recruitment: PGCIL, NTPC, BHEL)"]),
        "advantages": json.dumps([
            "Perennial foundational engineering discipline essential to all modern civilization and clean energy transition",
            "Substantial recruitment across prestigious public sector undertakings (PSUs: Power Grid, NTPC, BHEL, Metro Rail)",
            "Rapidly expanding opportunities in electric vehicles (EV), battery storage, and solar/wind megaprojects"
        ]),
        "challenges": json.dumps([
            "Strict safety requirements: working around high voltage lines involves inherent electrical flash hazards",
            "Heavy theoretical mathematics in differential equations, Laplace transforms, and complex power flow vectors",
            "Site engineer roles frequently require field travel to remote substations and industrial facilities in harsh weather"
        ]),
        "geographic_considerations": "Every electricity distribution board (DISCOM), thermal/hydro/solar plants, industrial manufacturing corridors, and metro railway systems.",
        "regulated": 0,
        "source_urls": json.dumps([
            {"title": "Central Electricity Authority (CEA)", "url": "https://cea.nic.in"},
            {"title": "Power Grid Corporation of India (POWERGRID)", "url": "https://www.powergrid.in"},
            {"title": "IEEE Power & Energy Society", "url": "https://www.ieee-pes.org"}
        ]),
        "last_verified": "2026-10-10"
    },
    {
        "slug": "aerospace-engineer",
        "title": "Aerospace & Aeronautical Engineer",
        "category": "Technology & Engineering",
        "short_description": "Researches, designs, and manufactures fixed-wing aircraft, drones, helicopters, launch vehicles, and spacecraft propulsion systems with emphasis on aerodynamics and structures.",
        "typical_responsibilities": json.dumps([
            "Calculate aircraft aerodynamic lift, drag, and stability characteristics using Computational Fluid Dynamics (CFD)",
            "Design lightweight airframe composite structures, wing spars, and landing gear in 3D CAD",
            "Perform structural finite element analysis (FEA) under extreme flight load and flutter conditions",
            "Design and test propulsion systems including gas turbines, ramjets, and solid/liquid rocket engines",
            "Coordinate with flight test crews and airworthiness certification authorities (DGCA / FAA)"
        ]),
        "relevant_interests": json.dumps(["aviation", "space", "aerodynamics", "engineering", "physics"]),
        "relevant_strengths": json.dumps(["analytical thinking", "advanced mathematics", "simulation", "attention to precision"]),
        "educational_requirements": "B.Tech / B.E. in Aerospace Engineering, Aeronautical Engineering, or Mechanical Engineering with aerospace specialization.",
        "min_education_level": "Class 11–12",
        "suitable_streams": json.dumps(["Science - PCM"]),
        "important_skills": json.dumps([
            "Computational Fluid Dynamics (CFD / OpenFOAM / ANSYS Fluent)",
            "Aerodynamics & High-Speed Flight Mechanics",
            "Propulsion Systems (Gas Turbines / Rocket Engines)",
            "Finite Element Analysis (FEA / Nastran / Abaqus)",
            "Avionics & Flight Control Systems",
            "Airworthiness Standards & Certification (FAR / CS-25)"
        ]),
        "suggested_beginner_projects": json.dumps([
            "Simulate aerodynamic lift and drag curves for an NACA 4412 airfoil in OpenFOAM or XFLR5",
            "Design, construct, and test-fly a custom RC fixed-wing glider or quadcopter drone",
            "Calculate payload capability and delta-V budget for a two-stage suborbital sounding rocket in Python"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Build Mastery in Advanced Mathematics & Physics", "explanation": "Master vector calculus, differential equations, thermodynamics, and fluid mechanics.", "action": "Score high in high school physics and math.", "duration": "High school"},
            {"step": 2, "title": "Pursue B.Tech in Aerospace or Mechanical Engineering", "explanation": "Study compressible aerodynamics, aircraft structures, flight mechanics, and propulsion.", "action": "Enroll in an accredited aerospace engineering program.", "duration": "4 years"},
            {"step": 3, "title": "Master Computational Aerodynamics Tools", "explanation": "Learn CFD modeling in open-source OpenFOAM or XFLR5, and CAD modeling in SolidWorks.", "action": "Complete aerodynamic wing simulation case study.", "duration": "4–6 months"},
            {"step": 4, "title": "Participate in UAV / Rocketry Student Competitions", "explanation": "Join SAE Aero Design, AIAA Design/Build/Fly, or CanSat satellite student teams.", "action": "Build and fly a team drone or sounding rocket.", "duration": "College year"},
            {"step": 5, "title": "Join Aerospace R&D, Defense, or Space Organizations", "explanation": "Work with aerospace defense companies, drone startups, or space agencies (HAL, ISRO, DRDO, Boeing, Airbus).", "action": "Apply to graduate engineering programs or take GATE (AE).", "duration": "Ongoing"}
        ]),
        "cost_category": "Moderate",
        "cost_estimate_detail": "IITs / NITs: ₹1,50,000–₹8,00,000 total; Private Aerospace Institutes: ₹4,00,000–₹12,00,000.",
        "low_cost_routes": "Government IITs/NITs with merit/means fee concessions, open CFD tools (OpenFOAM, NASA OpenVSP), open flight mechanics lectures on NPTEL.",
        "entrance_exams": json.dumps(["JEE Advanced", "JEE Main", "GATE Aerospace (AE)"]),
        "advantages": json.dumps([
            "Frontier engineering pushing physical limits of speed, altitude, and deep space exploration",
            "Surging domestic defense aerospace and commercial drone manufacturing under Make in India initiatives",
            "Deeply respected, intellectually elite technical discipline with global career mobility"
        ]),
        "challenges": json.dumps([
            "Strict aviation and defense regulatory oversight resulting in long certification cycles before flight",
            "High capital intensity limits the number of primary aircraft manufacturers",
            "Requires relentless mathematical discipline in compressible flows, supersonic shocks, and nonlinear elasticity"
        ]),
        "geographic_considerations": "Aviation hubs in Bengaluru (HAL, ISRO, NAL, Boeing/Airbus R&D), Hyderabad, Kanpur, and defense manufacturing nodes.",
        "regulated": 0,
        "source_urls": json.dumps([
            {"title": "Directorate General of Civil Aviation (DGCA India)", "url": "https://www.dgca.gov.in"},
            {"title": "Hindustan Aeronautics Limited (HAL)", "url": "https://hal-india.co.in"},
            {"title": "Aeronautical Society of India (AeSI)", "url": "https://aesi.org.in"}
        ]),
        "last_verified": "2026-10-10"
    },
    {
        "slug": "video-editor-media-producer",
        "title": "Video Editor & Digital Media Producer",
        "category": "Creative & Design",
        "short_description": "Assembles raw recorded footage, dialogue, sound effects, motion graphics, and color grading into polished visual stories for documentaries, streaming series, commercials, and digital education.",
        "typical_responsibilities": json.dumps([
            "Ingest, organize, and log multi-camera video footage, audio tracks, and production metadata",
            "Assemble assembly cuts, rough cuts, and fine cuts balancing narrative pacing and emotional arc",
            "Perform primary and secondary color correction and cinematic color grading (DaVinci Resolve)",
            "Design motion graphic title cards, lower thirds, and animated overlays (After Effects)",
            "Mix and master multi-track audio dialogue, ambient soundscapes, and musical scores"
        ]),
        "relevant_interests": json.dumps(["creativity", "video editing", "storytelling", "film", "visual arts", "technology"]),
        "relevant_strengths": json.dumps(["visual storytelling", "attention to detail", "rhythm and pacing", "creativity", "patience"]),
        "educational_requirements": "Degree or diploma in Film Editing, Mass Communication, or Visual Arts, or proven demonstrable editing showreel (many successful editors are self-taught or enter via apprenticeship).",
        "min_education_level": "Class 10",
        "suitable_streams": json.dumps(["Any stream with visual portfolio", "Humanities / Arts", "Commerce", "Vocational Media"]),
        "important_skills": json.dumps([
            "Non-Linear Editing (DaVinci Resolve / Premiere Pro / Final Cut)",
            "Color Correction & Grading (Color Wheels, Waveforms, LUTs)",
            "Audio Post-Production (Dialogue EQ, Noise Reduction, Audio Ducking)",
            "Motion Graphics & Keyframing (After Effects)",
            "Video Codecs, Bitrates & Export Compression",
            "Narrative Pacing & Visual Rhythm"
        ]),
        "suggested_beginner_projects": json.dumps([
            "Edit a 90-second dynamic documentary trailer from open-source stock footage with sound design and title cards",
            "Complete a cinematic color grading breakdown in free DaVinci Resolve using raw camera test clips",
            "Produce a 3-minute educational video explaining a complex science topic with synced motion graphics"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Learn Video Foundations & Grammar of the Edit", "explanation": "Understand shot types (wide, medium, close-up), match cuts, J-cuts, L-cuts, and the 180-degree rule.", "action": "Watch classic film editing breakdowns and analyze pacing.", "duration": "3 weeks"},
            {"step": 2, "title": "Master Professional NLE Software", "explanation": "Learn DaVinci Resolve (free) or Premiere Pro: keyboard shortcuts, timeline trimming, and multi-cam sync.", "action": "Complete Blackmagic Design's free certified DaVinci Resolve beginner training.", "duration": "4–6 weeks"},
            {"step": 3, "title": "Learn Sound Design and Audio Mixing", "explanation": "Master dialogue noise cleanup, room tone, Foley sound effects, and music synchronization.", "action": "Edit the sound design for a 60-second silent film scene.", "duration": "3 weeks"},
            {"step": 4, "title": "Study Color Grading and Motion Graphics", "explanation": "Understand color temperature, lift/gamma/gain curves, shot matching, and keyframing title animations.", "action": "Grade a 5-shot sequence for day-for-night and sunset moods.", "duration": "4 weeks"},
            {"step": 5, "title": "Build a Public Showreel and Freelance / Studio Work", "explanation": "Assemble a 60-second fast-paced showreel showcasing diversity in documentary, commercial, and narrative cuts.", "action": "Publish showreel and pitch to YouTube channels, advertising agencies, or production houses.", "duration": "Ongoing"}
        ]),
        "cost_category": "Low / Free Accessible",
        "cost_estimate_detail": "Free DaVinci Resolve software; Decent editing computer: ₹40,000–₹90,000; Film institute degrees: ₹1,00,000–₹6,00,000.",
        "low_cost_routes": "Free full version of DaVinci Resolve, YouTube tutorials, public domain archive footage (Internet Archive), freelance student projects.",
        "entrance_exams": json.dumps(["FTII / SRFTI JET (Film Editing)", "CUET (UG) Mass Communication", "Institutional Portfolio Review"]),
        "advantages": json.dumps([
            "Extremely high demand across streaming platforms (Netflix, Hotstar), YouTube creators, advertising, and corporate media",
            "Strong global freelance earning potential and location-independent remote work",
            "Deep creative fulfillment transforming raw fragmented footage into compelling emotional stories"
        ]),
        "challenges": json.dumps([
            "Tight turnaround deadlines and repetitive client revision cycles",
            "Extended sitting hours in dark edit suites causing eye fatigue and ergonomic strain",
            "Heavy computer rendering demands and large external hard drive storage overheads"
        ]),
        "geographic_considerations": "Major media hubs (Mumbai, Hyderabad, Chennai, NCR, Bengaluru) and completely distributed global remote contracts.",
        "regulated": 0,
        "source_urls": json.dumps([
            {"title": "Blackmagic Design DaVinci Resolve Free Training", "url": "https://www.blackmagicdesign.com/products/davinciresolve/training"},
            {"title": "Film and Television Institute of India (FTII)", "url": "https://www.ftiindia.com"},
            {"title": "National Career Service - Video Editing", "url": "https://www.ncs.gov.in"}
        ]),
        "last_verified": "2026-10-10"
    },
    {
        "slug": "music-producer-audio",
        "title": "Music Producer & Audio Engineer",
        "category": "Creative & Design",
        "short_description": "Composes, arranges, records, mixes, and masters music tracks, cinematic scores, podcast audio, and game soundscapes using modern Digital Audio Workstations (DAWs) and studio outboard equipment.",
        "typical_responsibilities": json.dumps([
            "Compose melodies, harmonic chord progressions, basslines, and rhythmic drum patterns in DAWs",
            "Record live acoustic instruments, vocals, and synthesizers with optimal microphone placement",
            "Perform audio mixing: surgical EQ, dynamic compression, spatial reverb, and stereo imaging",
            "Master finished tracks to international loudness streaming standards (LUFS / true peak limits)",
            "Collaborate with songwriters, film directors, and game developers on sonic branding and soundtracks"
        ]),
        "relevant_interests": json.dumps(["music", "singing", "audio engineering", "creativity", "technology", "sound design"]),
        "relevant_strengths": json.dumps(["musical ear", "creativity", "attention to audio detail", "rhythm", "technical patience"]),
        "educational_requirements": "Diploma or degree in Audio Engineering, Music Production, or Sound Design, or extensive practical studio apprenticeship and demonstrable audio portfolio.",
        "min_education_level": "Class 10",
        "suitable_streams": json.dumps(["Any stream with musical aptitude", "Humanities / Arts", "Vocational Sound Engineering"]),
        "important_skills": json.dumps([
            "Digital Audio Workstation (Ableton Live / Logic Pro / FL Studio / Pro Tools)",
            "Audio Mixing (Subtractive EQ, Multiband Compression, Saturation)",
            "Audio Mastering & Loudness Standards (LUFS / True Peak)",
            "MIDI Programming & Synthesizer Sound Design",
            "Studio Acoustics, Microphone Polar Patterns & Gain Staging",
            "Music Theory Fundamentals (Chords, Scales, Arrangements)"
        ]),
        "suggested_beginner_projects": json.dumps([
            "Produce a complete 2-minute original musical beat or soundtrack using free DAW (Reaper / BandLab / GarageBand)",
            "Record a live acoustic instrument or vocal track and clean background noise using spectral editing",
            "Create a custom sound design pack (50 sound effects) for a short indie video game trailer"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Understand Music Theory and Acoustic Physics", "explanation": "Learn scales, chord progressions, tempo, audio frequencies (20Hz–20kHz), and decibels.", "action": "Complete free interactive music theory tutorials (e.g. Ableton Learning Music).", "duration": "4 weeks"},
            {"step": 2, "title": "Master a Digital Audio Workstation (DAW)", "explanation": "Learn audio recording, MIDI sequencing, virtual instruments, and audio slicing.", "action": "Recreate the arrangement of a favorite song in your DAW.", "duration": "6 weeks"},
            {"step": 3, "title": "Master Audio Mixing Fundamentals", "explanation": "Learn high-pass filtering, dynamic range compression, sidechaining, and stereo panning.", "action": "Mix a multi-track stem session downloaded from free Cambridge Music Technology library.", "duration": "8 weeks"},
            {"step": 4, "title": "Study Audio Mastering & Delivery Standards", "explanation": "Learn bus limiting, multiband saturation, and streaming normalization standards (Spotify, Apple Music).", "action": "Master 3 tracks to -14 LUFS with dynamic preservation.", "duration": "4 weeks"},
            {"step": 5, "title": "Publish Music & Pitch for Sync Licensing / Games", "explanation": "Distribute original tracks, pitch for indie games, web series, or offer audio mixing services.", "action": "Upload portfolio to SoundCloud/Spotify and freelance platforms.", "duration": "Ongoing"}
        ]),
        "cost_category": "Low / Free Accessible",
        "cost_estimate_detail": "Affordable home setup (Budget studio headphones, USB audio interface, condenser mic, DAW): ₹25,000–₹60,000; Sound engineering colleges: ₹80,000–₹4,50,000.",
        "low_cost_routes": "Free DAWs (Reaper free trial, Cakewalk, BandLab), open audio sample packs, free acoustic tutorials, community church or campus audio volunteering.",
        "entrance_exams": json.dumps(["FTII JET (Sound Recording & Design)", "Institutional Music Production Auditions"]),
        "advantages": json.dumps([
            "Turn personal passion for music, melody, and rhythm into a sustainable professional craft",
            "Diverse avenues in film scoring, gaming, streaming podcasts, advertising jingles, and indie artist releases",
            "Global digital streaming allows publishing directly to worldwide audiences without traditional label gatekeepers"
        ]),
        "challenges": json.dumps([
            "Initial freelance income can be unpredictable while establishing an industry reputation",
            "Requires continuous critical ear training to discern subtle phase cancellations and frequency masking",
            "Late night studio sessions and highly subjective client revisions"
        ]),
        "geographic_considerations": "Major film and music capitals (Mumbai, Chennai, Hyderabad, Kolkata, Punjab, NCR) and home studios worldwide.",
        "regulated": 0,
        "source_urls": json.dumps([
            {"title": "Ableton Learning Music & Synths", "url": "https://learningmusic.ableton.com"},
            {"title": "Cambridge Music Technology Free Multitrack Library", "url": "https://www.cambridge-mt.com/ms/mtk"},
            {"title": "Audio Engineering Society (AES India)", "url": "https://aes.org"}
        ]),
        "last_verified": "2026-10-10"
    },
    {
        "slug": "animator-visual-artist",
        "title": "3D Animator & Visual Development Artist",
        "category": "Creative & Design",
        "short_description": "Brings virtual characters, objects, and environments to life through keyframe animation, 3D modeling, texturing, character rigging, and lighting for films, games, and VR experiences.",
        "typical_responsibilities": json.dumps([
            "Animate stylized and realistic character movement applying the 12 Principles of Animation",
            "Construct skeletal character armatures, inverse kinematics (IK), and skinning weights for rigging",
            "Model 3D hard-surface and organic assets in polygonal modeling software (Blender / Maya)",
            "Paint PBR (Physically Based Rendering) texture maps for roughness, metallic, and normal maps",
            "Set up cinematic three-point lighting, ambient occlusion, and camera focal lengths for final rendering"
        ]),
        "relevant_interests": json.dumps(["animation", "3d art", "creativity", "fine arts", "gaming", "visual storytelling"]),
        "relevant_strengths": json.dumps(["visual imagination", "attention to weight and timing", "patience", "spatial reasoning", "creativity"]),
        "educational_requirements": "Bachelor's degree in Animation, Visual Effects, Fine Arts (BFA), or diploma in 3D Animation with an outstanding showreel demonstrating body mechanics and acting.",
        "min_education_level": "Class 10",
        "suitable_streams": json.dumps(["Any stream with drawing / 3D aptitude", "Fine Arts", "Humanities", "Computer Science"]),
        "important_skills": json.dumps([
            "12 Principles of Animation (Timing, Spacing, Squash & Stretch, Anticipation)",
            "3D Animation Software (Blender / Maya / 3ds Max)",
            "Character Rigging & Weight Painting",
            "Texturing & UV Unwrapping (Substance 3D Painter / Blender)",
            "Lighting, Rendering & Compositing (Cycles / Eevee / Arnold)",
            "Real-Time Engines (Unreal Engine 5 basics)"
        ]),
        "suggested_beginner_projects": json.dumps([
            "Animate a classic bouncing ball with realistic weight, squash, and decay in free open-source Blender",
            "Model, texture, and rig a low-poly stylized character suitable for a mobile game in Blender",
            "Animate a dynamic 5-second character walk-cycle and jump obstacle in 3D"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Study the 12 Principles of Animation", "explanation": "Read 'The Animator's Survival Kit' by Richard Williams and study timing, spacing, and arcs.", "action": "Complete bouncing ball, pendulum, and flour sack exercises in 2D or 3D.", "duration": "4 weeks"},
            {"step": 2, "title": "Master Free 3D Software (Blender)", "explanation": "Learn Blender's interface, viewport navigation, keyframing, graph editor, and dope sheet.", "action": "Complete Blender Foundation official beginner Donut and Animation tutorials.", "duration": "6 weeks"},
            {"step": 3, "title": "Master Body Mechanics Animation", "explanation": "Use free character rigs to animate walk cycles, run cycles, heavy lifting, and athletic jumps.", "action": "Animate 3 distinct character locomotion cycles.", "duration": "8 weeks"},
            {"step": 4, "title": "Study Character Acting and Facial Animation", "explanation": "Animate dialogue lip-sync, subtle eye darts, emotional gestures, and subtext.", "action": "Animate a 10-second character acting sequence to an audio dialogue clip.", "duration": "6 weeks"},
            {"step": 5, "title": "Assemble Animation Showreel & Apply to Studios", "explanation": "Compile your best 45–60 seconds of character animation showing clean arcs and strong weight.", "action": "Apply to gaming, VFX, and animation studios.", "duration": "Ongoing"}
        ]),
        "cost_category": "Low / Free Accessible",
        "cost_estimate_detail": "Blender is 100% free and open-source; Mid-tier graphics workstation: ₹50,000–₹1,00,000; Private animation diplomas: ₹1,50,000–₹5,00,000.",
        "low_cost_routes": "Blender Foundation free official tutorials, open 3D rigs from Animation Mentor / Blender Studio, community art challenges.",
        "entrance_exams": json.dumps(["UCEED", "NID DAT", "Institutional Animation Entrance Tests"]),
        "advantages": json.dumps([
            "Massive global demand driven by video games, VFX blockbuster films, animated series, and virtual simulations",
            "Blender allows anyone with a computer to learn world-class 3D craft with zero software licensing costs",
            "Deep satisfaction bringing imaginary characters and fantasy worlds to vivid life"
        ]),
        "challenges": json.dumps([
            "Requires immense patience: a polished 5-second character animation can take days of meticulous fine-tuning",
            "Hardware intensive: requires capable GPU for smooth viewport playback and rendering",
            "Must keep pace with rapidly evolving real-time rendering pipelines (Unreal Engine 5) and AI procedural tools"
        ]),
        "geographic_considerations": "Major animation and VFX clusters in Mumbai, Hyderabad, Pune, Bengaluru, Chennai, and remote international studio contracts.",
        "regulated": 0,
        "source_urls": json.dumps([
            {"title": "Blender Foundation Open Source 3D", "url": "https://www.blender.org"},
            {"title": "National Institute of Design (NID Animation)", "url": "https://www.nid.edu"},
            {"title": "Animation Guild Open Resources", "url": "https://animationguild.org"}
        ]),
        "last_verified": "2026-10-10"
    },
    {
        "slug": "choreographer-performer",
        "title": "Choreographer & Movement Director",
        "category": "Creative & Design",
        "short_description": "Designs original movement sequences, stage blocking, and expressive dance choreography for films, music videos, theatrical productions, dance academies, and competitive athletic routines.",
        "typical_responsibilities": json.dumps([
            "Conceive and structure thematic dance routines matching musical tempo, lyrics, and emotional narrative",
            "Teach complex choreography, footwork, and movement dynamics to dancers of varying experience levels",
            "Coordinate stage blocking, spatial formations, and camera angles with directors and lighting crews",
            "Design physical warm-ups, conditioning routines, and injury prevention exercises for performers",
            "Direct live dance rehearsals, audition casting, and stage performances under production deadlines"
        ]),
        "relevant_interests": json.dumps(["dance", "choreography", "performing arts", "music", "fitness", "creativity"]),
        "relevant_strengths": json.dumps(["physical agility", "musical rhythm", "creativity", "spatial awareness", "leadership", "communication"]),
        "educational_requirements": "Degree or diploma in Performing Arts (Dance / Choreography) or extensive professional training under accredited dance masters (Gurus) and dance academies with proven performance credits.",
        "min_education_level": "Class 10",
        "suitable_streams": json.dumps(["Any stream with physical agility and musical rhythm", "Humanities / Arts", "Performing Arts"]),
        "important_skills": json.dumps([
            "Dance Technique & Movement Vocabulary (Classical, Contemporary, Urban/Hip-hop)",
            "Choreographic Composition & Spatial Formations",
            "Rhythm, Musicality & Tempo Counting",
            "Dancer Coaching & Rehearsal Leadership",
            "Stage Staging & Camera Framing Awareness",
            "Physical Conditioning & Injury Prevention"
        ]),
        "suggested_beginner_projects": json.dumps([
            "Choreograph and record a 60-second original dance piece interpreting a musical piece with a clear emotional arc",
            "Design a synchronized group routine for a 5-member campus or local dance team and conduct rehearsals",
            "Create an instructional video breaking down fundamental movement techniques and warm-up safety for beginners"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Build Rigorous Physical Technique in a Dance Form", "explanation": "Train extensively in classical, contemporary, folk, or street dance foundations.", "action": "Enroll in structured dance training with daily practice.", "duration": "2–4 years"},
            {"step": 2, "title": "Study Choreographic Principles and Composition", "explanation": "Learn spatial pathways, canon, unison, contrast, levels (high/low), and musical counts.", "action": "Choreograph a short solo piece and seek peer critique.", "duration": "6 months"},
            {"step": 3, "title": "Gain Assistant Choreographer / Troupe Experience", "explanation": "Perform in professional dance troupes, theatrical musicals, or assist senior choreographers on set.", "action": "Audition for dance ensembles or collegiate performance teams.", "duration": "1–2 years"},
            {"step": 4, "title": "Learn Video Staging and Lighting Design", "explanation": "Understand camera angles, movement tracking, and theatrical lighting to enhance movement visual impact.", "action": "Direct and film 2 dance concept videos with multicam coverage.", "duration": "4 months"},
            {"step": 5, "title": "Establish Independent Choreography Practice or Academy", "explanation": "Direct routines for films, commercials, music videos, or found a professional dance training academy.", "action": "Build a client portfolio and social media video showreel.", "duration": "Ongoing"}
        ]),
        "cost_category": "Low / Free Accessible",
        "cost_estimate_detail": "State Performing Arts Universities (BPA): ₹15,000–₹50,000 total; Specialized private academies: ₹50,000–₹2,00,000.",
        "low_cost_routes": "Government performing arts academies (Sangeet Natak Akademi affiliates, university dance departments), cultural scholarships, and community performance troupes.",
        "entrance_exams": json.dumps(["CUET (UG) Performing Arts", "Institutional Dance Auditions"]),
        "advantages": json.dumps([
            "Deep personal expression through visceral, energetic physical artistry",
            "Expanding commercial opportunities across film production, weddings, corporate events, reality television, and fitness dance academies",
            "Lifelong community building and mentorship of upcoming dance and movement talent"
        ]),
        "challenges": json.dumps([
            "High physical demands on joints and muscles; requires disciplined injury prevention and recovery regimens",
            "Income can be project-based and seasonal, requiring self-promotion and networking",
            "Requires patience and communication to train dancers of varying skill levels"
        ]),
        "geographic_considerations": "Entertainment centers (Mumbai, Chennai, Hyderabad, Kolkata), national cultural hubs, and dance studios across tier-1 and tier-2 cities.",
        "regulated": 0,
        "source_urls": json.dumps([
            {"title": "Sangeet Natak Akademi (National Academy of Music, Dance and Drama)", "url": "https://sangeetnatak.gov.in"},
            {"title": "Kathak Kendra / Kalakshetra Foundation", "url": "https://www.kalakshetra.in"},
            {"title": "International Dance Council (CID UNESCO)", "url": "https://www.cid-world.org"}
        ]),
        "last_verified": "2026-10-10"
    },
    {
        "slug": "public-policy-civil-services",
        "title": "Civil Services Officer & Public Policy Administrator",
        "category": "Education & Social",
        "short_description": "Directs administrative governance, policy implementation, law and order enforcement, socio-economic welfare schemes, and public revenue systems through constitutional and statutory authorities.",
        "typical_responsibilities": json.dumps([
            "Administer district governance, public revenue collection, and land administration",
            "Oversee execution of government welfare programs (rural employment, healthcare, public education)",
            "Coordinate emergency disaster response, humanitarian relief, and law-and-order maintenance",
            "Draft policy recommendations, cabinet briefing notes, and statutory regulatory notifications",
            "Address citizen grievances and ensure transparent delivery of public municipal services"
        ]),
        "relevant_interests": json.dumps(["public service", "governance", "law", "social impact", "leadership", "policy"]),
        "relevant_strengths": json.dumps(["leadership", "ethical integrity", "decision-making under pressure", "communication", "analytical thinking"]),
        "educational_requirements": "Bachelor's degree in any discipline from a recognized university. Mandatory qualification through competitive civil service examinations (UPSC Civil Services Examination for IAS/IPS/IFS or State Public Service Commission exams). Nonpartisan statutory administration.",
        "min_education_level": "Undergraduate",
        "suitable_streams": json.dumps(["Any stream", "Humanities / Arts (History, Pol Science, Geography)", "Commerce", "Science / Engineering"]),
        "important_skills": json.dumps([
            "Public Administration & District Governance",
            "Constitutional Law & Statutory Regulations",
            "Policy Analysis & Socio-Economic Assessment",
            "Disaster Management & Crisis Leadership",
            "Public Budgeting & Financial Allocation",
            "Empathetic Citizen Grievance Redressal"
        ]),
        "suggested_beginner_projects": json.dumps([
            "Conduct an empirical audit of a local municipal grievance redressal system or public distribution scheme",
            "Write a structured 5-page policy brief proposing solutions to urban solid waste management in your municipality",
            "Participate in a Model United Nations (MUN) or Youth Parliament debating public welfare legislation"
        ]),
        "learning_roadmap": json.dumps([
            {"step": 1, "title": "Build Broad General Studies & Current Affairs Awareness", "explanation": "Master NCERT fundamentals in history, geography, polity, economics, and environment.", "action": "Read NCERT Class 6–12 textbooks and daily national newspapers.", "duration": "1–2 years"},
            {"step": 2, "title": "Earn Bachelor's Degree in Any Discipline", "explanation": "Maintain strong graduation record while developing critical analytical and essay writing skills.", "action": "Complete undergraduate degree in arts, science, or engineering.", "duration": "3–4 years"},
            {"step": 3, "title": "Prepare for UPSC / State PSC Preliminary Exam", "explanation": "Master General Studies Paper I and Civil Services Aptitude Test (CSAT) with extensive mock tests.", "action": "Solve 30 full-length prelims previous-year question papers.", "duration": "9–12 months"},
            {"step": 4, "title": "UPSC Main Written Examination Prep", "explanation": "Practice intensive answer writing across 9 descriptive papers including Essay, GS I–IV, and Optional Subject.", "action": "Write 50 practice answers and participate in evaluation test series.", "duration": "6–9 months"},
            {"step": 5, "title": "Personality Test (Interview) & Academy Foundation Training", "explanation": "Clear interview panel on personality, ethics, and current issues; undergo training at LBSNAA.", "action": "Attend mock interviews and complete foundational civil service induction.", "duration": "Post-selection"}
        ]),
        "cost_category": "Low / Free Accessible",
        "cost_estimate_detail": "Govt University degree: ₹10,000–₹50,000 total; Exam fee: ₹100 (free for female/SC/ST candidates); NCERT textbooks: ₹1,500.",
        "low_cost_routes": "NCERT books (available free online), Press Information Bureau (PIB), Rajya Sabha / Sansad TV debates, public libraries, free civil services study initiatives.",
        "entrance_exams": json.dumps(["UPSC Civil Services Examination (Prelims, Mains, Interview)", "State Public Service Commission Examinations (State PSC)"]),
        "advantages": json.dumps([
            "Unmatched institutional scale to positively impact millions of lives and public welfare",
            "High constitutional status, security of tenure, and respect in society",
            "Diverse administrative exposure spanning rural development, health, transport, and finance"
        ]),
        "challenges": json.dumps([
            "Extremely competitive examination with acceptance rate below 0.1% among over 1 million applicants",
            "Demanding 24/7 public accountability during emergencies, natural disasters, and administrative crises",
            "Regular transfers across districts and remote administrative postings"
        ]),
        "geographic_considerations": "District collectorates, state secretariats, central government ministries (New Delhi), and diplomatic missions worldwide.",
        "regulated": 1,
        "source_urls": json.dumps([
            {"title": "Union Public Service Commission (UPSC)", "url": "https://www.upsc.gov.in"},
            {"title": "Lal Bahadur Shastri National Academy of Administration (LBSNAA)", "url": "https://www.lbsnaa.gov.in"},
            {"title": "National Portal of India - Governance", "url": "https://www.india.gov.in"}
        ]),
        "last_verified": "2026-10-10"
    }
]

print(f"Verified {len(EXPANDED_CAREERS)} expanded careers.")
for c in EXPANDED_CAREERS:
    print("-", c["slug"], ":", c["title"])
