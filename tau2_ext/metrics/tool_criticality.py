"""Tool Criticality Index (TCI) calculation."""

import pandas as pd
from typing import Dict


class ToolCriticalityMetric:
    """Calculate Tool Criticality Index (TCI) metrics."""
    
    def __init__(self, tool_schema_loader):
        self.tool_schema_loader = tool_schema_loader
    
    def _args_match(self, name: str, exp_args: Dict, act_args: Dict, domain: str) -> bool:
        """Check if arguments match for a given tool."""
        keys = self.tool_schema_loader.get_tool_schema(domain, name)
        
        return all(
            k in exp_args and k in act_args and exp_args[k] == act_args[k] 
            for k in keys
        )
    
    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate Tool Criticality Index (TCI)."""
        flags = []
        
        for _, row in df.iterrows():
            gt_tools = row.get("gt_tools", []) or []
            executed_tools = row.get("executed_tools", []) or []
            success = int(row.get("success", False))
            
            gt_names = [g.get("name", "") for g in gt_tools]
            
            for tool in set(gt_names):
                gt_args_list = [g.get("arguments", {}) for g in gt_tools if g.get("name") == tool]
                correct = 0
                
                for gargs in gt_args_list:
                    if any(self._args_match(tool, gargs, e.get("arguments", {}), row.get("domain")) 
                           for e in executed_tools if e.get("name") == tool):
                        correct = 1
                        break
                
                flags.append({
                    "tool": tool,
                    "correct": correct,
                    "success": success
                })
        
        f = pd.DataFrame(flags)
        if len(f) > 0:
            rows = []
            for tool in f["tool"].unique():
                tool_data = f[f["tool"] == tool]
                
                correct_data = tool_data[tool_data["correct"] == 1]
                incorrect_data = tool_data[tool_data["correct"] == 0]
                
                n_correct = len(correct_data)
                n_incorrect = len(incorrect_data)
                
                if n_correct > 0 or n_incorrect > 0:
                    p_correct = correct_data["success"].mean() if n_correct > 0 else 0.0
                    p_incorrect = incorrect_data["success"].mean() if n_incorrect > 0 else 0.0
                    
                    tci = p_correct - p_incorrect
                    
                    rows.append({
                        "tool": tool,
                        "TCI": tci,
                        "p_correct": p_correct,
                        "p_incorrect": p_incorrect,
                        "n_correct": n_correct,
                        "n_incorrect": n_incorrect
                    })
            
            return pd.DataFrame(rows)
        else:
            return pd.DataFrame(columns=["tool", "TCI", "p_correct", "p_incorrect", "n_correct", "n_incorrect"])
