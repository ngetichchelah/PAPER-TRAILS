#!/usr/bin/env python3
"""
KCSE Examination Participation Analysis
Research Question: How do KCSE examination participation rates vary by gender, age group, and county in Kenya, and what trends emerge over time?
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class KCSEAnalyzer:
    def __init__(self):
        self.data = {}
        self.cleaned_data = {}
        
    def load_data(self):
        """Load and initially examine all Excel files"""
        files = {
            'age_region': 'Age + Region.xlsx',
            'gender_region': 'Gender + Region.xlsx',
            'registered_vs_sat': 'Registered vs Sat.xlsx'
        }
        
        print("Loading data files...")
        for key, filename in files.items():
            if Path(filename).exists():
                print(f"Loading {filename}...")
                # Load all sheets for multi-sheet files
                if key == 'gender_region':
                    xl = pd.ExcelFile(filename)
                    self.data[key] = {}
                    for sheet in xl.sheet_names:
                        self.data[key][sheet] = pd.read_excel(filename, sheet_name=sheet)
                        print(f"  - Sheet '{sheet}': {self.data[key][sheet].shape}")
                else:
                    self.data[key] = pd.read_excel(filename)
                    print(f"  - Shape: {self.data[key].shape}")
            else:
                print(f"Warning: {filename} not found")
    
    def clean_registered_vs_sat_data(self):
        """Clean the time series data showing registered vs sat trends"""
        print("\nCleaning Registered vs Sat data...")
        df = self.data['registered_vs_sat'].copy()
        
        # Print original structure to understand layout
        print("Original structure:")
        print(df.head(10))
        
        # The data appears to start from row 1, with headers in row 0
        # Clean column names and extract meaningful data
        df_clean = df.iloc[1:].copy()  # Skip the header row
        df_clean.columns = ['Year', 'Total_Registered', 'Female_Registered', 'Male_Registered', 
                           'Females', 'Female_Sat', 'Female_Percentage', 'Males', 'Male_Sat', 'Male_Percentage']
        
        # Convert numeric columns
        numeric_cols = ['Year', 'Total_Registered', 'Female_Registered', 'Male_Registered', 
                       'Female_Sat', 'Male_Sat']
        for col in numeric_cols:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
        # Remove rows with missing years
        df_clean = df_clean.dropna(subset=['Year'])
        
        self.cleaned_data['time_trends'] = df_clean
        print(f"Cleaned time trends data: {df_clean.shape}")
        print("\nCleaned data preview:")
        print(df_clean.head())
        
    def clean_gender_region_data(self):
        """Clean the gender and region distribution data"""
        print("\nCleaning Gender + Region data...")
        
        # Check all sheets in gender_region file
        for sheet_name, df in self.data['gender_region'].items():
            print(f"\nProcessing sheet: {sheet_name}")
            print(f"Original shape: {df.shape}")
            print("First few rows:")
            print(df.head())
            
            # Skip if sheet is too small or empty
            if df.shape[0] < 3:
                continue
                
            # Try to identify data starting point
            # Look for rows that contain county codes or names
            df_clean = df.copy()
            
            # Find the row where actual data starts (usually after headers)
            data_start_idx = 0
            for i in range(min(5, len(df))):
                if pd.notna(df.iloc[i, 0]) and str(df.iloc[i, 0]).isdigit():
                    data_start_idx = i
                    break
            
            if data_start_idx > 0:
                df_clean = df.iloc[data_start_idx:].copy()
                print(f"Data starts at row {data_start_idx}")
            
            self.cleaned_data[f'gender_region_{sheet_name}'] = df_clean
            
    def clean_age_region_data(self):
        """Clean the age and region distribution data"""
        print("\nCleaning Age + Region data...")
        df = self.data['age_region'].copy()
        
        print("Original structure:")
        print(df.head(10))
        print(f"Columns: {df.columns.tolist()}")
        
        # Similar approach - find where actual data starts
        data_start_idx = 0
        for i in range(min(10, len(df))):
            if pd.notna(df.iloc[i, 0]) and str(df.iloc[i, 0]).strip().isdigit():
                data_start_idx = i
                break
        
        if data_start_idx > 0:
            df_clean = df.iloc[data_start_idx:].copy()
            print(f"Data starts at row {data_start_idx}")
        else:
            df_clean = df.copy()
            
        self.cleaned_data['age_region'] = df_clean
        print(f"Cleaned age region data: {df_clean.shape}")
        
    def analyze_time_trends(self):
        """Analyze trends over time (2020-2024)"""
        if 'time_trends' not in self.cleaned_data:
            print("No time trends data available")
            return
            
        df = self.cleaned_data['time_trends']
        
        print("\n" + "="*50)
        print("TIME TRENDS ANALYSIS (2020-2024)")
        print("="*50)
        
        # Calculate participation rates
        df['Total_Sat'] = df['Female_Sat'] + df['Male_Sat']
        df['Participation_Rate'] = (df['Total_Sat'] / df['Total_Registered']) * 100
        df['Female_Participation_Rate'] = (df['Female_Sat'] / df['Female_Registered']) * 100
        df['Male_Participation_Rate'] = (df['Male_Sat'] / df['Male_Registered']) * 100
        
        print(f"\nOverall Trends:")
        print(f"Years covered: {df['Year'].min():.0f} - {df['Year'].max():.0f}")
        print(f"Average participation rate: {df['Participation_Rate'].mean():.1f}%")
        print(f"Female participation rate: {df['Female_Participation_Rate'].mean():.1f}%")
        print(f"Male participation rate: {df['Male_Participation_Rate'].mean():.1f}%")
        
        # Gender gap analysis
        df['Gender_Gap'] = df['Female_Participation_Rate'] - df['Male_Participation_Rate']
        print(f"\nGender Gap Analysis:")
        print(f"Average gender gap (Female - Male): {df['Gender_Gap'].mean():.2f} percentage points")
        
        # Create visualizations
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('KCSE Participation Trends (2020-2024)', fontsize=16, fontweight='bold')
        
        # Plot 1: Overall participation rates
        axes[0,0].plot(df['Year'], df['Participation_Rate'], marker='o', linewidth=2, markersize=8)
        axes[0,0].set_title('Overall Participation Rate Over Time')
        axes[0,0].set_xlabel('Year')
        axes[0,0].set_ylabel('Participation Rate (%)')
        axes[0,0].grid(True, alpha=0.3)
        
        # Plot 2: Gender comparison
        axes[0,1].plot(df['Year'], df['Female_Participation_Rate'], marker='o', label='Female', linewidth=2)
        axes[0,1].plot(df['Year'], df['Male_Participation_Rate'], marker='s', label='Male', linewidth=2)
        axes[0,1].set_title('Participation Rate by Gender')
        axes[0,1].set_xlabel('Year')
        axes[0,1].set_ylabel('Participation Rate (%)')
        axes[0,1].legend()
        axes[0,1].grid(True, alpha=0.3)
        
        # Plot 3: Total candidates
        axes[1,0].bar(df['Year'], df['Total_Sat'], alpha=0.7, color='skyblue')
        axes[1,0].set_title('Total KCSE Candidates')
        axes[1,0].set_xlabel('Year')
        axes[1,0].set_ylabel('Number of Candidates')
        axes[1,0].grid(True, alpha=0.3)
        
        # Plot 4: Gender gap
        colors = ['red' if x > 0 else 'blue' for x in df['Gender_Gap']]
        axes[1,1].bar(df['Year'], df['Gender_Gap'], color=colors, alpha=0.7)
        axes[1,1].axhline(y=0, color='black', linestyle='-', alpha=0.5)
        axes[1,1].set_title('Gender Gap in Participation\n(Positive = Female advantage)')
        axes[1,1].set_xlabel('Year')
        axes[1,1].set_ylabel('Gender Gap (percentage points)')
        axes[1,1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('kcse_time_trends.png', dpi=300, bbox_inches='tight')
        print(f"\nVisualization saved as 'kcse_time_trends.png'")
        plt.show()
        
    def analyze_regional_patterns(self):
        """Analyze regional and county-level patterns"""
        print("\n" + "="*50)
        print("REGIONAL PATTERNS ANALYSIS")
        print("="*50)
        
        # This would require properly parsing the county-level data
        # For now, let's work with what we can extract
        
        available_datasets = [key for key in self.cleaned_data.keys() if 'region' in key]
        print(f"Available regional datasets: {available_datasets}")
        
        for dataset_name in available_datasets:
            df = self.cleaned_data[dataset_name]
            print(f"\n--- {dataset_name} ---")
            print(f"Shape: {df.shape}")
            print("Sample data:")
            print(df.head())
    
    def generate_insights_report(self):
        """Generate key insights and recommendations"""
        print("\n" + "="*60)
        print("KEY INSIGHTS AND RECOMMENDATIONS")
        print("="*60)
        
        insights = []
        
        if 'time_trends' in self.cleaned_data:
            df = self.cleaned_data['time_trends']
            
            # Participation rate trends
            if len(df) > 1:
                rate_change = df['Participation_Rate'].iloc[-1] - df['Participation_Rate'].iloc[0]
                if rate_change > 0:
                    insights.append(f"✓ Participation rates have improved by {rate_change:.1f} percentage points over the study period")
                else:
                    insights.append(f"⚠ Participation rates have declined by {abs(rate_change):.1f} percentage points over the study period")
            
            # Gender equity
            avg_gap = df['Gender_Gap'].mean()
            if avg_gap > 2:
                insights.append(f"⚠ Significant gender gap: Females participate {avg_gap:.1f} percentage points higher than males")
            elif avg_gap < -2:
                insights.append(f"⚠ Significant gender gap: Males participate {abs(avg_gap):.1f} percentage points higher than females")
            else:
                insights.append(f"✓ Relatively balanced gender participation (gap: {avg_gap:.1f} percentage points)")
            
            # Growth trends
            total_growth = ((df['Total_Sat'].iloc[-1] / df['Total_Sat'].iloc[0]) - 1) * 100
            insights.append(f"📈 Total candidate numbers have {'increased' if total_growth > 0 else 'decreased'} by {abs(total_growth):.1f}% over the period")
        
        print("\n🔍 KEY FINDINGS:")
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight}")
        
        print("\n📋 POLICY RECOMMENDATIONS:")
        recommendations = [
            "Focus on improving participation rates in underperforming counties",
            "Address gender disparities through targeted interventions",
            "Investigate age-related barriers to KCSE participation",
            "Develop region-specific strategies based on local challenges",
            "Monitor trends annually to track progress"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
            
    def run_full_analysis(self):
        """Run the complete analysis pipeline"""
        print("Starting KCSE Examination Participation Analysis")
        print("="*60)
        
        # Load data
        self.load_data()
        
        # Clean data
        self.clean_registered_vs_sat_data()
        self.clean_gender_region_data()
        self.clean_age_region_data()
        
        # Perform analyses
        self.analyze_time_trends()
        self.analyze_regional_patterns()
        
        # Generate report
        self.generate_insights_report()
        
        print(f"\n✅ Analysis complete! Check the generated visualizations and insights above.")

if __name__ == "__main__":
    analyzer = KCSEAnalyzer()
    analyzer.run_full_analysis()