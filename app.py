import streamlit as st

from ai_service import generate_questions


st.set_page_config(
    page_title="AI Interview Question & Answer Generator",
    page_icon="🎯",
    layout="centered",
)


def main() -> None:
    st.title("AI Interview Question & Answer Generator")
    st.write(
        "Generate role-specific interview questions and answers using AI."
    )

    with st.form("question_generator_form"):
        job_role = st.text_input("Job Role", placeholder="e.g. Python Developer")
        experience_level = st.selectbox(
            "Experience Level",
            ["Fresher", "1-2 years", "3-5 years"],
        )
        skills = st.text_input(
            "Skills",
            placeholder="e.g. Python, Django, REST API, SQL",
        )
        submitted = st.form_submit_button("Generate Questions")

    if not submitted:
        return

    if not job_role.strip() or not skills.strip():
        st.warning("Please enter both Job Role and Skills.")
        return

    with st.spinner("Generating interview questions and answers..."):
        try:
            results = generate_questions(
                job_role=job_role.strip(),
                experience=experience_level,
                skills=skills.strip(),
            )
        except ValueError as exc:
            st.error(str(exc))
            return
        except Exception as exc:
            st.error(f"Something went wrong while generating content: {exc}")
            return

    st.subheader("Generated Interview Questions & Answers")

    for index, item in enumerate(results, start=1):
        st.markdown(f"### Question {index}")
        st.write(item["question"])
        st.markdown("**Answer**")
        st.write(item["answer"])


if __name__ == "__main__":
    main()
