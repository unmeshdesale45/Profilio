import streamlit as st
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer

# Import your existing utility and matcher functions
from utils import extract_text_from_pdf, extract_text_from_docx
from matcher import calculate_similarity

# --- NEW HELPER FUNCTIONS for Side-by-Side View ---

def get_common_keywords(job_desc_text, resume_text):
    """
    Finds common keywords between two texts using TF-IDF.
    Returns a set of common words.
    """
    vectorizer = TfidfVectorizer(stop_words='english')
    # Create a corpus and fit the vectorizer
    corpus = [job_desc_text, resume_text]
    vectorizer.fit(corpus)
    # Get the feature names (vocabulary) for each document
    feature_names = vectorizer.get_feature_names_out()
    
    # Get the TF-IDF vectors for both texts
    vec1 = vectorizer.transform([job_desc_text]).toarray()
    vec2 = vectorizer.transform([resume_text]).toarray()
    
    # Find indices where both vectors have a non-zero value
    common_indices = (vec1 > 0) & (vec2 > 0)
    
    # Get the actual words using the common indices
    common_words = feature_names[common_indices[0]]
    
    return set(common_words)


def highlight_text(text, keywords):
    """
    Highlights a set of keywords in a given text using Streamlit's markdown.
    Returns the highlighted text as an HTML string.
    """
    for keyword in keywords:
        # Use regex for case-insensitive replacement and to avoid highlighting parts of words
        text = re.sub(r'\b({})\b'.format(re.escape(keyword)), r'<mark>\1</mark>', text, flags=re.IGNORECASE)
    return text

# --- Streamlit App Interface ---

st.set_page_config(page_title="Profilio", layout="wide", page_icon="🤖")

st.title("🤖  Profilio")
st.markdown("""
This advanced tool allows you to upload multiple resumes and rank them against a single job description. 
You can then select a candidate for a detailed side-by-side comparison with highlighted keywords.
""")
st.divider()

# --- Main App Logic ---

# Use session state to store results across reruns
if 'results_df' not in st.session_state:
    st.session_state.results_df = None

# Input fields in the sidebar for better layout
with st.sidebar:
    st.header("1. Enter Job Description")
    job_description = st.text_area("Paste the job description here", height=250)
    
    st.header("2. Upload Resumes")
    # MODIFIED: File uploader now accepts multiple files
    uploaded_resumes = st.file_uploader("Upload resumes (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files=True)
    
    analyze_button = st.button("Analyze Resumes", type="primary")

if analyze_button and job_description and uploaded_resumes:
    with st.spinner("Analyzing all resumes... This may take a moment."):
        results = []
        for resume_file in uploaded_resumes:
            resume_text = ""
            try:
                if resume_file.type == "application/pdf":
                    resume_text = extract_text_from_pdf(resume_file)
                else:
                    resume_text = extract_text_from_docx(resume_file)
                
                similarity_score = calculate_similarity(resume_text, job_description)
                
                results.append({
                    "Filename": resume_file.name,
                    "Score (%)": f"{similarity_score:.2f}",
                    "Full Resume Text": resume_text  # Store full text for later
                })
            except Exception as e:
                st.error(f"Error processing {resume_file.name}: {e}")
        
        # Convert results to a DataFrame and sort
        results_df = pd.DataFrame(results)
        results_df['Score (%)'] = pd.to_numeric(results_df['Score (%)'])
        results_df = results_df.sort_values(by="Score (%)", ascending=False).reset_index(drop=True)
        
        # Store the DataFrame in session state
        st.session_state.results_df = results_df

# --- Display Results and Comparison View ---

if st.session_state.results_df is not None:
    st.header("📈 Analysis Results")
    st.markdown("Here are the resumes ranked by their match score.")
    
    # Display the ranked list, hiding the full text column for a cleaner view
    st.dataframe(
        st.session_state.results_df[['Filename', 'Score (%)']],
        use_container_width=True,
        hide_index=True
    )
    
    st.divider()
    
    st.header("🔍 Side-by-Side Comparison")
    
    # Dropdown to select a candidate from the ranked list
    candidate_options = st.session_state.results_df['Filename'].tolist()
    selected_candidate = st.selectbox("Choose a candidate to compare:", options=candidate_options)
    
    if selected_candidate:
        # Get the resume text for the selected candidate
        resume_text = st.session_state.results_df[st.session_state.results_df['Filename'] == selected_candidate].iloc[0]['Full Resume Text']
        
        # Find and highlight common keywords
        common_keywords = get_common_keywords(job_description, resume_text)
        highlighted_jd = highlight_text(job_description, common_keywords)
        highlighted_resume = highlight_text(resume_text, common_keywords)
        
        # Create the two-column layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Job Description")
            # Use markdown with unsafe_allow_html to render the highlights
            st.markdown(f'<div style="height: 500px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px; border-radius: 5px;">{highlighted_jd}</div>', unsafe_allow_html=True)

        with col2:
            st.subheader(f"Resume: {selected_candidate}")
            st.markdown(f'<div style="height: 500px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px; border-radius: 5px;">{highlighted_resume}</div>', unsafe_allow_html=True)
else:
    st.info("Please provide a job description and upload resumes in the sidebar to begin analysis.")