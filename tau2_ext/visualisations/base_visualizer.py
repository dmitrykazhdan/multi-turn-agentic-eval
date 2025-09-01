"""Base visualizer class with common functionality."""
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime


class BaseVisualizer:
    """Base class for metric visualizers with common functionality."""
    
    def __init__(self):
        self.colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    
    def _create_timestamped_dir(self, save_dir: str) -> Path:
        """Create timestamped subfolder for saving figures."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        figures_dir = Path(save_dir) / f"figures_{timestamp}"
        figures_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 Saving figures to: {figures_dir}")
        return figures_dir
    
    def _save_figure(self, save_path: Path, dpi: int = 300):
        """Save current figure to file."""
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
    
    def _setup_domain_subplots(self, domains, figsize_per_domain=(6, 6)):
        """Create subplots for multiple domains."""
        fig, axes = plt.subplots(1, len(domains), figsize=(figsize_per_domain[0] * len(domains), figsize_per_domain[1]))
        
        if len(domains) == 1:
            axes = [axes]
        
        return fig, axes
    
    def _add_grid_and_styling(self, ax):
        """Add common grid and styling to an axis."""
        ax.grid(True, alpha=0.3)
    
    def _get_domain_color(self, domain_index: int) -> str:
        """Get color for a domain based on its index."""
        return self.colors[domain_index % len(self.colors)]
