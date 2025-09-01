"""Tool Criticality Index (TCI) visualizer."""

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from typing import Optional

from tau2_ext.visualisations.base_visualizer import BaseVisualizer


class TCIVisualizer(BaseVisualizer):
    """Visualizer for Tool Criticality Index (TCI) metrics."""
    
    def plot_by_domain(self, tci_df: pd.DataFrame, df: pd.DataFrame, k: int = 20, 
                      title: str = "Tool Criticality Index by Domain", 
                      save_path: Optional[Path] = None):
        """Plot TCI bar chart separated by domain."""
        domains = df["domain"].unique()
        fig, axes = self._setup_domain_subplots(domains, figsize_per_domain=(8, 6))
        
        for i, domain in enumerate(domains):
            domain_df = df[df["domain"] == domain]
            from tau2_ext.metrics.metrics_calculator import MetricsCalculator
            domain_calculator = MetricsCalculator()
            domain_tci = domain_calculator.calculate_tool_criticality(domain_df)
            
            # Get top k tools for this domain
            top_tools = domain_tci.dropna(subset=["TCI"]).sort_values("TCI", ascending=False).head(k)
            
            if not top_tools.empty:
                # Create simple bar plot without confidence intervals
                tci_values = top_tools["TCI"]
                bars = axes[i].bar(range(len(top_tools)), tci_values, alpha=0.8, color='lightcoral', 
                                 edgecolor='darkred')
                
                axes[i].set_xticks(range(len(top_tools)))
                axes[i].set_xticklabels(top_tools["tool"], rotation=45, ha="right")
                axes[i].set_ylabel("TCI = P(success|correct) − P(success|mis)")
                axes[i].set_title(f"{domain} Domain - Top {k} Tools")
                self._add_grid_and_styling(axes[i])
                
                # Add sample size annotations
                for j, (_, row) in enumerate(top_tools.iterrows()):
                    total_n = row["n_correct"] + row["n_incorrect"]
                    axes[i].text(j, row["TCI"] + 0.02, f'n={total_n}', 
                               ha='center', va='bottom', fontsize=8, fontweight='bold')
                
                # Add horizontal line at y=0 for reference
                axes[i].axhline(y=0, color='black', linestyle='--', alpha=0.5)
                
            else:
                axes[i].text(0.5, 0.5, f"No TCI data for {domain}", ha='center', va='center', transform=axes[i].transAxes)
                axes[i].set_title(f"{domain} Domain")
        
        plt.suptitle(title)
        plt.tight_layout()
        
        if save_path:
            self._save_figure(save_path)
        else:
            plt.show()
    
    def plot_simple(self, tci_df: pd.DataFrame, k: int = 20, 
                   title: str = "Tool Criticality Index (Top-k)",
                   save_path: Optional[Path] = None):
        """Plot simple TCI bar chart."""
        d = tci_df.dropna(subset=["TCI"]).sort_values("TCI", ascending=False).head(k)
        
        plt.figure(figsize=(10, 6))
        plt.bar(d["tool"], d["TCI"])
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("TCI = P(success|correct) − P(success|mis)")
        plt.title(title)
        plt.tight_layout()
        
        if save_path:
            self._save_figure(save_path)
        else:
            plt.show()
