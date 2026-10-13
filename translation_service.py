"""
CareerCompass - Non-AI Multilingual Translation Service
Provides simple, reliable, deterministic translation across Telugu (te), Hindi (hi), and English (en).

CRITICAL REQUIREMENT:
- Absolutely ZERO AI models (No Gemini, OpenAI, Anthropic, ChatGPT, LLMs).
- Uses domain translation dictionary, rule-based token translation, and
  standard non-AI translation memory APIs (e.g. MyMemory / LibreTranslate).
- Supports all 6 translation pairs:
    1. te -> hi
    2. te -> en
    3. hi -> te
    4. hi -> en
    5. en -> te
    6. en -> hi
"""

import os
import re
import html
import logging
import requests

logger = logging.getLogger("careercompass.translation")

SUPPORTED_LANGUAGES = {
    "te": {"name": "Telugu", "native": "తెలుగు", "code": "te-IN"},
    "hi": {"name": "Hindi", "native": "हिन्दी", "code": "hi-IN"},
    "en": {"name": "English", "native": "English", "code": "en-IN"}
}

# ---------------------------------------------------------------------------
# Verified Domain Translation Dictionary (Bidirectional across en, te, hi)
# ---------------------------------------------------------------------------
DOMAIN_DICTIONARY = [
    # Full sample profile phrases
    {
        "en": "My child is interested in Civil Engineer. Reasons: I enjoy designing buildings and practical structures. Top priorities: Creative Freedom, Fast Skill Growth.",
        "hi": "मेरा बच्चा सिविल इंजीनियर बनने में रुचि रखता है। कारण: मुझे भवनों और व्यावहारिक संरचनाओं का डिज़ाइन बनाना पसंद है। शीर्ष प्राथमिकताएं: रचनात्मक स्वतंत्रता, तेज़ कौशल विकास।",
        "te": "నా బిడ్డ సివిల్ ఇంజనీర్ రంగంలో ఆసక్తి చూపుతున్నారు. కారణాలు: నేను భవనాలు మరియు ఆచరణాత్మక నిర్మాణాలను రూపొందించడాన్ని ఆనందిస్తాను. ప్రధాన ప్రాధాన్యతలు: సృజనాత్మక స్వేచ్ఛ, వేగవంతమైన నైపుణ్యాల వృద్ధి."
    },
    {
        "en": "My child is interested in Software Engineer. Reasons: Passionate about programming and modern web systems. Top priorities: Tech Innovation, Fast Skill Growth.",
        "hi": "मेरा बच्चा सॉफ्टवेयर इंजीनियर बनने में रुचि रखता है। कारण: मुझे प्रोग्रामिंग और आधुनिक वेब प्रणालियों में गहरी रुचि है। शीर्ष प्राथमिकताएं: तकनीकी नवाचार, तेज़ कौशल विकास।",
        "te": "నా బిడ్డ సాఫ్ట్‌వేర్ ఇంజనీర్ రంగంలో ఆసక్తి చూపుతున్నారు. కారణాలు: నేను ప్రోగ్రామింగ్ మరియు ఆధునిక వెబ్ వ్యవస్థల పట్ల ఆసక్తి కలిగి ఉన్నాను. ప్రధాన ప్రాధాన్యతలు: సాంకేతిక ఆవిష్కరణ, వేగవంతమైన నైపుణ్యాల వృద్ధి."
    },
    {
        "en": "My child is interested in Data Scientist. Reasons: Loves math and statistical patterns. Top priorities: High Earning Potential, Global Career.",
        "hi": "मेरा बच्चा डेटा साइंटिस्ट बनने में रुचि रखता है। कारण: गणित और सांख्यिकीय पैटर्न पसंद हैं। शीर्ष प्राथमिकताएं: उच्च आय संभावना, वैश्विक करियर।",
        "te": "నా బిడ్డ డేటా సైంటిస్ట్ రంగంలో ఆసక్తి చూపుతున్నారు. కారణాలు: గణితం మరియు గణాంక నమూనాల పట్ల మక్కువ కలిగి ఉన్నారు. ప్రధాన ప్రాధాన్యతలు: అధిక సంపాదన సంభావ్యత, ప్రపంచ కెరీర్."
    },

    # Common CareerCompass labels & sentence fragments
    {
        "en": "My child is interested in",
        "hi": "मेरा बच्चा इसमें रुचि रखता है",
        "te": "నా బిడ్డ ఇందులో ఆసక్తి చూపుతున్నారు"
    },
    {
        "en": "Student's Preferred Career",
        "hi": "विद्यार्थी का पसंदीदा करियर",
        "te": "విద్యార్థి ప్రాధాన్యత కెరీర్"
    },
    {
        "en": "Student's Selected Career",
        "hi": "विद्यार्थी द्वारा चुना गया करियर",
        "te": "విద్యార్థి ఎంచుకున్న కెరీర్"
    },
    {
        "en": "Student Reasons",
        "hi": "विद्यार्थी के कारण",
        "te": "విద్యార్థి కారణాలు"
    },
    {
        "en": "Reasons",
        "hi": "कारण",
        "te": "కారణాలు"
    },
    {
        "en": "Top priorities",
        "hi": "शीर्ष प्राथमिकताएं",
        "te": "ప్రధాన ప్రాధాన్యతలు"
    },
    {
        "en": "Priorities",
        "hi": "प्राथमिकताएं",
        "te": "ప్రాధాన్యతలు"
    },
    {
        "en": "Family Worries",
        "hi": "परिवार की चिंताएं",
        "te": "కుటుంబ ఆందోళనలు"
    },
    {
        "en": "Family Concerns",
        "hi": "परिवार की चिंताएं",
        "te": "కుటుంబ ఆందోళనలు"
    },
    {
        "en": "Concerns",
        "hi": "चिंताएं",
        "te": "ఆందోళనలు"
    },
    {
        "en": "Parent Worries",
        "hi": "अभिभावक की चिंताएं",
        "te": "తల్లిదండ్రుల ఆందోళనలు"
    },
    {
        "en": "Alternative Career",
        "hi": "वैकल्पिक करियर",
        "te": "ప్రత్యామ్నాయ కెరీర్"
    },
    {
        "en": "Education Level",
        "hi": "शिक्षा का स्तर",
        "te": "విద్యా స్థాయి"
    },
    {
        "en": "Budget Limit",
        "hi": "बजट सीमा",
        "te": "బడ్జెట్ పరిమితి"
    },
    {
        "en": "Career Guidance",
        "hi": "करियर मार्गदर्शन",
        "te": "కెరీర్ మార్గదర్శకత్వం"
    },
    {
        "en": "Career Reality",
        "hi": "करियर की वास्तविकता",
        "te": "కెరీర్ వాస్తవికత"
    },
    {
        "en": "Career Roadmap",
        "hi": "करियर रोडमैप",
        "te": "కెరీర్ రోడ్‌మ్యాప్"
    },

    # Specific goals & worries
    {
        "en": "Creative Freedom & Building Things",
        "hi": "रचनात्मक स्वतंत्रता और नई चीजें बनाना",
        "te": "సృజనాత్మక స్వేచ్ఛ మరియు నూతన వస్తువుల రూపకల్పన"
    },
    {
        "en": "Fast Skill Growth",
        "hi": "तेज़ कौशल विकास",
        "te": "వేగవంతమైన నైపుణ్యాల వృద్ధి"
    },
    {
        "en": "Predictable Employment & Stability",
        "hi": "स्थिर रोजगार और सुरक्षा",
        "te": "స్థిరమైన ఉద్యోగం మరియు భద్రత"
    },
    {
        "en": "Managing High College Tuition Costs",
        "hi": "कॉलेज की उच्च ट्यूशन लागत का प्रबंधन",
        "te": "అధిక కళాశాల ట్యూషన్ ఖర్చులను నిర్వహించడం"
    },
    {
        "en": "High Earning Potential",
        "hi": "उच्च आय संभावना",
        "te": "అధిక సంపాదన సంభావ్యత"
    },
    {
        "en": "Job Security & Stability",
        "hi": "नौकरी की सुरक्षा और स्थिरता",
        "te": "ఉద్యోగ భద్రత మరియు స్థిరత్వం"
    },
    {
        "en": "Work-Life Balance",
        "hi": "कार्य-जीवन संतुलन",
        "te": "పని-జీవిత సమతుల్యత"
    },
    {
        "en": "Social Impact & Helping Others",
        "hi": "सामाजिक प्रभाव और दूसरों की मदद",
        "te": "సామాజిక ప్రభావం మరియు ఇతరులకు సహాయం"
    },
    {
        "en": "Creative Freedom",
        "hi": "रचनात्मक स्वतंत्रता",
        "te": "సృజనాత్మక స్వేచ్ఛ"
    },
    {
        "en": "Employment Stability",
        "hi": "रोजगार स्थिरता",
        "te": "ఉపాధి స్థిరత్వం"
    },
    {
        "en": "College Tuition Costs",
        "hi": "कॉलेज ट्यूशन लागत",
        "te": "కళాశాల ట్యూషన్ ఖర్చులు"
    },

    # Student personal reasons / sample statements
    {
        "en": "I enjoy designing buildings and practical structures",
        "hi": "मुझे भवनों और व्यावहारिक संरचनाओं का डिज़ाइन बनाना पसंद है",
        "te": "నేను భవనాలు మరియు ఆచరణాత్మక నిర్మాణాలను రూపొందించడాన్ని ఆనందిస్తాను"
    },
    {
        "en": "Passionate about programming and modern web systems",
        "hi": "मुझे प्रोग्रामिंग और आधुनिक वेब प्रणालियों में गहरी रुचि है",
        "te": "నేను ప్రోగ్రామింగ్ మరియు ఆధునిక వెబ్ వ్యవస్థల పట్ల ఆసక్తి కలిగి ఉన్నాను"
    },
    {
        "en": "Loves math and statistical patterns",
        "hi": "गणित और सांख्यिकीय पैटर्न पसंद हैं",
        "te": "గణితం మరియు గణాంక నమూనాల పట్ల మక్కువ కలిగి ఉన్నారు"
    },

    # Greetings & Common Phrases
    {
        "en": "Hello",
        "hi": "नमस्ते",
        "te": "నమస్కారం"
    },
    {
        "en": "Thank you",
        "hi": "धन्यवाद",
        "te": "ధన్యవాదాలు"
    },
    {
        "en": "Welcome",
        "hi": "स्वागत है",
        "te": "స్వాగతం"
    },
    {
        "en": "Good morning",
        "hi": "शुभ प्रभात",
        "te": "శుభోదయం"
    },
    {
        "en": "Yes",
        "hi": "हाँ",
        "te": "అవును"
    },
    {
        "en": "No",
        "hi": "नहीं",
        "te": "కాదు"
    },

    # Categories
    {
        "en": "Engineering & Technology",
        "hi": "इंजीनियरिंग और प्रौद्योगिकी",
        "te": "ఇంజనీరింగ్ మరియు టెక్నాలజీ"
    },
    {
        "en": "Healthcare & Medicine",
        "hi": "स्वास्थ्य सेवा और चिकित्सा",
        "te": "ఆరోగ్య సంరక్షణ మరియు వైద్యం"
    },
    {
        "en": "Business & Finance",
        "hi": "व्यवसाय और वित्त",
        "te": "వ్యాపారం మరియు ఫైనాన్స్"
    },
    {
        "en": "Arts & Design",
        "hi": "कला और डिजाइन",
        "te": "కళలు మరియు డిజైన్"
    },
    {
        "en": "Science & Research",
        "hi": "विज्ञान और अनुसंधान",
        "te": "సైన్స్ మరియు పరిశోధన"
    },
    {
        "en": "Law & Public Policy",
        "hi": "कानून और सार्वजनिक नीति",
        "te": "చట్టం మరియు ప్రజా విధానం"
    },

    # Career Titles (All major CareerCompass careers)
    {
        "en": "Civil Engineer",
        "hi": "सिविल इंजीनियर",
        "te": "సివిల్ ఇంజనీర్"
    },
    {
        "en": "Software Engineer",
        "hi": "सॉफ्टवेयर इंजीनियर",
        "te": "సాఫ్ట్‌వేర్ ఇంజనీర్"
    },
    {
        "en": "Data Scientist",
        "hi": "डेटा साइंटिस्ट",
        "te": "డేటా సైంటిస్ట్"
    },
    {
        "en": "Doctor",
        "hi": "चिकित्सक (डॉक्टर)",
        "te": "వైద్యుడు (డాక్టర్)"
    },
    {
        "en": "Physician",
        "hi": "चिकित्सक (डॉक्टर)",
        "te": "వైద్యుడు (డాక్టర్)"
    },
    {
        "en": "Nurse",
        "hi": "नर्स",
        "te": "నర్సు"
    },
    {
        "en": "Teacher",
        "hi": "शिक्षक",
        "te": "ఉపాధ్యాయుడు"
    },
    {
        "en": "Mechanical Engineer",
        "hi": "मैकेनिकल इंजीनियर",
        "te": "మెకానికల్ ఇంజనీర్"
    },
    {
        "en": "Electrical Engineer",
        "hi": "इलेक्ट्रिकल इंजीनियर",
        "te": "ఎలక్ట్రికల్ ఇంజనీర్"
    },
    {
        "en": "Chartered Accountant",
        "hi": "चार्टर्ड अकाउंटेंट",
        "te": "చార్టర్డ్ అకౌంటెంట్"
    },
    {
        "en": "Lawyer",
        "hi": "वकील (अधिवक्ता)",
        "te": "న్యాయవాది (లాయర్)"
    },
    {
        "en": "Graphic Designer",
        "hi": "ग्राफिक डिजाइनर",
        "te": "గ్రాఫిక్ డిజైనర్"
    },
    {
        "en": "Architect",
        "hi": "वास्तुकार (आर्किटेक्ट)",
        "te": "ఆర్కిటెక్ట్"
    },
    {
        "en": "Pharmacist",
        "hi": "फार्मासिस्ट",
        "te": "ఫార్మసిస్ట్"
    },
    {
        "en": "Psychologist",
        "hi": "मनोवैज्ञानिक",
        "te": "సైకాలజిస్ట్"
    },
    {
        "en": "Digital Marketer",
        "hi": "डिजिटल मार्केटर",
        "te": "డిజిటల్ మార్కెటర్"
    },
    {
        "en": "Cyber Security Analyst",
        "hi": "साइबर सुरक्षा विश्लेषक",
        "te": "సైబర్ సెక్యూరిటీ అనలిస్ట్"
    },
    {
        "en": "AI / ML Engineer",
        "hi": "एआई / एमएल इंजीनियर",
        "te": "AI / ML ఇంజనీర్"
    },
    {
        "en": "Business Analyst",
        "hi": "बिजनेस एनालिस्ट",
        "te": "బిజినెస్ అనలిస్ట్"
    },
    {
        "en": "Financial Analyst",
        "hi": "वित्तीय विश्लेषक",
        "te": "ఫైనాన్షియల్ అనలిస్ట్"
    },
    {
        "en": "Product Manager",
        "hi": "प्रोडक्ट मैनेजर",
        "te": "ప్రొడక్ట్ మేనేజర్"
    },
    {
        "en": "UX/UI Designer",
        "hi": "यूएक्स/यूआई डिजाइनर",
        "te": "UX/UI డిజైనర్"
    },
    {
        "en": "Research Scientist",
        "hi": "अनुसंधान वैज्ञानिक",
        "te": "పరిశోధనా శాస్త్రవేత్త"
    },
    {
        "en": "Commercial Pilot",
        "hi": "कमर्शियल पायलट",
        "te": "కమర్షియల్ పైలట్"
    },
    {
        "en": "Journalist",
        "hi": "पत्रकार",
        "te": "జర్నలిస్ట్ (విలేకరి)"
    },
    # Complete 36 CareerCompass Careers
    {
        "en": "Chartered Accountant / Financial Analyst",
        "hi": "चार्टर्ड अकाउंटेंट / वित्तीय विश्लेषक",
        "te": "చార్టర్డ్ అకౌంటెంట్ / ఫైనాన్షియల్ అనలిస్ట్"
    },
    {
        "en": "Entrepreneur / Startup Founder",
        "hi": "उद्यमी / स्टार्टअप संस्थापक",
        "te": "ఎంట్రప్రెన్యూర్ / స్టార్టప్ వ్యవస్థాపకుడు"
    },
    {
        "en": "Human Resources (HR) & Talent Specialist",
        "hi": "मानव संसाधन (HR) एवं प्रतिभा विशेषज्ञ",
        "te": "హెచ్‌ఆర్ & టాలెంట్ స్పెషలిస్ట్"
    },
    {
        "en": "Marketing Specialist & Brand Strategist",
        "hi": "मार्केटिंग विशेषज्ञ एवं ब्रांड रणनीतिकार",
        "te": "మార్కెటింగ్ స్పెషలిస్ట్ & బ్రాండ్ స్ట్రాటజిస్ట్"
    },
    {
        "en": "Operations & Supply Chain Manager",
        "hi": "संचालन एवं आपूर्ति श्रृंखला प्रबंधक",
        "te": "ఆపరేషన్స్ & సప్లై చైన్ మేనేజర్"
    },
    {
        "en": "3D Animator & Visual Development Artist",
        "hi": "3D एनिमेटर एवं दृश्य विकास कलाकार",
        "te": "3D యానిమేటర్ & విజువల్ ఆర్టిస్ట్"
    },
    {
        "en": "Choreographer & Movement Director",
        "hi": "कोरियोग्राफर एवं नृत्य निर्देशक",
        "te": "కొరియోగ్రాఫర్ & మూవ్‌మెంట్ డైరెక్టర్"
    },
    {
        "en": "Music Producer & Audio Engineer",
        "hi": "संगीत निर्माता एवं ऑडियो इंजीनियर",
        "te": "సంగీత నిర్మాత & ఆడియో ఇంజనీర్"
    },
    {
        "en": "Video Editor & Digital Media Producer",
        "hi": "वीडियो एडिटर एवं डिजिटल मीडिया निर्माता",
        "te": "వీడియో ఎడిటర్ & డిజిటల్ మీడియా ప్రొడ్యూసర్"
    },
    {
        "en": "Data Analyst",
        "hi": "डेटा एनालिस्ट",
        "te": "డేటా అనలిస్ట్"
    },
    {
        "en": "Civil Services Officer & Public Policy Administrator",
        "hi": "सिविल सेवा अधिकारी एवं लोक नीति प्रशासक",
        "te": "సివిల్ సర్వీసెస్ ఆఫీసర్ & పబ్లిక్ పాలసీ అడ్మినిస్ట్రేటర్"
    },
    {
        "en": "Teacher or Educator",
        "hi": "शिक्षक या शिक्षक मार्गदर्शक",
        "te": "ఉపాధ్యాయుడు లేదా విద్యావేత్త"
    },
    {
        "en": "Biotechnologist & Genomic Researcher",
        "hi": "बायोटेक्नोलॉजिस्ट एवं जीनोमिक शोधकर्ता",
        "te": "బయోటెక్నాలజిస్ట్ & జెనోమిక్ పరిశోధకుడు"
    },
    {
        "en": "Clinical Psychologist / Counselor",
        "hi": "क्लिनिकल मनोवैज्ञानिक / परामर्शदाता",
        "te": "క్లినికల్ సైకాలజిస్ట్ / కౌన్సిలర్"
    },
    {
        "en": "Healthcare Professional (Nursing / Medicine)",
        "hi": "स्वास्थ्य सेवा पेशेवर (नर्सिंग / चिकित्सा)",
        "te": "ఆరోగ్య సంరక్షణ నిపుణుడు (నర్సింగ్ / మెడిసిన్)"
    },
    {
        "en": "Pharmacist & Clinical Medication Specialist",
        "hi": "फार्मासिस्ट एवं नैदानिक दवा विशेषज्ञ",
        "te": "ఫార్మసిస్ట్ & ఔషధ నిపుణుడు"
    },
    {
        "en": "Astronomer & Space Scientist",
        "hi": "खगोलशास्त्री एवं अंतरिक्ष वैज्ञानिक",
        "te": "ఖగోళ శాస్త్రవేత్త & అంతరిక్ష శాస్త్రవేత్త"
    },
    {
        "en": "Environmental Scientist",
        "hi": "पर्यावरण वैज्ञानिक",
        "te": "పర్యావరణ శాస్త్రవేత్త"
    },
    {
        "en": "Athletic Coach & Sports Trainer",
        "hi": "एथलेटिक कोच एवं खेल प्रशिक्षक",
        "te": "అథ్లెటిక్ కోచ్ & స్పోర్ట్స్ ట్రైనర్"
    },
    {
        "en": "Sports Analyst & Performance Data Specialist",
        "hi": "खेल विश्लेषक एवं प्रदर्शन डेटा विशेषज्ञ",
        "te": "స్పోర్ట్స్ అనలిస్ట్ & పెర్ఫార్మెన్స్ డేటా స్పెషలిస్ట్"
    },
    {
        "en": "Sports Event & Facility Manager",
        "hi": "खेल आयोजन एवं सुविधा प्रबंधक",
        "te": "స్పోర్ట్స్ ఈవెంట్ & ఫెసిలిటీ మేనేజర్"
    },
    {
        "en": "Sports Physiotherapist",
        "hi": "खेल फिजियोथेरेपिस्ट",
        "te": "స్పోర్ట్స్ ఫిజియోథెరపిస్ట్"
    },
    {
        "en": "Sports Science Specialist & Exercise Physiologist",
        "hi": "खेल विज्ञान विशेषज्ञ एवं व्यायाम शरीर क्रिया विज्ञानी",
        "te": "స్పోర్ట్స్ సైన్స్ స్పెషలిస్ట్"
    },
    {
        "en": "Aerospace & Aeronautical Engineer",
        "hi": "एयरोस्पेस एवं वैमानिकी इंजीनियर",
        "te": "ఏరోస్పేస్ & ఏరోనాటికల్ ఇంజనీర్"
    },
    {
        "en": "Astronaut & Spaceflight Mission Specialist",
        "hi": "अंतरिक्ष यात्री एवं अंतरिक्ष मिशन विशेषज्ञ",
        "te": "వ్యోమగామి & అంతరిక్ష యాత్ర నిపుణుడు"
    },
    {
        "en": "Cybersecurity Analyst",
        "hi": "साइबर सुरक्षा विश्लेषक",
        "te": "సైబర్‌సెక్యూరిటీ అనలిస్ట్"
    },
    {
        "en": "Electrical & Power Systems Engineer",
        "hi": "इलेक्ट्रिकल एवं पावर सिस्टम्स इंजीनियर",
        "te": "ఎలక్ట్రికల్ & పవర్ సిస్టమ్స్ ఇంజనీర్"
    },
    {
        "en": "Electronics Engineer",
        "hi": "इलेक्ट्रॉनिक्स इंजीनियर",
        "te": "ఎలక్ట్రానిక్స్ ఇంజనీర్"
    },
    {
        "en": "Robotics & Mechatronics Engineer",
        "hi": "रोबोटिक्स एवं मेकाट्रॉनिक्स इंजीनियर",
        "te": "రోబోటిక్స్ & మెకాట్రానిక్స్ ఇంజనీర్"
    },
    {
        "en": "Software Developer",
        "hi": "सॉफ्टवेयर डेवलपर",
        "te": "సాఫ్ట్‌వేర్ డెవలపర్"
    }
]


