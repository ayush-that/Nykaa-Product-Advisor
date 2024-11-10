import selenium.webdriver as webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

AUTH = os.getenv("AUTH")
SBR_WEBDRIVER = f"https://{AUTH}@zproxy.lum-superproxy.io:9515"


def get_firefox_options():
    """Configure Firefox options."""
    options = Options()

    # Essential options for running in container environment
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")

    # Set Firefox binary location if specified
    if os.environ.get("FIREFOX_BIN"):
        options.binary_location = os.environ.get("FIREFOX_BIN")

    return options


def scrape_website(website):
    print("\nStarting scraping process...")

    try:
        options = get_firefox_options()

        # Set up Firefox driver
        if os.environ.get("GECKODRIVER_PATH"):
            service = Service(executable_path=os.environ.get("GECKODRIVER_PATH"))
        else:
            from webdriver_manager.firefox import GeckoDriverManager

            service = Service(GeckoDriverManager().install())

        print("Initializing Firefox WebDriver...")
        driver = webdriver.Firefox(service=service, options=options)

        print(f"Navigating to website: {website}")
        driver.get(website)

        print("Getting page source...")
        html = driver.page_source

        print("Successfully retrieved page content")
        return html

    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        raise

    finally:
        try:
            if "driver" in locals():
                driver.quit()
                print("WebDriver closed successfully")
        except Exception as e:
            print(f"Error while closing WebDriver: {str(e)}")


def extract_body_content(html_content):
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
