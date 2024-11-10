import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
import platform

load_dotenv()

AUTH = os.getenv("AUTH")
SBR_WEBDRIVER = f"https://{AUTH}@zproxy.lum-superproxy.io:9515"


def get_chrome_options():
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

    # Set binary location for Render
    if os.environ.get("CHROME_BIN"):
        options.binary_location = os.environ.get("CHROME_BIN")

    return options


def scrape_website(website):
    print("Setting up Chrome options...")
    options = get_chrome_options()

    print("Initializing WebDriver...")
    if os.environ.get("CHROMEDRIVER_PATH"):
        # Use the system-installed chromedriver on Render
        service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
    else:
        # Local development fallback
        from webdriver_manager.chrome import ChromeDriverManager

        service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)

    try:
        print("Navigating to website...")
        driver.get(website)
        print("Scraping page content...")
        html = driver.page_source
    finally:
        driver.quit()
    return html


# Rest of your functions remain the same
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
