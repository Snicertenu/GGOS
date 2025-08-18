# 🚀 GGOS Quick Start Guide

Get GGOS running in 3 simple steps!

## Step 1: Install Dependencies

**Option A: Automatic Installation (Recommended)**
```bash
python install.py
```

**Option B: Manual Installation**
```bash
pip install customtkinter==5.2.0 pillow
```

## Step 2: Run the Application

```bash
python main.py
```

## Step 3: Start Using GGOS!

1. **Setup Tab**: 
   - Browse and select from 20+ pre-generated exercises by category
   - Set quantities for each exercise you want to add
   - Create custom exercises if needed
   - Or load all defaults at once
2. **Workout Tab**: Enter your death count and generate workouts
3. **History Tab**: Track your progress over time
4. **Settings Tab**: Customize the app appearance

## 🎯 What's Included

**20+ Equipment-Free Exercises:**
- **Core**: Squats, Push-ups, Sit-ups, Plank
- **Cardio**: Jumping Jacks, Burpees, Mountain Climbers, High Knees
- **Legs**: Lunges, Calf Raises, Wall Sit
- **Arms**: Tricep Dips, Arm Circles
- **Core Variations**: Bicycle Crunches, Russian Twists, Superman Hold
- **Full Body**: Bear Crawls, Spider-Man Push-ups, Donkey Kicks, Fire Hydrants

## 🛠️ Troubleshooting

**If you get import errors:**
```bash
pip install --upgrade customtkinter pillow
```

**If the app doesn't start:**
```bash
python test_app.py
```

**For Windows users:**
- Make sure you have Python 3.8+ installed
- Run PowerShell as Administrator if you get permission errors

## 🎮 Example Workout

1. Enter "10" deaths
2. Click "Generate Workout"
3. Get something like:
   ```
   🎯 Workout for 10 deaths:
   
   💪 Reps:
     • 6 squats (3 deaths)
     • 4 sit-ups (2 deaths)
     • 15 jumping jacks (3 deaths)
   
   ⏱️ Time:
     • 10 seconds planking (2 deaths)
   
   📊 Summary: 25 reps + 10 seconds
   ```

## 🏗️ Build Executable (Optional)

Want a standalone .exe file?
```bash
python build.py
```

The executable will be in the `dist/` folder.

---

**Ready to turn your gaming deaths into fitness gains! 💪**
