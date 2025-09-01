"""Comprehensive metrics calculator for τ²-bench results."""
import pandas as pd

from tau2_ext.metrics.metric_results import MetricResults
from tau2_ext.metrics.per_tool_prf import PerToolPRFMetric
from tau2_ext.metrics.tool_criticality import ToolCriticalityMetric
from tau2_ext.metrics.sequence_compliance import SequenceComplianceMetric
from tau2_ext.metrics.complexity_metrics import ComplexityMetrics
from tau2_ext.data_processing.tool_schema_loader import ToolSchemaLoader


class MetricsCalculator:
    """Calculate comprehensive metrics for τ²-bench results."""
    
    def __init__(self, tau2_bench_path: str = "/Users/AdminDK/code/tau2-bench"):
        self.tool_schema_loader = ToolSchemaLoader(tau2_bench_path)
        
        # Initialize metric calculators
        self.per_tool_prf = PerToolPRFMetric(self.tool_schema_loader)
        self.tool_criticality = ToolCriticalityMetric(self.tool_schema_loader)
        self.sequence_compliance = SequenceComplianceMetric()
        self.complexity_metrics = ComplexityMetrics()
    
    def calculate_per_tool_prf(self, df: pd.DataFrame) -> pd.DataFrame:
        """Metric 1: Per-tool Precision/Recall/F1/Omission."""
        return self.per_tool_prf.calculate(df)
    
    def calculate_tool_criticality(self, df: pd.DataFrame) -> pd.DataFrame:
        """Metric 2: Tool Criticality Index (TCI)."""
        return self.tool_criticality.calculate(df)
    
    def calculate_sequence_compliance(self, df: pd.DataFrame) -> pd.DataFrame:
        """Metric 3: Sequence Compliance (nPED + Position Deviation)."""
        return self.sequence_compliance.calculate(df)
    
    def calculate_complexity_weighted_pass1(self, df: pd.DataFrame) -> float:
        """Metric 4a: Complexity-weighted pass@1."""
        return self.complexity_metrics.calculate_complexity_weighted_pass1(df)
    
    def calculate_bucket_pass1(self, df: pd.DataFrame) -> pd.DataFrame:
        """Metric 4b: Pass@1 by complexity bucket."""
        return self.complexity_metrics.calculate_bucket_pass1(df)
    
    def calculate_all_metrics(self, df: pd.DataFrame) -> MetricResults:
        """Calculate all metrics at once."""
        return MetricResults(
            per_tool_prf=self.calculate_per_tool_prf(df),
            tool_criticality=self.calculate_tool_criticality(df),
            sequence_compliance=self.calculate_sequence_compliance(df),
            complexity_weighted_pass1=self.calculate_complexity_weighted_pass1(df),
            bucket_pass1=self.calculate_bucket_pass1(df)
        )
