#!/usr/bin/env python3
"""
Installation script for GGOS
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Install customtkinter
        print("Installing customtkinter...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter==5.2.0"])
        
        # Install pillow
        print("Installing pillow...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow>=10.0.0"])
        
        print("✅ All dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def test_imports():
    """Test if all modules can be imported"""
    print("\n🧪 Testing imports...")
    
    try:
        import customtkinter
        import PIL
        print("✅ All dependencies imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def run_tests():
    """Run the test suite"""
    print("\n🧪 Running tests...")
    
    try:
        subprocess.check_call([sys.executable, "test_app.py"])
        return True
    except subprocess.CalledProcessError:
        print("❌ Some tests failed")
        return False

def main():
    """Main installation process"""
    print("🚀 GGOS Installation")
    print("=" * 30)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("⚠️ Tests failed, but installation may still work")
    
    print("\n🎉 Installation completed successfully!")
    print("\n📖 Next steps:")
    print("1. Run the application: python main.py")
    print("2. Or build executable: python build.py")
    print("\n💡 The app comes with 20+ equipment-free exercises pre-loaded!")
    print("✅ All import issues have been resolved!")

if __name__ == "__main__":
    main()
