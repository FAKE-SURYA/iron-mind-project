import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class PerformanceAnalyzer:
    def __init__(self, filepath='data/daily_logs.csv'):
        self.df = pd.read_csv(filepath)
        self.df['date'] = pd.to_datetime(self.df['date'])
        self._preprocess()
    
    def _preprocess(self):
        """Clean and prepare data"""
        # Convert workout type to numeric (encode)
        self.df['workout_numeric'] = pd.Categorical(self.df['workout_type']).codes
        
        # Handle missing values
        self.df = self.df.fillna(self.df.median(numeric_only=True))
    
    def correlation_matrix(self):
        """Calculate correlation between all metrics"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        return self.df[numeric_cols].corr()
    
    def gym_productivity_correlation(self):
        """Specific correlations: gym metrics vs productivity"""
        gym_metrics = ['weight_lifted_kg', 'protein_intake_g', 'workout_numeric']
        productivity_metrics = ['leetcode_solved', 'coding_hours', 'github_commits', 
                               'focus_score', 'brain_fog_level']
        
        correlations = {}
        for gym in gym_metrics:
            for prod in productivity_metrics:
                corr = self.df[gym].corr(self.df[prod])
                correlations[f"{gym}_vs_{prod}"] = corr
        
        return pd.Series(correlations).sort_values(ascending=False)
    
    def predict_productivity(self, weight_lifted, protein_intake):
        """Predict focus score based on gym metrics"""
        X = self.df[['weight_lifted_kg', 'protein_intake_g']]
        y = self.df['focus_score']
        
        model = LinearRegression()
        model.fit(X, y)
        
        prediction = model.predict([[weight_lifted, protein_intake]])
        return round(prediction[0], 2)
    
    def best_performing_days(self, top_n=10):
        """Find days with highest combined productivity"""
        self.df['total_productivity'] = (
            self.df['leetcode_solved'] * 3 +
            self.df['coding_hours'] * 2 +
            self.df['github_commits'] * 1.5 +
            self.df['focus_score'] * 2 -
            self.df['brain_fog_level'] * 1.5
        )
        return self.df.nlargest(top_n, 'total_productivity')[
            ['date', 'workout_type', 'weight_lifted_kg', 'total_productivity']
        ]
