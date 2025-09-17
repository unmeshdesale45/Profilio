from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import preprocess_text

def calculate_similarity(resume_text, job_description_text):
    """
    Calculates the cosine similarity between a resume and a job description.
    Returns a similarity score as a percentage.
    """
    # Preprocess both texts
    cleaned_resume = preprocess_text(resume_text)
    cleaned_jd = preprocess_text(job_description_text)

    # Create a corpus of the two documents
    corpus = [cleaned_resume, cleaned_jd]

    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()

    # Generate TF-IDF matrix
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Calculate cosine similarity
    # The result is a 2x2 matrix, similarity is at [0, 1]
    similarity_matrix = cosine_similarity(tfidf_matrix)
    similarity_score = similarity_matrix[0, 1]

    # Return as a percentage
    return similarity_score * 100