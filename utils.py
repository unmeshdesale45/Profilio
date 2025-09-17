import re
import nltk
import PyPDF2
import docx
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# This function must be named exactly 'extract_text_from_pdf'
def extract_text_from_pdf(file):
    """Extracts text from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# This function must be named exactly 'extract_text_from_docx'
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