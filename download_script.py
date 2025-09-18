import nltk
import os

# Define the download directory
DOWNLOAD_DIR = os.path.join(os.getcwd(), "nltk_data")
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Download the packages to the specified directory
nltk.download('punkt', download_dir=DOWNLOAD_DIR)
nltk.download('stopwords', download_dir=DOWNLOAD_DIR)

print(f"Downloaded NLTK data to: {DOWNLOAD_DIR}")