import re
import streamlit as st
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time

# Set up Selenium WebDriver (using Chrome in this example)
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Path to your ChromeDriver
driver = webdriver.Chrome(options=chrome_options)

# Function to extract emails from a webpage
def extract_emails(url):
    driver.get(url)
    
    time.sleep(5)
    
    page_source = driver.page_source
    
    soup = BeautifulSoup(page_source, 'html.parser')
    text = soup.get_text(separator=" ")

    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    
    emails = email_pattern.findall(text)
    
    unique_emails = list(set(emails))
    
    return unique_emails

def main():
    st.title("Email Extractor from URL")

    url = st.text_input("Enter the URL")

    if st.button("Extract Emails"):
        if url:
            emails = extract_emails(url)
            if emails:
                st.success(f"Found {len(emails)} email(s):")
                for email in emails:
                    st.write(email)
                driver.quit()    
            else:
                st.warning("No emails found on the page.")
        else:
            st.warning("Please enter a URL.")

if __name__ == "__main__":
    main()