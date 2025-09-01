"""Complexity-weighted and Bucketed pass@1 calculations."""

import pandas as pd


class ComplexityMetrics:
    """Calculate complexity-weighted and bucketed pass@1 metrics."""
    
    def calculate_complexity_weighted_pass1(self, df: pd.DataFrame) -> float:
        """Calculate complexity-weighted pass@1."""
        wsum = (df["success"] * df["exp_plan_len"]).sum()
        denom = df["exp_plan_len"].sum()
        return float(wsum / max(1, denom))
    
    def calculate_bucket_pass1(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate pass@1 by complexity bucket."""
        bins = pd.cut(
            df["exp_plan_len"], 
            bins=[0, 2, 5, 1e9], 
            labels=["simple", "medium", "complex"], 
            include_lowest=True
        )
        return df.groupby(bins)["success"].mean().rename("pass@1").reset_index()
