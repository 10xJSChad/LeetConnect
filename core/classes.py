from __future__ import annotations
from dataclasses import dataclass


@dataclass
class ResultText:
    text: str = None
    color_shell: str = "\033[97m"
    markdown_tags: list[str] = None


@dataclass
class WebsiteSpecifications:
    # This class should probably just be deleted
    # and merged into WebsiteDefinition
    url_root: str
    session_cookies: list


class WebsiteDefinition:
    # This class should be renamed.

    definitions_dict = {}

    def __init__(self, identifier: str, specifications: WebsiteSpecifications,
                 allow_forced_setup: bool = True) -> None:

        self.identifier = identifier
        self.specifications = specifications
        self.allow_forced_setup = allow_forced_setup
        self.add_to_definitions_dict()


    def add_to_definitions_dict(self) -> None:
        WebsiteDefinition.definitions_dict[self.identifier.lower()] = self


    @classmethod
    def get_definition_from_string(cls, definition_str: str) -> WebsiteDefinition:
        definition_str = definition_str.lower()

        return None if definition_str not in cls.definitions_dict \
                                      else cls.definitions_dict[definition_str]

    def parse_result(self, result: str) -> str: pass
    def parse_description(self, description: str) -> str: pass
    def script_get_embedded_code(self) -> str: pass
    def script_paste_solution_code(self) -> str: pass
    def script_test_solution(self) -> str: pass
    def script_submit_solution(self) -> str: pass
    def script_get_description(self) -> str: pass
    def script_get_result_output(self) -> str: pass
    def script_get_result_ready_element(self) -> str: pass