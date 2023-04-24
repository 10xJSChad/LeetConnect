"""This is where you can define custom trigger-string based parsing,
includes a useful example for Leetcode challenges that require using 
data structures and functions not defined in the solution code itself."""


# oh yeah baby we just wrote the slowest function
# the time complexity of this one is off the charts!
# (will rewrite eventually, just want to be done with this for now)
def get_trigger_strings(solution_code: str) ->  list[str]:
    triggers_found = []

    for key in trigger_strings_dict.keys():
        if key in solution_code:
            triggers_found.append(key)
    
    return triggers_found


def parse_solution_code(solution_code: str) -> str:
    trigger_strings_list = \
            get_trigger_strings(solution_code)

    for trigger in trigger_strings_list:
        solution_code = trigger_strings_dict[trigger](trigger, solution_code)
    
    return solution_code


def ignore_before(trigger_string: str, 
                    solution_code: str) -> str:
    """Ignores code before the trigger string, this
    can be used to define types and functions you may need
    in a Leetcode/Codewars problem, but that are not defined
    in the solution template."""    
    
    return solution_code[
        solution_code.index(trigger_string)
                      + len(trigger_string):]


trigger_strings_dict = {
    "#IGNORE_BEFORE": ignore_before,
    "//IGNORE_BEFORE": ignore_before,
}