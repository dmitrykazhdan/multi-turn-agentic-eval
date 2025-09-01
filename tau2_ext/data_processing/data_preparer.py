"""Data preparation for τ²-bench metrics analysis."""
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List

from tau2_ext.data_processing.conversation_data import ConversationData
from tau2_ext.data_processing.task_loader import TaskLoader

class DataPreparer:
    """Prepare conversation data for metrics analysis."""
    
    def __init__(self, tau2_bench_path: str = "/Users/AdminDK/code/tau2-bench"):
        self.tau2_bench_path = Path(tau2_bench_path)
        self.task_loader = TaskLoader(tau2_bench_path)
    

    def _extract_actual_tools(self, conversation_data: Dict) -> List[Dict]:
        """Extract actual tools used in a conversation."""
        executed_tools = []
        
        messages = conversation_data.get("messages", [])
        for msg in messages:
            if msg.get("role") == "assistant":
                tool_calls = msg.get("tool_calls")
                if tool_calls:
                    for tool_call in tool_calls:
                        if isinstance(tool_call, dict):
                            executed_tools.append({
                                "name": tool_call.get("name", ""),
                                "arguments": tool_call.get("arguments", {}),
                                "status": "ok",  
                                "error": None
                            })
        
        return executed_tools
    
    
    def _extract_task_id(self, conversation_data: Dict) -> str:
        """Extract task_id from conversation data."""
        if "task_id" in conversation_data:
            return str(conversation_data["task_id"])
        
        raise ValueError("task_id not found in conversation data")
    

    def _extract_domain_from_filename(self, filename: str) -> str:
        """Extract domain from simulation filename."""
        # Filename format: timestamp_domain_llm_agent_...json
        parts = filename.split("_")
        if len(parts) >= 2:
            return parts[1]  # Second part should be domain
        return "unknown"


    def _extract_success_status(self, conversation_data: Dict) -> bool:
        """Extract whether the conversation was successful."""
        reward_info = conversation_data.get("reward_info", {})
        if isinstance(reward_info, dict) and "reward" in reward_info:
            return float(reward_info["reward"]) > 0
        
        termination_reason = conversation_data.get("termination_reason", "")
        if termination_reason:
            return "success" in str(termination_reason).lower()
        
        reward = conversation_data.get("reward", 0)
        return float(reward) > 0
    

    def _extract_conversation_metrics(self, conversation_data: Dict) -> Dict:
        """Extract basic conversation metrics."""
        messages = conversation_data.get("messages", [])
        n_turns = len(messages)
        
        n_tool_calls = 0
        n_tool_success = 0
        n_tool_errors = 0
        
        for msg in messages:
            if msg.get("role") == "assistant":
                tool_calls = msg.get("tool_calls")
                if tool_calls:
                    n_tool_calls += len(tool_calls)
                    n_tool_success += len(tool_calls)
        
        return {
            "n_turns": n_turns,
            "n_tool_calls": n_tool_calls,
            "n_tool_success": n_tool_success,
            "n_tool_errors": n_tool_errors,
            "duration": conversation_data.get("duration", 0.0),
            "total_cost": conversation_data.get("total_cost", 0.0),
            "agent_cost": conversation_data.get("agent_cost", 0.0),
            "user_cost": conversation_data.get("user_cost", 0.0)
        }
    

    def prepare_conversation_data(self, conversation_data: Dict, domain: str = None) -> ConversationData:
        """Prepare a single conversation for analysis."""

        task_id = self._extract_task_id(conversation_data)
        # Domain should always be provided from filename extraction
        if not domain:
            raise ValueError("Domain must be provided when preparing conversation data")
        success = self._extract_success_status(conversation_data)
        
        # Get expected tools using task loader
        gt_tools = self.task_loader.get_task_tools(domain, task_id)
        exp_plan_len = len(gt_tools)
        
        # Get executed tools
        executed_tools = self._extract_actual_tools(conversation_data)
        
        # Get basic metrics
        metrics = self._extract_conversation_metrics(conversation_data)
        
        # Get messages
        messages = conversation_data.get("messages", [])
        
        return ConversationData(
            conversation_id=conversation_data.get("conversation_id", ""),
            task_id=task_id,
            domain=domain,
            success=success,
            exp_plan_len=exp_plan_len,
            gt_tools=gt_tools,
            executed_tools=executed_tools,
            messages=messages,
            n_turns=metrics["n_turns"],
            n_tool_calls=metrics["n_tool_calls"],
            n_tool_success=metrics["n_tool_success"],
            n_tool_errors=metrics["n_tool_errors"],
            duration=metrics["duration"],
            total_cost=metrics["total_cost"],
            agent_cost=metrics["agent_cost"],
            user_cost=metrics["user_cost"]
        )
    
    
    def prepare_simulation_file(self, simulation_file: str) -> pd.DataFrame:
        """Prepare all conversations from a simulation file."""
        with open(simulation_file, 'r') as f:
            simulation_data = json.load(f)
        
        # Extract domain from filename
        filename = Path(simulation_file).name
        domain = self._extract_domain_from_filename(filename)
        
        conversations = []
        
        # Get simulations from the standard structure
        simulations = simulation_data.get("simulations", [])
        
        for sim in simulations:
            conv_data = self.prepare_conversation_data(sim, domain)
            conversations.append(conv_data)
        
        # Convert to DataFrame
        if conversations:
            df = pd.DataFrame([
                {
                    "conversation_id": c.conversation_id,
                    "task_id": c.task_id,
                    "domain": c.domain,
                    "success": c.success,
                    "exp_plan_len": c.exp_plan_len,
                    "gt_tools": c.gt_tools,
                    "executed_tools": c.executed_tools,
                    "messages": c.messages,
                    "n_turns": c.n_turns,
                    "n_tool_calls": c.n_tool_calls,
                    "n_tool_success": c.n_tool_success,
                    "n_tool_errors": c.n_tool_errors,
                    "duration": c.duration,
                    "total_cost": c.total_cost,
                    "agent_cost": c.agent_cost,
                    "user_cost": c.user_cost
                }
                for c in conversations
            ])
            return df
        else:
            return pd.DataFrame()
    

    def prepare_multiple_simulation_files(self, simulation_files: List[str]) -> pd.DataFrame:
        """Prepare data from multiple simulation files."""
        all_data = []
        
        for file_path in simulation_files:
            df = self.prepare_simulation_file(file_path)
            if not df.empty:
                df["source_file"] = Path(file_path).name
                all_data.append(df)
        
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        else:
            return pd.DataFrame()

