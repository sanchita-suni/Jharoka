# scripts/seed_db.py
"""
Seed script to add sample artisan profiles to the database using Samika's add_artisan().
Run:
    python scripts/seed_db.py
Ensure that your Python path includes the project root (or run from repo root).
"""

import sys
import os

# make sure modules package is importable if running from repo root
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

try:
    from modules.database import add_artisan  # Samika's function
except Exception as e:
    print("Could not import modules.database.add_artisan. Is Samika's database module present?")
    print("Error:", e)
    print("Exiting seed script.")
    sys.exit(1)


def make_sample_profiles():
    return [
        {
            "essence": "Hand-thrown terracotta pots crafted using century-old Jaipur techniques.",
            "profile_en": "Suman is a potter from Jaipur who has been shaping clay since childhood. She specializes in hand-thrown terracotta pots with natural dyes.",
            "profile_hi": "सुमन जयपुर की एक कुम्हार हैं जो बचपन से माटी को आकार देती आई हैं। वह प्राकृतिक रंगों से टेराकोटा बर्तन बनाती हैं।",
            "profile_kn": "ಸುಮನ್ ಜೈಪುರ್‌ನ ಒಂದು ಕುಂಬಾರ್ತಿ. ಅವರು ಬಾಲ್ಯದಿಂದಲೇ ಮಣ್ಣನ್ನು ಆಕಾರಗೊಳಿಸುತ್ತಾರೆ ಮತ್ತು ಪ್ರಕೃತಿಕ ರಂಗುಗಳಿಂದ ಟೆರಾಕೊಟಾ ಪಾತ್ರೆಗಳನ್ನು ತಯಾರಿಸುತ್ತಾರೆ.",
            "meta": {"location": "Jaipur", "craft": "pottery", "years_experience": 18},
            "image_urls": [],
        },
        {
            "essence": "Intricate hand-block printed textiles from a family-run workshop in Bagru.",
            "profile_en": "Ravi runs a small family workshop in Bagru producing block-printed scarves and textiles using vegetable dyes.",
            "profile_hi": "रवि बैगरू में एक पारिवारिक कार्यशाला चलाते हैं जो वनस्पति रंगों से ब्लॉक-प्रिंटेड स्कार्फ बनाती है।",
            "profile_kn": "ರವಿ ಬಾಗ್ರುವಿನಲ್ಲಿ ಒಂದು ಕುಟುಂಬ ವರ್ಕ್‌ಶಾಪ್ ನಡೆಸುತ್ತಾರೆ. ಅವರು ಶಾಖಾ-ಭಿತ್ತಿಪಡಿತ ಸರ್ಕಳು ಮತ್ತು ಬಟ್ಟೆಗಳನ್ನು ನೈಸರ್ಗಿಕ ಬಣ್ಣಗಳಿಂದ ಮುದ್ರಣ ಮಾಡುತ್ತಾರೆ.",
            "meta": {"location": "Bagru", "craft": "block printing", "years_experience": 12},
            "image_urls": [],
        },
        {
            "essence": "Brassware maker blending modern forms with lost-wax casting techniques.",
            "profile_en": "Anita uses lost-wax casting to create contemporary brassware inspired by traditional motifs.",
            "profile_hi": "अनीता पारंपरिक रेखांकनों से प्रेरित आधुनिक पीतल के बर्तनों में खोई-मोम ढलाई का उपयोग करती हैं।",
            "profile_kn": "ಅನಿತಾ ಸಂಪ್ರದಾಯಿಕ ಮೊಟಿಫ್ಗಳಿಂದ ಪ್ರೇರಿತ ಆಧುನಿಕ ಬ್ರಾಸ್ವೇರ್ ಅನ್ನು ಲಾಟ್-ವ್ಯಾಕ್ಸ್ ದಾಖಲೆ ಪದ್ದತಿಯೊಂದಿಗೆ ರಚಿಸುತ್ತಾರೆ.",
            "meta": {"location": "Moradabad", "craft": "brassware", "years_experience": 20},
            "image_urls": [],
        },
    ]


def seed():
    profiles = make_sample_profiles()
    for p in profiles:
        pdata = {
            "essence": p["essence"],
            "profile_en": p["profile_en"],
            "profile_hi": p["profile_hi"],
            "profile_kn": p["profile_kn"],
            "meta": p["meta"],
        }
        image_urls = p.get("image_urls", [])
        print("Adding artisan:", pdata["meta"].get("location"), "-", pdata["essence"][:60])
        try:
            add_artisan(pdata, image_urls)
            print(" -> added successfully.")
        except Exception as e:
            print(" -> add_artisan raised exception:", e)
            print("Make sure the database server is running and modules.database.add_artisan signature is correct.")
    print("Seeding complete.")


if __name__ == "__main__":
    seed()
