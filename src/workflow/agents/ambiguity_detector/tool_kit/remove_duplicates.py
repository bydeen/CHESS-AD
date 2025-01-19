from typing import Dict
from tabulate import tabulate

from llm.models import get_llm_chain, async_llm_chain_call
from llm.prompts import get_prompt
from llm.parsers import get_parser
from workflow.system_state import SystemState
from workflow.agents.tool import Tool

class RemoveDuplicates(Tool):
    """
    Tool for removing redundant interpretations.
    """
    
    def __init__(self, mode: str, template_name: str = None, engine_config: str = None, parser_name: str = None):
        super().__init__()
        self.mode = mode
        self.template_name = template_name
        self.engine_config = engine_config
        self.parser_name = parser_name
        
    def _run(self, state: SystemState):
        request_kwargs = {
            "DATABASE_SCHEMA": state.get_schema_string(schema_type="tentative"),
            "INTERPRETATIONS": state.unambiguous_questions,
        }
        
        response = async_llm_chain_call(
            prompt=get_prompt(template_name=self.template_name),
            engine=get_llm_chain(**self.engine_config),
            parser=get_parser(self.parser_name),
            request_list=[request_kwargs],
            step=self.tool_name,
        )[0]
        
        state.unambiguous_questions = response[0].get("interpretations", [])
        state.example_tables = response[0].get("example_tables", [])
        
        for idx, (interpretation, table) in enumerate(zip(state.unambiguous_questions, state.example_tables), start=1):
            print(f"\nInterpretation {idx}: {interpretation}")
            headers = table.get("headers", [])
            data = table.get("data", [])
            example_table = tabulate(data, headers=headers, tablefmt="grid")
            print(f"{example_table}\n")
        
        if state.user_selection:
            self.choose_interpretation(state)

    def _get_updates(self, state: SystemState) -> Dict:
        return {"unambiguous_questions": state.unambiguous_questions, "example_tables": state.example_tables}
    
    def choose_interpretation(self, state: SystemState):
        """
        Allows the user to select a specific interpretation.

        Args:
            state (SystemState): The interpretations and example tables.
        """
        user_input = input("\nSelect an interpretation by entering its number, or press Enter to process all interpretations: ")
        if user_input.isdigit():
            choice = int(user_input)
            if 1 <= choice <= len(state.unambiguous_questions):
                print(f"\nProcessing interpretation {choice}...\n")
                selected = state.unambiguous_questions[choice - 1]
                state.unambiguous_questions = [selected]
            else:
                print("\nProcessing all interpretations...\n")
        else:
            print("\nProcessing all interpretations...\n")
