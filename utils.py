import re
import nltk
import os
import PyPDF2
import docx
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import streamlit as st
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# --- NLTK Data Path Configuration ---
# Add the local nltk_data directory to NLTK's search path.
# This is the definitive fix for the deployment error.
nltk_data_path = os.path.join(os.getcwd(), "nltk_data")
if nltk_data_path not in nltk.data.path:
    nltk.data.path.append(nltk_data_path)


# --- TEXT EXTRACTION FUNCTIONS ---

def extract_text_from_pdf(file):
    """Extracts text from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    """Extracts text from a DOCX file."""
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def preprocess_text(text):
    """Cleans and preprocesses text for NLP analysis."""
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation and special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    # Join tokens back into a string
    return " ".join(filtered_tokens)


# --- EMAIL RELATED FUNCTIONS ---

def extract_email_from_text(text):
    """
    Finds the first email address in a block of text using regex.
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    if match:
        return match.group(0)
    return None

def send_invitation_email(recipient_email, candidate_name, job_title):
    """
    Sends a personalized interview invitation email using SendGrid.
    """
    # Load credentials securely from st.secrets
    try:
        api_key = st.secrets["SENDGRID_API_KEY"]
        sender_email = st.secrets["SENDER_EMAIL"]
    except KeyError:
        st.error("Email credentials are not set up correctly in Streamlit Secrets.")
        return False

    message = Mail(
        from_email=sender_email,
        to_emails=recipient_email,
        subject=f"Invitation to Interview for the {job_title} Position",
        html_content=f"""
        <p>Dear {candidate_name},</p>
        <p>Thank you for your interest in the {job_title} position at our company.</p>
        <p>After reviewing your resume, we are impressed with your qualifications and would like to invite you to the next round of our selection process.</p>
        <p>Please let us know your availability for a brief preliminary interview.</p>
        <p>Best regards,<br>The Hiring Team</p>
        """
    )
    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        # A 2xx status code means the email was successfully sent
        if 200 <= response.status_code < 300:
            return True
        else:
            st.error(f"Failed to send email. Status code: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"An error occurred while sending the email: {e}")
        return False
