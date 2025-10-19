import pandas as pd
from datetime import datetime
import os

class GymCodingLogger:
    def __init__(self, filepath='data/daily_logs.csv'):
        self.filepath = filepath
        self.columns = [
            'date', 'weight_lifted_kg', 'workout_type', 'protein_intake_g',
            'rest_day', 'leetcode_solved', 'coding_hours', 'github_commits',
            'focus_score', 'brain_fog_level'
        ]
        self._initialize_csv()
    
    def _initialize_csv(self):
        """Create CSV if it doesn't exist"""
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            df = pd.DataFrame(columns=self.columns)
            df.to_csv(self.filepath, index=False)
    
    def add_entry(self, gym_data, productivity_data):
        """
        Add daily entry
        gym_data: dict with keys: weight_lifted_kg, workout_type, protein_intake_g, rest_day
        productivity_data: dict with keys: leetcode_solved, coding_hours, github_commits, 
                          focus_score, brain_fog_level
        """
        entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            **gym_data,
            **productivity_data
        }
        
        df = pd.read_csv(self.filepath)
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
        df.to_csv(self.filepath, index=False)
        print(f"✅ Entry logged for {entry['date']}")
        
    def view_logs(self, last_n=10):
        """View last n entries"""
        df = pd.read_csv(self.filepath)
        return df.tail(last_n)
