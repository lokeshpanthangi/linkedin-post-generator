from typing import TypedDict, List, Dict, Optional, Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):

    user_input: str
    generator: str 
    evaluators: List[str] 
    generated_post: Optional[str]
    evaluations: Dict[str, str]
    human_interrupt_confirmed: bool 
    human_interrupt_reason: Annotated[List[str], add_messages]