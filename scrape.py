import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import subprocess

load_dotenv()

AUTH = os.getenv("AUTH")
SBR_WEBDRIVER = f"https://{AUTH}@zproxy.lum-superproxy.io:9515"


def find_chromium_path():
    possible_paths = [
        # Common Linux paths
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        # Render-specific path
        "/opt/google/chrome/chrome",
        "/usr/bin/google-chrome-unstable"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found Chrome/Chromium at: {path}")
            return path
            
    # Attempt to find using which command
    try:
        path = subprocess.check_output(["which", "google-chrome"]).decode().strip()
        if os.path.exists(path):
            print(f"Found Chrome via which command at: {path}")
            return path
    except:
        pass
        
    print("Warning: Chrome binary not found in common locations")
    # Return None to allow ChromeDriver to attempt using system default
    return None


def scrape_website(website):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # Find Chrome binary
    chrome_path = find_chromium_path()
    if chrome_path:
        options.binary_location = chrome_path
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(website)
        html = driver.page_source
        return html
    except Exception as e:
        raise Exception(f"Failed to scrape website: {str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()


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
