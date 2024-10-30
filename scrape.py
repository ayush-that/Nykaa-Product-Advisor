import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

AUTH = os.getenv("AUTH")
SBR_WEBDRIVER = f"https://{AUTH}@zproxy.lum-superproxy.io:9515"


def scrape_website(website):
    print("Connecting to Scraping Browser...")
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print("Connected! Navigating...")
        driver.get(website)
        print("Taking page screenshot to file page.png")
        driver.get_screenshot_as_file("./page.png")
        print("Navigated! Scraping page content...")
        html = driver.page_source
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