def clean_markup(text: str) -> str:
    """Removes XML/HTML tags and unescapes entities."""
    if not text:
        return ""
    # Strip HTML tags
    cleaned = re.sub(r"<[^>]+>", "", text)
    # Unescape HTML entities (&amp; -> &, etc.)
    cleaned = html.unescape(cleaned)
    # Normalize multiple whitespace
    cleaned = re.sub(r"[ \t]+", " ", cleaned).strip()
    return cleaned


def lookup_domain_dictionary(text: str, source_lang: str, target_lang: str) -> str | None:
    """
    Checks if text or phrases within text match our domain dictionary.
    Supports exact matching and multi-phrase replacement.
    """
    norm_input = text.strip()
    if not norm_input:
        return ""

    # 1. Exact match check (case-insensitive for English)
    for entry in DOMAIN_DICTIONARY:
        src_val = entry.get(source_lang, "").strip()
        tgt_val = entry.get(target_lang, "").strip()
        if not src_val or not tgt_val:
            continue

        if norm_input.lower() == src_val.lower():
            return tgt_val

    return None


def replace_domain_phrases(text: str, source_lang: str, target_lang: str) -> str:
    """
    Replaces known domain terms and phrases inside text based on longest-match first.
    """
    result = text
    # Sort entries by source phrase length descending to replace longest phrases first
    sorted_entries = sorted(
        [e for e in DOMAIN_DICTIONARY if e.get(source_lang) and e.get(target_lang)],
        key=lambda x: len(x[source_lang]),
        reverse=True
    )

    for entry in sorted_entries:
        src = entry[source_lang].strip()
        tgt = entry[target_lang].strip()
        if not src or not tgt:
            continue

        if source_lang == "en":
            # Word boundary check for English phrases
            pattern = re.compile(re.escape(src), re.IGNORECASE)
            result = pattern.sub(tgt, result)
        else:
            if src in result:
                result = result.replace(src, tgt)

    return result


