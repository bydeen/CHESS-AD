from typing import Dict

from llm.models import get_llm_chain, async_llm_chain_call
from llm.prompts import get_prompt
from llm.parsers import get_parser
from workflow.system_state import SystemState
from workflow.agents.tool import Tool

class DetectSyntatic(Tool):
    """
    Tool for detecting syntactic ambiguity in the question.
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
            "QUESTION": state.task.question,
            "HINT": state.task.evidence,
        }
        
        response = async_llm_chain_call(
            prompt=get_prompt(template_name=self.template_name),
            engine=get_llm_chain(**self.engine_config),
            parser=get_parser(self.parser_name),
            request_list=[request_kwargs],
            step=self.tool_name,
        )[0]
        
        state.syntactic_ambiguity = response[0]
        print(f"Syntactic ambiguity: {state.syntactic_ambiguity}")
        
    def _get_updates(self, state: SystemState) -> Dict:
        return {"syntactic_ambiguity": state.syntactic_ambiguity}