# app/analyzer.py

import ollama
import json


def analyze_text(text: str):
    """
    Earnings Call / Management Commentary Research Tool

    Input:
        Extracted transcript text

    Output:
        Structured analyst-ready JSON
    """

    prompt = f"""
You are a professional equity research analyst.

Analyze the following earnings call transcript.

========================
STRICT RULES
========================
- Use ONLY information present in transcript.
- DO NOT hallucinate or assume data.
- If information is missing, return "Not Mentioned".
- Keep responses concise and analyst-style.
- Output MUST be valid JSON only.
- No explanations outside JSON.

========================
OUTPUT FORMAT (STRICT)
========================
{{
  "management_tone": "",
  "confidence_level": "",
  "key_positives": [],
  "key_concerns": [],
  "forward_guidance": "",
  "capacity_utilization_trends": "",
  "new_growth_initiatives": []
}}

========================
TRANSCRIPT
========================
{text}
"""

    # Call local Ollama model
    response = ollama.chat(
        model="gemma3:4b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw_output = response["message"]["content"]

    # -----------------------------
    # Ensure valid JSON output
    # (important for assignment)
    # -----------------------------
    try:
        parsed = json.loads(raw_output)
        return parsed
    except json.JSONDecodeError:
        # fallback if model adds extra text
        return {
            "error": "Model returned non-JSON output",
            "raw_response": raw_output
        }