from dataclasses import dataclass
from typing import Dict, List

@dataclass
class ConversationData:
    """Structured conversation data for analysis."""
    conversation_id: str
    task_id: str
    domain: str
    success: bool
    exp_plan_len: int
    gt_tools: List[Dict]
    executed_tools: List[Dict]
    messages: List[Dict]  
    n_turns: int
    n_tool_calls: int
    n_tool_success: int
    n_tool_errors: int
    duration: float
    total_cost: float
    agent_cost: float
    user_cost: float
