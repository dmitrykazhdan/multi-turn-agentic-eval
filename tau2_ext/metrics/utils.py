import numpy as np
from typing import Tuple, List, Dict
from collections import defaultdict

def wilson_ci(k: int, n: int, z: float = 1.96) -> Tuple[float, float]:
    """Calculate Wilson confidence interval for binomial proportion."""
    if n == 0:
        return (0, 0)
    
    p_hat = k / n
    denominator = 1 + z**2 / n
    centre_adjusted_probability = (p_hat + z * z / (2 * n)) / denominator
    adjusted_standard_error = z * np.sqrt((p_hat * (1 - p_hat) + z * z / (4 * n)) / n) / denominator
    ci_lower = max(0, centre_adjusted_probability - adjusted_standard_error)
    ci_upper = min(1, centre_adjusted_probability + adjusted_standard_error)
    
    return (ci_lower, ci_upper)


def levenshtein(a: List[str], b: List[str]) -> int:
    """Calculate Levenshtein distance between two lists."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
        
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
    
    return dp[m][n]


def tool_seq(lst: List[Dict]) -> List[str]:
    """Extract tool names from tool list."""
    return [x.get("name", "") for x in (lst or []) if x.get("name")]


def group_tools_by_name(tools: List[Dict]) -> Dict[str, List[Dict]]:
    """Group tools by name and extract their arguments."""
    grouped = defaultdict(list)
    for tool in tools:
        grouped[tool.get("name", "")].append(tool.get("arguments", {}))
    return grouped
