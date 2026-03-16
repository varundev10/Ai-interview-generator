# AI Interview Question & Answer Generator

A Streamlit web app that generates interview questions and answers based on a job role, experience level, and skills using the Groq API.

## Features

- Enter a job role
- Choose an experience level
- Add relevant skills
- Generate 5 interview questions with answers

## Project Structure

```text
ai-interview-generator/
├── app.py
├── ai_service.py
├── prompt_template.py
├── requirements.txt
├── .env
└── README.md
```

## Installation

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Setup

Open `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

For Streamlit Community Cloud, add the same key in your app `Secrets`:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

## Run the App

```bash
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this project to GitHub.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click `New app`.
4. Select your GitHub repository and choose `app.py` as the main file.
5. Open the app settings and add this secret:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

6. Deploy the app.

## How It Works

- `app.py` handles the Streamlit user interface.
- `ai_service.py` sends the prompt to Groq, reading the API key from Streamlit secrets or local `.env`.
- `prompt_template.py` stores the interviewer-style prompt template.

## Notes

- The app expects the model to return JSON with 5 question-answer pairs.
- If the API key is missing or invalid, the app will show an error message.
- The app uses Groq's OpenAI-compatible endpoint: `https://api.groq.com/openai/v1`
