"""Tool schema loader for τ²-bench domains."""

import json
from pathlib import Path
from typing import Dict, List, Optional


class ToolSchemaLoader:
    """Load and manage tool schemas from domain definition files."""
    
    def __init__(self, tau2_bench_path: str = "/Users/AdminDK/code/tau2-bench"):
        self.tau2_bench_path = Path(tau2_bench_path)
        self.schemas = self._load_all_domain_schemas()
    
    def _load_all_domain_schemas(self) -> Dict[str, Dict[str, List[str]]]:
        """Load tool schemas from all available domains using tasks.json."""
        schemas = {}
        
        # Look for domains in the tau2-bench data structure
        domains_dir = self.tau2_bench_path / "data" / "tau2" / "domains"
        
        if not domains_dir.exists():
            print(f"Warning: Domains directory not found: {domains_dir}")
            return schemas
        
        # Find all domain directories
        domain_dirs = [d for d in domains_dir.iterdir() if d.is_dir()]
        
        for domain_dir in domain_dirs:
            domain_name = domain_dir.name
            tasks_file = domain_dir / "tasks.json"
            
            if tasks_file.exists():
                try:
                    with open(tasks_file, 'r') as f:
                        tasks_data = json.load(f)
                    domain_schemas = self._extract_tool_schemas_from_tasks(tasks_data)
                    schemas[domain_name] = domain_schemas
                    print(f"✅ Loaded {len(domain_schemas)} tool schemas for domain: {domain_name}")
                except Exception as e:
                    print(f"❌ Error loading tasks.json for domain {domain_name}: {e}")
            else:
                print(f"⚠️  No tasks.json found for domain: {domain_name}")
        
        print(f"📋 Total domains with schemas: {len(schemas)}")
        return schemas
    

    
    def _extract_tool_schemas_from_tasks(self, tasks_data: List[Dict]) -> Dict[str, List[str]]:
        """Extract tool schemas by analyzing task evaluation criteria."""
        tool_schemas = {}
        
        for task in tasks_data:
            actions = task.get("evaluation_criteria", {}).get("actions", [])
            
            for action in actions:
                tool_name = action.get("name", "")
                if tool_name and tool_name not in tool_schemas:
                    # Extract arguments from the action
                    arguments = action.get("arguments", {})
                    if isinstance(arguments, dict):
                        tool_schemas[tool_name] = list(arguments.keys())
                    elif isinstance(arguments, list):
                        tool_schemas[tool_name] = arguments
        
        return tool_schemas
    
    def get_tool_schema(self, domain: str, tool_name: str) -> List[str]:
        """Get the schema (required arguments) for a specific tool in a domain."""
        domain_schemas = self.schemas.get(domain, {})
        return domain_schemas.get(tool_name, [])
    
    def get_domain_tools(self, domain: str) -> List[str]:
        """Get all tool names available in a domain."""
        domain_schemas = self.schemas.get(domain, {})
        return list(domain_schemas.keys())
    
    def has_tool(self, domain: str, tool_name: str) -> bool:
        """Check if a tool exists in a domain."""
        return tool_name in self.schemas.get(domain, {})
    
    def get_all_domains(self) -> List[str]:
        """Get list of all available domains."""
        return list(self.schemas.keys())
