import os
import json
import pandas as pd
import numpy as np 
import scipy
from random import choice, randint 
from collections import defaultdict

with open("users.json", 'r') as file:
    data = json.load(file)

class WorkoutPlan():
    def __init__(self, name, age, goal, daily_logs):
        self.name = name
        self.age = age
        self.goal = goal
        self.daily_logs = daily_logs

    def get_dates(self):
        """Getting the most recent date the user worked out"""
        dates = []
        for log in self.daily_logs:
            dates.append(log['date'])
        cleaned_dates = []
        for d in dates:
            cleaned_dates.append(pd.to_datetime(d))
        latest_date = np.max(cleaned_dates)
        return latest_date

    def get_steps(self):
        """Getting average steps of the user"""
        total_steps = 0
        workout_type = []
        for log in self.daily_logs:
            total_steps += log['steps']
        avg_steps = total_steps / len(self.daily_logs)
        return (avg_steps * 0.05) + (avg_steps)

    def get_workouts(self):
        """Getting workouts and providing the next one"""
        cadio_workouts = ['run', 'swim', 'boxing', 'HIIT', 'karate', 'hiking']
        strength_workouts = ['powerlifting', 'calisthetics', 'pushups', 'squats', 'deadlift']
        flexibility_workouts = ['yoga', 'stretch', 'swim']
        all_workouts = cadio_workouts + strength_workouts + flexibility_workouts
        workouts = []
        for workout in self.daily_logs:
            workouts.append(workout)
        if self.goal == "cardio" or self.goal == "flexibility":
            rand_choice_cardio = choice(cadio_workouts)
            return rand_choice_cardio
        elif self.goal == "strength" or self.goal == "muscle_gain": 
            rand_choice_strength = choice(strength_workouts)
            return rand_choice_strength
        elif self.goal == "flexibility":
            rand_choice_flex = choice(flexibility_workouts)
            return rand_choice_flex
        else:
            rand_choice_all = choice(all_workouts)
            return rand_choice_all          
        
    def get_cals_burned(self):
        """Analyzing statisticall distance between calories burned between workouts"""
        groups = defaultdict(list)

        for log in self.daily_logs:
            workout_type = log['workout']
            calories = log['calories']
            groups[workout_type].append(calories)

        group_lists = list(groups.values())

        if len(group_lists) < 2:
            raise ValueError("Need at least 2 workout types for analysis.")
        f_stat, p_value = scipy.stats.f_oneway(*group_lists)
        return f"F_stat: {f_stat}. p_value: {p_value}"
    
    def get_future_steps(self, days_into_future=7):
        """using linear regression to predict future progress"""
        # convert dates to numeric time index
        logs = sorted(self.daily_logs, key=lambda x: x['date'])
        x = list(range(len(logs)))
        y = [entry['steps'] for entry in logs]

        slope, intercept, r, p, stderr = scipy.stats.linregress(x, y)

        future_day = len(x) + days_into_future
        predicted_steps = slope * future_day + intercept 

        if abs(r) > 0.9:
            corr_strength = "very strong"
        elif abs(r) > 0.7:
            corr_strength = "strong"
        elif abs(r) > 0.5:
            corr_strength = "moderate"
        elif abs(r) > 0.3:
            corr_strength = "weak"
        else:
            corr_strength = "negligible"
        direction = "increasing" if r > 0 else "decreasing"
        return f"Predicted steps: {predicted_steps:.0f}. Correlation: {r:.3f} → {corr_strength} {direction} trend"
    
    def check_effectiveness(self):
        "using hypothesis testing to check effectivenes of workouts on weightloss"
        logs = self.daily_logs

        if len(logs) < 2:
            return "Not enough data for t-test."

        before_weights = [logs[i]['weight'] for i in range(len(logs)-1)]
        after_weights  = [logs[i+1]['weight'] for i in range(len(logs)-1)]

        t_stat, p_val = scipy.stats.ttest_rel(before_weights, after_weights)

        if p_val < 0.01:
            significance = "very significant"
        elif p_val < 0.05:
            significance = "significant"
        elif p_val < 0.10:
            significance = "marginally significant"
        else:
            significance = "not significant"

        return f"t_stat: {t_stat:.3f}. p_val: {p_val:.3f} → {significance}"

    def all_time_stats(self):
        """Get all time calories burned"""
        calorie_count = 0
        steps = 0
        for log in self.daily_logs:
            calorie_count += log['calories']
            steps += log['steps']

        return f"Total calories burned: {calorie_count}. Total steps: {steps} Total workouts completed: {len(self.daily_logs)}"
        
    def reccomendations(self):
        """Generating workout recommendation"""
        min_minutes = 15
        max_minutes = 60
        workout_time = randint(min_minutes, max_minutes)
        
        next_workout_date = self.get_dates() + pd.Timedelta(days=1)
        avg_steps = self.get_steps()
        todays_workout = self.get_workouts()
        future_steps = self.get_future_steps()
        effectiveness = self.check_effectiveness()
        total_stats = self.all_time_stats()
        
        rec = (
            f"{self.name} | Next workout: {next_workout_date.date()} + Snapshot\n"
            "---------------------------\n"
            f"1. Walk {avg_steps:.0f} steps\n"
            f"2. Today's workout: {todays_workout}\n"
            f"3. Duration: {workout_time} minutes\n"
            f"4. Next week step prediction: {future_steps}\n"
            f"5. Program effectiveness prediction: {effectiveness}\n"
            f"6. Stats: {total_stats}\n"
        )
        return rec    

if __name__ == "__main__":
    plans = []
    for user in data:
        plans.append(WorkoutPlan(
            name=user["name"], 
            age=user["age"], 
            goal=user["goal"], 
            daily_logs=user["daily_logs"]
        ))
    for p in plans:
        print(p.reccomendations())