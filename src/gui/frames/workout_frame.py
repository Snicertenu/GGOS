"""
Workout frame for GGOS
"""

import customtkinter as ctk
from typing import List, Callable
import tkinter as tk
from tkinter import messagebox

from src.models.exercise import Exercise
from src.models.workout import Workout


class WorkoutFrame(ctk.CTkFrame):
    """Frame for generating workouts from deaths"""
    
    def __init__(self, parent, exercises: List[Exercise], 
                 generate_callback: Callable[[int], Workout],
                 save_callback: Callable[[Workout, int], None]):
        super().__init__(parent)
        
        self.exercises = exercises
        self.generate_callback = generate_callback
        self.save_callback = save_callback
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Configure grid to fill entire frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="🏃 Generate Workout",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=20)
        
        # Input section
        self.create_input_section(self)
        
        # Results section
        self.create_results_section(self)
        

    
    def create_input_section(self, parent):
        """Create the input section"""
        input_frame = ctk.CTkFrame(parent)
        input_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Deaths input
        deaths_label = ctk.CTkLabel(
            input_frame,
            text="Number of Deaths:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        deaths_label.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="w")
        
        self.deaths_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter number of deaths...",
            width=300,
            height=40
        )
        self.deaths_entry.grid(row=0, column=1, padx=10, pady=20, sticky="w")
        
        # Generate button
        self.generate_btn = ctk.CTkButton(
            input_frame,
            text="Generate Workout",
            command=self.generate_workout,
            height=40,
            width=150
        )
        self.generate_btn.grid(row=0, column=2, padx=(10, 20), pady=20)
        
        # Bind Enter key
        self.deaths_entry.bind("<Return>", lambda event: self.generate_workout())
    
    def create_results_section(self, parent):
        """Create the results section"""
        results_frame = ctk.CTkFrame(parent)
        results_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)
        
        # Results title
        results_title = ctk.CTkLabel(
            results_frame,
            text="Your Workout:",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        results_title.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=20)
        
        # Results text area
        self.results_text = ctk.CTkTextbox(
            results_frame,
            wrap="word",
            font=ctk.CTkFont(size=14),
            height=300
        )
        self.results_text.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(results_frame)
        buttons_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Save button
        self.save_btn = ctk.CTkButton(
            buttons_frame,
            text="Save Workout",
            command=self.save_workout,
            height=40
        )
        self.save_btn.grid(row=0, column=0, padx=(0, 10), pady=10)
        
        # Clear button
        self.clear_btn = ctk.CTkButton(
            buttons_frame,
            text="Clear",
            command=self.clear_results,
            height=40
        )
        self.clear_btn.grid(row=0, column=1, padx=(10, 0), pady=10)
        
        # Initially disable save button
        self.save_btn.configure(state="disabled")
        
        # Store current workout
        self.current_workout = None
        self.current_deaths = 0
    
    def generate_workout(self):
        """Generate a workout based on input deaths"""
        try:
            deaths_text = self.deaths_entry.get().strip()
            if not deaths_text:
                messagebox.showwarning("Input Required", "Please enter the number of deaths.")
                return
            
            deaths = int(deaths_text)
            if deaths <= 0:
                messagebox.showwarning("Invalid Input", "Number of deaths must be positive.")
                return
            
            if not self.exercises:
                messagebox.showwarning("No Exercises", "Please add some exercises in the Setup tab first.")
                return
            
            # Generate workout
            workout = self.generate_callback(deaths)
            self.current_workout = workout
            self.current_deaths = deaths
            
            # Display results
            self.display_workout(workout)
            
            # Enable save button
            self.save_btn.configure(state="normal")
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for deaths.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def display_workout(self, workout: Workout):
        """Display the workout results"""
        self.results_text.delete("1.0", tk.END)
        
        if not workout.exercises:
            self.results_text.insert("1.0", "No exercises configured. Please add exercises in the Setup tab.")
            return
        
        # Header
        header = f"🎯 Workout for {self.current_deaths} deaths:\n\n"
        self.results_text.insert("1.0", header)
        
        # Exercises grouped by unit type
        grouped = workout.get_exercises_by_unit_type()
        
        # Reps exercises
        if grouped["reps"]:
            self.results_text.insert(tk.END, "💪 Reps:\n")
            for we in grouped["reps"]:
                line = f"  • {we.get_display_text()}\n"
                self.results_text.insert(tk.END, line)
            self.results_text.insert(tk.END, "\n")
        
        # Time-based exercises
        if grouped["seconds"]:
            self.results_text.insert(tk.END, "⏱️ Time:\n")
            for we in grouped["seconds"]:
                line = f"  • {we.get_display_text()}\n"
                self.results_text.insert(tk.END, line)
            self.results_text.insert(tk.END, "\n")
        
        # Summary
        summary = f"📊 Summary: {workout.get_summary()}\n"
        summary += f"✅ Total deaths accounted for: {workout.total_deaths}/{self.current_deaths}\n"
        
        if workout.total_deaths < self.current_deaths:
            summary += f"⚠️ Note: {self.current_deaths - workout.total_deaths} deaths not allocated (random distribution)\n"
        
        self.results_text.insert(tk.END, summary)
    
    def save_workout(self):
        """Save the current workout"""
        if self.current_workout and self.current_deaths > 0:
            self.save_callback(self.current_workout, self.current_deaths)
            messagebox.showinfo("Success", "Workout saved to history!")
    
    def clear_results(self):
        """Clear the results and input"""
        self.results_text.delete("1.0", tk.END)
        self.deaths_entry.delete(0, tk.END)
        self.save_btn.configure(state="disabled")
        self.current_workout = None
        self.current_deaths = 0
    
    def update_exercises(self, exercises: List[Exercise]):
        """Update the exercises list"""
        self.exercises = exercises
