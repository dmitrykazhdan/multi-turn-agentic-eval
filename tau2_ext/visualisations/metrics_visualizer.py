import matplotlib.pyplot as plt
from typing import Optional
from pathlib import Path
from tau2_ext.metrics.metric_results import MetricResults
import pandas as pd

from tau2_ext.visualisations.base_visualizer import BaseVisualizer
from tau2_ext.visualisations.tci_visualizer import TCIVisualizer
from tau2_ext.visualisations.prf_visualizer import PRFVisualizer
from tau2_ext.visualisations.sequence_visualizer import SequenceVisualizer
from tau2_ext.visualisations.complexity_visualizer import ComplexityVisualizer


class MetricsVisualizer(BaseVisualizer):
    """Create visualizations for the calculated metrics."""
    
    def __init__(self):
        super().__init__()
        self.tci_visualizer = TCIVisualizer()
        self.prf_visualizer = PRFVisualizer()
        self.sequence_visualizer = SequenceVisualizer()
        self.complexity_visualizer = ComplexityVisualizer()
    
    def plot_tci_bar_by_domain(self, tci_df: pd.DataFrame, df: pd.DataFrame, k: int = 10, title: str = "Tool Criticality Index by Domain", save_path: Optional[Path] = None):
        """Plot TCI bar chart with confidence intervals, separated by domain."""
        return self.tci_visualizer.plot_by_domain(tci_df, df, k, title, save_path)
    
    def plot_precision_omission_by_domain(self, prf_df: pd.DataFrame, df: pd.DataFrame, title: str = "Precision vs Recall by Domain", save_path: Optional[Path] = None):
        """Plot standard PR curve with circle size reflecting omission rate."""
        return self.prf_visualizer.plot_precision_recall_by_domain(prf_df, df, title, save_path)
    
    def plot_nped_box_by_domain(self, seq_df: pd.DataFrame, title: str = "Sequence Compliance by Domain and Outcome", save_path: Optional[Path] = None):
        """Plot nPED boxplot by domain and success/failure."""
        return self.sequence_visualizer.plot_nped_by_domain(seq_df, title, save_path)
    
    def plot_bucket_pass1_by_domain(self, bucket_df: pd.DataFrame, df: pd.DataFrame, title: str = "Pass@1 by Plan Complexity and Domain", save_path: Optional[Path] = None):
        """Plot pass@1 by complexity bucket with separate subplots for each domain and confidence intervals."""
        return self.complexity_visualizer.plot_bucket_pass1_by_domain(bucket_df, df, title, save_path)
    
    def plot_all_metrics_by_domain(self, results: MetricResults, df: pd.DataFrame, save_dir: Optional[str] = None):
        """Create all visualizations with domain separation."""
        if save_dir:
            figures_dir = self._create_timestamped_dir(save_dir)
        else:
            figures_dir = None
        
        # Plot 1: TCI by domain
        tci_path = figures_dir / "tci_by_domain.png" if figures_dir else None
        self.plot_tci_bar_by_domain(results.tool_criticality, df, save_path=tci_path)
        
        # Plot 2: Precision vs Recall by domain
        prf_path = figures_dir / "precision_recall_by_domain.png" if figures_dir else None
        self.plot_precision_omission_by_domain(results.per_tool_prf, df, save_path=prf_path)
        
        # Plot 3: nPED boxplot by domain
        nped_path = figures_dir / "nped_by_domain.png" if figures_dir else None
        self.plot_nped_box_by_domain(results.sequence_compliance, save_path=nped_path)
        
        # Plot 4: Bucket pass@1 by domain
        bucket_path = figures_dir / "bucket_pass1_by_domain.png" if figures_dir else None
        self.plot_bucket_pass1_by_domain(results.bucket_pass1, df, save_path=bucket_path)
        
        # Show plots if not saving
        if not save_dir:
            plt.show()
        else:
            plt.close('all')  # Close all figures when saving
    
    def plot_tci_bar(self, tci_df: pd.DataFrame, k: int = 10, title: str = "Tool Criticality Index (Top-k)", save_path: Optional[Path] = None):
        """Plot TCI bar chart."""
        return self.tci_visualizer.plot_simple(tci_df, k, title, save_path)
    
    def plot_precision_omission(self, prf_df: pd.DataFrame, title: str = "Precision vs Omission (per tool)", save_path: Optional[Path] = None):
        """Plot precision vs omission scatter."""
        return self.prf_visualizer.plot_precision_omission(prf_df, title, save_path)
    
    def plot_nped_box(self, seq_df: pd.DataFrame, title: str = "Sequence Compliance by Outcome", save_path: Optional[Path] = None):
        """Plot nPED boxplot by success/failure."""
        return self.sequence_visualizer.plot_nped_simple(seq_df, title, save_path)
    
    def plot_bucket_pass1(self, bucket_df: pd.DataFrame, title: str = "Pass@1 by Plan Complexity", save_path: Optional[Path] = None):
        """Plot pass@1 by complexity bucket."""
        return self.complexity_visualizer.plot_bucket_pass1_simple(bucket_df, title, save_path)
    
    def plot_all_metrics(self, results: MetricResults, save_path: Optional[str] = None):
        """Create all visualizations."""
        self.plot_tci_bar(results.tool_criticality, save_path=save_path)
        self.plot_precision_omission(results.per_tool_prf, save_path=save_path)
        self.plot_nped_box(results.sequence_compliance, save_path=save_path)
        self.plot_bucket_pass1(results.bucket_pass1, save_path=save_path)
        
        if not save_path:
            plt.show()