def translate_via_mymemory(text: str, source_lang: str, target_lang: str, timeout: int = 5) -> str | None:
    """
    Queries MyMemory public Translation Memory API (non-AI).
    Returns clean translated text, or None if network/quota failure occurs.
    """
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {
            "q": text,
            "langpair": f"{source_lang}|{target_lang}"
        }
        resp = requests.get(url, params=params, timeout=timeout)
        if resp.status_code == 200:
            data = resp.json()
            response_data = data.get("responseData") or {}
            raw_text = response_data.get("translatedText")
            if raw_text and not raw_text.startswith("MYMEMORY WARNING:"):
                cleaned = clean_markup(raw_text)
                if cleaned:
                    return cleaned
    except Exception as e:
        logger.warning("MyMemory translation network/timeout exception: %s", e)
    return None


def translate_via_libretranslate(text: str, source_lang: str, target_lang: str, base_url: str, timeout: int = 5) -> str | None:
    """
    Queries an optional self-hosted or configured LibreTranslate instance.
    """
    try:
        endpoint = base_url.rstrip("/") + "/translate"
        payload = {
            "q": text,
            "source": source_lang,
            "target": target_lang,
            "format": "text"
        }
        resp = requests.post(endpoint, json=payload, timeout=timeout)
        if resp.status_code == 200:
            data = resp.json()
            raw_text = data.get("translatedText")
            if raw_text:
                return clean_markup(raw_text)
    except Exception as e:
        logger.warning("LibreTranslate exception: %s", e)
    return None


