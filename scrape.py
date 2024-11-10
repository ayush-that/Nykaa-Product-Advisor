import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
import subprocess
import sys

load_dotenv()

AUTH = os.getenv("AUTH")
SBR_WEBDRIVER = f"https://{AUTH}@zproxy.lum-superproxy.io:9515"


def get_chrome_path():
    """Get the Chrome binary path."""
    if os.environ.get("CHROME_BIN"):
        return os.environ.get("CHROME_BIN")

    chrome_paths = [
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
    ]

    for path in chrome_paths:
        if os.path.exists(path):
            return path

    try:
        chrome_path = (
            subprocess.check_output(
                ["which", "google-chrome"], stderr=subprocess.STDOUT
            )
            .decode()
            .strip()
        )
        if chrome_path:
            return chrome_path
    except subprocess.CalledProcessError:
        pass

    return None


def get_chrome_options():
    """Configure Chrome options."""
    options = Options()

    chrome_path = get_chrome_path()
    if chrome_path:
        print(f"Using Chrome binary at: {chrome_path}")
        options.binary_location = chrome_path
    else:
        print("Warning: Could not find Chrome binary!")

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--window-size=1920,1080")

    return options


def get_chromedriver_path():
    """Get the ChromeDriver path."""
    if os.environ.get("CHROMEDRIVER_PATH"):
        return os.environ.get("CHROMEDRIVER_PATH")

    chromedriver_paths = [
        "/usr/bin/chromedriver",
        "/usr/local/bin/chromedriver",
    ]

    for path in chromedriver_paths:
        if os.path.exists(path):
            return path

    return None


def scrape_website(website):
    print("\nStarting scraping process...")
    print(f"Python version: {sys.version}")

    try:
        options = get_chrome_options()
        chromedriver_path = get_chromedriver_path()
        if chromedriver_path:
            print(f"Using ChromeDriver at: {chromedriver_path}")
            service = Service(executable_path=chromedriver_path)
        else:
            print("ChromeDriver path not found, falling back to webdriver_manager")
            from webdriver_manager.chrome import ChromeDriverManager

            service = Service(ChromeDriverManager().install())

        print("Initializing Chrome WebDriver...")
        driver = webdriver.Chrome(service=service, options=options)

        print(f"Navigating to website: {website}")
        driver.get(website)

        print("Getting page source...")
        html = driver.page_source

        print("Successfully retrieved page content")
        return html

    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {e.args}")
        raise

    finally:
        try:
            if "driver" in locals():
                driver.quit()
                print("WebDriver closed successfully")
        except Exception as e:
            print(f"Error while closing WebDriver: {str(e)}")


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
