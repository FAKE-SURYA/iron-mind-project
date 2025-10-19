import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate 30 days of realistic sample data
np.random.seed(42)
dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30, 0, -1)]

data = {
    'date': dates,
    'weight_lifted_kg': np.random.randint(25, 35, 30),
    'workout_type': np.random.choice(['Push (Chest, Triceps)', 'Pull (Back, Biceps)', 'Legs', 'Rest Day'], 30),
    'protein_intake_g': np.random.randint(100, 140, 30),
    'rest_day': [1 if w == 'Rest Day' else 0 for w in np.random.choice(['Push (Chest, Triceps)', 'Pull (Back, Biceps)', 'Legs', 'Rest Day'], 30)],
    'leetcode_solved': np.random.randint(0, 5, 30),
    'coding_hours': np.random.uniform(2, 8, 30).round(1),
    'github_commits': np.random.randint(0, 8, 30),
    'focus_score': np.random.randint(4, 10, 30),
    'brain_fog_level': np.random.randint(2, 8, 30)
}

df = pd.DataFrame(data)
df.to_csv('data/daily_logs.csv', index=False)
print("✅ Sample data generated! You can now test the app.")
