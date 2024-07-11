import requests
from bs4 import BeautifulSoup
import re
from bs4 import BeautifulSoup
import re
import streamlit as st

def fetch_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to extract emails from the webpage content
def extract_emails_from_text(text):
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    return email_pattern.findall(text)

# Function to scrape emails from a webpage
def scrape_emails(url):
    webpage_content = fetch_webpage(url)
    if not webpage_content:
        return []

    soup = BeautifulSoup(webpage_content, 'lxml')
    text = soup.get_text()
    emails = extract_emails_from_text(text)
    return emails
import streamlit as st
def main():
    st.title("Email Extractor from URL")

    # Input field for the URL
    url = st.text_input("Enter the URL")

    if st.button("Extract Emails"):
        if url:
            emails = scrape_emails(url)
            if emails:
                st.success(f"Found {len(emails)} email(s):")
                for email in emails:
                    st.write(email)
            else:
                st.warning("No emails found on the page.")
        else:
            st.warning("Please enter a URL.")

if __name__ == "__main__":
    main()