from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()


def scrape_website(website):
    """Scrape website content using headless Chrome"""
    print("Setting up Chrome options...")
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    if os.environ.get("CHROME_BIN"):
        options.binary_location = os.environ.get("CHROME_BIN")

    print("Initializing WebDriver...")
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"Local Chrome failed: {e}, trying remote...")
        driver = webdriver.Chrome(
            options=options, service=Service("/usr/bin/chromedriver")
        )

    try:
        print("Navigating to website...")
        driver.get(website)
        print("Scraping page content...")
        html = driver.page_source
        return html
    except Exception as e:
        print(f"Error during scraping: {e}")
        raise
    finally:
        driver.quit()


def extract_body_content(html_content):
    """Extract body content using BeautifulSoup"""
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return "No body content found"


def clean_body_content(body_content):
    """Clean and format the body content"""
    soup = BeautifulSoup(body_content, "html.parser")
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    """Split content into chunks if needed"""
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]


if __name__ == "__main__":
    main()
