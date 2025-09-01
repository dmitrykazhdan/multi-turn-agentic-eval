#!/usr/bin/env python3
"""Minimal τ²-bench runner for model comparison."""

import os
import subprocess
import time
from pathlib import Path
from typing import List
from datetime import timedelta
from dotenv import load_dotenv

# Define path variables
PARENT_PATH = Path(__file__).parent.parent.parent
CODE_PATH = PARENT_PATH / "multi-turn-agentic-eval"
TAU2_PATH = PARENT_PATH / "tau2-bench"

print(f"PARENT_PATH: {PARENT_PATH}")
print(f"CODE_PATH: {CODE_PATH}")
print(f"TAU2_PATH: {TAU2_PATH}")


def setup_environment() -> bool:
    """Set up environment and API keys."""
    project_env_file = CODE_PATH / ".env"
    
    if not project_env_file.exists():
        print("❌ Project .env file not found")
        return False
    
    try:
        # Load API keys into environment variables using python-dotenv
        load_dotenv(project_env_file)
        print("✅ API keys loaded from project .env file into environment")
        return True
        
    except Exception as e:
        print(f"❌ Error loading API keys: {e}")
        return False


def run_model_evaluation(model: str, domain: str = "telecom", tasks: int = 20, trials: int = 5, user_llm: str = "gpt-4o-mini") -> bool:
    """Run evaluation for a single model."""
    
    tau2_cmd = str(TAU2_PATH / ".venv" / "bin" / "tau2")
    
    print(f"\n🚀 Running {model} on {domain} ({tasks} tasks, {trials} trials)")
    
    cmd = [
        tau2_cmd, "run",
        "--domain", domain,
        "--agent-llm", model,
        "--user-llm", user_llm,
        "--num-trials", str(trials),
        "--num-tasks", str(tasks),
        "--max-concurrency", "4",
        "--seed", "42"
    ]
    
    start_time = time.time()
    
    try:
        original_cwd = os.getcwd()
        os.chdir(TAU2_PATH)
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        os.chdir(original_cwd)
        
        elapsed_time = time.time() - start_time
        time_str = str(timedelta(seconds=int(elapsed_time)))
        
        if result.returncode == 0:
            print(f"✅ {model} evaluation completed in {time_str}!")
            return True
        else:
            print(f"❌ {model} evaluation failed after {time_str}!")
            print(result.stderr)
            return False
            
    except Exception as e:
        elapsed_time = time.time() - start_time
        time_str = str(timedelta(seconds=int(elapsed_time)))
        print(f"❌ Error running {model} after {time_str}: {e}")
        return False


def run_tau2_eval(models: List[str], domain: str = "telecom", tasks: int = 20, trials: int = 5, user_llm: str = "gpt-4o-mini"):
    """Run comparison for multiple models."""
    
    print("=" * 60)
    print("τ²-Bench Model Comparison")
    print("=" * 60)
    
    if not setup_environment():
        print("❌ Failed to setup environment")
        return
    
    start_time = time.time()
    success_count = 0
    
    for model in models:
        if run_model_evaluation(model, domain, tasks, trials, user_llm):
            success_count += 1
    
    total_time = time.time() - start_time
    total_time_str = str(timedelta(seconds=int(total_time)))
    
    print(f"\n✅ Completed {success_count}/{len(models)} evaluations in {total_time_str}")
    
if __name__ == "__main__":
    models = ["xai/grok-3", "xai/grok-4"]
    run_tau2_eval(models, domain="telecom", tasks=2, trials=2, user_llm="gpt-4o-mini")
