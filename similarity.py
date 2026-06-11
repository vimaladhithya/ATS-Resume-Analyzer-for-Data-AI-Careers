from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model=SentenceTransformer("all-MiniLM-L6-v2")

def similarity_score(resume_text,jd_text):
    embeddings=model.encode([resume_text,jd_text])
    similarity=cosine_similarity([embeddings[0]],[embeddings[1]])[0][0]
    result=round(similarity*100,2)
    return result   