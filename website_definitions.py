from __future__ import annotations
import textwrap

from html.parser import HTMLParser
from classes import *
from interaction_handler import switch_to_frame, run_script_until_valid

class LeetcodeDefinition(WebsiteDefinition) :
    pass


class CodewarsDefinition(WebsiteDefinition):

    def parse_result(self, result: str, markdown=False) -> str:
        # Prepare yourself for the worst parsing function 
        # you will ever see
        
        class ResultParser(HTMLParser):
            def __init__(self, parse_markdown=markdown):
                super().__init__()
                self.reset()
                self.convert_charrefs = True
                self.output = []
                self.markdown = parse_markdown
                self.tag_stack = []

            def handle_data(self, d):
                if self.tag_stack:
                    return

                if not self.markdown:
                    self.output[-1].append(d)
                else:
                    self.output.append(d)

            newline_tags = {"code", "placeholdertag"}

            def handle_endtag(self, tag: str):
                if self.tag_stack and \
                        tag == self.tag_stack[-1]:
                
                    self.tag_stack.pop()

                if self.markdown and not self.tag_stack:
                    if tag in ResultParser.newline_tags:
                        self.output.append("{{NEWL}}")


            def handle_starttag(self, tag, attrs):
                flag = True
                for x in attrs:
                    if self.tag_stack:
                        continue
                    
                    if "display: none;" in x:
                        self.tag_stack.append(tag)
                        continue

                    if self.markdown and not self.tag_stack:
                        if tag in ResultParser.newline_tags:
                            self.output.append("{{NEWL}}")
                    
                    if "class" in x and not markdown:
                        if flag:
                            self.output.append([x[1]])
                        else:
                            self.output[-1].append(x[1])
                        flag = False



        rp = ResultParser()
        rp.feed(result)
        result = rp.output
        if markdown:
                         #jesus christ what is this why did i write this who let me write this
            return [ResultText(text="\n".join([a for a in (
                                                "".join([a for b in result for a in b 
                                                if "cm-" not in a and a])).split("\n") if a != ""])
                                                .replace("{{NEWL}}", "\n"))]

        result_text_list = []
        text_mod = ("", "")

        for x in result:
            trigger_classes = {
                "run-output__body": ("\n", ""),
                "run-results": ("\n-", "-\n"),
                "result-type--time": ("", "\n"),
                "run-tip": ("\n", ""),
                "result-type__chevron":  ("\n", ""),
                "run-results__congrats": ("\n############################################\n\n",
                                          "\n\n############################################")
                                         
            }

            if x[0] in trigger_classes:
                (text_mod) = trigger_classes[x[0]]

            if len(x) > 1:
                joined = "".join(x[1:]).strip()
                element_class = x[0]
                text_color = "\033[97m"

                if "failed" in element_class:
                    text_color = "\033[91m"

                if "passed" in element_class:
                    text_color = "\033[92m"

                if "Test Results:" in joined:
                    joined = "Test Results"

                if "STDERR" in joined or "Traceback" in joined:
                    text_color = "\033[91m"

                if "passed" in joined:
                    text_color = "\033[92m"

                result_text_list.append(ResultText(
                    text=f"{text_mod[0]}{joined}{text_mod[1]}",
                    color_shell=text_color,
                    markdown_tags=[]
                ))

                text_mod = ("", "")

        return result_text_list


    def parse_description(self, description: str) -> str:
        return self.parse_result(description, markdown=True)


    def script_paste_solution_code(self, code: str) -> str:
        js_code = textwrap.dedent(\
        f"""
        var solution_code_abcdefg = `{code}`
        var solutionBox = document.querySelector('.CodeMirror');
        var codeMirrorInstance = solutionBox.CodeMirror;
        codeMirrorInstance.setValue(solution_code_abcdefg);
        """)

        return js_code


    def script_get_embedded_code(self) -> str:
        js_code = textwrap.dedent(\
        f"""
        var solutionBox = document.querySelector('.CodeMirror');
        var codeMirrorInstance = solutionBox.CodeMirror;
        return codeMirrorInstance.getValue();
        """)

        return js_code


    def script_test_solution(self) -> str:
        return "document.getElementById('validate_btn').click();"


    def script_submit_solution(self) -> str:
        return "document.getElementById('attempt_btn').click();"


    def script_get_description(self) -> str:
        return "return document.getElementById('description').innerHTML;"


    def script_get_result_output(self) -> str:
        return (run_script_until_valid, "return document.getElementById('runner_frame');",
                switch_to_frame, "return document.querySelector('.run-output').outerHTML;")


    def script_get_result_ready_element(self) -> str | tuple[function | str]:
        return (run_script_until_valid, "return document.getElementById('runner_frame');",
                switch_to_frame, "return document.querySelector('.run-results').outerHTML;")


# Leetcode = LeetcodeDefinition(
#     identifier="Leetcode",
#     specifications=WebsiteSpecifications(
#         url_root="https://leetcode.com/",
#         session_cookies=["LEETCODE_SESSION", "csrftoken"]
#     )
# )


Codewars = CodewarsDefinition(
    identifier="Codewars",
    specifications=WebsiteSpecifications(
        url_root="https://www.codewars.com",
        session_cookies=["remember_user_token", "CSRF-TOKEN", "_session_id"]
    )
)