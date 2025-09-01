"""Comprehensive metrics calculator for τ²-bench results."""
import pandas as pd
import numpy as np
from collections import defaultdict
from typing import Dict, List, Tuple
from scipy import stats

from metrics.utils import wilson_ci, levenshtein
from metrics.metric_results import MetricResults


class MetricsCalculator:
    """Calculate comprehensive metrics for τ²-bench results."""
    
    # Key arguments for each tool type
    KEY_ARGS = {
        "get_order_details": ["order_id"],
        "cancel_pending_order": ["order_id", "reason"],
        "return_delivered_order_items": ["order_id", "item_ids"],
        "exchange_delivered_order_items": ["order_id", "item_ids", "new_item_ids"],
        "modify_pending_order_items": ["order_id", "item_ids", "new_item_ids"],
        "modify_pending_order_address": ["order_id", "address1", "city", "state", "zip"],
        "find_user_id_by_email": ["email"],
        "find_user_id_by_name_zip": ["first_name", "last_name", "zip"],
        "get_user_details": ["user_id"],
        "get_product_details": ["product_id"],
        "calculate": ["expression"],
    }
    
    def _tool_seq(self, lst: List[Dict]) -> List[str]:
        """Extract tool names from tool list."""
        return [x.get("name", "") for x in (lst or []) if x.get("name")]
    
    def _args_match(self, name: str, exp_args: Dict, act_args: Dict) -> bool:
        """Check if arguments match for a given tool."""
        keys = self.KEY_ARGS.get(name, [])
        return all(
            k in exp_args and k in act_args and exp_args[k] == act_args[k] 
            for k in keys
        )
    
    def _group_tools_by_name(self, tools: List[Dict]) -> Dict[str, List[Dict]]:
        """Group tools by name and extract their arguments."""
        grouped = defaultdict(list)
        for tool in tools:
            grouped[tool.get("name", "")].append(tool.get("arguments", {}))
        return grouped
    
    def _greedy_match_tools(self, gt_list: List[Dict], ex_list: List[Dict], tool_name: str) -> int:
        """Count true positives using greedy matching algorithm."""
        tp = 0
        used = [False] * len(ex_list)
        
        for gt_args in gt_list:
            match_idx = None
            for j, ex_args in enumerate(ex_list):
                if not used[j] and self._args_match(tool_name, gt_args, ex_args):
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
    
    def calculate_per_tool_prf(self, df: pd.DataFrame) -> pd.DataFrame:
        """Metric 1: Per-tool Precision/Recall/F1/Omission."""
        rows = []
        
        for _, row in df.iterrows():
            gt_tools = row.get("gt_tools", []) or []
            executed_tools = row.get("executed_tools", []) or []
            
            # Group by tool name
            gt_by_name = self._group_tools_by_name(gt_tools)
            ex_by_name = self._group_tools_by_name(executed_tools)
            
            # Calculate metrics for each tool
            all_tools = set(list(gt_by_name.keys()) + list(ex_by_name.keys()))
            
            for tool in all_tools:
                gt_list = gt_by_name[tool].copy()
                ex_list = ex_by_name[tool].copy()
                
                # Count true positives via greedy matching
                tp = self._greedy_match_tools(gt_list, ex_list, tool)
                
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
    

    def calculate_tool_criticality(self, df: pd.DataFrame) -> pd.DataFrame:
        """Metric 2: Tool Criticality Index (TCI) with confidence intervals."""
        flags = []
        
        for _, row in df.iterrows():
            gt_tools = row.get("gt_tools", []) or []
            executed_tools = row.get("executed_tools", []) or []
            success = int(row.get("success", False))
            
            gt_names = [g.get("name", "") for g in gt_tools]
            
            # Calculate per-tool correctness
            for tool in set(gt_names):
                gt_args_list = [g.get("arguments", {}) for g in gt_tools if g.get("name") == tool]
                correct = 0
                
                for gargs in gt_args_list:
                    if any(self._args_match(tool, gargs, e.get("arguments", {})) 
                           for e in executed_tools if e.get("name") == tool):
                        correct = 1
                        break
                
                flags.append({
                    "tool": tool,
                    "correct": correct,
                    "success": success
                })
        
        # Calculate TCI with confidence intervals
        f = pd.DataFrame(flags)
        if len(f) > 0:
            rows = []
            for tool in f["tool"].unique():
                tool_data = f[f["tool"] == tool]
                
                # Calculate success rates for correct vs incorrect
                correct_data = tool_data[tool_data["correct"] == 1]
                incorrect_data = tool_data[tool_data["correct"] == 0]
                
                n_correct = len(correct_data)
                n_incorrect = len(incorrect_data)
                
                if n_correct > 0 and n_incorrect > 0:
                    # Success rates
                    p_correct = correct_data["success"].mean()
                    p_incorrect = incorrect_data["success"].mean()
                    
                    # TCI
                    tci = p_correct - p_incorrect
                    
                    # Confidence intervals for each proportion
                    k_correct = correct_data["success"].sum()
                    k_incorrect = incorrect_data["success"].sum()
                    
                    try:
                        ci_correct = stats.proportion_conf_int(k_correct, n_correct, method='wilson')
                        ci_incorrect = stats.proportion_conf_int(k_incorrect, n_incorrect, method='wilson')
                    except AttributeError:
                        # Manual Wilson CI calculation
                        z = 1.96
                        ci_correct = wilson_ci(k_correct, n_correct, z)
                        ci_incorrect = wilson_ci(k_incorrect, n_incorrect, z)
                    
                    # Propagate uncertainty for TCI (difference of proportions)
                    # Var(diff) = Var(p1) + Var(p2) - 2*Cov(p1,p2)
                    # Assuming independence: Var(diff) = Var(p1) + Var(p2)
                    var_correct = (ci_correct[1] - ci_correct[0])**2 / (4 * z**2)
                    var_incorrect = (ci_incorrect[1] - ci_incorrect[0])**2 / (4 * z**2)
                    var_tci = var_correct + var_incorrect
                    
                    tci_se = np.sqrt(var_tci)
                    tci_ci_lower = tci - z * tci_se
                    tci_ci_upper = tci + z * tci_se
                    
                    rows.append({
                        "tool": tool,
                        "TCI": tci,
                        "TCI_ci_lower": tci_ci_lower,
                        "TCI_ci_upper": tci_ci_upper,
                        "p_correct": p_correct,
                        "p_incorrect": p_incorrect,
                        "n_correct": n_correct,
                        "n_incorrect": n_incorrect
                    })
            
            return pd.DataFrame(rows)
        else:
            return pd.DataFrame(columns=["tool", "TCI", "TCI_ci_lower", "TCI_ci_upper", "p_correct", "p_incorrect", "n_correct", "n_incorrect"])
    

    def calculate_sequence_compliance(self, df: pd.DataFrame) -> pd.DataFrame:
        """Metric 3: Sequence Compliance (nPED + Position Deviation)."""
        rows = []
        
        for _, row in df.iterrows():
            gt_tools = row.get("gt_tools", []) or []
            executed_tools = row.get("executed_tools", []) or []
            
            gt_names = self._tool_seq(gt_tools)
            ex_names = self._tool_seq(executed_tools)
            
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
    

    def calculate_complexity_weighted_pass1(self, df: pd.DataFrame) -> float:
        """Metric 4a: Complexity-weighted pass@1."""
        wsum = (df["success"] * df["exp_plan_len"]).sum()
        denom = df["exp_plan_len"].sum()
        return float(wsum / max(1, denom))
    

    def calculate_bucket_pass1(self, df: pd.DataFrame) -> pd.DataFrame:
        """Metric 4b: Pass@1 by complexity bucket."""
        bins = pd.cut(
            df["exp_plan_len"], 
            bins=[0, 2, 5, 1e9], 
            labels=["simple", "medium", "complex"], 
            include_lowest=True
        )
        return df.groupby(bins)["success"].mean().rename("pass@1").reset_index()
    

    def calculate_all_metrics(self, df: pd.DataFrame) -> MetricResults:
        """Calculate all metrics at once."""
        return MetricResults(
            per_tool_prf=self.calculate_per_tool_prf(df),
            tool_criticality=self.calculate_tool_criticality(df),
            sequence_compliance=self.calculate_sequence_compliance(df),
            complexity_weighted_pass1=self.calculate_complexity_weighted_pass1(df),
            bucket_pass1=self.calculate_bucket_pass1(df)
        )
