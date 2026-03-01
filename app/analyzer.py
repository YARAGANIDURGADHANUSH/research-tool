import os
import json
from openai import OpenAI

# Groq uses OpenAI-compatible SDK
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
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

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        raw_output = response.choices[0].message.content

    except Exception as e:
        return {
            "error": "LLM call failed",
            "details": str(e)
        }

    # Ensure valid JSON
    try:
        return json.loads(raw_output)
    except:
        try:
            start = raw_output.find("{")
            end = raw_output.rfind("}") + 1
            return json.loads(raw_output[start:end])
        except:
            return {
                "error": "Invalid JSON output",
                "raw_response": raw_output
            }