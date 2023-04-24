import pickle
import textwrap
from typing import Any
from selenium.webdriver.remote.webdriver import WebDriver
from classes import WebsiteDefinition
from config import config


def load_cookies(exit_on_fail: bool = False) -> dict:
    stored_cookies = None

    try:
        with open(config["cookies_directory_path"]
                  + config["cookies_filename"], "rb") as file:

            try:
                stored_cookies = pickle.load(file)
            except EOFError:
                print("File appears to be empty, re-creating it...")
                dump_cookies(stored_cookies)

    except EnvironmentError:
        print("File not found, creating it...")
        dump_cookies(stored_cookies)

    if stored_cookies is None:

        if not exit_on_fail:
            print("Attempting to re-load cookies file")
            return load_cookies(exit_on_fail=True)
        else:
            print("Failed to load, exiting.")
            raise SystemExit

    elif exit_on_fail:
        print("Successfully loaded.\n\n")

    return stored_cookies


def dump_cookies(stored_cookies: dict) -> None:
    dump_data(stored_cookies if stored_cookies is not None else {},
              config["cookies_directory_path"]
            + config["cookies_filename"])


def dump_data(data: Any, file_path: str) -> None:
    with open(file_path, "wb+") as file:
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)


def update_stored_cookies(stored_cookies: dict,
                          target: WebsiteDefinition,
                          update_dict: dict) -> None:


    stored_cookies.update({target.identifier: update_dict})
    dump_cookies(stored_cookies)


def get_session_cookies_stored(target: WebsiteDefinition,
                               stored_cookies: dict) -> dict:

    """Gets the session cookies specified by the target's
    WebsiteSpecifications from the stored_cookies dict
    containing all cookies"""

    return {} if not stored_cookies or target.identifier not in stored_cookies \
                                        else stored_cookies[target.identifier]


def get_session_cookies_driver(target: WebsiteDefinition,
                               driver: WebDriver) -> dict:

    """Gets the session cookies specified by the target's
    WebsiteSpecifications from the WebDriver passed as an argument"""

    return {cookie: driver.get_cookie(cookie)
            for cookie in target.specifications.session_cookies}


def validate_target_cookies(target: WebsiteDefinition,
                            driver: WebDriver,
                            target_cookies: dict) -> dict:


    if target.allow_forced_setup and (not target_cookies or
                                              None in [val for
                                              val in target_cookies.values()]):

        print_setup_text_wait_for_input(target)
        session_cookies = get_session_cookies_driver(target, driver)

        if not session_cookies or None in [val for val
                                              in session_cookies.values()]:

            print("One or more cookies are invalid, exiting.\n")
            print("Cookies:")
            print("--------")
            print("".join([(f"{key}: {val}\n") for
                               key, val in session_cookies.items()]))

            raise SystemExit
        else: 
            return session_cookies

    return target_cookies

def set_session_cookies_driver(driver: WebDriver,
                               target_cookies: dict) -> None:

    """Sets the session cookies specified by the target's
    WebsiteSpecifications in the WebDriver passed as an argument"""
    for cookie in target_cookies.values():
        driver.add_cookie(cookie)


def get_target_cookies(target: WebsiteDefinition, 
                       driver: WebDriver) -> dict:

    stored_cookies = load_cookies()
    target_cookies = validate_target_cookies(
        target, driver,
        get_session_cookies_stored(target, stored_cookies)
        )

    update_stored_cookies(stored_cookies, target, target_cookies)
    return target_cookies


def print_setup_text_wait_for_input(target) -> None:

    print(textwrap.dedent(f"""\
    {target.identifier} has one or more empty or invalid cookies
    Proceeding with cookies setup, the instructions must be followed.
    -------------------------------------------------------------
    Sign in to your target website, or do whatever else is necessary
    to get the required cookies, then press ENTER in the console
    If cookies are not needed, then the target's WebsiteDefinition is incorrect.
    Set WebsiteDefinition.allow_forced_setup to False if this is the case."""))
    input()