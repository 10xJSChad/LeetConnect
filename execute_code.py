from __future__ import annotations

import session_handler
import interaction_handler
import solution_parser
import subprocess
import platform
import os

from log_handler import *
from functools import partial
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from classes import WebsiteDefinition, ResultText


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def import_code(solution_path: str):
    interaction_handler.get_embedded_editor_code()
    with open(solution_path, "w") as file:
        file.write(interaction_handler.get_embedded_editor_code())


def get_and_parse_solution(solution_path: str = None):
    with open(solution_path, "r") as file:
        solution_raw = file.read()
    
    solution_parsed = \
            solution_parser.parse_solution_code(solution_raw)

    return solution_parsed


def print_ResultText(result_text: list[ResultText]):
    for text in result_text:
        print(f"{text.color_shell}{text.text}")


def print_result() -> None:
    print_ResultText(get_result())


def print_description() -> None:
    print_ResultText(get_description())


def print_result_and_description() -> None:
    clear()

    print_result()
    if config.config["show_description"]:
        print("\n-----------------------------\n")
        print_description()


def get_description() -> None:                                
    return interaction_handler.get_description()

        
def get_result() -> None:
    return interaction_handler.get_solution_result()


def submit_solution(solution_path: str) -> None:
    interaction_handler.submit_solution(
        get_and_parse_solution(solution_path))

    print_result_and_description()


def test_solution(solution_path: str) -> None:
    interaction_handler.test_solution(
        get_and_parse_solution(solution_path))

    print_result_and_description()


def close_session() -> None:
    interaction_handler.close_driver()


def get_does_session_exist(print_result: bool = True) -> None:
    result = session_handler.get_existing_session() is not None
    if print_result:
        if result:
            print("Previous session is still active")
        else:
            print("Previous session is not active")
    return result



def get_session_and_initialize() -> None:
    existing_session = session_handler.get_existing_session(
                                     return_everything=True)
    
    if not existing_session:
        raise TypeError("No existing session was found")

    (driver, 
    target_definition,
    server_port)     =     (existing_session[0],
                            existing_session[1],
                            existing_session[2])
    
    return initialize(driver, target_definition)
    

def create_session_server(target_website_and_port: tuple[str, int]) -> None:
    print("Starting session server...")
    print("Note: Closing this will not cancel the server startup")

    target_website, port = target_website_and_port

    if platform.system() == "Windows":
        creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP |\
                         subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW

        extra_kwargs = {"creationflags": creation_flags}
    else:
        extra_kwargs = {"start_new_session": True}

    clear_log(SERVER_LOG_PATH + SERVER_LOG_FILENAME)

    subprocess.Popen(["python", "server.py",
                      target_website, str(port)],
                      **extra_kwargs)

    while True:
        server_status = read_log_until_string(SERVER_LOG_PATH 
                                             + SERVER_LOG_FILENAME, 
                                               SERVER_SUCCESS)
        if server_status == SERVER_SUCCESS \
                    or server_status == LOG_TIMED_OUT:
            break


    # Quick sleep so the user can read the success message
    time.sleep(2)


# Unused for now, does the same thing as the server without making a server
def create_session_and_initialize(target_website: str) -> None:
    target_definition =  WebsiteDefinition\
                                        .get_definition_from_string(
                                                     target_website)

    driver = session_handler.get_or_create_session(target_definition)
    initialize(driver, target_definition)


def perform_cookie_setup(target_website: str) -> None:
    target_definition =  WebsiteDefinition\
                                        .get_definition_from_string(
                                                     target_website)

    print("Starting setup")
    session_handler.get_or_create_session(target_definition, force_create=True)
    print("Setup complete, hit ENTER to close.")

    input()


def initialize(driver: WebDriver, 
               target_definition: WebsiteDefinition) -> None:

    interaction_handler.assign_driver(driver)
    interaction_handler.assign_website(target_definition)


def execute_command(action: function = None, 
                    action_argument: str |
                                     tuple[str, int] = None) -> None:

    if action != create_session_server and \
       action != get_does_session_exist and \
       action != perform_cookie_setup:

        get_session_and_initialize()

    function_arg_builder = {
        # *action_argument will raise an exception if it is not a tuple
        # even if this function is not being called
        create_session_server: partial(create_session_server, 
                                            action_argument),

        perform_cookie_setup: partial(perform_cookie_setup, 
                                          action_argument),

        close_session: close_session,
        get_does_session_exist: get_does_session_exist,
        import_code:  partial(import_code, action_argument),
        test_solution: partial(test_solution, action_argument),
        submit_solution: partial(test_solution, action_argument),
    }

    function_arg_builder[action]()