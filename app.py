import streamlit as st
from playwright.sync_api import sync_playwright, TimeoutError

st.title("Twitter Post Screenshot Generator")

def capture_tweet(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        page.goto(url, wait_until='domcontentloaded', timeout=60000)
        page.wait_for_load_state('networkidle', timeout=60000)
        page.wait_for_selector('article', timeout=60000)
        tweet = page.locator("article").first
        screenshot = tweet.screenshot()
        browser.close()
        return screenshot

url = st.text_input("Enter Twitter Post URL:")

if url and st.button("Generate Screenshot"):
    try:
        with st.spinner("Capturing tweet..."):
            screenshot = capture_tweet(url)
            st.image(screenshot, caption="Tweet Screenshot")
    except TimeoutError:
        st.error("Timeout: Tweet took too long to load. Please try again.")
    except Exception as e:
        st.error(f"Error: {str(e)}")