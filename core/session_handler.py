import time
import pickle
from . import website_definitions #Nothing from here is used, just initializing it.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver
from .classes import WebsiteDefinition
from .cookie_handler import get_target_cookies, set_session_cookies_driver
from config import config
from subprocess import CREATE_NO_WINDOW

SESSION_SUCCESS_STR = "Session Live!"

# Very nice function by someone else
# I'm not exactly sure who came up with this, but someone on
# StackOverflow said they got it from Tarun Lalwani's (@ask4tarun) blog
# The url is dead now so I can't read the blog post for more context
def attach_to_session(executor_url: str, 
                            session_id: str) -> WebDriver:

    original_execute = WebDriver.execute

    def new_command_execute(self, command, params=None):
        
        if command == "newSession":
            return {'success': 0, 'value': None, 
                                    'sessionId': session_id}
        else:
            return original_execute(self, command, params)

    WebDriver.execute = new_command_execute
    driver = webdriver.Remote(command_executor=executor_url, 
                                    desired_capabilities={})
    driver.session_id = session_id
    WebDriver.execute = original_execute
    return driver


def dump_session_data(session_data: tuple):
    with open(config["last_session_directory_path"]
            + config["last_session_filename"], "wb+") as file:

        pickle.dump(session_data, file, protocol=pickle.HIGHEST_PROTOCOL)


def load_session_data() -> tuple:
    with open(config["last_session_directory_path"]
            + config["last_session_filename"], "rb") as file:

        return(pickle.load(file))


def get_existing_session(return_everything=False) -> \
            WebDriver | tuple[WebDriver, WebsiteDefinition, int]:

    try:
        last_session = load_session_data()

        (executor_url, 
        session_id, 
        website_definition,
        server_port)     =    (last_session[0], 
                               last_session[1], 
                               last_session[2],
                               last_session[3])

        driver = attach_to_session(executor_url, session_id)     
        driver.get_cookie("My name is skyler white yo") # exception if session is invalid
        # this goes off instantly if the previous process is still running
        # if it isn't, it'll take about 10 seconds to figure out the session isn't valid.
        # but the previous session really shouldn't be running, that is a problem.

        return driver if not return_everything \
                      else (driver, website_definition, server_port)

    except:
        return None


def get_or_create_session(target_website: WebsiteDefinition, 
                          server_port: int = None, 
                          force_create: bool = False) -> WebDriver:

    driver = get_existing_session() if not force_create else None

    if not driver:
        print("No valid sessions to re-connect to, starting new session...")

        if config["browser"].lower() == "chrome":
            chrome_service = ChromeService('chromedriver')
            chrome_service.creation_flags = CREATE_NO_WINDOW
            driver = webdriver.Chrome(service=chrome_service)

        dump_session_data((driver.command_executor._url, 
                           driver.session_id, target_website, server_port))
                           
        driver.get(target_website.specifications.url_root)

        try:
            target_cookies = get_target_cookies(target_website, driver)
            set_session_cookies_driver(driver, target_cookies)
            
            time.sleep(2) # should be replaced with waiting for the page to load

            driver.get(target_website.specifications.url_root)

        except Exception as e:
            print(f"EXCEPTION: {e}")
            driver.close()

    print(SESSION_SUCCESS_STR)

    # !!!! It is the responsibility of whatever receives this to close the driver !!!!
    return driver