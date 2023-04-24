import time
from typing import Any
from .classes import WebsiteDefinition, WebsiteSpecifications
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from xmlrpc.client import ServerProxy


_driver: WebDriver = None
_website: WebsiteDefinition = None
_server_port: int = None
_is_server: bool = False


def switch_to_frame(identifier: str) -> None:
    _driver.switch_to.frame(identifier)


def switch_to_default_frame() -> None:
    _driver.switch_to.default_content()


def get_embedded_editor_code() -> None:
    return run_script(_website.script_get_embedded_code())


def set_is_server(new_val: bool) -> None:
    global _is_server
    _is_server = new_val


def assign_driver(driver: WebDriver) -> None:   
    global _driver

    if not isinstance(driver, WebDriver):
        raise TypeError("No driver was passed to module interaction_handler")
        
    _driver = driver


def assign_website(website: WebsiteDefinition) -> None:
    global _website

    if not website:
        raise TypeError("Invalid website definition passed to assign_website")
    
    _website = website


def close_driver() -> None:
    if not _driver:
        raise TypeError("No driver was passed to module interaction_handler")
    
    if _is_server or _server_port == None:
        _driver.close()
    else:
        print("Terminating server and session...")
        try:
            proxy = ServerProxy(f"http://localhost:{_server_port}", allow_none=True)
            proxy.close()
            print("Successfully terminated.")
        except Exception as e:
            raise(e)


def get_driver() -> WebDriver:
    if not _driver:
        raise TypeError("No driver was passed to module interaction_handler")
    
    return _driver


def get_website() -> WebsiteDefinition:
    if not _website: 
        raise TypeError("No platform was passed to module interaction_handler")

    return _website


def paste_code(code: str) -> None:
    run_script(_website.script_paste_solution_code(code))


def get_solution_result() -> str:
    time.sleep(0.1)
    run_script(_website.script_get_result_ready_element())
    parsed_result = _website.parse_result(
                             run_script(
                             _website.script_get_result_output()))

    return parsed_result


def submit_solution(code: str) -> None:
    paste_code(code)
    run_script(_website.script_submit_solution())


def test_solution(code: str) -> None:
    paste_code(code)
    run_script(_website.script_test_solution())


def get_description() -> str:                                
    return _website.parse_description(
            run_script(_website.script_get_description()))

        
def get_output() -> str:
    return run_script_until_valid(_website.script_get_result_output())


def run_script_sequence(sequence: tuple) -> Any:
    last_value: WebElement = None
    runner: function = run_script

    for script in sequence:
        runner = runner if script not in \
                (run_script, run_script_until_valid) else script

        if isinstance(script, str):
            if runner == run_script:
                last_value = run_script(script, False)
            else:
                last_value = run_script_until_valid(script, False)
                
        elif script != runner:
            script(last_value)

    return last_value


def run_script(code_or_sequence: str | tuple, 
                            from_default_frame=True) -> Any:

    if from_default_frame:
        switch_to_default_frame()
        
    if isinstance(code_or_sequence, tuple):
        return run_script_sequence(code_or_sequence)

    return _driver.execute_script(code_or_sequence)
    

def run_script_until_valid(js_code: str, 
                           from_default_frame=True,
                           attempts = 0) -> Any:

    if from_default_frame:
        switch_to_default_frame()

    try:
        result = _driver.execute_script(js_code,
                                        from_default_frame)

        if result:
            return result

    except Exception as E:
        pass
        
    time.sleep(0.5)
    
    if attempts >= 60:
        raise TimeoutError(f"Could not find element after {attempts} attempts")

    return run_script_until_valid(js_code, 
                                  from_default_frame, attempts + 1)