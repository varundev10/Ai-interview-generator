import json
import os
from typing import List, Dict

from dotenv import load_dotenv
from openai import OpenAI

from prompt_template import INTERVIEW_PROMPT_TEMPLATE


load_dotenv()


def _build_prompt(job_role: str, experience: str, skills: str) -> str:
    return INTERVIEW_PROMPT_TEMPLATE.format(
        job_role=job_role,
        experience=experience,
        skills=skills,
    )


def _extract_json_payload(text: str) -> List[Dict[str, str]]:
    cleaned = text.strip()

    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()

    start = cleaned.find("[")
    end = cleaned.rfind("]")

    if start == -1 or end == -1:
        raise ValueError("The model response did not contain a valid JSON array.")

    payload = cleaned[start : end + 1]
    data = json.loads(payload)

    if not isinstance(data, list) or not data:
        raise ValueError("The model returned an empty or invalid result.")

    formatted = []
    for item in data[:5]:
        question = str(item.get("question", "")).strip()
        answer = str(item.get("answer", "")).strip()
        if question and answer:
            formatted.append({"question": question, "answer": answer})

    if len(formatted) < 5:
        raise ValueError("The model response did not include 5 usable questions.")

    return formatted


def generate_questions(job_role: str, experience: str, skills: str) -> List[Dict[str, str]]:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "Missing GROQ_API_KEY. Add it to your .env file before running the app."
        )
    if not api_key.startswith("gsk_"):
        raise ValueError(
            "Invalid GROQ_API_KEY format. Please use a Groq key that starts with 'gsk_'."
        )

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )
    prompt = _build_prompt(job_role, experience, skills)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.4,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an experienced technical interviewer. "
                    "Return only valid JSON."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )
    text = response.choices[0].message.content.strip()

    if not text:
        raise ValueError("The API returned an empty response.")

    data = json.loads(text)
    if isinstance(data, dict) and "items" in data and isinstance(data["items"], list):
        data = data["items"]
    elif isinstance(data, dict):
        data = [data]

    return _extract_json_payload(json.dumps(data))
