from workflow.agents.agent import Agent
from workflow.system_state import SystemState

from workflow.agents.ambiguity_detector.tool_kit.detect_scope import DetectScope
from workflow.agents.ambiguity_detector.tool_kit.detect_attach import DetectAttach
from workflow.agents.ambiguity_detector.tool_kit.detect_vague import DetectVague
from workflow.agents.ambiguity_detector.tool_kit.remove_duplicates import RemoveDuplicates

class AmbiguityDetector(Agent):
    """
    Agent responsible for detecting ambiguity in the question.
    """
    
    def __init__(self, config: dict):
        """Initialize the tools needed for ambiguity detection"""
        super().__init__(
            name="Ambiguity Detector",
            task=("detect ambiguity in the question (scope, attachment, vagueness) and ",
                         "generate a list of possible interpretations for the entire question."),
            config=config
        )
        
        self.tools = {
            "detect_scope": DetectScope(**config["tools"]["detect_scope"]),
            "detect_attach": DetectAttach(**config["tools"]["detect_attach"]),
            "detect_vague": DetectVague(**config["tools"]["detect_vague"]),
            "remove_duplicates": RemoveDuplicates(**config["tools"]["remove_duplicates"])
        }