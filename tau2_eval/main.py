#!/usr/bin/env python3
"""Simple script to run τ²-bench model comparisons."""

from tau2_eval.tau2_runner import run_tau2_eval

def main():
    """Run model comparison."""

    # User default userLLM from original paper, unless required to use a different one
    user_llm = "gpt-4o-mini"
    
    # Specify models to compare
    models = ["xai/grok-3"]
    
    # Run comparison
    domains = ["retail", "telecom"]

    domain_configs = {
        "retail": {
            "tasks": 60,
            "trials": 4
        },
        "telecom": {
            "tasks": 60,
            "trials": 4
        }
    }

    for domain in domains:
        tasks = domain_configs[domain]["tasks"]
        trials = domain_configs[domain]["trials"]
        run_tau2_eval(models, domain=domain, tasks=tasks, trials=trials, user_llm=user_llm)

if __name__ == "__main__":
    main()
