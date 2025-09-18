# 🤖 AI Resume Screener & Candidate Ranker

This is an intelligent HR Assistant web application designed to streamline the initial screening process for recruiters. The tool leverages Natural Language Processing (NLP) to analyze, score, and rank multiple resumes against a given job description, helping to quickly identify the most qualified candidates.

The application is built entirely in Python, using Streamlit for the user interface and Scikit-learn for the core NLP analysis.

![AI Resume Screener Dashboard](https://i.imgur.com/4J1QZ7w.png)
_Note: You can replace the link above with a screenshot of your own running application!_

---

## ✨ Key Features

-   **Batch Resume Processing:** Upload multiple resumes (PDF or DOCX) at once to analyze them against a single job description.
-   **Candidate Ranking Dashboard:** View all candidates in a clean, sorted table ranked by their job-fit score, from highest to lowest.
-   **Side-by-Side Comparison:** Select any candidate from the ranked list to see a detailed view of their resume next to the job description.
-   **Automated Keyword Highlighting:** Common keywords and skills found in both the resume and the job description are automatically highlighted for quick visual scanning.
-   **Intuitive Web Interface:** A simple and clean user interface built with Streamlit, requiring no installation for the end-user.

---

## 🛠️ Technology Stack

-   **Frontend:** [Streamlit](https://streamlit.io/)
-   **Backend & NLP:** Python
-   **Core Libraries:**
    -   `scikit-learn`: For TF-IDF vectorization and cosine similarity calculation.
    -   `pandas`: For data manipulation and displaying the ranked results.
    -   `nltk`: For text preprocessing (tokenization and stopword removal).
    -   `PyPDF2` & `python-docx`: For extracting text from PDF and DOCX files.

---

## 🚀 How to Run Locally

Follow these steps to set up and run the project on your own machine.

### 1. Prerequisites
-   [Git](https://git-scm.com/)
-   [Python 3.8+](https://www.python.org/downloads/)

### 2. Clone the Repository
```bash
git clone <your-repository-url>
cd <repository-folder-name>
```

### 3. Create a Virtual Environment (Recommended)
```bash
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
Install all the required packages from the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

### 5. Download NLTK Data
The NLTK library requires specific datasets for text processing. Run a Python interpreter and enter the following:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### 6. Run the Streamlit App
Launch the application using the following command:
```bash
streamlit run app.py
```
Your browser should automatically open with the application running!

---

## ☁️ Deployment

This application is ready for deployment on [Streamlit Community Cloud](https://streamlit.io/cloud). Simply connect your GitHub repository, and it will be live in minutes.

---
## 💡 Future Enhancements

-   **Semantic Search:** Upgrade from keyword matching to a model that understands the meaning behind words (e.g., using sentence transformers).
-   **Skill/Entity Extraction:** Automatically extract and list all identified skills, years of experience, and educational qualifications from each resume.
-   **Database Integration:** Add a database (like SQLite or Firestore) to save job descriptions and past analysis results.
