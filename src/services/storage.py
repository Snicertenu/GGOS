"""
Storage service for GGOS
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.models.exercise import Exercise, UnitType


class StorageService:
    """Handles data persistence for GGOS"""
    
    def __init__(self, data_dir: Optional[str] = None):
        """Initialize storage service"""
        if data_dir is None:
            # Use user's home directory
            self.data_dir = Path.home() / ".ggos"
        else:
            self.data_dir = Path(data_dir)
        
        # Ensure data directory exists
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # File paths
        self.exercises_file = self.data_dir / "exercises.json"
        self.settings_file = self.data_dir / "settings.json"
        self.workout_history_file = self.data_dir / "workout_history.json"
    
    def save_exercises(self, exercises: List[Exercise]) -> bool:
        """Save exercises to file"""
        try:
            data = [exercise.to_dict() for exercise in exercises]
            with open(self.exercises_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving exercises: {e}")
            return False
    
    def load_exercises(self) -> List[Exercise]:
        """Load exercises from file"""
        try:
            if not self.exercises_file.exists():
                return []
            
            with open(self.exercises_file, 'r') as f:
                data = json.load(f)
            
            return [Exercise.from_dict(item) for item in data]
        except Exception as e:
            print(f"Error loading exercises: {e}")
            return []
    
    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file"""
        default_settings = {
            "auto_input_enabled": False,
            "fitness_tracker_enabled": False,
            "theme": "dark",
            "window_size": "800x600"
        }
        
        try:
            if not self.settings_file.exists():
                return default_settings
            
            with open(self.settings_file, 'r') as f:
                data = json.load(f)
            
            # Merge with defaults to ensure all keys exist
            for key, value in default_settings.items():
                if key not in data:
                    data[key] = value
            
            return data
        except Exception as e:
            print(f"Error loading settings: {e}")
            return default_settings
    
    def save_workout_history(self, workout_data: Dict[str, Any]) -> bool:
        """Save workout to history"""
        try:
            history = self.load_workout_history()
            history.append(workout_data)
            
            # Keep only last 100 workouts
            if len(history) > 100:
                history = history[-100:]
            
            with open(self.workout_history_file, 'w') as f:
                json.dump(history, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving workout history: {e}")
            return False
    
    def load_workout_history(self) -> List[Dict[str, Any]]:
        """Load workout history"""
        try:
            if not self.workout_history_file.exists():
                return []
            
            with open(self.workout_history_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading workout history: {e}")
            return []
    
    def get_default_exercises(self) -> List[Exercise]:
        """Get default exercises for new users (equipment-free)"""
        return [
            # Core exercises
            Exercise("Squats", UnitType.REPS, 2),
            Exercise("Push-ups", UnitType.REPS, 1),
            Exercise("Sit-ups", UnitType.REPS, 2),
            Exercise("Plank", UnitType.SECONDS, 5),
            
            # Cardio exercises
            Exercise("Jumping Jacks", UnitType.REPS, 5),
            Exercise("Burpees", UnitType.REPS, 1),
            Exercise("Mountain Climbers", UnitType.REPS, 3),
            Exercise("High Knees", UnitType.REPS, 4),
            
            # Leg exercises
            Exercise("Lunges", UnitType.REPS, 2),
            Exercise("Calf Raises", UnitType.REPS, 3),
            Exercise("Wall Sit", UnitType.SECONDS, 3),
            
            # Arm exercises
            Exercise("Tricep Dips", UnitType.REPS, 2),
            Exercise("Arm Circles", UnitType.REPS, 4),
            
            # Core variations
            Exercise("Bicycle Crunches", UnitType.REPS, 2),
            Exercise("Russian Twists", UnitType.REPS, 3),
            Exercise("Superman Hold", UnitType.SECONDS, 4),
            
            # Full body
            Exercise("Bear Crawls", UnitType.REPS, 1),
            Exercise("Spider-Man Push-ups", UnitType.REPS, 1),
            Exercise("Donkey Kicks", UnitType.REPS, 2),
            Exercise("Fire Hydrants", UnitType.REPS, 2)
        ]
