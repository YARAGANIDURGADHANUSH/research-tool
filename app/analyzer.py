import os
import json
from openai import OpenAI

# -------------------------------------------------
# Validate API Key
# -------------------------------------------------
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY environment variable not set")

# Groq OpenAI-compatible client
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


def analyze_text(text: str) -> dict:

    if not text.strip():
        return {"error": "Empty transcript"}

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
{text[:12000]}
"""

    # -------------------------------------------------
    # CALL GROQ SAFELY
    # -------------------------------------------------
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

    except Exception as e:
        return {
            "error": "LLM call failed",
            "details": str(e)
        }

    # -------------------------------------------------
    # SAFE RESPONSE EXTRACTION
    # -------------------------------------------------
    try:
        if not response or not response.choices:
            return {"error": "Empty response from Groq"}

        message = response.choices[0].message

        if not message or not message.content:
            return {"error": "No content returned by model"}

        raw_output = message.content.strip()

    except Exception as e:
        return {
            "error": "Failed to read model response",
            "details": str(e)
        }

    # -------------------------------------------------
    # SAFE JSON PARSING
    # -------------------------------------------------
    try:
        return json.loads(raw_output)

    except json.JSONDecodeError:
        # Try extracting JSON block
        try:
            start = raw_output.find("{")
            end = raw_output.rfind("}") + 1

            if start != -1 and end != -1:
                return json.loads(raw_output[start:end])

        except Exception:
            pass

        return {
            "warning": "Model returned non-JSON output",
            "raw_response": raw_output
        }