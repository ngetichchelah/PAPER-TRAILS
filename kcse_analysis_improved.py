#!/usr/bin/env python3
"""
KCSE Examination Participation Analysis - Improved Version
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

class KCSEAnalyzerImproved:
    def __init__(self):
        self.data = {}
        self.cleaned_data = {}
        
    def load_and_clean_time_series_data(self):
        """Load and clean the time series data from both Excel files"""
        print("Loading and cleaning time series data...")
        
        # Load from Registered vs Sat.xlsx
        df_main = pd.read_excel('Registered vs Sat.xlsx')
        
        # Create proper column names based on the structure we observed
        df_clean = df_main.iloc[1:].copy()  # Skip header row
        df_clean.columns = [
            'Year', 'Total_Registered', 'Total_Sat', 'Total_Change',
            'Female_Registered', 'Female_Sat', 'Female_Change', 
            'Male_Registered', 'Male_Sat', 'Male_Change'
        ]
        
        # Convert to numeric
        numeric_cols = ['Year', 'Total_Registered', 'Total_Sat', 'Total_Change',
                       'Female_Registered', 'Female_Sat', 'Female_Change',
                       'Male_Registered', 'Male_Sat', 'Male_Change']
        
        for col in numeric_cols:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
        # Remove any rows with missing years
        df_clean = df_clean.dropna(subset=['Year'])
        df_clean = df_clean.sort_values('Year')
        
        self.cleaned_data['time_series'] = df_clean
        print(f"Cleaned time series data: {df_clean.shape[0]} years of data")
        return df_clean
    
    def load_county_gender_data(self):
        """Load and clean county-level gender distribution data"""
        print("Loading county-level gender data...")
        
        # Load from Gender + Region sheet
        df = pd.read_excel('Gender + Region.xlsx', sheet_name='Gender + Region')
        
        # Find where the actual data starts (after headers)
        data_start = 2  # Based on our examination
        df_clean = df.iloc[data_start:].copy()
        
        # Set proper column names - need to examine the actual structure
        print("Sample of gender+region data:")
        print(df_clean.head())
        
        self.cleaned_data['county_gender'] = df_clean
        return df_clean
    
    def load_county_age_data(self):
        """Load and clean county-level age distribution data"""
        print("Loading county-level age data...")
        
        df = pd.read_excel('Age + Region.xlsx')
        
        # Find where actual data starts
        data_start = 3  # Based on our examination
        df_clean = df.iloc[data_start:].copy()
        
        print("Sample of age+region data:")
        print(df_clean.head())
        
        self.cleaned_data['county_age'] = df_clean
        return df_clean
    
    def analyze_participation_trends(self):
        """Analyze participation trends over time"""
        df = self.cleaned_data['time_series']
        
        print("\n" + "="*60)
        print("KCSE PARTICIPATION TRENDS ANALYSIS (2020-2024)")
        print("="*60)
        
        # Calculate participation rates
        df['Total_Participation_Rate'] = (df['Total_Sat'] / df['Total_Registered']) * 100
        df['Female_Participation_Rate'] = (df['Female_Sat'] / df['Female_Registered']) * 100
        df['Male_Participation_Rate'] = (df['Male_Sat'] / df['Male_Registered']) * 100
        df['Gender_Gap'] = df['Female_Participation_Rate'] - df['Male_Participation_Rate']
        
        # Print key statistics
        print(f"\n📊 OVERALL STATISTICS:")
        print(f"Years analyzed: {int(df['Year'].min())} - {int(df['Year'].max())}")
        print(f"Average total participation rate: {df['Total_Participation_Rate'].mean():.2f}%")
        print(f"Average female participation rate: {df['Female_Participation_Rate'].mean():.2f}%")
        print(f"Average male participation rate: {df['Male_Participation_Rate'].mean():.2f}%")
        
        # Trend analysis
        total_rate_change = df['Total_Participation_Rate'].iloc[-1] - df['Total_Participation_Rate'].iloc[0]
        female_rate_change = df['Female_Participation_Rate'].iloc[-1] - df['Female_Participation_Rate'].iloc[0]
        male_rate_change = df['Male_Participation_Rate'].iloc[-1] - df['Male_Participation_Rate'].iloc[0]
        
        print(f"\n📈 TREND ANALYSIS (2020 to 2024):")
        print(f"Total participation rate change: {total_rate_change:+.2f} percentage points")
        print(f"Female participation rate change: {female_rate_change:+.2f} percentage points")
        print(f"Male participation rate change: {male_rate_change:+.2f} percentage points")
        
        # Gender equity analysis
        avg_gender_gap = df['Gender_Gap'].mean()
        print(f"\n⚖️ GENDER EQUITY ANALYSIS:")
        print(f"Average gender gap (Female - Male): {avg_gender_gap:+.2f} percentage points")
        if abs(avg_gender_gap) < 1:
            print("✅ Gender parity is well maintained")
        elif avg_gender_gap > 1:
            print("⚠️ Females have higher participation rates")
        else:
            print("⚠️ Males have higher participation rates")
        
        # Candidate numbers growth
        total_growth = ((df['Total_Sat'].iloc[-1] / df['Total_Sat'].iloc[0]) - 1) * 100
        female_growth = ((df['Female_Sat'].iloc[-1] / df['Female_Sat'].iloc[0]) - 1) * 100
        male_growth = ((df['Male_Sat'].iloc[-1] / df['Male_Sat'].iloc[0]) - 1) * 100
        
        print(f"\n📊 CANDIDATE NUMBERS GROWTH:")
        print(f"Total candidates: {total_growth:+.1f}%")
        print(f"Female candidates: {female_growth:+.1f}%")
        print(f"Male candidates: {male_growth:+.1f}%")
        
        # Create comprehensive visualizations
        self.create_trend_visualizations(df)
        
        return df
    
    def create_trend_visualizations(self, df):
        """Create comprehensive visualizations"""
        
        # Create a comprehensive dashboard
        fig = plt.figure(figsize=(18, 14))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Participation rates over time
        ax1 = fig.add_subplot(gs[0, :2])
        ax1.plot(df['Year'], df['Total_Participation_Rate'], 'o-', linewidth=3, markersize=8, label='Total', color='purple')
        ax1.plot(df['Year'], df['Female_Participation_Rate'], 's-', linewidth=2, markersize=6, label='Female', color='red')
        ax1.plot(df['Year'], df['Male_Participation_Rate'], '^-', linewidth=2, markersize=6, label='Male', color='blue')
        ax1.set_title('KCSE Participation Rates by Gender (2020-2024)', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Participation Rate (%)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(95, 101)  # Focus on the relevant range
        
        # 2. Gender gap over time
        ax2 = fig.add_subplot(gs[0, 2])
        colors = ['red' if x > 0 else 'blue' for x in df['Gender_Gap']]
        bars = ax2.bar(df['Year'], df['Gender_Gap'], color=colors, alpha=0.7)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax2.set_title('Gender Gap in Participation\n(Positive = Female advantage)', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Year')
        ax2.set_ylabel('Gap (percentage points)')
        ax2.grid(True, alpha=0.3)
        
        # 3. Total candidates over time
        ax3 = fig.add_subplot(gs[1, 0])
        ax3.bar(df['Year'], df['Total_Sat'], alpha=0.8, color='skyblue', edgecolor='navy')
        ax3.set_title('Total KCSE Candidates', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Year')
        ax3.set_ylabel('Number of Candidates')
        ax3.grid(True, alpha=0.3)
        # Format y-axis to show values in thousands
        ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K'))
        
        # 4. Male vs Female candidates
        ax4 = fig.add_subplot(gs[1, 1])
        width = 0.35
        x = np.arange(len(df))
        ax4.bar(x - width/2, df['Female_Sat'], width, label='Female', color='red', alpha=0.7)
        ax4.bar(x + width/2, df['Male_Sat'], width, label='Male', color='blue', alpha=0.7)
        ax4.set_title('Male vs Female Candidates', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Year')
        ax4.set_ylabel('Number of Candidates')
        ax4.set_xticks(x)
        ax4.set_xticklabels([int(year) for year in df['Year']])
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K'))
        
        # 5. Registered vs Sat comparison
        ax5 = fig.add_subplot(gs[1, 2])
        ax5.plot(df['Year'], df['Total_Registered'], 'o-', label='Registered', linewidth=2, markersize=6)
        ax5.plot(df['Year'], df['Total_Sat'], 's-', label='Sat for Exam', linewidth=2, markersize=6)
        ax5.set_title('Registered vs Actual Participants', fontsize=12, fontweight='bold')
        ax5.set_xlabel('Year')
        ax5.set_ylabel('Number of Students')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        ax5.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K'))
        
        # 6. Year-over-year changes
        ax6 = fig.add_subplot(gs[2, :])
        changes = df['Total_Change'].values
        colors = ['green' if x > 0 else 'red' for x in changes]
        bars = ax6.bar(df['Year'], changes, color=colors, alpha=0.7)
        ax6.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax6.set_title('Year-over-Year Change in Total Candidates', fontsize=12, fontweight='bold')
        ax6.set_xlabel('Year')
        ax6.set_ylabel('Change in Number of Candidates')
        ax6.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, value in zip(bars, changes):
            height = bar.get_height()
            ax6.text(bar.get_x() + bar.get_width()/2., height + (1000 if height > 0 else -3000),
                    f'{int(value):,}', ha='center', va='bottom' if height > 0 else 'top', fontweight='bold')
        
        plt.suptitle('KCSE Examination Participation Analysis Dashboard\nKenya 2020-2024', 
                     fontsize=16, fontweight='bold', y=0.98)
        
        plt.savefig('kcse_comprehensive_analysis.png', dpi=300, bbox_inches='tight')
        print(f"\n📊 Comprehensive dashboard saved as 'kcse_comprehensive_analysis.png'")
        plt.show()
    
    def analyze_county_patterns(self):
        """Analyze county-level patterns (basic analysis given data structure)"""
        print("\n" + "="*60)
        print("COUNTY-LEVEL PATTERNS ANALYSIS")
        print("="*60)
        
        if 'county_gender' in self.cleaned_data:
            df_gender = self.cleaned_data['county_gender']
            print(f"\nGender distribution data: {df_gender.shape[0]} counties")
            print("Sample data structure:")
            print(df_gender.head())
        
        if 'county_age' in self.cleaned_data:
            df_age = self.cleaned_data['county_age']
            print(f"\nAge distribution data: {df_age.shape[0]} counties")
            print("Sample data structure:")
            print(df_age.head())
    
    def generate_policy_insights(self):
        """Generate policy insights and recommendations"""
        print("\n" + "="*70)
        print("POLICY INSIGHTS AND RECOMMENDATIONS")
        print("="*70)
        
        df = self.cleaned_data['time_series']
        
        insights = []
        recommendations = []
        
        # Participation rate analysis
        avg_participation = df['Total_Participation_Rate'].mean()
        if avg_participation > 99:
            insights.append(f"✅ Excellent overall participation rate ({avg_participation:.2f}%)")
        elif avg_participation > 95:
            insights.append(f"✓ Good overall participation rate ({avg_participation:.2f}%)")
        else:
            insights.append(f"⚠️ Concerning participation rate ({avg_participation:.2f}%)")
            recommendations.append("Investigate barriers preventing registered students from sitting exams")
        
        # Growth trend analysis
        total_growth = ((df['Total_Sat'].iloc[-1] / df['Total_Sat'].iloc[0]) - 1) * 100
        if total_growth > 10:
            insights.append(f"📈 Strong growth in candidate numbers ({total_growth:.1f}%)")
        elif total_growth > 0:
            insights.append(f"📈 Positive growth in candidate numbers ({total_growth:.1f}%)")
        else:
            insights.append(f"📉 Decline in candidate numbers ({total_growth:.1f}%)")
            recommendations.append("Address factors causing decline in KCSE participation")
        
        # Gender equity analysis
        gender_gap = df['Gender_Gap'].mean()
        if abs(gender_gap) < 0.5:
            insights.append(f"⚖️ Excellent gender parity (gap: {gender_gap:+.2f} pp)")
        elif abs(gender_gap) < 2:
            insights.append(f"✓ Good gender balance (gap: {gender_gap:+.2f} pp)")
        else:
            insights.append(f"⚠️ Significant gender gap ({gender_gap:+.2f} pp)")
            if gender_gap > 0:
                recommendations.append("Investigate why female participation exceeds male participation")
            else:
                recommendations.append("Address barriers preventing female participation in KCSE")
        
        # Print insights
        print("\n🔍 KEY FINDINGS:")
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight}")
        
        print("\n📋 POLICY RECOMMENDATIONS:")
        base_recommendations = [
            "Maintain high participation rates through continued support",
            "Monitor gender parity trends annually",
            "Investigate regional variations in participation",
            "Study age-related factors affecting KCSE completion",
            "Strengthen data collection for county-level analysis"
        ]
        
        all_recommendations = recommendations + base_recommendations
        for i, rec in enumerate(all_recommendations, 1):
            print(f"{i}. {rec}")
        
        # Research priorities
        print("\n🔬 RESEARCH PRIORITIES:")
        research_areas = [
            "County-level analysis of participation disparities",
            "Age distribution patterns and over-age candidate trends",
            "Socioeconomic factors affecting KCSE completion",
            "Regional infrastructure and resource allocation impact",
            "Long-term trends in secondary education completion"
        ]
        
        for i, area in enumerate(research_areas, 1):
            print(f"{i}. {area}")
    
    def run_comprehensive_analysis(self):
        """Run the complete analysis"""
        print("🎓 KCSE EXAMINATION PARTICIPATION ANALYSIS")
        print("="*70)
        print("Research Question: How do KCSE examination participation rates vary")
        print("by gender, age group, and county in Kenya, and what trends emerge over time?")
        print("="*70)
        
        # Load and clean data
        self.load_and_clean_time_series_data()
        self.load_county_gender_data()
        self.load_county_age_data()
        
        # Perform analyses
        self.analyze_participation_trends()
        self.analyze_county_patterns()
        self.generate_policy_insights()
        
        print(f"\n✅ Comprehensive analysis completed!")
        print("📊 Check the generated visualization: kcse_comprehensive_analysis.png")

if __name__ == "__main__":
    analyzer = KCSEAnalyzerImproved()
    analyzer.run_comprehensive_analysis()