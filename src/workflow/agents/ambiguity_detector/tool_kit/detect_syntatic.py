from typing import Dict

from llm.models import get_llm_chain, async_llm_chain_call
from llm.prompts import get_prompt
from workflow.system_state import SystemState
from workflow.agents.tool import Tool

class DetectSyntatic(Tool):
    """
    Tool for detecting syntactic ambiguity in the question.
    """
    
    def __init__(self, template_name: str = None, engine_config: str = None):
        super().__init__()
        
        self.template_name = template_name
        self.engine_config = engine_config
        
    def _run(self, state: SystemState):
        request_kwargs = {
            "QUESTION": state.task.question,
        }
        
        response = async_llm_chain_call(
            prompt=get_prompt(template_name=self.template_name),
            engine=get_llm_chain(**self.engine_config),
            request_list=[request_kwargs],
            step=self.tool_name,
            sampling_count=1
        )[0]
        
        state.syntactic_ambiguity = response[0]
        
    def _get_updates(self, state: SystemState) -> Dict:
        return {"syntactic_ambiguity": state.syntactic_ambiguity}