"""ADB configuration validation module.

This module provides functionality to validate ADB path configuration
by loading config files and testing ADB connectivity.
"""

import os
import subprocess
from .load_config import load_config


def ping_adb(config_path="config.json"):
    """Load configuration file and validate ADB path.
    
    This function loads the configuration file, validates the ADB path,
    and tests ADB connectivity by running the 'adb version' command.
    
    Args:
        config_path (str, optional): Path to the configuration file. 
            Defaults to "config.json".
    
    Returns:
        str: Validation result based on different scenarios:
            - "pong": ADB path is valid and working
            - "config file not found": Configuration file does not exist
            - "invalid config format": JSON format error
            - "missing adb_path setting": No adb_path in configuration
            - "please set correct adb_path": Using default placeholder value
            - "adb file not found": Specified ADB path does not exist
            - "adb file not executable": ADB file exists but lacks execute permission
            - "adb command failed": ADB command execution failed
            - "adb command timeout": ADB command execution timed out
    
    Example:
        >>> result = ping_adb()
        >>> if result == "pong":
        ...     print("ADB configuration is valid!")
        >>> else:
        ...     print(f"ADB configuration issue: {result}")
    """
    # Load configuration file
    config = load_config(config_path)
    
    # Check if configuration file was found
    if config == 0:
        return "config file not found"
    
    # Check configuration file format
    if not isinstance(config, dict):
        return "invalid config format"
    
    # Check if adb_path setting exists
    adb_path = config.get("adb_path")
    if not adb_path:
        return "missing adb_path setting"
    
    # Check if using default placeholder value
    if adb_path == "/path/to/your/adb":
        return "please set correct adb_path"
    
    # Check if ADB file exists
    if not os.path.exists(adb_path):
        return "adb file not found"
    
    # Check if ADB file has execute permission
    if not os.access(adb_path, os.X_OK):
        return "adb file not executable"
    
    # Execute ADB version command for validation
    try:
        result = subprocess.run(
            [adb_path, "version"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if result.returncode == 0:
            return "pong"
        else:
            return "adb command failed"
            
    except subprocess.TimeoutExpired:
        return "adb command timeout"
    except Exception:
        return "adb command failed"