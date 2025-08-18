"""
Main GUI application for GGOS
"""

import customtkinter as ctk
from typing import List, Optional
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from src.models.exercise import Exercise, UnitType
from src.models.workout import WorkoutGenerator, Workout
from src.services.storage import StorageService
from src.gui.frames.setup_frame import SetupFrame
from src.gui.frames.workout_frame import WorkoutFrame
from src.gui.frames.settings_frame import SettingsFrame
from src.gui.frames.history_frame import HistoryFrame


class GGOSApp:
    """Main application class for GGOS"""
    
    def __init__(self):
        """Initialize the application"""
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize storage
        self.storage = StorageService()
        
        # Load data
        self.exercises = self.storage.load_exercises()
        self.settings = self.storage.load_settings()
        
        # If no exercises exist, load defaults
        if not self.exercises:
            self.exercises = self.storage.get_default_exercises()
            self.storage.save_exercises(self.exercises)
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("GGOS - Gaming Death Workout System")
        self.root.geometry(self.settings.get("window_size", "900x700"))
        self.root.minsize(800, 600)
        
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Create navigation
        self.create_navigation()
        
        # Create main content area
        self.create_content_area()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Show initial frame
        self.show_frame("workout")
    
    def create_navigation(self):
        """Create the navigation bar"""
        nav_frame = ctk.CTkFrame(self.root)
        nav_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        nav_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Navigation buttons
        self.nav_buttons = {}
        
        nav_items = [
            ("workout", "🏃 Workout", "Generate workout from deaths"),
            ("setup", "⚙️ Setup", "Configure exercises"),
            ("history", "📊 History", "View workout history"),
            ("settings", "🔧 Settings", "Application settings")
        ]
        
        for i, (key, text, tooltip) in enumerate(nav_items):
            btn = ctk.CTkButton(
                nav_frame,
                text=text,
                command=lambda k=key: self.show_frame(k),
                height=40
            )
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            self.nav_buttons[key] = btn
        
        # Update button styles
        self.update_nav_buttons()
    
    def create_content_area(self):
        """Create the main content area with frames"""
        # Create main content frame that fills the entire available space
        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Create frames
        self.frames = {}
        
        # Workout frame
        self.frames["workout"] = WorkoutFrame(
            self.content_frame,
            self.exercises,
            self.generate_workout,
            self.save_workout
        )
        
        # Setup frame
        self.frames["setup"] = SetupFrame(
            self.content_frame,
            self.exercises,
            self.save_exercises,
            self.load_default_exercises
        )
        
        # History frame
        self.frames["history"] = HistoryFrame(
            self.content_frame,
            self.storage.load_workout_history()
        )
        
        # Settings frame
        self.frames["settings"] = SettingsFrame(
            self.content_frame,
            self.settings,
            self.save_settings
        )
    
    def show_frame(self, frame_name: str):
        """Show the specified frame"""
        # Hide all frames
        for frame in self.frames.values():
            frame.grid_remove()
        
        # Show selected frame
        if frame_name in self.frames:
            self.frames[frame_name].grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Update navigation buttons
        self.update_nav_buttons(frame_name)
    
    def update_nav_buttons(self, active_frame: Optional[str] = None):
        """Update navigation button styles"""
        for key, btn in self.nav_buttons.items():
            if key == active_frame:
                btn.configure(fg_color=("gray75", "gray25"))
            else:
                btn.configure(fg_color=("gray70", "gray30"))
    
    def generate_workout(self, deaths: int) -> Workout:
        """Generate a workout for the given number of deaths"""
        return WorkoutGenerator.generate_workout(self.exercises, deaths)
    
    def save_workout(self, workout: Workout, deaths: int):
        """Save workout to history"""
        workout_data = {
            "timestamp": datetime.now().isoformat(),
            "deaths": deaths,
            "total_deaths_accounted": workout.total_deaths,
            "summary": workout.get_summary(),
            "exercises": [
                {
                    "name": we.exercise.name,
                    "amount": we.allocated_amount,
                    "unit": we.exercise.get_unit_display(),
                    "deaths_allocated": we.deaths_allocated
                }
                for we in workout.exercises
            ]
        }
        
        self.storage.save_workout_history(workout_data)
        
        # Refresh history frame
        if "history" in self.frames:
            self.frames["history"].refresh_history(self.storage.load_workout_history())
    
    def save_exercises(self, exercises: List[Exercise]):
        """Save exercises and update the application"""
        self.exercises = exercises
        self.storage.save_exercises(exercises)
        
        # Update workout frame
        if "workout" in self.frames:
            self.frames["workout"].update_exercises(exercises)
    
    def load_default_exercises(self):
        """Load default exercises"""
        self.exercises = self.storage.get_default_exercises()
        self.storage.save_exercises(self.exercises)
        
        # Update setup frame
        if "setup" in self.frames:
            self.frames["setup"].update_exercises(self.exercises)
        
        # Update workout frame
        if "workout" in self.frames:
            self.frames["workout"].update_exercises(self.exercises)
    
    def save_settings(self, settings: dict):
        """Save settings and update the application"""
        self.settings = settings
        self.storage.save_settings(settings)
        
        # Apply theme changes
        if "theme" in settings:
            ctk.set_appearance_mode(settings["theme"])
    
    def on_closing(self):
        """Handle application closing"""
        # Save window size
        self.settings["window_size"] = self.root.geometry()
        self.storage.save_settings(self.settings)
        
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()
