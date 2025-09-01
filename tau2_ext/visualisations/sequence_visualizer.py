"""Sequence Compliance visualizer."""

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from typing import Optional

from tau2_ext.visualisations.base_visualizer import BaseVisualizer


class SequenceVisualizer(BaseVisualizer):
    """Visualizer for Sequence Compliance metrics."""
    
    def plot_nped_by_domain(self, seq_df: pd.DataFrame, 
                           title: str = "Sequence Compliance by Domain and Outcome",
                           save_path: Optional[Path] = None):
        """Plot nPED boxplot by domain and success/failure."""
        domains = seq_df["domain"].unique()
        fig, axes = self._setup_domain_subplots(domains, figsize_per_domain=(5, 6))
        
        for i, domain in enumerate(domains):
            domain_data = seq_df[seq_df["domain"] == domain]
            
            data = [
                domain_data[domain_data.success == 0]["nPED"].dropna(),
                domain_data[domain_data.success == 1]["nPED"].dropna()
            ]
            
            axes[i].boxplot(data, labels=["Failure", "Success"])
            axes[i].set_ylabel("nPED")
            axes[i].set_title(f"{domain} Domain")
            self._add_grid_and_styling(axes[i])
        
        plt.suptitle(title)
        plt.tight_layout()
        
        if save_path:
            self._save_figure(save_path)
        else:
            plt.show()
    
    def plot_nped_simple(self, seq_df: pd.DataFrame, 
                        title: str = "Sequence Compliance by Outcome",
                        save_path: Optional[Path] = None):
        """Plot simple nPED boxplot by success/failure."""
        data = [
            seq_df[seq_df.success == 0]["nPED"].dropna(),
            seq_df[seq_df.success == 1]["nPED"].dropna()
        ]
        
        plt.figure(figsize=(8, 6))
        plt.boxplot(data, labels=["Failure", "Success"])
        plt.ylabel("nPED")
        plt.title(title)
        plt.tight_layout()
        
        if save_path:
            self._save_figure(save_path)
        else:
            plt.show()
