INTERVIEW_PROMPT_TEMPLATE = """
You are an experienced technical interviewer.

Generate exactly 5 interview questions with detailed answers.

Role: {job_role}
Experience Level: {experience}
Skills: {skills}

Rules:
- Questions must be relevant to the role, skills, and experience level.
- Mix conceptual and practical questions.
- Provide clear, concise, and technically correct answers.
- Keep the difficulty suitable for the experience level.
- Return the result as valid JSON only.
- Return a JSON object with an `items` array that contains exactly 5 objects.
- Use this exact JSON schema:
{{
  "items": [
    {{
      "question": "Question text",
      "answer": "Detailed answer text"
    }}
  ]
}}
"""
