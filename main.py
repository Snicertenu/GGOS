#!/usr/bin/env python3
"""
GGOS - Gaming Death Workout System
Main application entry point
"""

import sys
import os
from pathlib import Path

# Handle both development and executable environments
if getattr(sys, 'frozen', False):
    # Running as executable (PyInstaller)
    base_path = Path(sys._MEIPASS)
    src_path = base_path / "src"
else:
    # Running in development
    base_path = Path(__file__).parent
    src_path = base_path / "src"

# Add the src directory to the Python path
if src_path.exists():
    sys.path.insert(0, str(src_path))

# Import using the full path structure
try:
    from src.gui.app import GGOSApp
except ImportError:
    try:
        # Fallback for development
        from gui.app import GGOSApp
    except ImportError as e:
        print(f"Import error: {e}")
        print(f"Current sys.path: {sys.path}")
        print(f"Looking for src at: {src_path}")
        print(f"src_path exists: {src_path.exists()}")
        if src_path.exists():
            print(f"src_path contents: {list(src_path.iterdir())}")
        sys.exit(1)

def main():
    """Main entry point for the GGOS application"""
    try:
        app = GGOSApp()
        app.run()
    except Exception as e:
        print(f"Error starting GGOS: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
