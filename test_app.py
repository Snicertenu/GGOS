#!/usr/bin/env python3
"""
Simple test script for GGOS
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from src.models.exercise import Exercise, UnitType
        from src.models.workout import WorkoutGenerator, Workout
        from src.services.storage import StorageService
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_exercise_creation():
    """Test exercise creation and methods"""
    print("\nTesting exercise creation...")
    
    try:
        from src.models.exercise import Exercise, UnitType
        
        # Create exercises
        squats = Exercise("Squats", UnitType.REPS, 2)
        plank = Exercise("Plank", UnitType.SECONDS, 5)
        
        # Test methods
        assert squats.name == "Squats"
        assert squats.unit_type == UnitType.REPS
        assert squats.amount_per_death == 2
        assert squats.calculate_total(5) == 10
        assert squats.get_unit_display() == "reps"
        
        assert plank.name == "Plank"
        assert plank.unit_type == UnitType.SECONDS
        assert plank.amount_per_death == 5
        assert plank.calculate_total(3) == 15
        assert plank.get_unit_display() == "seconds"
        
        print("✅ Exercise creation and methods work correctly")
        return True
    except Exception as e:
        print(f"❌ Exercise test failed: {e}")
        return False

def test_workout_generation():
    """Test workout generation"""
    print("\nTesting workout generation...")
    
    try:
        from src.models.exercise import Exercise, UnitType
        from src.models.workout import WorkoutGenerator
        
        # Create test exercises
        exercises = [
            Exercise("Squats", UnitType.REPS, 2),
            Exercise("Sit-ups", UnitType.REPS, 2),
            Exercise("Plank", UnitType.SECONDS, 5)
        ]
        
        # Generate workout
        workout = WorkoutGenerator.generate_workout(exercises, 10)
        
        # Basic validation
        assert workout is not None
        assert hasattr(workout, 'exercises')
        assert hasattr(workout, 'total_deaths')
        assert workout.total_deaths <= 10
        
        print(f"✅ Workout generated successfully")
        print(f"   Total deaths accounted: {workout.total_deaths}")
        print(f"   Exercises in workout: {len(workout.exercises)}")
        
        return True
    except Exception as e:
        print(f"❌ Workout generation test failed: {e}")
        return False

def test_storage():
    """Test storage functionality"""
    print("\nTesting storage...")
    
    try:
        from src.services.storage import StorageService
        from src.models.exercise import Exercise, UnitType
        
        # Create temporary storage
        import tempfile
        temp_dir = tempfile.mkdtemp()
        storage = StorageService(temp_dir)
        
        # Test default exercises
        default_exercises = storage.get_default_exercises()
        assert len(default_exercises) > 0
        assert all(isinstance(ex, Exercise) for ex in default_exercises)
        
        # Test save/load
        test_exercises = [Exercise("Test", UnitType.REPS, 1)]
        storage.save_exercises(test_exercises)
        loaded_exercises = storage.load_exercises()
        
        assert len(loaded_exercises) == 1
        assert loaded_exercises[0].name == "Test"
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
        
        print("✅ Storage functionality works correctly")
        return True
    except Exception as e:
        print(f"❌ Storage test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running GGOS Tests")
    print("=" * 30)
    
    tests = [
        test_imports,
        test_exercise_creation,
        test_workout_generation,
        test_storage
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application should work correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
