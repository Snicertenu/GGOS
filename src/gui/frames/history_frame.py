"""
History frame for GGOS
"""

import customtkinter as ctk
from typing import List, Dict, Any
import tkinter as tk
from datetime import datetime


class HistoryFrame(ctk.CTkFrame):
    """Frame for displaying workout history"""
    
    def __init__(self, parent, workout_history: List[Dict[str, Any]]):
        super().__init__(parent)
        
        self.workout_history = workout_history
        
        self.setup_ui()
        self.refresh_history()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Configure grid to fill entire frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="📊 Workout History",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=20)
        
        # Controls section
        self.create_controls_section(self)
        
        # History display section
        self.create_history_section(self)
    
    def create_controls_section(self, parent):
        """Create the controls section"""
        controls_frame = ctk.CTkFrame(parent)
        controls_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        controls_frame.grid_columnconfigure(1, weight=1)
        
        # Filter label
        filter_label = ctk.CTkLabel(controls_frame, text="Filter by:")
        filter_label.grid(row=0, column=0, padx=(20, 10), pady=15, sticky="w")
        
        # Filter options
        self.filter_var = ctk.StringVar(value="all")
        filter_menu = ctk.CTkOptionMenu(
            controls_frame,
            values=["all", "recent", "high_deaths", "low_deaths"],
            variable=self.filter_var,
            command=self.apply_filter,
            width=150
        )
        filter_menu.grid(row=0, column=1, padx=10, pady=15, sticky="w")
        
        # Clear history button
        clear_btn = ctk.CTkButton(
            controls_frame,
            text="Clear History",
            command=self.clear_history,
            width=120,
            height=30
        )
        clear_btn.grid(row=0, column=2, padx=(10, 20), pady=15)
    
    def create_history_section(self, parent):
        """Create the history display section"""
        history_frame = ctk.CTkFrame(parent)
        history_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        history_frame.grid_columnconfigure(0, weight=1)
        history_frame.grid_rowconfigure(1, weight=1)
        
        # History title
        history_title = ctk.CTkLabel(
            history_frame,
            text="Recent Workouts:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        history_title.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=20)
        
        # History text area
        self.history_text = ctk.CTkTextbox(
            history_frame,
            wrap="word",
            font=ctk.CTkFont(size=12),
            height=300
        )
        self.history_text.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Statistics frame
        stats_frame = ctk.CTkFrame(history_frame)
        stats_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Statistics labels
        self.total_workouts_label = ctk.CTkLabel(
            stats_frame,
            text="Total Workouts: 0",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.total_workouts_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.total_deaths_label = ctk.CTkLabel(
            stats_frame,
            text="Total Deaths: 0",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.total_deaths_label.grid(row=0, column=1, padx=10, pady=10)
        
        self.avg_deaths_label = ctk.CTkLabel(
            stats_frame,
            text="Avg Deaths: 0",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.avg_deaths_label.grid(row=0, column=2, padx=10, pady=10)
        
        self.total_reps_label = ctk.CTkLabel(
            stats_frame,
            text="Total Reps: 0",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.total_reps_label.grid(row=0, column=3, padx=10, pady=10)
    
    def refresh_history(self, workout_history: List[Dict[str, Any]] = None):
        """Refresh the history display"""
        if workout_history is not None:
            self.workout_history = workout_history
        
        self.apply_filter()
        self.update_statistics()
    
    def apply_filter(self, *args):
        """Apply the selected filter"""
        filter_type = self.filter_var.get()
        filtered_history = self.workout_history.copy()
        
        if filter_type == "recent":
            # Show only last 10 workouts
            filtered_history = filtered_history[-10:]
        elif filter_type == "high_deaths":
            # Show workouts with 10+ deaths
            filtered_history = [w for w in filtered_history if w.get("deaths", 0) >= 10]
        elif filter_type == "low_deaths":
            # Show workouts with < 10 deaths
            filtered_history = [w for w in filtered_history if w.get("deaths", 0) < 10]
        
        self.display_history(filtered_history)
    
    def display_history(self, history: List[Dict[str, Any]]):
        """Display the workout history"""
        self.history_text.delete("1.0", tk.END)
        
        if not history:
            self.history_text.insert("1.0", "No workout history found.\nGenerate some workouts to see them here!")
            return
        
        # Sort by timestamp (newest first)
        sorted_history = sorted(history, key=lambda x: x.get("timestamp", ""), reverse=True)
        
        for i, workout in enumerate(sorted_history, 1):
            # Parse timestamp
            timestamp = workout.get("timestamp", "")
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                date_str = dt.strftime("%Y-%m-%d %H:%M")
            except:
                date_str = "Unknown date"
            
            # Format workout entry
            deaths = workout.get("deaths", 0)
            summary = workout.get("summary", "No summary")
            
            entry = f"📅 {date_str}\n"
            entry += f"💀 Deaths: {deaths}\n"
            entry += f"📊 Summary: {summary}\n"
            
            # Add exercises if available
            exercises = workout.get("exercises", [])
            if exercises:
                entry += "🏃‍♂️ Exercises:\n"
                for exercise in exercises:
                    name = exercise.get("name", "Unknown")
                    amount = exercise.get("amount", 0)
                    unit = exercise.get("unit", "")
                    deaths_allocated = exercise.get("deaths_allocated", 0)
                    entry += f"  • {amount} {name} ({deaths_allocated} deaths)\n"
            
            entry += "\n" + "─" * 50 + "\n\n"
            
            self.history_text.insert(tk.END, entry)
    
    def update_statistics(self):
        """Update the statistics display"""
        if not self.workout_history:
            self.total_workouts_label.configure(text="Total Workouts: 0")
            self.total_deaths_label.configure(text="Total Deaths: 0")
            self.avg_deaths_label.configure(text="Avg Deaths: 0")
            self.total_reps_label.configure(text="Total Reps: 0")
            return
        
        total_workouts = len(self.workout_history)
        total_deaths = sum(w.get("deaths", 0) for w in self.workout_history)
        avg_deaths = total_deaths / total_workouts if total_workouts > 0 else 0
        
        # Calculate total reps (approximate from summary)
        total_reps = 0
        for workout in self.workout_history:
            summary = workout.get("summary", "")
            if "reps" in summary:
                try:
                    # Extract reps number from summary like "25 reps + 30 seconds"
                    parts = summary.split("+")
                    for part in parts:
                        if "reps" in part:
                            reps_str = part.strip().split()[0]
                            total_reps += int(reps_str)
                except:
                    pass
        
        self.total_workouts_label.configure(text=f"Total Workouts: {total_workouts}")
        self.total_deaths_label.configure(text=f"Total Deaths: {total_deaths}")
        self.avg_deaths_label.configure(text=f"Avg Deaths: {avg_deaths:.1f}")
        self.total_reps_label.configure(text=f"Total Reps: {total_reps}")
    
    def clear_history(self):
        """Clear all workout history"""
        import tkinter.messagebox as messagebox
        
        result = messagebox.askyesno(
            "Clear History",
            "Are you sure you want to clear all workout history? This action cannot be undone."
        )
        
        if result:
            self.workout_history.clear()
            self.refresh_history()
            messagebox.showinfo("Success", "Workout history cleared!")
