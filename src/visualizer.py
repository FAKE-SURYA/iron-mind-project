import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class PerformanceVisualizer:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.df = analyzer.df
        sns.set_style("darkgrid")
        plt.rcParams['figure.figsize'] = (12, 8)
    
    def correlation_heatmap(self, save_path=None):
        """Create correlation heatmap between all metrics"""
        corr_matrix = self.analyzer.correlation_matrix()
        
        plt.figure(figsize=(14, 10))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                   center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
        plt.title('Iron Mind: Gym Performance vs Coding Productivity', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return plt
    
    def time_series_trends(self):
        """Show trends over time for all key metrics"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Plot 1: Coding Hours over time
        axes[0, 0].plot(self.df['date'], self.df['coding_hours'], 
                       marker='o', color='#2ecc71', linewidth=2, markersize=6)
        axes[0, 0].set_title('Coding Hours Trend', fontweight='bold', fontsize=12)
        axes[0, 0].set_ylabel('Hours', fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Plot 2: Weight Lifted over time
        axes[0, 1].plot(self.df['date'], self.df['weight_lifted_kg'], 
                       marker='s', color='#e74c3c', linewidth=2, markersize=6)
        axes[0, 1].set_title('Weight Lifted Trend', fontweight='bold', fontsize=12)
        axes[0, 1].set_ylabel('Kg', fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Plot 3: Focus Score vs Brain Fog
        axes[1, 0].plot(self.df['date'], self.df['focus_score'], 
                       marker='o', label='Focus Score', color='#3498db', linewidth=2, markersize=6)
        axes[1, 0].plot(self.df['date'], self.df['brain_fog_level'], 
                       marker='x', label='Brain Fog', color='#e67e22', linewidth=2, markersize=6)
        axes[1, 0].set_title('Mental Clarity Metrics', fontweight='bold', fontsize=12)
        axes[1, 0].set_ylabel('Score (1-10)', fontweight='bold')
        axes[1, 0].legend(loc='best')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Plot 4: LeetCode Progress
        axes[1, 1].bar(self.df['date'], self.df['leetcode_solved'], 
                      color='#9b59b6', alpha=0.7, edgecolor='black')
        axes[1, 1].set_title('LeetCode Problems Solved', fontweight='bold', fontsize=12)
        axes[1, 1].set_ylabel('Problems', fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        return fig
    
    def workout_comparison(self):
        """Compare productivity across different workout types"""
        workout_productivity = self.df.groupby('workout_type').agg({
            'coding_hours': 'mean',
            'leetcode_solved': 'mean',
            'focus_score': 'mean',
            'brain_fog_level': 'mean'
        }).round(2)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        workout_productivity.plot(kind='bar', ax=ax, width=0.8)
        plt.title('Average Productivity by Workout Type', fontsize=14, fontweight='bold', pad=20)
        plt.xlabel('Workout Type', fontweight='bold', fontsize=11)
        plt.ylabel('Average Score', fontweight='bold', fontsize=11)
        plt.xticks(rotation=45, ha='right')
        plt.legend(title='Metrics', loc='best')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        return fig
    
    def productivity_score_distribution(self):
        """Show distribution of total productivity scores"""
        if 'total_productivity' not in self.df.columns:
            self.df['total_productivity'] = (
                self.df['leetcode_solved'] * 3 +
                self.df['coding_hours'] * 2 +
                self.df['github_commits'] * 1.5 +
                self.df['focus_score'] * 2 -
                self.df['brain_fog_level'] * 1.5
            )
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(self.df['total_productivity'], bins=15, color='#3498db', 
                edgecolor='black', alpha=0.7)
        ax.axvline(self.df['total_productivity'].mean(), color='red', 
                   linestyle='--', linewidth=2, label=f"Mean: {self.df['total_productivity'].mean():.1f}")
        ax.set_title('Distribution of Total Productivity Scores', fontweight='bold', fontsize=14)
        ax.set_xlabel('Productivity Score', fontweight='bold')
        ax.set_ylabel('Frequency', fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        return fig
    
    def weekly_summary(self):
        """Create weekly performance summary"""
        self.df['week'] = pd.to_datetime(self.df['date']).dt.isocalendar().week
        
        weekly_data = self.df.groupby('week').agg({
            'coding_hours': 'sum',
            'leetcode_solved': 'sum',
            'github_commits': 'sum',
            'focus_score': 'mean'
        }).round(2)
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        weekly_data['coding_hours'].plot(kind='bar', ax=axes[0, 0], color='#2ecc71')
        axes[0, 0].set_title('Weekly Coding Hours', fontweight='bold')
        axes[0, 0].set_ylabel('Hours')
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        
        weekly_data['leetcode_solved'].plot(kind='bar', ax=axes[0, 1], color='#9b59b6')
        axes[0, 1].set_title('Weekly LeetCode Problems', fontweight='bold')
        axes[0, 1].set_ylabel('Problems')
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        weekly_data['github_commits'].plot(kind='bar', ax=axes[1, 0], color='#e74c3c')
        axes[1, 0].set_title('Weekly GitHub Commits', fontweight='bold')
        axes[1, 0].set_ylabel('Commits')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        weekly_data['focus_score'].plot(kind='line', ax=axes[1, 1], color='#3498db', 
                                        marker='o', linewidth=2, markersize=8)
        axes[1, 1].set_title('Weekly Average Focus Score', fontweight='bold')
        axes[1, 1].set_ylabel('Focus Score')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
