"""
Settings frame for GGOS
"""

import customtkinter as ctk
from typing import Dict, Any, Callable
import tkinter as tk


class SettingsFrame(ctk.CTkFrame):
    """Frame for application settings"""
    
    def __init__(self, parent, settings: Dict[str, Any], 
                 save_callback: Callable[[Dict[str, Any]], None]):
        super().__init__(parent)
        
        self.settings = settings.copy()
        self.save_callback = save_callback
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Configure grid to fill entire frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="🔧 Settings",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=20)
        
        # Create settings sections
        self.create_appearance_section(self)
        self.create_auto_input_section(self)
        self.create_fitness_tracker_section(self)
        self.create_about_section(self)
        
        # Save button
        save_btn = ctk.CTkButton(
            self,
            text="Save Settings",
            command=self.save_settings,
            height=40,
            width=150
        )
        save_btn.grid(row=5, column=0, pady=20)
    
    def create_appearance_section(self, parent):
        """Create appearance settings section"""
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        section_frame.grid_columnconfigure(1, weight=1)
        
        # Section title
        title = ctk.CTkLabel(
            section_frame,
            text="🎨 Appearance",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(20, 15), sticky="w", padx=20)
        
        # Theme selection
        theme_label = ctk.CTkLabel(section_frame, text="Theme:")
        theme_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")
        
        self.theme_var = ctk.StringVar(value=self.settings.get("theme", "dark"))
        theme_menu = ctk.CTkOptionMenu(
            section_frame,
            values=["dark", "light", "system"],
            variable=self.theme_var,
            width=150
        )
        theme_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Window size
        size_label = ctk.CTkLabel(section_frame, text="Window Size:")
        size_label.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="w")
        
        self.size_var = ctk.StringVar(value=self.settings.get("window_size", "900x700"))
        size_menu = ctk.CTkOptionMenu(
            section_frame,
            values=["800x600", "900x700", "1000x800", "1200x900"],
            variable=self.size_var,
            width=150
        )
        size_menu.grid(row=2, column=1, padx=10, pady=10, sticky="w")
    
    def create_auto_input_section(self, parent):
        """Create auto-input settings section"""
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        section_frame.grid_columnconfigure(1, weight=1)
        
        # Section title
        title = ctk.CTkLabel(
            section_frame,
            text="🎮 Auto-Input (Future Feature)",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(20, 15), sticky="w", padx=20)
        
        # Auto-input enabled
        self.auto_input_var = ctk.BooleanVar(value=self.settings.get("auto_input_enabled", False))
        auto_input_check = ctk.CTkCheckBox(
            section_frame,
            text="Enable automatic death input from games",
            variable=self.auto_input_var,
            state="disabled"  # Disabled for now (future feature)
        )
        auto_input_check.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
        # Supported games info
        games_info = ctk.CTkLabel(
            section_frame,
            text="Supported games: League of Legends, Valorant, CS:GO, Overwatch (coming soon)",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        games_info.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 15), sticky="w")
    
    def create_fitness_tracker_section(self, parent):
        """Create fitness tracker settings section"""
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        section_frame.grid_columnconfigure(1, weight=1)
        
        # Section title
        title = ctk.CTkLabel(
            section_frame,
            text="📱 Fitness Tracker Integration (Future Feature)",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(20, 15), sticky="w", padx=20)
        
        # Fitness tracker enabled
        self.fitness_tracker_var = ctk.BooleanVar(value=self.settings.get("fitness_tracker_enabled", False))
        fitness_check = ctk.CTkCheckBox(
            section_frame,
            text="Enable fitness tracker integration",
            variable=self.fitness_tracker_var,
            state="disabled"  # Disabled for now (future feature)
        )
        fitness_check.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
        # Supported trackers info
        trackers_info = ctk.CTkLabel(
            section_frame,
            text="Supported trackers: Apple Health, Fitbit, Garmin, Strava (coming soon)",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        trackers_info.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 15), sticky="w")
    
    def create_about_section(self, parent):
        """Create about section"""
        section_frame = ctk.CTkFrame(parent)
        section_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=10)
        section_frame.grid_columnconfigure(0, weight=1)
        
        # Section title
        title = ctk.CTkLabel(
            section_frame,
            text="ℹ️ About GGOS",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, pady=(20, 15), sticky="w", padx=20)
        
        # About text
        about_text = """GGOS - Gaming Death Workout System

Turn your gaming deaths into fitness motivation!

Features:
• Configure custom exercises with reps or time-based units
• Generate randomized workouts based on death count
• Save workout history and track progress
• Modern, intuitive interface

Future Enhancements:
• Auto-input from popular games
• Fitness tracker integration
• Workout presets and profiles
• Sound alerts and timers

Version: 1.0.0
"""
        
        about_label = ctk.CTkLabel(
            section_frame,
            text=about_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        about_label.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")
    
    def save_settings(self):
        """Save the current settings"""
        # Update settings dictionary
        self.settings["theme"] = self.theme_var.get()
        self.settings["window_size"] = self.size_var.get()
        self.settings["auto_input_enabled"] = self.auto_input_var.get()
        self.settings["fitness_tracker_enabled"] = self.fitness_tracker_var.get()
        
        # Save settings
        self.save_callback(self.settings)
        
        # Show success message
        import tkinter.messagebox as messagebox
        messagebox.showinfo("Success", "Settings saved successfully!")
