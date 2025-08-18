#!/usr/bin/env python3
"""
Build script for GGOS executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Install PyInstaller for building executable
    print("Installing PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Create a single executable file
        "--windowed",  # Don't show console window on Windows
        "--name=GGOS",  # Name of the executable
        "--icon=assets/icon.ico" if os.path.exists("assets/icon.ico") else "",  # Icon if available
        "--add-data=src;src",  # Include source files
        "main.py"
    ]
    
    # Remove empty strings
    cmd = [arg for arg in cmd if arg]
    
    subprocess.check_call(cmd)
    
    print("Executable built successfully!")
    print(f"Location: {os.path.join('dist', 'GGOS.exe')}")

def create_assets_directory():
    """Create assets directory if it doesn't exist"""
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)
    
    # Create a simple icon placeholder if none exists
    icon_path = assets_dir / "icon.ico"
    if not icon_path.exists():
        print("No icon found. Creating placeholder...")
        # You can add icon creation logic here if needed

def main():
    """Main build process"""
    print("🚀 Building GGOS Executable")
    print("=" * 40)
    
    try:
        # Create assets directory
        create_assets_directory()
        
        # Install requirements
        install_requirements()
        
        # Build executable
        build_executable()
        
        print("\n✅ Build completed successfully!")
        print("\n📁 Files created:")
        print("  - dist/GGOS.exe (Windows executable)")
        print("  - build/ (Build files)")
        print("  - GGOS.spec (PyInstaller spec file)")
        
        print("\n🎯 To run the application:")
        print("  - Double-click dist/GGOS.exe")
        print("  - Or run: python main.py")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
