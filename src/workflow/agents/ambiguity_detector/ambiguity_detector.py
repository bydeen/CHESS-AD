from workflow.agents.agent import Agent
from workflow.system_state import SystemState

from workflow.agents.ambiguity_detector.tool_kit.detect_lexical import DetectLexical
from workflow.agents.ambiguity_detector.tool_kit.detect_syntatic import DetectSyntatic
from workflow.agents.ambiguity_detector.tool_kit.detect_underspec import DetectUnderspec

class AmbiguityDetector(Agent):
    """
    Agent responsible for detecting ambiguity in the question.
    """
    
    def __init__(self, config: dict):
        """Initialize the tools needed for ambiguity detection"""
        super().__init__(
            name="Ambiguity Detector",
            task=("detect ambiguity in the question (lexical, syntatic, underspecification) and ",
                         "generate a list of possible interpretations for the entire question."),
            config=config
        )
        
        self.tools = {
            "detect_lexical": DetectLexical(**config["tools"]["detect_lexical"]),
            "detect_syntatic": DetectSyntatic(**config["tools"]["detect_syntatic"]),
            "detect_underspec": DetectUnderspec(**config["tools"]["detect_underspec"])
        }