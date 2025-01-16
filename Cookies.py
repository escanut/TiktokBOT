import json
import os


# File path for storing cookies
COOKIE_FILE = "tiktok_cookies.json"



def save_cookies(context):
    """Save cookies to a file."""
    cookies = context.storage_state()
    with open(COOKIE_FILE, "w") as f:
        json.dump(cookies, f)


def load_cookies(context):
    """Load cookies from a file if it exists."""
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, "r") as f:
            cookies_data = json.load(f)

            # If the cookies are stored in the expected format
            if "cookies" in cookies_data:
                context.add_cookies(cookies_data["cookies"])
                print("Cookies loaded successfully.")
            else:
                print("Invalid cookie format. Unable to load cookies.")