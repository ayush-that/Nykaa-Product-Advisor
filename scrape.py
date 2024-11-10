import selenium.webdriver as webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

AUTH = os.getenv("AUTH")
SBR_WEBDRIVER = f"https://{AUTH}@zproxy.lum-superproxy.io:9515"


def find_firefox_binary():
    """Find Firefox binary path."""
    possible_paths = [
        os.getenv("FIREFOX_BINARY_PATH"),
        "/usr/bin/firefox-esr",
        "/usr/bin/firefox",
        "/snap/bin/firefox",
    ]

    for path in possible_paths:
        if path and os.path.exists(path):
            print(f"Found Firefox binary at: {path}")
            return path

    # If not found in common locations, try using which
    try:
        firefox_path = (
            subprocess.check_output(["which", "firefox-esr"]).decode().strip()
        )
        if firefox_path and os.path.exists(firefox_path):
            print(f"Found Firefox binary using which at: {firefox_path}")
            return firefox_path
    except:
        pass

    return None


def scrape_website(website):
    print("\nStarting scraping process...")

    try:
        options = FirefoxOptions()

        # Find Firefox binary
        firefox_binary = find_firefox_binary()
        if not firefox_binary:
            raise Exception("Firefox binary not found!")

        print(f"Using Firefox binary at: {firefox_binary}")
        options.binary_location = firefox_binary

        # Set up Firefox options
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

        # Log Firefox version
        try:
            version = (
                subprocess.check_output([firefox_binary, "--version"]).decode().strip()
            )
            print(f"Firefox version: {version}")
        except:
            print("Could not determine Firefox version")

        # Set up service
        service = Service("/usr/local/bin/geckodriver")

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
        print(f"Error type: {type(e).__name__}")
        import traceback

        print(f"Traceback: {traceback.format_exc()}")
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
