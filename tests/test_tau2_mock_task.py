#!/usr/bin/env python3
"""
Minimal example of using τ²-Bench with Grok for agent evaluation.

This script demonstrates how to:
1. Set up the environment for tau2-bench
2. Load API keys from our .env file into environment variables
3. Configure Grok as the agent LLM
4. Run a simple evaluation on the mock domain
5. View and analyze results

Prerequisites:
- tau2-bench installed in ../tau2-bench
- .env file with API keys in our multi-turn folder
- Python 3.10+
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Add tau2-bench to Python path
PARENT_PATH = Path("/Users/AdminDK/code")
CODE_PATH = PARENT_PATH / "multi-turn-agentic-eval"
TAU2_PATH = PARENT_PATH / "tau2-bench"
sys.path.insert(0, str(TAU2_PATH))

def setup_environment():
    """Set up the environment for tau2-bench with Grok."""
    
    # Set the data directory to point to tau2-bench
    os.environ["TAU2_DATA_DIR"] = str(TAU2_PATH / "data")
    
    # Check if .env file exists in project directory
    project_env_file = CODE_PATH / ".env"
    
    if not project_env_file.exists():
        print("❌ .env file not found in project directory")
        print("Please create a .env file with your API keys:")
        print("XAI_API_KEY=your_actual_grok_api_key")
        print("OPENAI_API_KEY=your_actual_openai_api_key")
        return False
    
    # Load API keys into environment variables using python-dotenv
    try:
        load_dotenv(project_env_file)
        print("✅ API keys loaded from project .env file into environment")
        return True
        
    except Exception as e:
        print(f"❌ Error loading API keys: {e}")
        return False


def run_minimal_evaluation(model="xai/grok-3-mini", user_llm="gpt-4o-mini"):
    """Run a minimal evaluation using Grok on the mock domain."""

    print("🚀 Running minimal τ²-Bench evaluation with Grok...")
    print("Domain: mock (simplest domain for testing)")
    print("Agent LLM: " + model + " (via XAI)")
    print("User LLM: " + user_llm + " (for cost efficiency)")
    print("Tasks: 2 (minimal for testing)")
    print("Trials: 1 per task")
    
    # Command to run the evaluation (using full path to tau2)
    tau2_cmd = str(TAU2_PATH / ".venv" / "bin" / "tau2")
    cmd = [
        tau2_cmd, "run",
        "--domain", "mock",
        "--agent-llm", model,  # Use correct model identifier
        "--user-llm", user_llm, 
        "--num-trials", "1",
        "--num-tasks", "2",
        "--max-concurrency", "1"
    ]
    
    try:
        # Change to tau2-bench directory to run the command
        original_cwd = os.getcwd()
        os.chdir(TAU2_PATH)
        
        print(f"\n📋 Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Change back to original directory
        os.chdir(original_cwd)
        
        if result.returncode == 0:
            print("✅ Evaluation completed successfully!")
            print("\n📊 Results saved to: data/tau2/simulations/")
            return True
        else:
            print("❌ Evaluation failed!")
            print("Error output:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running evaluation: {e}")
        return False


def view_results():
    """View the evaluation results."""
    
    print("\n📈 Viewing evaluation results...")
    
    tau2_cmd = str(TAU2_PATH / ".venv" / "bin" / "tau2")
    cmd = [tau2_cmd, "view"]
    
    try:
        # Change to tau2-bench directory to run the command
        original_cwd = os.getcwd()
        os.chdir(TAU2_PATH)
        
        # Don't capture output for interactive commands
        print("💡 Opening interactive results viewer...")
        print("   (This will open in a new terminal window)")
        print("   You can also run manually: cd ../tau2-bench && .venv/bin/tau2 view")
        
        # Just show the command instead of running it
        print(f"   Command: {' '.join(cmd)}")
        
        # Change back to original directory
        os.chdir(original_cwd)
        
        print("✅ Results viewer instructions provided!")
            
    except Exception as e:
        print(f"❌ Error with results viewer: {e}")


def main():
    """Main function to run the minimal example."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="xai/grok-3-mini")
    parser.add_argument("--user_llm", type=str, default="gpt-4o-mini")
    args = parser.parse_args()
    model = args.model
    user_llm = args.user_llm
    
    print("=" * 60)
    print("τ²-Bench Minimal Example with Grok")
    print("=" * 60)
    
    # Step 1: Setup environment
    print("\n1️⃣ Setting up environment...")
    if not setup_environment():
        print("⚠️  Please configure your API keys and run again")
        return
    
    # Step 2: Run evaluation
    print("\n2️⃣ Running evaluation...")
    success = run_minimal_evaluation(model=model, user_llm=user_llm)
    
    if success:
        # Step 3: View results
        print("\n3️⃣ Viewing results...")
        view_results()
        
        print("\n🎉 Example completed successfully!")
        print("\n📁 Next steps:")
        print("  - Check results in: ../tau2-bench/data/tau2/simulations/")
        print("  - Try different domains: airline, retail, telecom")
        print("  - Experiment with different LLM combinations")
        print("  - Run more tasks and trials for comprehensive evaluation")
    else:
        print("\n❌ Example failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
