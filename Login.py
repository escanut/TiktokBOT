import random
import time

import Cookies as cookies

from playwright.sync_api import sync_playwright


def handle_captcha(page):
    """
    Handles captchas using an id selector and waits until it's resolved.
    """
    captcha_id = "#captcha-verify-container-main-page"  # Replace with the actual id of the captcha element
    try:
        # Wait for the captcha container to appear
        page.wait_for_selector(captcha_id, timeout=10000)
        print("Captcha detected. Waiting for manual resolution.")

        # Infinite delay until captcha is resolved
        while True:
            # Check if the captcha container is no longer visible
            if not page.is_visible(captcha_id):
                print("Captcha solved. Resuming bot operation.")
                break
            print("Waiting for captcha to be solved...")
            time.sleep(5)

    except TimeoutError:
        # No CAPTCHA detected within the timeout (handle this gracefully)
        print("Captcha not detected. Proceeding with other actions.")
        # Optionally, you can call other functions or proceed with the rest of the process here.
    except Exception as e:
        print(f"An error occurred: {e}")



def random_delay(min_delay=2, max_delay=5):
    """Introduce a random delay to simulate human interaction."""
    time.sleep(random.uniform(min_delay, max_delay))




def login_tiktok(username, password, hashtag, maximum_post, comment_list):
    with sync_playwright() as p:
        # Launch browser in non-headless mode for better observation
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context()

        # Load cookies if available
        cookies.load_cookies(context)

        # Open a new page
        page = context.new_page()
        page.goto("https://www.tiktok.com/login")

        # Check if already logged in by looking for a specific element
        try:
            page.wait_for_selector('[data-e2e=nav-profile]', timeout=10000)
            print("Already logged in!")

            scrape(page, hashtag, maximum_post, comment_list)
            
        except TimeoutError:
            print("Not logged in, proceeding with login.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        # Interact with the login form directly
        try:

            # Click on the 'Use phone / email / username' option
            page.click("text=Use phone / email / username")
            random_delay()

            # Click on the 'Email / Username' tab if necessary
            page.click("text=Log in with email or username")
            random_delay()

            # Fill in the username and password fields
            page.fill("input[name='username']", username)
            random_delay()
            page.fill("input[type='password']", password)
            random_delay()

            handle_captcha(page)

            # Click the 'Log in' button
            page.click("button[type='submit']")
            random_delay(5, 10)

            # Check for captcha and handle it
            time.sleep(20)
            print("Login successful!")
            random_delay(5, 11)

            # Save cookies after successful login
            cookies.save_cookies(context)

            handle_captcha(page)

            scrape(page, hashtag, maximum_post, comment_list)

        except TimeoutError:
            print("Login failed. Timeout waiting for elements. Please verify selectors.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        # Close the browser
        browser.close()





def comment_on_page(page, links, comment_list):
    for link in links:
        handle_captcha(page)

        try:
            # Navigate to the link
            print(f"Navigating to: {link}")
            page.goto(link, timeout=30000)
            page.wait_for_selector("body", timeout=5000)  # Ensure the page has loaded

            # Wait for the comment box span to appear
            comment_box_selector = 'div[contenteditable="true"]'  # Selector for contenteditable span
            page.wait_for_selector(comment_box_selector, timeout=10000)

            comment_text = random.choice(comment_list)
            # Focus on the comment box and type the comment
            print(f"Posting comment: {comment_text}")
            page.fill(comment_box_selector, comment_text)  # Use the contenteditable span

            # Simulate pressing 'Enter' to post the comment
            page.press(comment_box_selector, "Enter")

            # Random delay to simulate human behavior
            random_delay(5, 10)

        except TimeoutError:
            print(f"Timeout while trying to comment on: {link}")
        except Exception as e:
            print(f"Error while commenting on {link}: {e}")

def scrape(page, hashtag, maximum_post, comment_list):

    page.fill("input[type='search']", hashtag)
    random_delay()

    page.click("button[type='submit']")
    time.sleep(20)

    handle_captcha(page)

    div_selector = 'div[data-e2e="search_top-item"]'

    page.wait_for_selector(div_selector)
    div_elements = page.query_selector_all(div_selector)

    links = []
    for i, div in enumerate(div_elements[:maximum_post]):
        try:
            # Find the child 'a' tag within the div
            link_element = div.query_selector('a')
            if link_element:
                href = link_element.get_attribute("href")
                if href:
                    links.append(href)
                    print(f"Link {i + 1}: {href}")
        except Exception as e:
            print(f"Error processing div {i + 1}: {e}")

    print(f"Total links found: {len(links)}")
    handle_captcha(page)

    comment_on_page(page, links, comment_list)




"id:captcha-verify-container-main-page"
"class=TUXModal captcha-verify-container"