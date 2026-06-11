def ats_score(resume_skill,jd_skill): # prameters in list

    resume_skill = [skill.lower().strip() for skill in resume_skill]
    jd_skill = [skill.lower().strip() for skill in jd_skill]
    matched=list(set(resume_skill)&set(jd_skill))
    missed=list(set(jd_skill)-set(resume_skill))
    

    if len(jd_skill)==0:
        score=0
    else:
        score=(len(matched)/len(jd_skill))*100
    return score,matched,missed