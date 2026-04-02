#!/usr/bin/env python3
"""
Basic tests for Shared Memory System
"""

import os
import tempfile
import shutil
import yaml
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_directory_structure():
    """Test that required directories exist"""
    from scripts.init_system import create_directory_structure, SHARED_MEMORY_ROOT
    
    # Use temporary directory for testing
    test_root = Path(tempfile.mkdtemp())
    original_root = SHARED_MEMORY_ROOT
    
    try:
        # Monkey patch for testing
        import scripts.init_system as init_module
        init_module.SHARED_MEMORY_ROOT = test_root
        
        # Create directories
        init_module.create_directory_structure()
        
        # Check directories
        required_dirs = [
            test_root,
            test_root / "tags",
            test_root / "data",
            test_root / "data" / "public",
            test_root / "data" / "confidential",
            test_root / "data" / "financial",
            test_root / "data" / "technical",
            test_root / "access_log",
            test_root / "backups"
        ]
        
        for directory in required_dirs:
            assert directory.exists(), f"Directory {directory} should exist"
            assert directory.is_dir(), f"{directory} should be a directory"
        
        print("✅ Directory structure test passed")
        return True
        
    finally:
        # Cleanup
        if test_root.exists():
            shutil.rmtree(test_root)
        # Restore original
        import scripts.init_system as init_module
        init_module.SHARED_MEMORY_ROOT = original_root

def test_yaml_parsing():
    """Test YAML configuration parsing"""
    test_yaml = """
agent: test_agent
allowed_tags:
  - public
  - technical
denied_tags:
  - financial
role: technical_analyst
access_level: read_only
created: 2024-04-02
expires: 2024-12-31
description: Test agent
"""
    
    data = yaml.safe_load(test_yaml)
    
    assert data["agent"] == "test_agent"
    assert "public" in data["allowed_tags"]
    assert "financial" in data["denied_tags"]
    assert data["role"] == "technical_analyst"
    assert data["access_level"] == "read_only"
    
    print("✅ YAML parsing test passed")
    return True

def test_permission_logic():
    """Test permission checking logic"""
    from scripts.get_agent_memory import can_access_memory
    
    # Test case 1: Agent can access public memory
    permissions = {
        "allowed_tags": ["public", "technical"],
        "denied_tags": ["financial"]
    }
    memory_tags = ["public"]
    
    assert can_access_memory(memory_tags, permissions) == True, "Should allow public memory"
    
    # Test case 2: Agent cannot access financial memory
    memory_tags = ["financial", "confidential"]
    assert can_access_memory(memory_tags, permissions) == False, "Should deny financial memory"
    
    # Test case 3: Agent can access technical memory
    memory_tags = ["technical", "system"]
    assert can_access_memory(memory_tags, permissions) == True, "Should allow technical memory"
    
    # Test case 4: Admin can access everything
    permissions = {
        "allowed_tags": ["*"],
        "denied_tags": []
    }
    memory_tags = ["financial", "confidential", "user_private"]
    assert can_access_memory(memory_tags, permissions) == True, "Admin should allow everything"
    
    print("✅ Permission logic test passed")
    return True

def test_memory_id_generation():
    """Test memory ID generation"""
    from scripts.add_memory import generate_memory_id
    
    id1 = generate_memory_id()
    id2 = generate_memory_id()
    
    assert id1.startswith("memory_"), "Memory ID should start with 'memory_'"
    assert len(id1) == len("memory_") + 8, "Memory ID should be 8 hex chars after prefix"
    assert id1 != id2, "Memory IDs should be unique"
    
    print("✅ Memory ID generation test passed")
    return True

def test_tag_parsing():
    """Test tag parsing logic"""
    from scripts.add_memory import parse_tags
    
    # Test comma-separated tags
    tags = parse_tags("public,technical,system")
    assert tags == ["public", "technical", "system"], "Should parse comma-separated tags"
    
    # Test single tag
    tags = parse_tags("public")
    assert tags == ["public"], "Should parse single tag"
    
    # Test empty tags (default to public)
    tags = parse_tags("")
    assert tags == ["public"], "Empty tags should default to public"
    
    # Test tags with spaces
    tags = parse_tags(" public , technical , system ")
    assert tags == ["public", "technical", "system"], "Should trim spaces"
    
    print("✅ Tag parsing test passed")
    return True

def run_all_tests():
    """Run all tests"""
    print("🧪 Running Shared Memory System Tests")
    print("="*60)
    
    tests = [
        ("Directory Structure", test_directory_structure),
        ("YAML Parsing", test_yaml_parsing),
        ("Permission Logic", test_permission_logic),
        ("Memory ID Generation", test_memory_id_generation),
        ("Tag Parsing", test_tag_parsing),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} error: {e}")
    
    print("="*60)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)