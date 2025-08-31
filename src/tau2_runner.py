#!/usr/bin/env python3
"""Minimal τ²-bench runner for model comparison."""

import os
import subprocess
import time
from pathlib import Path
from typing import List
from datetime import timedelta


def setup_environment() -> bool:
    """Set up environment and API keys."""
    project_env_file = Path(__file__).parent.parent / ".env"
    tau2_path = Path(__file__).parent.parent.parent / "tau2-bench"
    tau2_env_file = tau2_path / ".env"
    
    if not project_env_file.exists():
        print("❌ Project .env file not found")
        return False
    
    try:
        with open(project_env_file, 'r') as f:
            project_env_content = f.read()
        
        api_keys = {}
        for line in project_env_content.split('\n'):
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                api_keys[key.strip()] = value.strip()
        
        with open(tau2_env_file, 'w') as f:
            if 'XAI_API_KEY' in api_keys:
                f.write(f"XAI_API_KEY={api_keys['XAI_API_KEY']}\n")
            if 'OPENAI_API_KEY' in api_keys:
                f.write(f"OPENAI_API_KEY={api_keys['OPENAI_API_KEY']}\n")
        
        print("✅ API keys loaded from project .env file")
        return True
        
    except Exception as e:
        print(f"❌ Error loading API keys: {e}")
        return False


def run_model_evaluation(model: str, domain: str = "telecom", tasks: int = 20, trials: int = 5) -> bool:
    """Run evaluation for a single model."""
    
    tau2_path = Path(__file__).parent.parent.parent / "tau2-bench"
    tau2_cmd = str(tau2_path / ".venv" / "bin" / "tau2")
    
    print(f"\n🚀 Running {model} on {domain} ({tasks} tasks, {trials} trials)")
    
    cmd = [
        tau2_cmd, "run",
        "--domain", domain,
        "--agent-llm", model,
        "--user-llm", "gpt-4o-mini",
        "--num-trials", str(trials),
        "--num-tasks", str(tasks),
        "--max-concurrency", "4",
        "--seed", "42"
    ]
    
    start_time = time.time()
    
    try:
        original_cwd = os.getcwd()
        os.chdir(tau2_path)
        
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


def view_results():
    """View results using tau2 view command."""
    
    tau2_path = Path(__file__).parent.parent.parent / "tau2-bench"
    tau2_cmd = str(tau2_path / ".venv" / "bin" / "tau2")
    
    print("\n📊 Viewing results...")
    print("💡 Run this command to see results:")
    print(f"   cd {tau2_path} && {tau2_cmd} view")


def run_comparison(models: List[str], domain: str = "telecom", tasks: int = 20, trials: int = 5):
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
        if run_model_evaluation(model, domain, tasks, trials):
            success_count += 1
    
    total_time = time.time() - start_time
    total_time_str = str(timedelta(seconds=int(total_time)))
    
    print(f"\n✅ Completed {success_count}/{len(models)} evaluations in {total_time_str}")
    
    if success_count > 0:
        view_results()


if __name__ == "__main__":
    # Example usage
    models = ["xai/grok-3", "xai/grok-4"]
    run_comparison(models, domain="telecom", tasks=2, trials=2)
