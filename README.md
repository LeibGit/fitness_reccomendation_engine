# WorkoutPlan Analyzer

A Python project to track, analyze, and provide recommendations for individual workout plans. It uses user workout logs to calculate statistics, predict future progress, and evaluate the effectiveness of exercise programs.

---

## Features

- **Track Workout Logs**: Steps, calories burned, and weights recorded for each workout.
- **Predict Future Steps**: Uses linear regression to forecast step counts for upcoming days.
- **Workout Effectiveness Analysis**: Performs paired t-tests on weight data to determine statistical significance of progress.
- **Calories Analysis**: Uses ANOVA to check differences in calories burned between workout types.
- **All-Time Stats**: Summarizes total workouts, calories burned, and steps taken.
- **Workout Recommendations**: Suggests the next workout type, duration, and estimated steps.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/workoutplan-analyzer.git
cd workoutplan-analyzer
