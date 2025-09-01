#!/usr/bin/env python3
"""Test script for ToolSchemaLoader."""

import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from tau2_ext import ToolSchemaLoader


def test_tool_schema_loader():
    """Test the ToolSchemaLoader functionality."""
    print("🧪 Testing ToolSchemaLoader...")
    
    # Initialize the loader
    loader = ToolSchemaLoader()
    
    # Test basic functionality
    print(f"📋 Available domains: {loader.get_all_domains()}")
    
    # Test retail domain
    if "retail" in loader.get_all_domains():
        print(f"\n🛍️  Retail domain tools: {loader.get_domain_tools('retail')}")
        
        # Test a specific tool
        tool_name = "cancel_pending_order"
        if loader.has_tool("retail", tool_name):
            schema = loader.get_tool_schema("retail", tool_name)
            print(f"🔧 {tool_name} schema: {schema}")
        else:
            print(f"❌ Tool {tool_name} not found in retail domain")
    
    # Test telecom domain
    if "telecom" in loader.get_all_domains():
        print(f"\n📱 Telecom domain tools: {loader.get_domain_tools('telecom')}")
    
    print("\n✅ ToolSchemaLoader test completed!")


if __name__ == "__main__":
    test_tool_schema_loader()
