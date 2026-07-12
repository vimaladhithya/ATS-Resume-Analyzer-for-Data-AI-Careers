import streamlit as st
import nltk_setup
from ats_score import ats_score
from similarity import similarity_score
from extract_text import extract_text_pdf
from preprocess import preprocess_text
from skills import extract_skills
from gemini import gen_ai
from final_score import final_score_skill_requirements
from final_score import final_score_job_description
from optimize_resume_gemini import improve_resume
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import google.generativeai as genai



if "optimized_resume" not in st.session_state:
    st.session_state.optimized_resume = ""

if "analyzed" not in st.session_state:
    st.session_state.analyzed=False

if "resume_text" not in st.session_state:
    st.session_state.resume_text=""

if "jd_text" not in st.session_state:
    st.session_state.jd_text=""

if "skill_score" not in st.session_state:
    st.session_state.skill_score = 0.0

if "similarity_score_sentence" not in st.session_state:
    st.session_state.similarity_score_sentence = 0.0

if "final_score" not in st.session_state:
    st.session_state.final_score = 0.0

if "verdict" not in st.session_state:
    st.session_state.verdict = ""

if "matched" not in st.session_state:
    st.session_state.matched = []

if "missing" not in st.session_state:
    st.session_state.missing = []

if "ai_feedback" not in st.session_state:
    st.session_state.ai_feedback = ""

if "jd_skills" not in st.session_state:
    st.session_state.jd_skills = ""

st.set_page_config(
    page_title="ATS AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("AI-Powered ATS Resume Analyzer and Optimizer for Data & AI Careers")
st.markdown("Upload Resume + Job Description to get ATS Score, Similarity & AI Feedback")

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

option = st.radio(
    "Choose Input Method",
    ["Job Description", "Skill Requirements"]
)


jd_text = ""
jd_skills=""

if option == "Job Description":
    jd_text = st.text_area("Paste Job Description")
else:
    manual_skills = st.text_input("Enter Skill Requirements (comma separated)", "")
    jd_skills= [s.strip().lower() for s in manual_skills.split(",")]
    jd_skills = ", ".join(jd_skills) 

api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
models = [model.name for model in genai.list_models()]

selected_model_temp = st.selectbox("Select Gemini Model",models)
selected_model=selected_model_temp.split("/")[1]


if st.button("Analyze Resume"):

    if resume_file is None:
        st.error("Please upload resume  and enter job description")
        st.stop()

    if option == "Job Description" and not jd_text:
        st.error("Please enter a Job Description")
        st.stop()

    if option == "Skill Requirements" and not manual_skills:
        st.error("Please enter Skill Requirements")
        st.stop()

    
    resume_text = extract_text_pdf(resume_file)
    resume_text_clean = preprocess_text(resume_text)
    resume_skills_list = extract_skills(resume_text_clean)

    if jd_text:
        jd_text_clean = preprocess_text(jd_text)
        jd_skills_list = extract_skills(jd_text_clean)
    else:
        jd_text_clean=preprocess_text(jd_skills)
        jd_skills_list = extract_skills(jd_text_clean)


    skill_score, matched, missing = ats_score(resume_skills_list, jd_skills_list) #returns list
    similarity_score_sentence = similarity_score(
        resume_text_clean,
        jd_text_clean
    )

    if jd_text:
        score, verdict = final_score_job_description(skill_score,similarity_score_sentence)
    else:
        score, verdict = final_score_skill_requirements(skill_score)

    if jd_text:
        ai_feedback = gen_ai(
            resume_text,
            jd_text,
            matched,
            missing,
            score,
            selected_model
        )
    else:
        ai_feedback = gen_ai(
            resume_text,
            jd_skills,
            matched,
            missing,
            score,
            selected_model
        )

    st.session_state.analyzed=True
    st.session_state.resume_text=resume_text
    st.session_state.jd_text=jd_text
    st.session_state.jd_skills = jd_skills
    st.session_state.matched=matched
    st.session_state.missing=missing
    st.session_state.ai_feedback=ai_feedback
    st.session_state.skill_score=skill_score
    st.session_state.similarity_score_sentence=similarity_score_sentence
    st.session_state.final_score=score
    st.session_state.verdict=verdict

if st.session_state.analyzed==True:

    st.subheader("ATS RESULTS")

    if jd_text:
        col1, col2, col3, col4 = st.columns(4)    

        with col1:
            st.metric("Skill Score", f"{st.session_state.skill_score:.2f}")

        with col2:
            st.metric("Similarity Score", f"{st.session_state.similarity_score_sentence:.2f}")

        with col3:
            st.metric("Final ATS Score", f"{st.session_state.final_score:.2f}")

        with col4:
            st.metric("Overall:",st.session_state.verdict)
    else:
        col11,col21=st.columns(2)
        with col11:
            st.metric("ATS Score", f"{st.session_state.final_score:.2f}")

        with col21:
            st.metric("Overall:",st.session_state.verdict)

    st.subheader("Matched Skills")
    st.write(st.session_state.matched)

    st.subheader("Missing Skills")
    st.write(st.session_state.missing)

    st.subheader("AI Feedback (Gemini)")
    st.write(st.session_state.ai_feedback)

    if st.button("Make ATS Friendly Resume"):
        if st.session_state.jd_text:
            st.session_state.optimized_resume = improve_resume(
                st.session_state.resume_text,
                st.session_state.jd_text,
                selected_model
            )
        else:
            st.session_state.optimized_resume = improve_resume(
                st.session_state.resume_text,
                st.session_state.jd_skills,
                selected_model
            )

       
if st.session_state.optimized_resume:

    st.text_area(
        "ATS Optimized Resume",
        st.session_state.optimized_resume,
        height=1000
    )

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()
    style = styles["Normal"]

    content = [] # [()
                  # ()]

    
    for line in st.session_state.optimized_resume.split("\n"):
        content.append(Paragraph(line, style))
        content.append(Spacer(1, 5))


    doc.build(content)

    buffer.seek(0)

    st.download_button(
        label="Download ATS Resume",
        data=buffer,
        file_name="ATS_Optimized_Resume.pdf",
        mime="application/pdf"
    )