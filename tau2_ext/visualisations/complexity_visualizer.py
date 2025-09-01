"""Complexity metrics visualizer."""
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from typing import Optional
from scipy import stats
import numpy as np

from .base_visualizer import BaseVisualizer


class ComplexityVisualizer(BaseVisualizer):
    """Visualizer for Complexity metrics."""
    
    def plot_bucket_pass1_by_domain(self, bucket_df: pd.DataFrame, df: pd.DataFrame, 
                                   title: str = "Pass@1 by Plan Complexity and Domain",
                                   save_path: Optional[Path] = None):
        """Plot pass@1 by complexity bucket with separate subplots for each domain and confidence intervals."""
        domains = df["domain"].unique()
        fig, axes = self._setup_domain_subplots(domains, figsize_per_domain=(6, 6))
        
        for i, domain in enumerate(domains):
            # For complexity metrics, we need to calculate per domain for proper confidence intervals
            domain_df = df[df["domain"] == domain]
            from tau2_ext.metrics.metrics_calculator import MetricsCalculator
            domain_calculator = MetricsCalculator()
            domain_bucket = domain_calculator.calculate_bucket_pass1(domain_df)
            
            if not domain_bucket.empty:
                complexity_levels = domain_bucket.iloc[:, 0].astype(str)
                pass_rates = domain_bucket["pass@1"]
                
                # Calculate confidence intervals for each bucket
                confidence_intervals = []
                sample_sizes = []
                
                for level in complexity_levels:
                    # Get data for this complexity level
                    level_data = domain_df[domain_df["exp_plan_len"].apply(
                        lambda x: (x <= 2 and level == "simple") or 
                                (2 < x <= 5 and level == "medium") or 
                                (x > 5 and level == "complex")
                    )]
                    
                    n = len(level_data)
                    k = level_data["success"].sum()
                    sample_sizes.append(n)
                    
                    if n > 0:
                        # Wilson confidence interval for binomial proportion
                        try:
                            ci_lower, ci_upper = stats.proportion_conf_int(k, n, method='wilson')
                        except AttributeError:
                            # Manual Wilson confidence interval calculation
                            z = 1.96  # 95% confidence level
                            p_hat = k / n
                            denominator = 1 + z**2 / n
                            centre_adjusted_probability = (p_hat + z * z / (2 * n)) / denominator
                            adjusted_standard_error = z * np.sqrt((p_hat * (1 - p_hat) + z * z / (4 * n)) / n) / denominator
                            ci_lower = max(0, centre_adjusted_probability - adjusted_standard_error)
                            ci_upper = min(1, centre_adjusted_probability + adjusted_standard_error)
                        
                        confidence_intervals.append((ci_lower, ci_upper))
                    else:
                        confidence_intervals.append((0, 0))
                
                # Create bar plot with error bars
                x_pos = range(len(complexity_levels))
                yerr_lower = [pass_rates[j] - confidence_intervals[j][0] for j in range(len(pass_rates))]
                yerr_upper = [confidence_intervals[j][1] - pass_rates[j] for j in range(len(pass_rates))]
                
                bars = axes[i].bar(x_pos, pass_rates, alpha=0.8, color='skyblue', edgecolor='navy', 
                                 yerr=[yerr_lower, yerr_upper], capsize=5)
                
                axes[i].set_xlabel("Complexity Bucket")
                axes[i].set_ylabel("Pass@1")
                axes[i].set_title(f"{domain} Domain")
                self._add_grid_and_styling(axes[i])
                axes[i].set_xticks(x_pos)
                axes[i].set_xticklabels(complexity_levels)
                
                # Add value labels on bars with sample sizes (positioned at top of CI)
                for j, (level, rate, n) in enumerate(zip(complexity_levels, pass_rates, sample_sizes)):
                    # Position label right at the top of the confidence interval
                    label_y = confidence_intervals[j][1]
                    
                    axes[i].text(j, label_y, f'{rate:.1%}\n(n={n})', 
                               ha='center', va='bottom', fontweight='bold', fontsize=9)
            else:
                axes[i].text(0.5, 0.5, f"No complexity data for {domain}", ha='center', va='center', transform=axes[i].transAxes)
                axes[i].set_title(f"{domain} Domain")
        
        plt.suptitle(title)
        plt.tight_layout()
        
        if save_path:
            self._save_figure(save_path)
        else:
            plt.show()
    
    def plot_bucket_pass1_simple(self, bucket_df: pd.DataFrame, 
                                title: str = "Pass@1 by Plan Complexity",
                                save_path: Optional[Path] = None):
        """Plot simple pass@1 by complexity bucket."""
        plt.figure(figsize=(8, 6))
        plt.bar(bucket_df.iloc[:, 0].astype(str), bucket_df["pass@1"])
        plt.xlabel("Complexity Bucket")
        plt.ylabel("Pass@1")
        plt.title(title)
        plt.tight_layout()
        
        if save_path:
            self._save_figure(save_path)
        else:
            plt.show()
