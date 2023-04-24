import session_handler
import interaction_handler
from log_handler import *
from argparse import ArgumentParser
from classes import WebsiteDefinition
from xmlrpc.server import SimpleXMLRPCServer


_driver = None

def create_session_and_initialize(target_website: str) -> None:
    global _driver
    target_definition =  WebsiteDefinition\
                                        .get_definition_from_string(
                                                     target_website)

    _driver = session_handler.get_or_create_session(target_definition)
    interaction_handler.set_is_server(True)

    write_to_log(SERVER_LOG_PATH + SERVER_LOG_FILENAME, SERVER_SUCCESS)


def close() -> None:
    write_to_log(SERVER_LOG_PATH + SERVER_LOG_FILENAME, SERVER_TERMINATED)
    _driver.close()
    exit()


def main() -> None:
    parser = ArgumentParser(description="Server script, keeps the Selenium driver alive")
    parser.add_argument("target_website", help="Platform name")
    parser.add_argument("port", type=int, default=9000, help="Port to listen on")

    args = parser.parse_args()
    server = SimpleXMLRPCServer(("localhost", args.port), allow_none=True)

    write_to_log(SERVER_LOG_PATH + SERVER_LOG_FILENAME, SERVER_INPROGRESS)
    create_session_and_initialize(args.target_website)
        
    server.register_function(close, "close_session")
    server.serve_forever()


if __name__ == "__main__":
    write_to_log(SERVER_LOG_PATH + SERVER_LOG_FILENAME, SERVER_INITIALIZE)
    try:
        main()
    except:
        write_to_log(SERVER_LOG_PATH + SERVER_LOG_FILENAME, SERVER_EXCEPTION)
