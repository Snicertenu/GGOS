# GGOS - Gaming Death Workout System

Turn your gaming deaths into fitness motivation! 🎮💪

GGOS is a desktop application that generates randomized workouts based on the number of deaths you experience in your gaming sessions. Instead of getting frustrated by deaths, use them as motivation to stay fit!

## 🎯 Features

### MVP Features (Current)
- **Exercise Setup**: Select from 20+ pre-generated exercises or create custom ones
- **Categorized Exercises**: Browse exercises by category (Core, Cardio, Legs, Arms, etc.)
- **Death Input**: Enter the number of deaths from your gaming session
- **Randomized Workouts**: Generate varied workouts with random death distribution
- **Workout History**: Track and view your workout progress over time
- **Modern GUI**: Clean, intuitive interface with scrollbars built with CustomTkinter

### Future Enhancements (Planned)
- **Auto-Input**: Automatic death detection from popular games (League of Legends, Valorant, CS:GO, Overwatch)
- **Fitness Tracker Integration**: Sync with Apple Health, Fitbit, Garmin, Strava
- **Workout Presets**: Save and load different exercise configurations
- **Sound Alerts**: Audio cues and countdown timers for timed exercises
- **Intensity Multipliers**: Adjust workout difficulty based on skill level

## 🚀 Quick Start

### Option 1: Run from Source
1. **Clone or download** this repository
2. **Install Python 3.8+** if not already installed
3. **Run the installation script**:
   ```bash
   python install.py
   ```
4. **Or install dependencies manually**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the application**:
   ```bash
   python main.py
   ```

### Option 2: Build Executable
1. **Run the build script**:
   ```bash
   python build.py
   ```
2. **Find the executable** in the `dist/` folder
3. **Double-click** `GGOS.exe` to run

## 📖 How to Use

### 1. Setup Phase
1. Open the **Setup** tab
2. **Select from pre-generated exercises**:
   - Browse through categorized exercises (Core, Cardio, Legs, Arms, etc.)
   - Check the exercises you want to add
   - Set quantity for each exercise
   - Click "Add Selected" to add them to your workout
3. **Add custom exercises**:
   - Exercise name (e.g., "Custom Exercise")
   - Unit type (Reps or Seconds)
   - Amount per death (e.g., 2 reps, 5 seconds)
4. **Load all defaults** for quick start with all pre-configured exercises

### 2. Game Phase
1. After your gaming session, count your deaths
2. Go to the **Workout** tab
3. Enter the number of deaths
4. Click **Generate Workout**

### 3. Workout Output
The system will generate a randomized workout like:
```
🎯 Workout for 10 deaths:

💪 Reps:
  • 6 squats (3 deaths)
  • 4 sit-ups (2 deaths)
  • 15 jumping jacks (3 deaths)

⏱️ Time:
  • 10 seconds planking (2 deaths)

📊 Summary: 25 reps + 10 seconds
✅ Total deaths accounted for: 10/10
```

### 4. Track Progress
- View your **History** to see past workouts
- Check **Statistics** for total workouts, deaths, and reps
- **Filter** workouts by different criteria

## 🛠️ Technical Details

### Architecture
- **Frontend**: CustomTkinter (modern Tkinter-based GUI)
- **Backend**: Pure Python with object-oriented design
- **Data Storage**: JSON files in user's home directory
- **Build System**: PyInstaller for executable creation

### Project Structure
```
GGOS/
├── main.py                 # Application entry point
├── build.py               # Build script for executable
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── src/                  # Source code
│   ├── models/          # Data models
│   │   ├── exercise.py  # Exercise class
│   │   └── workout.py   # Workout generation logic
│   ├── services/        # Business logic
│   │   └── storage.py   # Data persistence
│   └── gui/             # User interface
│       ├── app.py       # Main application
│       └── frames/      # GUI components
│           ├── workout_frame.py
│           ├── setup_frame.py
│           ├── history_frame.py
│           └── settings_frame.py
└── assets/              # Icons and resources
```

### Data Storage
- **Location**: `~/.ggos/` (user's home directory)
- **Files**:
  - `exercises.json`: Exercise configurations
  - `settings.json`: Application settings
  - `workout_history.json`: Workout records

## 🎮 Example Use Case

### Setup:
| Exercise | Unit | Per Death |
|----------|------|-----------|
| Squats | Reps | 2 |
| Sit-ups | Reps | 2 |
| Jumping Jacks | Reps | 5 |
| Plank | Seconds | 5 |

### Game Session:
- **Deaths**: 10

### Generated Workout:
- 6 squats (3 deaths)
- 4 sit-ups (2 deaths)  
- 15 jumping jacks (3 deaths)
- 10 seconds planking (2 deaths)

**Total**: 25 reps + 10 seconds

## 🔧 Configuration

### Settings
- **Theme**: Dark/Light/System
- **Window Size**: Various preset sizes
- **Auto-Input**: Future feature for automatic death detection
- **Fitness Tracker**: Future feature for health app integration

### Default Exercises (Equipment-Free)
The app comes with 20+ pre-configured exercises that require no equipment:

**Core Exercises:**
- Squats (2 reps per death)
- Push-ups (1 rep per death)
- Sit-ups (2 reps per death)
- Plank (5 seconds per death)

**Cardio Exercises:**
- Jumping Jacks (5 reps per death)
- Burpees (1 rep per death)
- Mountain Climbers (3 reps per death)
- High Knees (4 reps per death)

**Leg Exercises:**
- Lunges (2 reps per death)
- Calf Raises (3 reps per death)
- Wall Sit (3 seconds per death)

**Arm Exercises:**
- Tricep Dips (2 reps per death)
- Arm Circles (4 reps per death)

**Core Variations:**
- Bicycle Crunches (2 reps per death)
- Russian Twists (3 reps per death)
- Superman Hold (4 seconds per death)

**Full Body:**
- Bear Crawls (1 rep per death)
- Spider-Man Push-ups (1 rep per death)
- Donkey Kicks (2 reps per death)
- Fire Hydrants (2 reps per death)

## 🚀 Future Roadmap

### Phase 1: Auto-Input Integration
- **Game APIs**: Integrate with game APIs for automatic death detection
- **Process Monitoring**: Monitor game processes for death events
- **Configurable Games**: Support for multiple game types

### Phase 2: Fitness Tracker Integration
- **Health APIs**: Connect to Apple Health, Google Fit, Fitbit
- **Data Sync**: Automatically log workouts to health apps
- **Progress Tracking**: Long-term fitness progress analysis

### Phase 3: Advanced Features
- **Workout Presets**: Save different exercise configurations
- **Difficulty Levels**: Adjust workout intensity
- **Audio Integration**: Sound alerts and timers
- **Social Features**: Share workouts and achievements

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Submit** a pull request

### Development Setup
```bash
# Clone repository
git clone <your-fork-url>
cd GGOS

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python main.py

# Run tests (when available)
python -m pytest
```

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **CustomTkinter**: For the beautiful modern GUI
- **PyInstaller**: For making standalone executables possible
- **Gaming Community**: For the inspiration to turn frustration into motivation

---

**Made with ❤️ for gamers who want to stay fit!**

*Remember: Every death is just another opportunity to get stronger! 💪*
