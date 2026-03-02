import os
import json
from openai import OpenAI


def analyze_text(text: str) -> dict:

    if not text.strip():
        return {"error": "Empty transcript"}

    # Load API key at runtime (Render-safe)
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return {"error": "GROQ_API_KEY not set"}

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    prompt = f"""
You are a professional equity research analyst.

STRICT RULES:
- Use ONLY transcript information
- No hallucinations
- If missing → "Not Mentioned"
- Return VALID JSON ONLY

OUTPUT FORMAT:
{{
  "management_tone": "",
  "confidence_level": "",
  "key_positives": [],
  "key_concerns": [],
  "forward_guidance": "",
  "capacity_utilization_trends": "",
  "new_growth_initiatives": []
}}

TRANSCRIPT:
{text[:3000]}
"""

    # ---- CALL GROQ ----
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
    except Exception as e:
        return {"error": "LLM call failed", "details": str(e)}

    # ---- SAFE RESPONSE EXTRACTION ----
    try:
        if not response.choices:
            return {"error": "Empty model response"}

        content = response.choices[0].message.content

        if not content:
            return {"error": "Model returned empty content"}

        raw_output = content.strip()

    except Exception as e:
        return {"error": "Response parsing failed", "details": str(e)}

    # ---- SAFE JSON PARSE ----
    try:
        return json.loads(raw_output)

    except json.JSONDecodeError:
        try:
            start = raw_output.find("{")
            end = raw_output.rfind("}") + 1
            return json.loads(raw_output[start:end])
        except Exception:
            return {
                "warning": "Non-JSON output",
                "raw_response": raw_output
            }