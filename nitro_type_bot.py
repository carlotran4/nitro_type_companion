"""
Use selenium to make a NitroType bot.
It will race at a given users average wpm.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions
from webdriver_manager.chrome import ChromeDriverManager

# Adding ad blocker to selenium instance because ads take long time to load.
options = Options()
options.add_extension("C:\\Users\\carlo\\Downloads\\uBlock-Origin.crx")
options.add_argument("--mute-audio")

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                           options=options)
browser.get("https://www.nitrotype.com/login")

# Password: fivethetaoneone
# Username: nitro_type_bot_1


def main(public_user_url, username="nitro_type_bot_1",
         password="fivethetaoneone"):
    """Concatenate all functions."""

    login(username, password)
    avg_wpm = get_average_wpm(public_user_url=public_user_url)
    add_friend()
    accept_game_invite()
    while not browser.find_elements(By.CLASS_NAME, "icon icon-warn modal-alertIcon"):
        print("starting loop")
        wait_for_start()
        start = time.perf_counter()
        paragraph = get_paragraph()
        print(f"time to get paragraph{time.perf_counter()-start}")
        type_paragraph(paragraph, avg_wpm)
        actions = ActionChains(browser)
        actions.send_keys(Keys.ENTER)
        actions.perform()


def login(username, password) -> str:
    """Logs in to bot account

    Args:
        username (String): username of bot account
        password (String): password for bot account
    """

    username_box = browser.find_element(By.ID, 'username')
    username_box.send_keys(username)
    time.sleep(0.5)
    password_box = browser.find_element(By.ID, "password")
    password_box.send_keys(password+Keys.ENTER)
    time.sleep(0.5)


def get_average_wpm(public_user_url) -> int:
    """Get the words per minute of certain user

    Args:
        public_user_url (String): url to public profile of users page.
        Must use default profile settings;

    Returns:
        int: Words per minute for given user.
    """
    browser.get(public_user_url)
    xpath = "/html/body/div/div/main/section[1]/div[3]/div[2]/div[3]/div/div[1]/div[2]/div[1]"
    item = browser.find_element(By.XPATH, xpath)
    return int(item.text)


def add_friend() -> None:
    """Add account with given username as friend if they are not yet added.
    """
    try:
        xpath = "/html/body/div/div/main/section[1]/ul/li[1]/button"
        friend_button = browser.find_element(By.XPATH, xpath)
        friend_button.click()
        print("Sent friend invite")
    except selenium.common.exceptions.NoSuchElementException:
        print("Did not send friend invite")


def accept_game_invite() -> None:
    """
    Wait to receive invite to game that user will send to bot.
    Accept invite, break.
    """
    xpath = "/html/body/div/div[1]/div/div/div[2]/a"
    while True:
        try:
            join_race_button = browser.find_element(By.XPATH, xpath)
            join_race_button.click()
            return None
        except selenium.common.exceptions.NoSuchElementException:
            print("waiting")
            time.sleep(10)


def wait_for_start():
    """Wait for the countdown of the match.
    """
    while not browser.find_elements(By.CLASS_NAME, "dash-letter"):
        pass
    print("match_starting")


def get_paragraph() -> list:
    """Get the paragraph that needs to be typed.

    Returns:
        list: list of characters to be typed.
    """
    letters = browser.find_elements(By.CLASS_NAME, "dash-letter")
    for idx, i in enumerate(letters):
        letters[idx] = i.text
    return letters


def type_paragraph(letters, wpm) -> None:
    """Type the given paragraph at certain wpm.

    Args:
        letters (list): List of letters to be typed.
        wpm (int): How fast the words should be typed.
    """

    # Calculate sec_per_char accounting for fact that Get_paragraph() takes on average 7 seconds.
    ideal_time = (12/wpm)*len(letters)
    sec_per_char = (ideal_time-7)/len(letters)

    actions = ActionChains(browser)
    for letter in letters:
        if letter == " ":
            actions.send_keys(Keys.SPACE)
        else:
            actions.send_keys(letter)
        actions.perform()
        time.sleep(sec_per_char)


# PUT USERNAME HERE
main("https://www.nitrotype.com/racer/uwuleon")