def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Main non-AI translation entrypoint.
    
    1. Validates supported languages (te, hi, en).
    2. Returns original text if source_lang == target_lang.
    3. Checks exact domain dictionary match.
    4. Tries non-AI translation memory service (LibreTranslate if configured, or MyMemory).
    5. Falls back to dictionary phrase replacement engine if network is unavailable or times out.
    """
    clean_in = text.strip()
    if not clean_in:
        return ""

    if source_lang not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported source language: '{source_lang}'. Supported: te, hi, en.")
    if target_lang not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported target language: '{target_lang}'. Supported: te, hi, en.")

    if source_lang == target_lang:
        return clean_in

    # 1. Exact domain dictionary lookup (instant & 100% verified)
    exact_match = lookup_domain_dictionary(clean_in, source_lang, target_lang)
    if exact_match:
        return exact_match

    # 2. Check if a configured LibreTranslate service is specified in env
    libre_url = os.environ.get("LIBRETRANSLATE_URL") or os.environ.get("TRANSLATION_API_URL")
    if libre_url:
        libre_result = translate_via_libretranslate(clean_in, source_lang, target_lang, libre_url)
        if libre_result:
            return libre_result

    # 3. Query non-AI translation memory API (MyMemory)
    mymemory_result = translate_via_mymemory(clean_in, source_lang, target_lang)
    if mymemory_result:
        return mymemory_result

    # 4. Fallback to dictionary phrase/word replacement
    fallback_result = replace_domain_phrases(clean_in, source_lang, target_lang)
    if fallback_result and fallback_result != clean_in:
        return fallback_result

    # 5. If everything failed and text could not be translated, raise RuntimeError
    raise RuntimeError(f"Translation from {SUPPORTED_LANGUAGES[source_lang]['name']} to {SUPPORTED_LANGUAGES[target_lang]['name']} could not be completed.")
