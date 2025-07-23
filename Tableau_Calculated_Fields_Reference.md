# Tableau Calculated Fields Reference - KCSE Analysis

## 📊 Essential Calculated Fields for KCSE Data

### 1. **Participation Rate** (Manual Calculation)
```tableau
SUM([Sat]) / SUM([Registered]) * 100
```
*Use when you need to calculate participation rate from raw registered/sat numbers*

### 2. **Year-over-Year Growth Rate**
```tableau
(ZN(SUM([Sat])) - LOOKUP(ZN(SUM([Sat])), -1)) / ABS(LOOKUP(ZN(SUM([Sat])), -1))
```
*Shows percentage change from previous year*

### 3. **Gender Gap**
```tableau
{FIXED [Year] : MAX(IF [Gender] = "Female" THEN [Participation_Rate] END)} -
{FIXED [Year] : MAX(IF [Gender] = "Male" THEN [Participation_Rate] END)}
```
*Calculates the participation rate difference between genders*

### 4. **Compound Annual Growth Rate (CAGR)**
```tableau
POWER(
    LAST() / FIRST(), 
    1/DATEDIFF('year', 
        {MIN([Year])}, 
        {MAX([Year])}
    )
) - 1
```
*Shows average annual growth rate over the entire period*

### 5. **Running Total**
```tableau
RUNNING_SUM(SUM([Sat]))
```
*Cumulative count of candidates over time*

### 6. **Moving Average (3-Year)**
```tableau
WINDOW_AVG(SUM([Sat]), -1, 1)
```
*Smooths out yearly fluctuations*

### 7. **Rank by Participation Rate**
```tableau
RANK(AVG([Participation_Rate]), 'desc')
```
*Ranks years by participation performance*

### 8. **Growth Category**
```tableau
IF [YoY Growth Rate] > 0.05 THEN "High Growth"
ELSEIF [YoY Growth Rate] > 0.02 THEN "Moderate Growth"
ELSEIF [YoY Growth Rate] > 0 THEN "Low Growth"
ELSE "Decline"
END
```
*Categorizes growth into buckets*

### 9. **Performance Indicator**
```tableau
IF [Participation_Rate] >= 99.5 THEN "Excellent"
ELSEIF [Participation_Rate] >= 99.0 THEN "Very Good"
ELSEIF [Participation_Rate] >= 98.0 THEN "Good"
ELSE "Needs Improvement"
END
```
*Creates performance categories*

### 10. **Target vs Actual**
```tableau
// Assuming 99% target participation rate
[Participation_Rate] - 99
```
*Shows how much above/below target*

---

## 🎯 Parameters for Interactivity

### Year Range Parameter
- **Name:** `Year_Range`
- **Type:** Integer Range
- **Current Value:** 2020 to 2024
- **Use in Filter:** `[Year] >= [Year_Range_Start] AND [Year] <= [Year_Range_End]`

### Metric Selector Parameter
- **Name:** `Metric_Choice`
- **Type:** String
- **Values:** "Registered", "Sat", "Participation_Rate"
- **Use in Calculated Field:**
```tableau
CASE [Metric_Choice]
WHEN "Registered" THEN SUM([Registered])
WHEN "Sat" THEN SUM([Sat])
WHEN "Participation_Rate" THEN AVG([Participation_Rate])
END
```

### Gender Focus Parameter
- **Name:** `Gender_Focus`
- **Type:** String
- **Values:** "All", "Male", "Female", "Comparison"

---

## 🔢 Key Performance Indicators (KPIs)

### Overall Success Rate
```tableau
// Shows the 99.56% success story
AVG([Participation_Rate])
```

### Total Growth
```tableau
// Shows 28.8% growth
(MAX([Sat]) - MIN([Sat])) / MIN([Sat]) * 100
```

### Gender Equity Score
```tableau
// Lower is better (closer to 0 = perfect equity)
ABS([Female Participation Rate] - [Male Participation Rate])
```

### Capacity Utilization
```tableau
// How well Kenya utilizes its educational capacity
SUM([Sat]) / SUM([Registered]) * 100
```

---

## 📈 Advanced Analytics

### Trend Analysis
```tableau
// Linear trend line slope
INDEX() / SIZE()
```

### Seasonal Adjustment (if you had monthly data)
```tableau
// This is theoretical for demonstration
[Participation_Rate] / WINDOW_AVG([Participation_Rate])
```

### Outlier Detection
```tableau
// Identifies years that are significantly different
ABS([Participation_Rate] - WINDOW_AVG([Participation_Rate])) > 
WINDOW_STDEV([Participation_Rate]) * 2
```

---

## 💡 Pro Tips

1. **Always use ZN()** to handle null values in calculations
2. **Test calculated fields** with sample data before using in dashboards
3. **Name fields descriptively** so other users understand them
4. **Comment complex calculations** using // for future reference
5. **Use table calculations** for relative comparisons (ranks, percentages)

---

## 🚨 Common Mistakes to Avoid

❌ **Don't:** Use SUM() when you mean AVG() for rates  
✅ **Do:** Use AVG() for participation rates, SUM() for counts

❌ **Don't:** Forget to handle nulls in time series calculations  
✅ **Do:** Use ZN() or ISNULL() checks

❌ **Don't:** Mix aggregated and non-aggregated fields  
✅ **Do:** Be consistent with aggregation levels

---

**Copy these calculated fields into your Tableau workbook to enhance your KCSE analysis!** 📊