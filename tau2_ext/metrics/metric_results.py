from dataclasses import dataclass
import pandas as pd

@dataclass
class MetricResults:
    """Container for all calculated metrics."""
    per_tool_prf: pd.DataFrame
    tool_criticality: pd.DataFrame
    sequence_compliance: pd.DataFrame
    complexity_weighted_pass1: float
    bucket_pass1: pd.DataFrame
