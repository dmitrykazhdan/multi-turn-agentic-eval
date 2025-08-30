#!/usr/bin/env python3
"""Minimal test for direct LiteLLM calls."""

import os
import sys

# Load environment variables (like LiteLLMClient does)
from dotenv import load_dotenv
load_dotenv()

import litellm

def test_direct_litellm():
    """Test direct LiteLLM calls."""
    
    print("🧪 Testing LiteLLM calls...")
    
    # Get XAI API key
    xai_api_key = os.getenv("XAI_API_KEY")
    if not xai_api_key:
        print("❌ XAI_API_KEY not found in environment")
        return False
    
    # Test grok-3 with direct litellm.completion
    print("\n=== Testing grok-3 with direct litellm.completion ===")
    try:
        response = litellm.completion(
            model="xai/grok-3",
            messages=[{"role": "user", "content": "What is 2+2? Answer with just the number."},
                      {"role": "user", "content": "What is the weather like? Answer in 20 words or less."}],
            max_tokens=20,
            temperature=0
        )
        
        print(f"Response: '{response.choices[0].message.content}'")
        print(f"Response length: {len(response.choices[0].message.content)}")
        print(f"Usage: {response.usage}")
        
        if response.choices[0].message.content.strip():
            print("✅ grok-3 direct call works!")
            return True
        else:
            print("❌ grok-3 direct call returned empty response")
            return False
            
    except Exception as e:
        print(f"❌ Error with grok-3 direct call: {e}")
        return False

def test_async_litellm():
    """Test async LiteLLM calls."""
    
    print("\n=== Testing grok-3 with async litellm.acompletion ===")
    
    import asyncio
    
    async def test_async():
        try:
            response = await litellm.acompletion(
                model="xai/grok-3",
                messages=[{"role": "user", "content": "What is 2+2? Answer with just the number."},
                          {"role": "user", "content": "What is the weather like? Answer in 20 words or less."}],
                max_tokens=20,
                temperature=0
            )
            
            print(f"Response: '{response.choices[0].message.content}'")
            print(f"Response length: {len(response.choices[0].message.content)}")
            print(f"Usage: {response.usage}")
            
            if response.choices[0].message.content.strip():
                print("✅ grok-3 async call works!")
                return True
            else:
                print("❌ grok-3 async call returned empty response")
                return False
                
        except Exception as e:
            print(f"❌ Error with grok-3 async call: {e}")
            return False
    
    return asyncio.run(test_async())

def main():
    """Run all tests."""
    print("Testing direct LiteLLM calls...")
    
    # Test sync completion
    sync_result = test_direct_litellm()
    
    # Test async completion
    async_result = test_async_litellm()
    
    # Summary
    print(f"\n=== Summary ===")
    print(f"Sync litellm.completion: {'✅ Working' if sync_result else '❌ Failed'}")
    print(f"Async litellm.acompletion: {'✅ Working' if async_result else '❌ Failed'}")
    
    if sync_result or async_result:
        print("\n🎉 Direct LiteLLM calls work!")
        return 0
    else:
        print("\n❌ Direct LiteLLM calls still fail")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
