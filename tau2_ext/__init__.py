"""τ²-bench Extended Analytics Package."""

from .conversation_analyzer import ConversationAnalyzer, ConversationFeatures
from .metrics_calculator import MetricsCalculator, MetricsVisualizer, MetricResults
from .data_processing.data_preparer import DataPreparer, ConversationData
from .data_processing.task_loader import TaskLoader
from .tool_analyzer import ToolAnalyzer, ToolMetrics, PerToolAggregatedMetrics
from .pipeline import Tau2Pipeline
from .filter_convos import ConversationFilter, FilterCriteria

__version__ = "0.1.0"
__all__ = [
    # Core analysis
    "ConversationAnalyzer",
    "ConversationFeatures",
    "DataPreparer",
    "ConversationData",

    # Data processing
    "TaskLoader",

    # Metrics calculation
    "MetricsCalculator",
    "MetricsVisualizer",
    "MetricResults",

    # Tool analysis
    "ToolAnalyzer",
    "ToolMetrics",
    "PerToolAggregatedMetrics",

    # Pipeline
    "Tau2Pipeline",

    # Filtering
    "ConversationFilter",
    "FilterCriteria",
]
