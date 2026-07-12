import google.generativeai as genai

def improve_resume(resume_text,jd_text,selected_model):
        model = genai.GenerativeModel(selected_model)
        prompt = f"""
        You are an ATS resume expert.

        Resume:{resume_text}
        Job Description:{jd_text}

        Tasks:
        1. Rewrite the resume to improve ATS compatibility.
        2. Keep all truthful information.
        3. Add missing relevant keywords from the job description where appropriate.
        4. Use ATS-friendly section headings.
        5. Improve bullet points with action verbs.
        6. Return the complete optimized resume.
        """
        response=model.generate_content(prompt)
        return response.text
