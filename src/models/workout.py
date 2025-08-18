"""
Workout model for GGOS
"""

from dataclasses import dataclass
from typing import List, Dict
import random
from src.models.exercise import Exercise


@dataclass
class WorkoutExercise:
    """Represents an exercise in a workout with allocated amount"""
    exercise: Exercise
    allocated_amount: int
    deaths_allocated: int
    
    def get_display_text(self) -> str:
        """Get display text for the workout exercise"""
        return f"{self.allocated_amount} {self.exercise.name} ({self.deaths_allocated} deaths)"


@dataclass
class Workout:
    """Represents a complete workout session"""
    exercises: List[WorkoutExercise]
    total_deaths: int
    
    def get_summary(self) -> str:
        """Get summary of the workout"""
        reps_total = 0
        seconds_total = 0
        
        for workout_exercise in self.exercises:
            if workout_exercise.exercise.unit_type.value == "reps":
                reps_total += workout_exercise.allocated_amount
            else:  # seconds
                seconds_total += workout_exercise.allocated_amount
        
        summary_parts = []
        if reps_total > 0:
            summary_parts.append(f"{reps_total} reps")
        if seconds_total > 0:
            summary_parts.append(f"{seconds_total} seconds")
        
        return " + ".join(summary_parts) if summary_parts else "No exercises"
    
    def get_exercises_by_unit_type(self) -> Dict[str, List[WorkoutExercise]]:
        """Group exercises by unit type"""
        grouped = {"reps": [], "seconds": []}
        for workout_exercise in self.exercises:
            unit_type = workout_exercise.exercise.unit_type.value
            grouped[unit_type].append(workout_exercise)
        return grouped


class WorkoutGenerator:
    """Generates randomized workouts based on exercises and deaths"""
    
    @staticmethod
    def generate_workout(exercises: List[Exercise], deaths: int) -> Workout:
        """Generate a randomized workout"""
        if not exercises or deaths <= 0:
            return Workout(exercises=[], total_deaths=deaths)
        
        # Calculate total amount for each exercise
        exercise_totals = {}
        for exercise in exercises:
            exercise_totals[exercise.id] = exercise.calculate_total(deaths)
        
        # Randomly distribute deaths among exercises
        workout_exercises = []
        remaining_deaths = deaths
        available_exercises = exercises.copy()
        
        while remaining_deaths > 0 and available_exercises:
            # Randomly select an exercise
            exercise = random.choice(available_exercises)
            
            # Randomly allocate 1-3 deaths to this exercise (or remaining deaths if less)
            max_allocation = min(3, remaining_deaths)
            allocation = random.randint(1, max_allocation)
            
            # Calculate allocated amount
            allocated_amount = exercise.amount_per_death * allocation
            
            # Create workout exercise
            workout_exercise = WorkoutExercise(
                exercise=exercise,
                allocated_amount=allocated_amount,
                deaths_allocated=allocation
            )
            workout_exercises.append(workout_exercise)
            
            # Update remaining deaths
            remaining_deaths -= allocation
            
            # Remove exercise if all its potential deaths are used
            if allocation >= exercise.amount_per_death * 3:  # Max allocation reached
                available_exercises.remove(exercise)
        
        return Workout(
            exercises=workout_exercises,
            total_deaths=deaths - remaining_deaths
        )
