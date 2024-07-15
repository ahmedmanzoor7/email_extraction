from lib2to3.pgen2 import driver
import re
import requests
import streamlit as st
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import urljoin, urlparse
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_links(url):
    urls = set()

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        page_source = driver.page_source
        driver.close()
        soup = BeautifulSoup(page_source, "html.parser")
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                continue
            href = urljoin(url, href)
            href = href.split("#")[0]
            href = href.split("?")[0]
            if is_valid(href):
                urls.add(href)

    except requests.exceptions.RequestException as e:
        driver.close()
        print(f"Error accessing {url}: {e}")
    except:
      print("error")
    return urls


def crawl(url, max_depth=2):
    visited = set()
    to_visit = set([url])
    for _ in range(max_depth):
        new_to_visit = set()
        for link in to_visit:
            if link not in visited:
                visited.add(link)
                new_to_visit.update(get_all_links(link))
        to_visit = new_to_visit - visited
    return visited

# Function to extract emails from a webpage
def extract_emails(url):
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    time.sleep(5)

    page_source = driver.page_source

    driver.close()

    soup = BeautifulSoup(page_source, 'html.parser')
    text = soup.get_text(separator=" ")

    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

    emails = email_pattern.findall(text)

    unique_emails = list(set(emails))

    return unique_emails

def main():
   st.title("Email Extractor from URL")
   start_url = st.text_input("Enter the URL")
   depth = st.text_input("Enter an level:")
   if depth:
        try:

            depth=int(depth)
            if st.button("Extract Emails"):
                all_links = crawl(start_url,depth)
                list(all_links)
                all_links = list(all_links)
                new_links= []
                for i in range(len(all_links)):
                    if start_url in list(all_links)[i]:
                        new_links.append(all_links[i])
                    if new_links:
                        emails = []
                        for urls in new_links:
                            email = extract_emails(urls)
                            emails += email
                        
                        if emails:
                            st.success(f"Found {len(emails)} email(s):")
                            for email in emails:
                                st.write(email)   
                        else:
                            st.warning("No emails found on the page.")
                    else:
                        st.warning("Please enter a URL.")
        except ValueError:
            st.error("Please enter a valid integer")               
if __name__ == "__main__":
    main()