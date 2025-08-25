"""
Setup frame for GGOS
"""

import customtkinter as ctk
from typing import List, Callable
import tkinter as tk
from tkinter import messagebox

from src.models.exercise import Exercise, UnitType


class SetupFrame(ctk.CTkFrame):
    """Frame for managing exercises"""
    
    def __init__(self, parent, exercises: List[Exercise], 
                 save_callback: Callable[[List[Exercise]], None],
                 load_defaults_callback: Callable[[], None]):
        super().__init__(parent)
        
        self.exercises = exercises
        self.save_callback = save_callback
        self.load_defaults_callback = load_defaults_callback
        
        self.setup_ui()
        self.refresh_exercise_list()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Configure grid to fill entire frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main scrollable frame
        self.main_scrollable_frame = ctk.CTkScrollableFrame(self)
        self.main_scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            self.main_scrollable_frame,
            text="⚙️ Exercise Setup",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=20)
        
        # Add exercise section
        self.create_add_section(self.main_scrollable_frame)
        
        # Exercise list section
        self.create_list_section(self.main_scrollable_frame)
    
    def create_add_section(self, parent):
        """Create the add exercise section"""
        add_frame = ctk.CTkFrame(parent)
        add_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        add_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        add_title = ctk.CTkLabel(
            add_frame,
            text="Add Exercises:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        add_title.grid(row=0, column=0, columnspan=4, pady=(20, 15), sticky="w", padx=20)
        
        # Pre-generated exercises section
        self.create_pregenerated_section(add_frame)
        
        # Custom exercise section
        self.create_custom_section(add_frame)
        
        # Load defaults button
        defaults_btn = ctk.CTkButton(
            add_frame,
            text="Load All Defaults",
            command=self.load_defaults,
            width=150
        )
        defaults_btn.grid(row=8, column=0, columnspan=4, padx=20, pady=10)
    
    def create_pregenerated_section(self, parent):
        """Create the pre-generated exercises section"""
        # Section title
        preg_title = ctk.CTkLabel(
            parent,
            text="Pre-generated Exercises:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        preg_title.grid(row=1, column=0, columnspan=4, pady=(10, 5), sticky="w", padx=20)
        
        # Create scrollable frame for pre-generated exercises
        self.pregenerated_frame = ctk.CTkScrollableFrame(
            parent,
            width=800,
            height=200,
            label_text="Select exercises to add:"
        )
        self.pregenerated_frame.grid(row=2, column=0, columnspan=4, padx=20, pady=5, sticky="ew")
        
        # Load pre-generated exercises
        self.load_pregenerated_exercises()
        
        # Add selected button
        add_selected_btn = ctk.CTkButton(
            parent,
            text="Add Selected",
            command=self.add_selected_exercises,
            width=120
        )
        add_selected_btn.grid(row=3, column=0, columnspan=4, padx=20, pady=5)
    
    def create_custom_section(self, parent):
        """Create the custom exercise section"""
        # Section title
        custom_title = ctk.CTkLabel(
            parent,
            text="Custom Exercise:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        custom_title.grid(row=4, column=0, columnspan=4, pady=(15, 5), sticky="w", padx=20)
        
        # Exercise name
        name_label = ctk.CTkLabel(parent, text="Exercise Name:")
        name_label.grid(row=5, column=0, padx=(20, 10), pady=5, sticky="w")
        
        self.name_entry = ctk.CTkEntry(
            parent,
            placeholder_text="e.g., Custom Exercise...",
            width=200
        )
        self.name_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        
        # Unit type
        unit_label = ctk.CTkLabel(parent, text="Unit Type:")
        unit_label.grid(row=6, column=0, padx=(20, 10), pady=5, sticky="w")
        
        self.unit_var = ctk.StringVar(value="reps")
        unit_frame = ctk.CTkFrame(parent)
        unit_frame.grid(row=6, column=1, padx=10, pady=5, sticky="w")
        
        reps_radio = ctk.CTkRadioButton(
            unit_frame,
            text="Reps",
            variable=self.unit_var,
            value="reps"
        )
        reps_radio.pack(side="left", padx=(10, 20))
        
        seconds_radio = ctk.CTkRadioButton(
            unit_frame,
            text="Seconds",
            variable=self.unit_var,
            value="seconds"
        )
        seconds_radio.pack(side="left", padx=(0, 10))
        
        # Amount per death
        amount_label = ctk.CTkLabel(parent, text="Amount per Death:")
        amount_label.grid(row=7, column=0, padx=(20, 10), pady=5, sticky="w")
        
        self.amount_entry = ctk.CTkEntry(
            parent,
            placeholder_text="e.g., 2",
            width=100
        )
        self.amount_entry.grid(row=7, column=1, padx=10, pady=5, sticky="w")
        
        # Add custom button
        self.add_btn = ctk.CTkButton(
            parent,
            text="Add Custom",
            command=self.add_exercise,
            width=120
        )
        self.add_btn.grid(row=7, column=2, padx=(10, 20), pady=5)
        
        # Bind Enter key
        self.name_entry.bind("<Return>", lambda event: self.add_exercise())
        self.amount_entry.bind("<Return>", lambda event: self.add_exercise())
    
    def load_pregenerated_exercises(self):
        """Load pre-generated exercises into the scrollable frame"""
        from src.services.storage import StorageService
        
        # Get all pre-generated exercises
        storage = StorageService()
        all_exercises = storage.get_default_exercises()
        
        # Group exercises by category
        categories = {
            "Core": [],
            "Cardio": [],
            "Legs": [],
            "Arms": [],
            "Core Variations": [],
            "Full Body": []
        }
        
        # Categorize exercises (this is a simple mapping)
        exercise_categories = {
            "Squats": "Core", "Push-ups": "Core", "Sit-ups": "Core", "Plank": "Core",
            "Jumping Jacks": "Cardio", "Burpees": "Cardio", "Mountain Climbers": "Cardio", "High Knees": "Cardio",
            "Lunges": "Legs", "Calf Raises": "Legs", "Wall Sit": "Legs",
            "Tricep Dips": "Arms", "Arm Circles": "Arms",
            "Bicycle Crunches": "Core Variations", "Russian Twists": "Core Variations", "Superman Hold": "Core Variations",
            "Bear Crawls": "Full Body", "Spider-Man Push-ups": "Full Body", "Donkey Kicks": "Full Body", "Fire Hydrants": "Full Body"
        }
        
        for exercise in all_exercises:
            category = exercise_categories.get(exercise.name, "Core")
            categories[category].append(exercise)
        
        # Create exercise selection widgets
        self.exercise_vars = {}
        self.quantity_entries = {}  # Store quantity entries separately
        row = 0
        
        for category, exercises in categories.items():
            if exercises:
                # Category label
                cat_label = ctk.CTkLabel(
                    self.pregenerated_frame,
                    text=f"📁 {category}:",
                    font=ctk.CTkFont(size=12, weight="bold")
                )
                cat_label.grid(row=row, column=0, columnspan=4, pady=(10, 5), sticky="w")
                row += 1
                
                # Exercises in this category
                for exercise in exercises:
                    # Checkbox
                    var = ctk.BooleanVar()
                    self.exercise_vars[exercise.name] = var
                    
                    checkbox = ctk.CTkCheckBox(
                        self.pregenerated_frame,
                        text=f"{exercise.name}",
                        variable=var
                    )
                    checkbox.grid(row=row, column=0, pady=2, sticky="w")
                    
                    # Amount per death entry
                    amount_label = ctk.CTkLabel(self.pregenerated_frame, text="Amount per death:")
                    amount_label.grid(row=row, column=1, padx=(20, 5), pady=2)
                    
                    amount_entry = ctk.CTkEntry(
                        self.pregenerated_frame,
                        placeholder_text=str(exercise.amount_per_death),
                        width=80
                    )
                    amount_entry.insert(0, str(exercise.amount_per_death))
                    amount_entry.grid(row=row, column=2, padx=5, pady=2)
                    
                    # Unit type selection
                    unit_var = ctk.StringVar(value=exercise.unit_type.value)
                    unit_menu = ctk.CTkOptionMenu(
                        self.pregenerated_frame,
                        values=["reps", "seconds"],
                        variable=unit_var,
                        width=80
                    )
                    unit_menu.grid(row=row, column=3, padx=5, pady=2)
                    
                    # Store references
                    self.quantity_entries[exercise.name] = {
                        'amount': amount_entry,
                        'unit': unit_var
                    }
                    
                    row += 1
    
    def create_list_section(self, parent):
        """Create the exercise list section"""
        list_frame = ctk.CTkFrame(parent)
        list_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(1, weight=1)
        
        # List title
        list_title = ctk.CTkLabel(
            list_frame,
            text="Current Exercises:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        list_title.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=20)
        
        # Exercise list
        self.exercise_listbox = ctk.CTkTextbox(
            list_frame,
            wrap="word",
            font=ctk.CTkFont(size=12),
            height=250
        )
        self.exercise_listbox.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(list_frame)
        buttons_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Edit button
        self.edit_btn = ctk.CTkButton(
            buttons_frame,
            text="Edit Selected",
            command=self.edit_exercise,
            height=35
        )
        self.edit_btn.grid(row=0, column=0, padx=(0, 10), pady=10)
        
        # Delete button
        self.delete_btn = ctk.CTkButton(
            buttons_frame,
            text="Delete Selected",
            command=self.delete_exercise,
            height=35
        )
        self.delete_btn.grid(row=0, column=1, padx=10, pady=10)
        
        # Clear all button
        clear_btn = ctk.CTkButton(
            buttons_frame,
            text="Clear All",
            command=self.clear_all_exercises,
            height=35
        )
        clear_btn.grid(row=0, column=2, padx=(10, 0), pady=10)
        
        # Initially disable edit/delete buttons
        self.edit_btn.configure(state="disabled")
        self.delete_btn.configure(state="disabled")
        
        # Store selected exercise
        self.selected_exercise = None
    
    def add_exercise(self):
        """Add a new exercise"""
        try:
            name = self.name_entry.get().strip()
            if not name:
                messagebox.showwarning("Input Required", "Please enter an exercise name.")
                return
            
            amount_text = self.amount_entry.get().strip()
            if not amount_text:
                messagebox.showwarning("Input Required", "Please enter amount per death.")
                return
            
            amount = int(amount_text)
            if amount <= 0:
                messagebox.showwarning("Invalid Input", "Amount must be positive.")
                return
            
            unit_type = UnitType(self.unit_var.get())
            
            # Check for duplicate names
            if any(ex.name.lower() == name.lower() for ex in self.exercises):
                messagebox.showwarning("Duplicate", "An exercise with this name already exists.")
                return
            
            # Create new exercise
            new_exercise = Exercise(name, unit_type, amount)
            self.exercises.append(new_exercise)
            
            # Save and refresh
            self.save_callback(self.exercises)
            self.refresh_exercise_list()
            
            # Clear inputs
            self.name_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.name_entry.focus()
            
            messagebox.showinfo("Success", f"Exercise '{name}' added successfully!")
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for amount.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def edit_exercise(self):
        """Edit the selected exercise"""
        if not self.selected_exercise:
            return
        
        # Create edit dialog
        dialog = EditExerciseDialog(self, self.selected_exercise)
        self.wait_window(dialog)
        
        if dialog.result:
            # Update exercise
            self.selected_exercise.name = dialog.result["name"]
            self.selected_exercise.unit_type = dialog.result["unit_type"]
            self.selected_exercise.amount_per_death = dialog.result["amount"]
            
            # Save and refresh
            self.save_callback(self.exercises)
            self.refresh_exercise_list()
            
            messagebox.showinfo("Success", "Exercise updated successfully!")
    
    def delete_exercise(self):
        """Delete the selected exercise"""
        if not self.selected_exercise:
            return
        
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{self.selected_exercise.name}'?"
        )
        
        if result:
            self.exercises.remove(self.selected_exercise)
            self.save_callback(self.exercises)
            self.refresh_exercise_list()
            self.selected_exercise = None
            self.edit_btn.configure(state="disabled")
            self.delete_btn.configure(state="disabled")
    
    def clear_all_exercises(self):
        """Clear all exercises"""
        if not self.exercises:
            return
        
        result = messagebox.askyesno(
            "Confirm Clear",
            "Are you sure you want to delete all exercises?"
        )
        
        if result:
            self.exercises.clear()
            self.save_callback(self.exercises)
            self.refresh_exercise_list()
            self.selected_exercise = None
            self.edit_btn.configure(state="disabled")
            self.delete_btn.configure(state="disabled")
    
    def add_selected_exercises(self):
        """Add selected pre-generated exercises"""
        from src.services.storage import StorageService
        from src.models.exercise import UnitType
        
        storage = StorageService()
        all_exercises = storage.get_default_exercises()
        
        added_count = 0
        for exercise in all_exercises:
            if exercise.name in self.exercise_vars and self.exercise_vars[exercise.name].get():
                try:
                    # Get custom amount and unit from user input
                    amount_text = self.quantity_entries[exercise.name]['amount'].get().strip()
                    unit_type = self.quantity_entries[exercise.name]['unit'].get()
                    
                    if not amount_text:
                        continue
                    
                    amount = int(amount_text)
                    if amount <= 0:
                        continue
                    
                    # Check if exercise already exists
                    existing_names = [ex.name.lower() for ex in self.exercises]
                    if exercise.name.lower() in existing_names:
                        continue
                    
                    # Create new exercise with custom settings
                    new_exercise = Exercise(
                        name=exercise.name,
                        unit_type=UnitType(unit_type),
                        amount_per_death=amount
                    )
                    
                    # Add the exercise
                    self.exercises.append(new_exercise)
                    added_count += 1
                    
                except ValueError:
                    continue
        
        if added_count > 0:
            self.save_callback(self.exercises)
            self.refresh_exercise_list()
            messagebox.showinfo("Success", f"Added {added_count} exercise(s)!")
        else:
            messagebox.showwarning("No Selection", "Please select at least one exercise to add.")
    
    def load_defaults(self):
        """Load default exercises"""
        result = messagebox.askyesno(
            "Load Defaults",
            "This will replace all current exercises with default ones. Continue?"
        )
        
        if result:
            self.load_defaults_callback()
            self.refresh_exercise_list()
            messagebox.showinfo("Success", "Default exercises loaded!")
    
    def refresh_exercise_list(self):
        """Refresh the exercise list display"""
        self.exercise_listbox.delete("1.0", tk.END)
        
        if not self.exercises:
            self.exercise_listbox.insert("1.0", "No exercises configured.\nAdd some exercises above or load defaults.")
            return
        
        for i, exercise in enumerate(self.exercises, 1):
            line = f"{i}. {exercise.name} - {exercise.amount_per_death} {exercise.get_unit_display()} per death\n"
            self.exercise_listbox.insert(tk.END, line)
    
    def update_exercises(self, exercises: List[Exercise]):
        """Update the exercises list"""
        self.exercises = exercises
        self.refresh_exercise_list()


class EditExerciseDialog(ctk.CTkToplevel):
    """Dialog for editing exercises"""
    
    def __init__(self, parent, exercise: Exercise):
        super().__init__(parent)
        
        self.exercise = exercise
        self.result = None
        
        self.title("Edit Exercise")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
        
        # Center dialog
        self.center_window()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Edit Exercise",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(20, 20))
        
        # Form frame
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Exercise name
        name_label = ctk.CTkLabel(form_frame, text="Exercise Name:")
        name_label.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="w")
        
        self.name_entry = ctk.CTkEntry(form_frame, width=200)
        self.name_entry.insert(0, self.exercise.name)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Unit type
        unit_label = ctk.CTkLabel(form_frame, text="Unit Type:")
        unit_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")
        
        self.unit_var = ctk.StringVar(value=self.exercise.unit_type.value)
        unit_frame = ctk.CTkFrame(form_frame)
        unit_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        reps_radio = ctk.CTkRadioButton(
            unit_frame,
            text="Reps",
            variable=self.unit_var,
            value="reps"
        )
        reps_radio.pack(side="left", padx=(10, 20))
        
        seconds_radio = ctk.CTkRadioButton(
            unit_frame,
            text="Seconds",
            variable=self.unit_var,
            value="seconds"
        )
        seconds_radio.pack(side="left", padx=(0, 10))
        
        # Amount per death
        amount_label = ctk.CTkLabel(form_frame, text="Amount per Death:")
        amount_label.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="w")
        
        self.amount_entry = ctk.CTkEntry(form_frame, width=100)
        self.amount_entry.insert(0, str(self.exercise.amount_per_death))
        self.amount_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=20)
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Save button
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Save",
            command=self.save_changes,
            height=35
        )
        save_btn.grid(row=0, column=0, padx=(0, 10), pady=10)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=self.cancel,
            height=35
        )
        cancel_btn.grid(row=0, column=1, padx=(10, 0), pady=10)
    
    def save_changes(self):
        """Save the changes"""
        try:
            name = self.name_entry.get().strip()
            if not name:
                messagebox.showwarning("Input Required", "Please enter an exercise name.")
                return
            
            amount_text = self.amount_entry.get().strip()
            if not amount_text:
                messagebox.showwarning("Input Required", "Please enter amount per death.")
                return
            
            amount = int(amount_text)
            if amount <= 0:
                messagebox.showwarning("Invalid Input", "Amount must be positive.")
                return
            
            unit_type = UnitType(self.unit_var.get())
            
            self.result = {
                "name": name,
                "unit_type": unit_type,
                "amount": amount
            }
            
            self.destroy()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for amount.")
    
    def cancel(self):
        """Cancel the dialog"""
        self.destroy()
    
    def center_window(self):
        """Center the dialog on screen"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
