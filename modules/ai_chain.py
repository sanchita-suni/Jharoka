# modules/ai_chain.py
"""
Samhitha's Gemini content generation module for Google Cloud Vertex AI.
This version directly uses Vertex AI SDK instead of generic REST calls.
"""

import json
import logging
import re
from typing import Dict, Any, Optional

import vertexai
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Vertex AI (auto-picks up creds on Cloud Run or gcloud locally)
vertexai.init()  # You can pass project=..., location=... if needed


def _find_first_json(text: str) -> Optional[str]:
    """Extract the first JSON object from a string (brace-matching)."""
    start = None
    brace_count = 0
    for i, ch in enumerate(text):
        if ch == "{":
            if start is None:
                start = i
            brace_count += 1
        elif ch == "}":
            brace_count -= 1
            if start is not None and brace_count == 0:
                return text[start : i + 1]
    return None


def _safe_parse_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """Try to extract and parse JSON from text output."""
    candidate = _find_first_json(text)
    if not candidate:
        return None
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        fixed = re.sub(r",\s*}", "}", candidate)
        fixed = re.sub(r",\s*]", "]", fixed)
        try:
            return json.loads(fixed)
        except Exception:
            return None


def generate_artisan_content(image: bytes, text: str) -> Dict[str, Any]:
    """
    Calls Vertex AI Gemini 1.5 Pro to generate artisan content.

    Returns dict:
      {
        "essence": str,
        "profile_en": str,
        "profile_hi": str,
        "profile_kn": str,
        "image_prompts": list[str]
      }
    """

    # Encode image
    image_part = Part.from_data(mime_type="image/jpeg", data=image)

    # Build prompt
    user_prompt = f"""
You are a content-generation assistant for an Artisan marketplace app.

You will be given:
- An image of the artisan or their product.
- A short descriptive text.

Task:
Produce a single JSON object with the following keys:
- essence: short 1-2 sentence summary.
- profile_en: English profile.
- profile_hi: Hindi translation.
- profile_kn: Kannada translation.
- image_prompts: list of 3-6 text prompts for mockup generation.

Constraints:
- Return ONLY valid JSON (no explanation).
"""

    model = GenerativeModel("gemini-1.5-pro")

    response = model.generate_content(
        [user_prompt, image_part, text],
        generation_config=GenerationConfig(
            max_output_tokens=800,
            temperature=0.3,
        ),
    )

    text_output = response.text.strip()
    parsed = _safe_parse_json_from_text(text_output)

    if parsed:
        return {
            "essence": parsed.get("essence", ""),
            "profile_en": parsed.get("profile_en", ""),
            "profile_hi": parsed.get("profile_hi", ""),
            "profile_kn": parsed.get("profile_kn", ""),
            "image_prompts": parsed.get("image_prompts", []) or [],
            "_raw_model_response": text_output,
        }
    else:
        logger.warning("Gemini did not return JSON, fallback returning raw text.")
        return {
            "essence": "",
            "profile_en": text_output[:200],
            "profile_hi": "",
            "profile_kn": "",
            "image_prompts": [],
            "_raw_model_response": text_output,
        }
