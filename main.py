#!/usr/bin/env python3
"""
GGOS - Gaming Death Workout System
Main application entry point
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from gui.app import GGOSApp

def main():
    """Main entry point for the GGOS application"""
    try:
        app = GGOSApp()
        app.run()
    except Exception as e:
        print(f"Error starting GGOS: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
