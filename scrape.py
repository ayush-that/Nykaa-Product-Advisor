import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options

load_dotenv()

AUTH = os.getenv("AUTH")
SBR_WEBDRIVER = f"https://{AUTH}@zproxy.lum-superproxy.io:9515"


def scrape_website(website):
    print("Setting up Chrome options...")
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")

    print("Initializing WebDriver...")
    chrome_driver_path = "/usr/bin/chromedriver"
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    try:
        print("Navigating to website...")
        driver.get(website)
        print("Scraping page content...")
        html = driver.page_source
    finally:
        driver.quit()
    return html


def extract_body_content(html_content):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return "No body content found"


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]


if __name__ == "__main__":
    main()
