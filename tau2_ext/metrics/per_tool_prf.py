"""Per-tool Precision/Recall/F1/Omission calculation."""

import numpy as np
import pandas as pd
from typing import List, Dict

from tau2_ext.metrics.utils import group_tools_by_name


class PerToolPRFMetric:
    """Calculate per-tool Precision/Recall/F1/Omission metrics."""
    
    def __init__(self, tool_schema_loader):
        self.tool_schema_loader = tool_schema_loader
    
    def _args_match(self, name: str, exp_args: Dict, act_args: Dict, domain: str) -> bool:
        """Check if arguments match for a given tool."""
        keys = self.tool_schema_loader.get_tool_schema(domain, name)
        
        # Use schema info for matching
        return all(
            k in exp_args and k in act_args and exp_args[k] == act_args[k] 
            for k in keys
        )
    
    def _greedy_match_tools(self, gt_list: List[Dict], ex_list: List[Dict], tool_name: str, domain: str) -> int:
        """Count true positives using greedy matching algorithm."""
        tp = 0
        used = [False] * len(ex_list)
        
        for gt_args in gt_list:
            match_idx = None
            for j, ex_args in enumerate(ex_list):
                if not used[j] and self._args_match(tool_name, gt_args, ex_args, domain):
                    match_idx = j
                    break
            if match_idx is not None:
                tp += 1
                used[match_idx] = True
        
        return tp
    
    def _calculate_prf_metrics(self, agg_df: pd.DataFrame) -> pd.DataFrame:
        """Calculate precision, recall, F1, and omission rate from aggregated TP/FP/FN counts."""
        agg_df["precision"] = agg_df["tp"] / (agg_df["tp"] + agg_df["fp"]).replace(0, np.nan)
        agg_df["recall"] = agg_df["tp"] / (agg_df["tp"] + agg_df["fn"]).replace(0, np.nan)
        agg_df["f1"] = 2 * (agg_df["precision"] * agg_df["recall"]) / (agg_df["precision"] + agg_df["recall"])
        agg_df["omission_rate"] = agg_df["fn"] / agg_df["requires_tool"].replace(0, np.nan)
        return agg_df

    
    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate per-tool Precision/Recall/F1/Omission metrics."""
        rows = []
        
        for _, row in df.iterrows():
            gt_tools = row.get("gt_tools", []) or []
            executed_tools = row.get("executed_tools", []) or []
            
            # Group by tool name
            gt_by_name = group_tools_by_name(gt_tools)
            ex_by_name = group_tools_by_name(executed_tools)
            
            # Calculate metrics for each tool
            all_tools = set(list(gt_by_name.keys()) + list(ex_by_name.keys()))
            
            for tool in all_tools:
                gt_list = gt_by_name[tool].copy()
                ex_list = ex_by_name[tool].copy()
                
                # Count true positives via greedy matching
                tp = self._greedy_match_tools(gt_list, ex_list, tool, row.get("domain"))
                
                fn = max(0, len(gt_list) - tp)
                fp = max(0, len(ex_list) - tp)
                
                rows.append({
                    "tool": tool,
                    "tp": tp,
                    "fp": fp,
                    "fn": fn,
                    "requires_tool": int(len(gt_list) > 0)
                })
        
        # Aggregate and calculate final metrics
        agg = pd.DataFrame(rows).groupby("tool").sum(numeric_only=True)
        agg = self._calculate_prf_metrics(agg)
        
        return agg.reset_index()
