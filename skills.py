import pandas as pd
import re

skills_db = pd.read_csv(r"data\skills.csv")

def extract_skills(text):
    if isinstance(text, list):
        text = " ".join(text)

    text = text.lower()
    matched_skill = []

    for skill in skills_db["skill"]:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            matched_skill.append(skill)

    return list(set(matched_skill))