#!/usr/bin/env python3
"""
Build script for GGOS - Gaming Death Workout System
Creates a standalone executable using PyInstaller
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages for building"""
    print("Installing build requirements...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install PyInstaller: {e}")
        return False
    return True

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building GGOS executable...")
    
    # Check if spec file exists
    spec_file = Path("GGOS.spec")
    if spec_file.exists():
        print("Using existing GGOS.spec file...")
        cmd = [sys.executable, "-m", "PyInstaller", "GGOS.spec"]
    else:
        print("Creating new executable with PyInstaller...")
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name=GGOS",
            "--add-data=src;src",  # Include src directory
            "--hidden-import=src.gui.app",
            "--hidden-import=src.gui.frames.workout_frame",
            "--hidden-import=src.gui.frames.setup_frame",
            "--hidden-import=src.gui.frames.history_frame", 
            "--hidden-import=src.gui.frames.settings_frame",
            "--hidden-import=src.models.exercise",
            "--hidden-import=src.models.workout",
            "--hidden-import=src.services.storage",
            "--hidden-import=customtkinter",
            "--hidden-import=PIL",
            "main.py"
        ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Executable built successfully!")
        
        # Check if executable was created
        exe_path = Path("dist/GGOS.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📁 Executable created: {exe_path} ({size_mb:.1f} MB)")
            return True
        else:
            print("❌ Executable not found in dist/ directory")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def main():
    """Main build process"""
    print("🔨 Building GGOS - Get Good or Swole!")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Build executable
    if not build_executable():
        sys.exit(1)
    
    print("\n🎉 Build completed successfully!")
    print("You can now run the executable from the dist/ directory")

if __name__ == "__main__":
    main()
