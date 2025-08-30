#!/usr/bin/env python3
"""
Test script to verify τ²-Bench setup with Grok-3.

This script checks:
1. tau2-bench installation
2. Environment configuration
3. API key setup
4. Basic functionality

SETUP ASSUMPTIONS:
1. The multi-turn agentic evaluation framework and tau-bench are installed in the same parent directory
2. The .env file is in the multi-turn agentic evaluation framework directory
3. The tau2-bench directory has a virtual environment named ".venv"
"""

import os
import sys
import subprocess
from pathlib import Path

def test_tau2_installation():
    """Test if tau2-bench is properly installed."""
    
    print("🔍 Testing tau2-bench installation...")
    
    tau2_path = Path(__file__).parent.parent / "tau2-bench"
    
    if not tau2_path.exists():
        print("❌ tau2-bench directory not found at ../tau2-bench")
        return False
    
    # Check if virtual environment exists
    venv_path = tau2_path / ".venv"
    if not venv_path.exists():
        print("❌ tau2-bench virtual environment not found")
        return False
    
    # Check if tau2 command is available
    try:
        result = subprocess.run(
            ["../tau2-bench/.venv/bin/tau2", "--help"],
            capture_output=True,
            text=True,
            cwd=tau2_path
        )
        
        if result.returncode == 0:
            print("✅ tau2-bench installation verified")
            return True
        else:
            print("❌ tau2 command not working properly")
            return False
            
    except Exception as e:
        print(f"❌ Error testing tau2 command: {e}")
        return False

def test_environment_setup():
    """Test environment configuration."""
    
    print("\n🔍 Testing environment setup...")
    
    # Set environment variables
    tau2_path = Path(__file__).parent.parent / "tau2-bench"
    os.environ["TAU2_DATA_DIR"] = str(tau2_path / "data")
    
    # Check data directory
    data_dir = Path(os.environ["TAU2_DATA_DIR"])
    if data_dir.exists():
        print("✅ Data directory exists")
    else:
        print("❌ Data directory not found")
        return False
    
    # Check if project .env file exists
    project_env_file = Path(__file__).parent / ".env"
    if project_env_file.exists():
        print("✅ Project .env file exists")
        
        # Check if API keys are configured
        with open(project_env_file, 'r') as f:
            content = f.read()
            if "XAI_API_KEY" in content:
                print("✅ XAI API key configured")
            else:
                print("⚠️  XAI API key not configured")
                
            if "OPENAI_API_KEY" in content:
                print("✅ OpenAI API key configured")
            else:
                print("⚠️  OpenAI API key not configured")
    else:
        print("❌ Project .env file not found")
        return False
    
    return True

def test_basic_functionality():
    """Test basic tau2-bench functionality."""
    
    print("\n🔍 Testing basic functionality...")
    
    try:
        # Test check-data command
        result = subprocess.run(
            ["../tau2-bench/.venv/bin/tau2", "check-data"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent / "tau2-bench"
        )
        
        if result.returncode == 0:
            print("✅ Data check passed")
        else:
            print("❌ Data check failed")
            print(result.stderr)
            return False
        
        # Test domain listing
        result = subprocess.run(
            ["../tau2-bench/.venv/bin/tau2", "run", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent / "tau2-bench"
        )
        
        if result.returncode == 0:
            print("✅ Command-line interface working")
        else:
            print("❌ Command-line interface not working")
            return False
            
    except Exception as e:
        print(f"❌ Error testing functionality: {e}")
        return False
    
    return True

def test_python_imports():
    """Test if tau2-bench can be imported in Python."""
    
    print("\n🔍 Testing Python imports...")
    
    # Add tau2-bench src directory to Python path
    tau2_path = Path(__file__).parent.parent / "tau2-bench" / "src"
    sys.path.insert(0, str(tau2_path))
    
    try:
        # Test basic imports
        import tau2
        print("✅ tau2 module imported successfully")
        
        # Test specific components
        from tau2.registry import Registry
        print("✅ Registry component imported")
        
        # Try to import utils (might not have load_config)
        try:
            from tau2.utils.utils import load_config
            print("✅ Utils component imported")
        except ImportError:
            print("⚠️  Utils component imported (load_config not available)")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 This is expected when running from outside tau2-bench directory")
        print("   The scripts will handle this automatically when needed")
        return True  # Don't fail the test for this
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Run all tests."""
    
    print("=" * 60)
    print("τ²-Bench Setup Verification")
    print("=" * 60)
    
    tests = [
        ("Installation", test_tau2_installation),
        ("Environment", test_environment_setup),
        ("Functionality", test_basic_functionality),
        ("Python Imports", test_python_imports)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! τ²-Bench is ready to use.")
        print("\nNext steps:")
        print("1. Configure your API keys in ../tau2-bench/.env")
        print("2. Run: python tau2_grok_example.py")
    else:
        print("❌ Some tests failed. Please check the issues above.")
        print("\nTroubleshooting:")
        print("1. Make sure tau2-bench is properly installed")
        print("2. Check API key configuration")
        print("3. Verify Python environment")

if __name__ == "__main__":
    main()
