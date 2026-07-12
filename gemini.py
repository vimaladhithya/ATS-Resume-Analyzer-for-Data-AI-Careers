import google.generativeai as genai
import streamlit as st

def gen_ai(resume_text,jd_text,matched_skills,missing_skills,final_score,selected_model):
        model = genai.GenerativeModel(selected_model)
        prompt = f"""
        You are an ATS resume expert.
        Resume:{resume_text}
        Job Description:{jd_text}
        Matched Skills:{matched_skills}
        Missing Skills:{missing_skills}
        Final ATS Score: {final_score}

        Give:
        1. Short feedback
        2. Proficient in the following skills
        3. Improvements
        4. Skill suggestions
        5. Career advice
        """
        response=model.generate_content(prompt)
        return response.text
