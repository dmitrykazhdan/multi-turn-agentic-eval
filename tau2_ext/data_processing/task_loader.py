"""Task loader for τ²-bench domain tasks."""

import json
from pathlib import Path
from typing import Dict, List


class TaskLoader:
    """Load and manage static task information from domain tasks.json files."""
    
    def __init__(self, tau2_bench_path: str = "/Users/AdminDK/code/tau2-bench"):
        self.tau2_bench_path = Path(tau2_bench_path)
        self.tasks_data = self._load_all_domain_tasks()
    
    def _load_all_domain_tasks(self) -> Dict[str, List[Dict]]:
        """Load expected tools for all available domains from tasks.json."""
        expected_tools = {}
        
        # Look for domains in the tau2-bench data structure
        domains_dir = self.tau2_bench_path / "data" / "tau2" / "domains"
        
        if not domains_dir.exists():
            print(f"Warning: Domains directory not found: {domains_dir}")
            return expected_tools
        
        # Find all domain directories
        domain_dirs = [d for d in domains_dir.iterdir() if d.is_dir()]
        
        for domain_dir in domain_dirs:
            domain_name = domain_dir.name
            tasks_file = domain_dir / "tasks.json"
            
            if tasks_file.exists():
                try:
                    with open(tasks_file, 'r') as f:
                        tasks = json.load(f)
                    
                    # Extract expected tools per task for this domain
                    for task in tasks:
                        task_id = task["id"]
                        # Use domain prefix to avoid conflicts
                        full_task_id = f"{domain_name}_{task_id}"
                        expected_tools[full_task_id] = [
                            {
                                "name": action["name"],
                                "arguments": action["arguments"]
                            }
                            for action in task["evaluation_criteria"]["actions"]
                        ]
                    
                    print(f"✅ Loaded {len(tasks)} tasks for domain: {domain_name}")
                    
                except Exception as e:
                    print(f"❌ Error loading tasks for domain {domain_name}: {e}")
            else:
                print(f"⚠️  No tasks.json found for domain: {domain_name}")
        
        print(f"📋 Total tasks loaded: {len(expected_tools)}")
        return expected_tools
    
    def get_task_tools(self, domain: str, task_id: str) -> List[Dict]:
        """Get expected tools for a specific task."""
        full_task_id = f"{domain}_{task_id}"
        return self.tasks_data.get(full_task_id, [])
    
    def get_task_count(self, domain: str) -> int:
        """Get the number of tasks for a specific domain."""
        domain_tasks = [k for k in self.tasks_data.keys() if k.startswith(f"{domain}_")]
        return len(domain_tasks)
    
    def get_all_domains(self) -> List[str]:
        """Get list of all available domains."""
        domains = set()
        for task_key in self.tasks_data.keys():
            domain = task_key.split("_")[0]
            domains.add(domain)
        return sorted(list(domains))
