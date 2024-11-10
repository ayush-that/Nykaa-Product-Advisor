from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

AUTH = os.getenv("AUTH")
SBR_WEBDRIVER = f"https://{AUTH}@zproxy.lum-superproxy.io:9515"


def scrape_website(website):
    print("\nStarting scraping process...")

    try:
        with sync_playwright() as p:
            print("Launching browser...")
            browser = p.firefox.launch(headless=True)

            print("Creating new page...")
            page = browser.new_page()

            print(f"Navigating to website: {website}")
            page.goto(website, wait_until="networkidle")

            print("Getting page content...")
            html = page.content()

            print("Closing browser...")
            browser.close()

            print("Successfully retrieved page content")
            return html

    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        raise


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
