import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

from prompts import SYSTEM_PROMPT

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT,
)


def get_test_type(item):
    keys = " ".join(item.get("keys", [])).lower()

    if "personality" in keys:
        return "P"

    if "ability" in keys or "aptitude" in keys:
        return "A"

    if "knowledge" in keys:
        return "K"

    if "assessment exercises" in keys or "simulation" in keys:
        return "S"

    return "C"


def generate_reply(messages, retrieved_items):

    conversation = ""

    for msg in messages:
        conversation += f"{msg.role.upper()}: {msg.content}\n"

    catalog = []

    for item in retrieved_items:

        catalog.append({
            "name": item["name"],
            "url": item["url"],
            "description": item.get("description", ""),
            "test_type": get_test_type(item)
        })

    prompt = f"""
Conversation:

{conversation}

Available SHL assessments:

{json.dumps(catalog, indent=2)}

You are selecting SHL Individual Test Solutions.

Return ONLY valid JSON.

Schema:

{{
  "reply": "...",
  "recommendations": [
    {{
      "name": "...",
      "url": "...",
      "test_type": "..."
    }}
  ],
  "end_of_conversation": false
}}

IMPORTANT DECISION RULES

A request is VAGUE only if BOTH are missing:
- job role OR job description
- skills/competencies to assess

If the user has already provided ANY of these:
- job role
- job description
- seniority
- years of experience
- required skills
- competencies

THEN YOU ALREADY HAVE ENOUGH INFORMATION.

DO NOT ask more questions.

Recommend assessments immediately.

Recommendation rules

1. Recommend between 1 and 10 assessments.

2. Use ONLY assessments from Available SHL assessments.

3. Never invent assessment names.

4. Never invent URLs.

5. Copy names and URLs exactly.

6. If the user changes requirements,
update the recommendations.

7. If the user asks to compare two assessments,
compare ONLY using the provided assessment descriptions.

8. If the request is unrelated to SHL assessments,
politely refuse and return:

{{
  "reply":"...",
  "recommendations":[],
  "end_of_conversation":true
}}

9. If clarification is required:

{{
  "reply":"...",
  "recommendations":[],
  "end_of_conversation":false
}}

10. If recommendations are returned:

- Include between 1 and 10 assessments.
- Set end_of_conversation=true.

Return ONLY JSON.
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    elif text.startswith("```"):
        text = text.replace("```", "").strip()

    return json.loads(text)