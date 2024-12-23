from fastapi import FastAPI
from pydantic import BaseModel
from playwright.sync_api import sync_playwright

app = FastAPI()


class URLRequest(BaseModel):
    url: str


@app.get("/scrape")
def scrape_page():
    try:
        with sync_playwright() as p:
            # Launch the browser
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Navigate to the provided URL
            page.goto("https://infin.ai/")

            # Get the page title
            title = page.title()

            # Take a screenshot and save it
            screenshot_path = "screenshot.png"
            page.screenshot(path=screenshot_path)

            # Close the browser
            browser.close()

        return {
            "message": "Page scraped successfully",
            "title": title,
            "screenshot_path": screenshot_path,
        }
    except Exception as e:
        return {"error": str(e)}
