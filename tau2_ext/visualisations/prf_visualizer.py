"""Precision-Recall-F1 (PRF) visualizer."""

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from typing import Optional

from tau2_ext.visualisations.base_visualizer import BaseVisualizer


class PRFVisualizer(BaseVisualizer):
    """Visualizer for Precision-Recall-F1 metrics."""
    
    def plot_precision_recall_by_domain(self, prf_df: pd.DataFrame, df: pd.DataFrame, 
                                       title: str = "Precision vs Recall by Domain",
                                       save_path: Optional[Path] = None):
        """Plot standard PR curve with circle size reflecting omission rate."""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        domains = df["domain"].unique()
        
        for i, domain in enumerate(domains):
            domain_df = df[df["domain"] == domain]
            from tau2_ext.metrics.metrics_calculator import MetricsCalculator
            domain_calculator = MetricsCalculator()
            domain_prf = domain_calculator.calculate_per_tool_prf(domain_df)
            
            # Standard PR plot: Recall on X, Precision on Y
            x = domain_prf["recall"]  # X-axis: Recall
            y = domain_prf["precision"]  # Y-axis: Precision
            sizes = domain_prf["omission_rate"] * 1000 + 50  # Circle size based on omission rate
            
            color = self._get_domain_color(i)
            ax.scatter(x, y, c=color, label=domain, alpha=0.7, s=sizes, edgecolors='black', linewidth=0.5)
            
            # Add tool labels with better positioning
            for _, row in domain_prf.iterrows():
                # Use different offset directions to reduce overlap
                offset_x = 0.02 if i % 2 == 0 else -0.02
                offset_y = 0.02 if i % 3 == 0 else -0.02
                
                ax.annotate(
                    row["tool"], 
                    (row["recall"], row["precision"]), 
                    fontsize=9, 
                    xytext=(offset_x, offset_y), 
                    textcoords="offset points",
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.7, edgecolor='gray'),
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.1", alpha=0.6)
                )
        
        ax.set_xlabel("Recall")
        ax.set_ylabel("Precision")
        ax.set_title(title)
        self._add_grid_and_styling(ax)
        
        # Set axes to 0.0-1.19 to prevent circle cutoff
        ax.set_xlim(0.0, 1.19)
        ax.set_ylim(0.0, 1.19)
        
        # Create combined legend with domain colors and circle sizes
        legend_elements = []
        
        # Add domain legend
        for i, domain in enumerate(domains):
            color = self._get_domain_color(i)
            legend_elements.append(plt.scatter([], [], c=color, alpha=0.7, label=domain))
        
        # Add circle size legend
        legend_elements.extend([
            plt.scatter([], [], s=100, c='gray', alpha=0.7, label='Low Omission'),
            plt.scatter([], [], s=500, c='gray', alpha=0.7, label='Medium Omission'),
            plt.scatter([], [], s=1000, c='gray', alpha=0.7, label='High Omission')
        ])
        
        ax.legend(handles=legend_elements, title="Circle Size = Omission Rate", loc='lower left')
        
        plt.tight_layout()
        
        if save_path:
            self._save_figure(save_path)
        else:
            plt.show()
    
    def plot_precision_omission(self, prf_df: pd.DataFrame, 
                               title: str = "Precision vs Omission (per tool)",
                               save_path: Optional[Path] = None):
        """Plot precision vs omission scatter."""
        plt.figure(figsize=(10, 6))
        x = prf_df["omission_rate"]
        y = prf_df["recall"]
        
        plt.scatter(x, y)
        for _, row in prf_df.iterrows():
            plt.annotate(
                row["tool"], 
                (row["omission_rate"], row["recall"]), 
                fontsize=8, 
                xytext=(2, 2), 
                textcoords="offset points"
            )
        
        plt.xlabel("Omission Rate")
        plt.ylabel("Recall")
        plt.title(title)
        plt.tight_layout()
        
        if save_path:
            self._save_figure(save_path)
        else:
            plt.show()
