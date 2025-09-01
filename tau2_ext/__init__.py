"""τ²-bench Extended Analytics Package."""
from .metrics.metrics_calculator import MetricsCalculator, MetricResults
from .visualisations.metrics_visualizer import MetricsVisualizer
from .data_processing.data_preparer import DataPreparer, ConversationData
from .data_processing.task_loader import TaskLoader
from .data_processing.tool_schema_loader import ToolSchemaLoader

__version__ = "0.1.0"
__all__ = [
    # Core analysis
    "DataPreparer",
    "ConversationData",

    # Data processing
    "TaskLoader",
    "ToolSchemaLoader",

    # Metrics calculation
    "MetricsCalculator",
    "MetricResults",
    "MetricsVisualizer",
    "MetricResults",
]
