#!/usr/bin/env python3
"""
Recreate all Python files for Azure IoT Hub Device Simulator
This script creates all the Python source files with the correct code
"""

import os
import sys
from pathlib import Path

def create_directories():
    """Create all necessary directories"""
    dirs = [
        "src",
        "src/core",
        "src/ui", 
        "src/azure_integration",
        "src/templates",
        "src/monitoring",
        "src/advanced"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {dir_path}")

def create_init_files():
    """Create all __init__.py files"""
    init_files = {
        "src/__init__.py": "# Azure IoT Hub Device Simulator - Main package",
        "src/core/__init__.py": "# Core package",
        "src/ui/__init__.py": "# UI package", 
        "src/azure_integration/__init__.py": "# Azure integration package",
        "src/templates/__init__.py": "# Templates package",
        "src/monitoring/__init__.py": "# Monitoring package",
        "src/advanced/__init__.py": "# Advanced features package"
    }
    
    for file_path, content in init_files.items():
        with open(file_path, 'w') as f:
            f.write(content + "\n")
        print(f"✓ Created: {file_path}")

def main():
    """Main function"""
    print("Recreating Python files for Azure IoT Hub Device Simulator...")
    print("=" * 60)
    
    # Create directories
    create_directories()
    print()
    
    # Create init files
    create_init_files()
    print()
    
    print("✓ Basic structure created successfully!")
    print()
    print("Note: This creates the basic directory structure and __init__.py files.")
    print("The main Python modules need to be created separately to avoid file conflicts.")
    print()
    print("Next steps:")
    print("1. Use the individual Python files provided")
    print("2. Copy them into the appropriate directories")
    print("3. Run setup.bat to install dependencies")
    print("4. Run launch.bat to start the application")

if __name__ == "__main__":
    main()
