"""Sequence Compliance (nPED + Position Deviation) calculation."""

import pandas as pd
import numpy as np

from tau2_ext.metrics.utils import tool_seq, levenshtein


class SequenceComplianceMetric:
    """Calculate Sequence Compliance metrics."""
    
    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate Sequence Compliance (nPED + Position Deviation)."""
        rows = []
        
        for _, row in df.iterrows():
            gt_tools = row.get("gt_tools", []) or []
            executed_tools = row.get("executed_tools", []) or []
            
            gt_names = tool_seq(gt_tools)
            ex_names = tool_seq(executed_tools)
            
            # Calculate normalized edit distance
            ped = levenshtein(gt_names, ex_names)
            nPED = ped / max(1, len(gt_names))
            
            # Calculate position deviation
            pos_dev = []
            ex_index = {name: i for i, name in enumerate(ex_names)}
            
            for i, name in enumerate(gt_names):
                if name in ex_index:
                    pos_dev.append(abs(ex_index[name] - i))
            
            PD = np.mean(pos_dev) if pos_dev else np.nan
            
            rows.append({
                "task_id": row.get("task_id", ""),
                "trial_id": row.get("trial_id", ""),
                "success": int(row.get("success", False)),
                "nPED": nPED,
                "PD": PD,
                "exp_plan_len": row.get("exp_plan_len", 0),
                "domain": row.get("domain", "")
            })
        
        return pd.DataFrame(rows)
