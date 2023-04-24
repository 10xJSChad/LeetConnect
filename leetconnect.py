from execute_code import *
from argparse import ArgumentParser
from functools import partial

def main():
    parser = ArgumentParser(description="Words about the thing")

    parser.add_argument("-o", "--open", type=str, nargs="?", help="Opens a new LeetConnect server configured for the target platform")
    parser.add_argument("-r", "--run", type=str, nargs="?", help="Runs the solution file on the target platform and shows the results")
    parser.add_argument("-s", "--submit", type=str, nargs="?", help="Submits the solution file on the target platform and shows the submission result")
    parser.add_argument("-i", "--import", dest="i", type=str, nargs="?", help="Imports code from the target platform's embedded editor")
    parser.add_argument("--setup", type=str, nargs="?", help="Perform cookie setup on the target platform")
    parser.add_argument("-p", "--port", type=int, nargs="?", default=9000, help="Port to listen on or send commands to")
    parser.add_argument("-c", "--close", action="store_true", help="Closes the active LeetConnect server")
    parser.add_argument("--status", action="store_true", help="Returns whether the previous session is still active")

    args = parser.parse_args()
    arg_handler(args)


def arg_handler(args):
    arg_functions = {
        "open":     partial(execute_command, create_session_server, (args.open, args.port)),
        "run":      partial(execute_command, test_solution, args.run),
        "submit":   partial(execute_command, submit_solution, args.submit),
        "i":        partial(execute_command, import_code, args.i),
        "setup":    partial(execute_command, perform_cookie_setup, args.setup),
        "status":   partial(execute_command, get_does_session_exist),
        "close":    partial(execute_command, close_session),
    }

    for arg, val in vars(args).items():
        if val and arg in arg_functions:
            arg_functions[arg]()

if __name__ == "__main__":
    main()