def final_score_job_description(ats_score,similarity_score):
    final_score=(ats_score*0.6)+(similarity_score*0.4)
    if final_score>=80:
        verdict="Strong Match"
    elif final_score>=60:
        verdict="Moderate Match"
    else:
        verdict="Weak Match"
    return round(final_score,2),verdict

def final_score_skill_requirements(ats_score):
    final_score=ats_score
    if final_score>=80:
        verdict="Strong Match"
    elif final_score>=60:
        verdict="Moderate Match"
    else:
        verdict="Weak Match"
    return round(final_score,2),verdict