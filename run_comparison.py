#!/usr/bin/env python3
"""Simple script to run τ²-bench model comparisons."""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from tau2_runner import run_comparison

def main():
    """Run model comparison."""
    
    # Specify models to compare
    models = ["gpt-4o-mini", "xai/grok-3"]
    
    # Run comparison
    domains = ["retail", "telecom"]
    for domain in domains:
        run_comparison(models, domain=domain, tasks=25, trials=4)

if __name__ == "__main__":
    main()
