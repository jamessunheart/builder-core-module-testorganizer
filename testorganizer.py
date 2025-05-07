"""
TestOrganizer - Module for Builder Core v2
================================================================================
A module that helps organize and verify module structure in the Builder Core v2 system.
"""

from typing import Dict, Any, List
import os
import logging

logger = logging.getLogger(__name__)

def check_module_structure(module_name: str) -> Dict[str, Any]:
    """
    Check if a module has the proper directory structure
    
    Args:
        module_name (str): Name of the module to check
        
    Returns:
        Dict[str, Any]: Results of the structure check
    """
    results = {
        "module": module_name,
        "exists": False,
        "has_tool_py": False,
        "has_tool_yaml": False,
        "has_legacy_module": False
    }
    
    # Check for module directory
    module_dir = os.path.join("modules", module_name)
    if os.path.exists(module_dir) and os.path.isdir(module_dir):
        results["exists"] = True
        
        # Check for tool.py
        tool_path = os.path.join(module_dir, "tool.py")
        results["has_tool_py"] = os.path.exists(tool_path)
        
        # Check for tool.yaml
        yaml_path = os.path.join(module_dir, "tool.yaml")
        results["has_tool_yaml"] = os.path.exists(yaml_path)
    
    # Check for legacy module file
    legacy_path = f"modules/{module_name.lower()}.py"
    results["has_legacy_module"] = os.path.exists(legacy_path)
    
    # Determine if structure is complete
    results["is_complete"] = (
        results["exists"] and 
        results["has_tool_py"] and 
        results["has_tool_yaml"]
    )
    
    return results

def list_all_modules() -> List[Dict[str, Any]]:
    """
    List all modules in the filesystem
    
    Returns:
        List[Dict[str, Any]]: List of modules and their structure status
    """
    modules = []
    
    if not os.path.exists("modules"):
        return modules
        
    # Get all directories in modules folder
    for item in os.listdir("modules"):
        # Check if it's a directory
        item_path = os.path.join("modules", item)
        if os.path.isdir(item_path) and not item.startswith("."):
            # Check structure
            modules.append(check_module_structure(item))
    
    return modules

def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for the TestOrganizer module
    
    Args:
        params (Dict[str, Any]): Parameters for module execution
            - operation (str): Operation to execute (check, list)
            - module_name (str): Module name to check (for check operation)
        
    Returns:
        Dict[str, Any]: Result of module execution
    """
    operation = params.get("operation", "list")
    
    if operation == "check":
        module_name = params.get("module_name")
        if not module_name:
            return {
                "status": "error",
                "message": "Missing module_name parameter for check operation",
                "module": "TestOrganizer"
            }
            
        result = check_module_structure(module_name)
        status = "complete" if result["is_complete"] else "incomplete"
        
        return {
            "status": status,
            "message": f"Module structure check completed for {module_name}",
            "module": "TestOrganizer",
            "result": result
        }
    
    elif operation == "list":
        modules = list_all_modules()
        
        complete_count = sum(1 for m in modules if m["is_complete"])
        incomplete_count = len(modules) - complete_count
        
        return {
            "status": "success",
            "message": f"Found {len(modules)} modules ({complete_count} complete, {incomplete_count} incomplete)",
            "module": "TestOrganizer",
            "modules": modules
        }
    
    else:
        return {
            "status": "error",
            "message": f"Unknown operation: {operation}",
            "module": "TestOrganizer"
        }