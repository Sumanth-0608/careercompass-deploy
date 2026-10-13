import os
import json

seeds_file = "database_seeds.py"
with open(seeds_file, "r", encoding="utf-8") as f:
    content = f.read()

from expand_seeds import EXPANDED_CAREERS
from test_appointments_seed import INITIAL_APPOINTMENT_PROVIDERS, INITIAL_APPOINTMENT_TYPES

# 1. Format EXPANDED_CAREERS as python code text
import pprint

# Generate code for additional careers
import io

def format_career_dict(c):
    lines = ["    {"]
    for k, v in c.items():
        if isinstance(v, str) and (v.startswith("[") or v.startswith("{")) and k != "slug" and k != "title" and k != "category" and k != "short_description" and k != "educational_requirements" and k != "min_education_level" and k != "cost_category" and k != "cost_estimate_detail" and k != "low_cost_routes" and k != "geographic_considerations" and k != "last_verified":
            # json string
            lines.append(f'        "{k}": json.dumps(' + pprint.pformat(json.loads(v), indent=12, width=120) + '),')
        else:
            lines.append(f'        "{k}": ' + pprint.pformat(v, indent=8, width=120) + ',')
    lines.append("    },")
    return "\n".join(lines)

expanded_code = "\n".join([format_career_dict(c) for c in EXPANDED_CAREERS])

# Insert before `]\n\n# ============================================================================\n# Curated & Verified Opportunities`
target_marker = "]\n\n# ============================================================================\n# Curated & Verified Opportunities Seed Data"

if target_marker not in content:
    raise ValueError(f"Target marker not found in {seeds_file}")

replacement = ",\n" + expanded_code + "\n" + target_marker
new_content = content.replace(target_marker, replacement, 1)

# Now append appointment providers, types, and slot generator at the bottom
appointments_code = '''

# ============================================================================
# Real-Time Appointment Booking System Seed Data
# ============================================================================

from datetime import datetime, timedelta

INITIAL_APPOINTMENT_PROVIDERS = ''' + pprint.pformat(INITIAL_APPOINTMENT_PROVIDERS, indent=4, width=120) + '''

INITIAL_APPOINTMENT_TYPES = ''' + pprint.pformat(INITIAL_APPOINTMENT_TYPES, indent=4, width=120) + '''

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
'''

new_content += appointments_code

with open(seeds_file, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Successfully applied seeds to database_seeds.py!")
