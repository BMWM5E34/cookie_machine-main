from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import random
import time

# Function to load cookies from a file, with a default value if the file doesn't exist
def load_cookies_from_file(file_path):
    try:
        with open(file_path, "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return []

# Function to save cookies to a file
def save_cookies_to_file(file_path, cookies):
    with open(file_path, "w") as json_file:
        json.dump(cookies, json_file, indent=4)

# Ask the user whether to append cookies from the cookies.json file
append_existing_cookies = input("Do you want to append cookies from the cookies.json file? (y/n): ").lower() == 'y'

if append_existing_cookies:
    # Load existing cookies from cookies.json
    existing_cookies = load_cookies_from_file("cookies.json")
else:
    existing_cookies = []

# Set up Chrome options for running in headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')  # Required if running on Windows

# Read websites from a file
with open("websites.txt", "r") as file:
    websites = file.read().splitlines()

num_cookie_files = int(input("Enter the number of cookies: "))
num_websites = int(input("Enter the number of websites: "))

# Use a range to iterate over the number of cookie files
for i in range(num_cookie_files):
    driver = webdriver.Chrome(options=chrome_options)
    all_cookies = []

    # Randomly select websites from the list
    random_websites = random.sample(websites, num_websites)

    for site in random_websites:
        try:
            driver.set_page_load_timeout(5)
            driver.get(site)
            time.sleep(1.3)
            cookies = driver.get_cookies()

            # Simplify the cookie formatting
            formatted_cookies = [{
                "domain": cookie["domain"],
                "hostOnly": "." not in cookie["domain"],
                **{key: cookie[key] for key in ["httpOnly", "name", "path", "sameSite", "secure"]},
                "session": "expiry" not in cookie,
                "storeId": "0",
                "value": cookie["value"]
            } for cookie in cookies]

            all_cookies.extend(formatted_cookies)

        except Exception as e:
            print(f"Error fetching cookies for {site}: {e}")

    # Append existing cookies to the new ones if requested by the user
    if append_existing_cookies:
        all_cookies += existing_cookies

    filename = f"cookies/cookies_{i}.json"

    # Save the cookies to a file
    save_cookies_to_file(filename, all_cookies)
    print(f"Cookies have been saved to a file: {filename}")

    driver.quit()

driver.quit()
