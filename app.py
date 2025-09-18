import streamlit as st
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk

# --- NLTK Data Download ---
# Simplified download function for Streamlit Cloud
def download_nltk_data():
    """
    Directly downloads the necessary NLTK data. This is the most reliable
    method for resolving persistent errors on Streamlit Cloud.
    """
    try:
        nltk.data.find('tokenizers/punkt')
    except (OSError, LookupError):
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/stopwords')
    except (OSError, LookupError):
        nltk.download('stopwords')

# Run the download function at the start of the script
download_nltk_data()


# Import utility and matcher functions from other project files
from utils import extract_text_from_pdf, extract_text_from_docx, extract_email_from_text, send_invitation_email
from matcher import calculate_similarity


# --- HELPER FUNCTIONS for Side-by-Side View ---

def get_common_keywords(job_desc_text, resume_text):
    """
    Finds common keywords between two texts using TF-IDF.
    Returns a set of common words.
    """
    vectorizer = TfidfVectorizer(stop_words='english')
    corpus = [job_desc_text, resume_text]
    vectorizer.fit(corpus)
    feature_names = vectorizer.get_feature_names_out()
    
    vec1 = vectorizer.transform([job_desc_text]).toarray()
    vec2 = vectorizer.transform([resume_text]).toarray()
    
    common_indices = (vec1 > 0) & (vec2 > 0)
    common_words = feature_names[common_indices[0]]
    
    return set(common_words)


def highlight_text(text, keywords):
    """
    Highlights a set of keywords in a given text using Streamlit's markdown.
    Returns the highlighted text as an HTML string.
    """
    for keyword in keywords:
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
    uploaded_resumes = st.file_uploader("Upload resumes (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files=True)
    
    analyze_button = st.button("Analyze Resumes", type="primary")
    st.divider()
    st.markdown(
        '<h6>Made with &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp by <a href="https://github.com/unmeshdesale45">unmeshdesale45</a></h6>',
        unsafe_allow_html=True,
    )

# --- Analysis loop to process resumes ---
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
                email = extract_email_from_text(resume_text)
                
                results.append({
                    "Filename": resume_file.name,
                    "Score (%)": f"{similarity_score:.2f}",
                    "Email": email,
                    "Full Resume Text": resume_text
                })
            except Exception as e:
                st.error(f"Error processing {resume_file.name}: {e}")
        
        results_df = pd.DataFrame(results)
        results_df['Score (%)'] = pd.to_numeric(results_df['Score (%)'])
        results_df = results_df.sort_values(by="Score (%)", ascending=False).reset_index(drop=True)
        
        st.session_state.results_df = results_df

# --- Display Results and Features ---
if st.session_state.results_df is not None:
    st.header("📈 Analysis Results")
    st.markdown("Here are the resumes ranked by their match score.")
    
    st.dataframe(
        st.session_state.results_df[['Filename', 'Score (%)', 'Email']],
        use_container_width=True,
        hide_index=True
    )
    
    st.divider()
    
    st.header("🔍 Side-by-Side Comparison")
    
    candidate_options = st.session_state.results_df['Filename'].tolist()
    selected_candidate = st.selectbox("Choose a candidate to compare:", options=candidate_options)
    
    if selected_candidate:
        resume_text = st.session_state.results_df[st.session_state.results_df['Filename'] == selected_candidate].iloc[0]['Full Resume Text']
        common_keywords = get_common_keywords(job_description, resume_text)
        highlighted_jd = highlight_text(job_description, common_keywords)
        highlighted_resume = highlight_text(resume_text, common_keywords)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Job Description")
            st.markdown(f'<div style="height: 500px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px; border-radius: 5px;">{highlighted_jd}</div>', unsafe_allow_html=True)
        with col2:
            st.subheader(f"Resume: {selected_candidate}")
            st.markdown(f'<div style="height: 500px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px; border-radius: 5px;">{highlighted_resume}</div>', unsafe_allow_html=True)

    st.divider()

    st.header("📧 Send Interview Invitations")
    st.markdown("Select qualified candidates (score > 50%) to send an invitation.")

    qualified_candidates = st.session_state.results_df[st.session_state.results_df['Score (%)'] > 50]

    if not qualified_candidates.empty:
        candidate_email_options = qualified_candidates.set_index('Filename')['Email'].to_dict()
        
        selected_filename_for_email = st.selectbox(
            "Choose a candidate to email:",
            options=candidate_email_options.keys()
        )
        
        if st.button("Send Invitation Email", type="primary"):
            recipient_email = candidate_email_options.get(selected_filename_for_email)
            if recipient_email:
                with st.spinner(f"Sending email to {selected_filename_for_email}..."):
                    candidate_name = selected_filename_for_email.split('.')[0].replace('_', ' ').title()
                    job_title = "Data Scientist" # This can be made dynamic in a future version
                    
                    if send_invitation_email(recipient_email, candidate_name, job_title):
                        st.success(f"✅ Invitation successfully sent to {recipient_email}!")
            else:
                st.error(f"❌ Could not find an email address in the resume for {selected_filename_for_email}.")
    else:
        st.info("No candidates scored above 50% to send an invitation.")

else:
    st.info("Please provide a job description and upload resumes in the sidebar to begin analysis.")

