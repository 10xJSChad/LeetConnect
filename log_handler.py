"""Intended to log server messages to be read by 
clients, because I couldn't reliably pipe stdout or achieve
consistent behaviour between shells.\n

I would have greatly preferred this module not exist,
but apparently achieving compatability for all the shells
is just way harder than cheaping out and making this instead.
I hate it, but it works for now, and that lets me get on with 
developing the rest of this project."""

import time
import config

def write_to_log(log_path: str, log_str: str) -> None:
    with open(log_path, "w+") as f:
        f.write(log_str)


def clear_log(log_path):
    with open(log_path, "w+") as f:
        f.write("")


def read_log(log_path: str, print_log: bool = True, 
                            force_create_log: bool = True) -> str:
    try:
        with open(log_path, "r") as log_file:
            lines = log_file.read().split("\n")

            if print_log:
                for line in lines:
                    print(line)

            return "\n".join(lines)
    except:
        print(f"Unable to access file '{log_path}'")
        if force_create_log:
            print("Creating it now...")
            with open(log_path, "w+") as f:
                f.write("")
                return("")


def read_log_until_string(log_path: str, 
                          trigger_string: str, 
                          print_log: bool = False,
                          print_log_printstrings: bool = True,
                          timeout: int = 25) -> str:

    already_read_lines = set() 
    timeout_start = time.time()
    while time.time() < timeout_start + timeout:
        lines = read_log(log_path, False).split("\n")
        for line in lines:
            if line not in already_read_lines:
                if print_log:
                    print(line)
                    
                if print_log_printstrings and \
                        line in SERVER_LOG_PRINT_STRINGS:

                    print(SERVER_LOG_PRINT_STRINGS[line])

                already_read_lines.add(line)

            if trigger_string in line:
                return trigger_string
            
            # This loop doesn't really need to be fast
            # and I don't like the sound my computer makes
            # when I don't limit it.
            time.sleep(0.2)
    
    return LOG_TIMED_OUT



SERVER_LOG_PATH = config.config["server_log_path"]
SERVER_LOG_FILENAME = config.config["server_log_filename"]

SERVER_INITIALIZE = "SERVER_INITIALIZE"
SERVER_INPROGRESS = "SERVER_INPROGRESS"
SERVER_TERMINATED = "SERVER_TERMINATED"
SERVER_EXCEPTION = "SERVER_EXCEPTION"
SERVER_SUCCESS = "SERVER_SUCCESS"


SERVER_LOG_PRINT_STRINGS = {
    SERVER_INITIALIZE: "Server initializing",
    SERVER_INPROGRESS: "Server live, starting session...",
    SERVER_SUCCESS: "Session live!\nDon't forget to close the server eventually.",
    SERVER_TERMINATED: "Server and session terminated.",
    SERVER_EXCEPTION: "Server ran into a critical failure, selenium remote may still be running!"
}


LOG_TIMED_OUT = "LOG_TIMED_OUT"