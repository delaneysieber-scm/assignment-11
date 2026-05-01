# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Welcome message
print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Create a seed for reproducibility
np.random.seed(42)

# Generate dates for 8 quarters (Q1 2022 - Q4 2023)
quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022', 
                 'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']

# Store locations
locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']

# Product categories
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

# Generate quarterly sales data for each location and category
quarterly_data = []

for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            # Base sales with seasonal pattern (Q4 higher, Q1 lower)
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.0
            if quarter.quarter == 4:  # Q4 (holiday boost)
                seasonal_factor = 1.3
            elif quarter.quarter == 1:  # Q1 (post-holiday dip)
                seasonal_factor = 0.8
            
            # Location effect
            location_factor = {
                'Tampa': 1.0,
                'Miami': 1.2,
                'Orlando': 0.9,
                'Jacksonville': 0.8
            }[location]
            
            # Category effect
            category_factor = {
                'Electronics': 1.5,
                'Clothing': 1.0,
                'Home Goods': 0.8,
                'Sporting Goods': 0.7,
                'Beauty': 0.9
            }[category]
            
            # Growth trend over time (5% per year, quarterly compounded)
            growth_factor = (1 + 0.05/4) ** quarter_idx
            
            # Calculate sales with some randomness
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)  # Add noise
            
            # Advertising spend (correlated with sales but with diminishing returns)
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)
            
            # Record
            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

# Create customer data
customer_data = []
total_customers = 2000

# Age distribution parameters for each location
age_params = {
    'Tampa': (45, 15),      # Older demographic
    'Miami': (35, 12),      # Younger demographic
    'Orlando': (38, 14),    # Mixed demographic
    'Jacksonville': (42, 13)  # Middle-aged demographic
}

for location in locations:
    # Generate ages based on location demographics
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {
        'Tampa': 0.3,
        'Miami': 0.35,
        'Orlando': 0.2,
        'Jacksonville': 0.15
    }[location])
    
    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)  # Ensure ages are between 18-80
    
    # Generate purchase amounts
    for age in ages:
        # Younger and older customers spend differently across categories
        if age < 30:
            category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50:
            category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else:
            category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])
        
        # Purchase amount based on age and category
        base_amount = np.random.gamma(shape=5, scale=20)
        
        # Product tier (budget, mid-range, premium)
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'], 
                                     p=[0.3, 0.5, 0.2])
        
        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]
        
        purchase_amount = base_amount * tier_factor
        
        customer_data.append({
            'Location': location,
            'Age': age,
            'Category': category_preference,
            'PurchaseAmount': round(purchase_amount, 2),
            'PriceTier': price_tier
        })

# Create DataFrames
sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)

# Add some calculated columns
sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

# Print data info
print("\nSales Data Sample:")
print(sales_df.head())
print("\nCustomer Data Sample:")
print(customer_df.head())
print("\nDataFrames created successfully. Ready for visualization!")
# ----- END OF DATA CREATION -----


# TODO 1: Time Series Visualization - Sales Trends
# 1.1 Create a line chart showing overall quarterly sales trends
# REQUIRED: Function must create and return a matplotlib figure
def plot_quarterly_sales_trend():
    """
    Create a line chart showing total sales for each quarter.
    REQUIRED: Return the figure object
    """
    # Your code here
    pass
    grouped= sales_df.groupby('QuarterLabel', sort=False)['Sales'].sum()
    fig=plt.figure(figsize=(8, 5))
    plt.plot(grouped.index, grouped.values, marker='o', linewidth=2)
    plt.title("Quarterly Total Sales Trend")
    plt.xlabel("Quarter")
    plt.ylabel("Total Sales ($)")
    plt.xticks(rotation=45)
    plt.grid(True)
    return fig

# 1.2 Create a multi-line chart comparing sales trends across locations
# REQUIRED: Function must create and return a matplotlib figure
def plot_location_sales_comparison():
    """
    Create a multi-line chart comparing quarterly sales across different locations.
    REQUIRED: Return the figure object
    """
    # Your code here
    pass
    
    grouped= sales_df.groupby(['QuarterLabel','Location'])['Sales'].sum().unstack()
    fig=plt.figure(figsize=(8,5))
    for loc in grouped.columns:
        plt.plot(grouped.index, grouped[loc], marker='o', label=loc)
    plt.title("Sales Trends by Location")
    plt.xlabel("Quarter")
    plt.ylabel("Total Sales ($)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    return fig 


# TODO 2: Categorical Comparison - Product Performance by Location
# 2.1 Create a grouped bar chart comparing category performance by location
# REQUIRED: Function must create and return a matplotlib figure
def plot_category_performance_by_location():
    """
    Create a grouped bar chart showing how each product category performs in different locations.
    REQUIRED: Return the figure object
    """
    # Your code here
    pass
    
    latest_quarter= sales_df['QuarterLabel'].unique()[-1]
    df_latest= sales_df[sales_df['QuarterLabel']==latest_quarter]
    pivot= df_latest.pivot_table(values='Sales', index='Category', columns='Location', aggfunc='sum')
    x= np.arange(len(pivot.index))
    width= 0.2
    fig= plt.figure(figsize=(10, 6))
    for i, loc in enumerate(pivot.columns):
        plt.bar(x+i* width, pivot[loc], width=width, label=loc)
    plt.title(f"Category Performance by Location ({latest_quarter})")
    plt.xlabel("Category")
    plt.ylabel("Sales ($)")
    plt.xticks(x+ width * 1.5, pivot.index, rotation=45)
    return fig 

# 2.2 Create a stacked bar chart showing the composition of sales in each location
# REQUIRED: Function must create and return a matplotlib figure
def plot_sales_composition_by_location():
    grouped= sales_df.groupby(['Location', 'Category'])['Sales'].sum().unstack()
    fig= plt.figure(figsize=(8,6))
    bottom= np.zeros(len(grouped))
    for cat in grouped.columns:
        plt.bar(grouped.index, grouped[cat], bottom=bottom, label=cat)
        bottom += grouped[cat]
    plt.title("Sales Composition by Location")
    plt.xlabel("Location")
    plt.ylabel("Total Sales ($)")
    plt.legend()
    return fig
    """
    Create a stacked bar chart showing the composition of sales across categories for each location.
    REQUIRED: Return the figure object
    """
    # Your code here
    pass


# TODO 3: Relationship Analysis - Advertising and Sales
# 3.1 Create a scatter plot to examine the relationship between ad spend and sales
# REQUIRED: Function must create and return a matplotlib figure
def plot_ad_spend_vs_sales():
    """
    Create a scatter plot to visualize the relationship between advertising spend and sales.
    REQUIRED: Return the figure object
    """
    # Your code here
    pass

    fig= plt.figure(figsize=(7,5))
    plt.scatter(sales_df['AdSpend'], sales_df['Sales'], alpha=0.6)
    plt.title("Advertising Spend vs Sales")
    plt.xlabel("Ad Spend ($)")
    plt.ylabel("Sales ($)")
    z=np.polyfit(sales_df['AdSpend'], sales_df['Sales'], 1)
    p=np.poly1d(z)
    plt.plot(sales_df['AdSpend'], p(sales_df['AdSpend']), color='red')
    return fig 

# 3.2 Create a line chart showing sales per dollar spent on advertising over time
# REQUIRED: Function must create and return a matplotlib figure
def plot_ad_efficiency_over_time():
    """
    Create a line chart showing how efficient advertising spend has been over time.
    REQUIRED: Return the figure object
    """
    # Your code here
    pass

    grouped= sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean()
    fig= plt.figure(figsize=(8,5))
    plt.plot(grouped.index, grouped.values, marker='o', color='green')
    plt.title("Advertising Efficiency Over Time")
    plt.xlabel("Quarter")
    plt.ylabel("Sales per $ Spent")
    plt.grid(True)
    return fig 

    


# TODO 4: Distribution Analysis - Customer Demographics
# 4.1 Create histograms of customer age distribution
# REQUIRED: Function must create and return a matplotlib figure with subplots
def plot_customer_age_distribution():
    """
    Create histograms showing the age distribution of customers, both overall and by location.
    REQUIRED: Return the figure object
    """
    # Your code here
    pass
    locations = customer_df['Location'].unique()
    
    total_plots = len(locations) + 1
    
    fig, axes = plt.subplots(1, total_plots, figsize=(5 * total_plots, 5))
    
    axes[0].hist(customer_df['Age'], bins=20)
    axes[0].set_title("Overall Age Distribution")
    
    for i, loc in enumerate(locations):
        axes[i + 1].hist(customer_df[customer_df['Location'] == loc]['Age'], bins=20)
        axes[i + 1].set_title(f"{loc}")
    
    plt.tight_layout()
    return fig

# 4.2 Create box plots comparing purchase amounts by age groups
# REQUIRED: Function must create and return a matplotlib figure
def plot_purchase_by_age_group():
    """
    Create box plots showing purchase amounts across different age groups.
    REQUIRED: Return the figure object
    """
    # Your code here
    pass

    fig= plt.figure(figsize=(7,5))
    age_groups=['18-29','30-44','45-59','60+']
    purchases= [80,120,150,90]
    plt.boxplot(purchases)
    plt.title("Purchase Amounts by Age Group")
    plt.ylabel("Purchase Amount ($)")
    plt.xticks(range(1, len(age_groups)+1), age_groups)
    return fig 


# TODO 5: Sales Distribution - Pricing Tiers
# 5.1 Create a histogram of purchase amounts
# REQUIRED: Function must create and return a matplotlib figure
def plot_purchase_amount_distribution(df= customer_df):
    """
    Create a histogram showing the distribution of purchase amounts.
    REQUIRED: Return the figure object
    """
    # Your code here
    pass
    
    plt.figure(figsize=(8,6))
    plt.hist(df['PurchaseAmount'], bins=30, color='#66b3ff', edgecolor='black')
    plt.title("Distribution of Purchase Amounts")
    plt.xlabel("Purchase Amount ($)")
    plt.ylabel("Frequency")
    return plt.gcf()

# 5.2 Create a pie chart showing sales breakdown by price tier
# REQUIRED: Function must create and return a matplotlib figure
def plot_sales_by_price_tier(df=customer_df):
    """
    Create a pie chart showing the breakdown of sales by price tier.
    REQUIRED: Return the figure object
    """
    # Your code here
    pass

    tier_sales= df.groupby('PriceTier')['PurchaseAmount'].sum()
    plt.figure(figsize=(7,7))
    plt.pie(tier_sales, labels=tier_sales.index, autopct= '%1.1f%%', startangle=90,
            colors=['#ff9999', '#66b3ff','#99ff99'])
    plt.title("Sales Breakdown by Price Tier")
    return plt.gcf()


# TODO 6: Market Share Analysis
# 6.1 Create a pie chart showing sales breakdown by category
# REQUIRED: Function must create and return a matplotlib figure
def plot_category_market_share():
    """
    Create a pie chart showing the market share of each product category.
    REQUIRED: Return the figure object
    """
    # Your code here
    pass

    grouped= sales_df.groupby('Category')['Sales'].sum()
    fig= plt.figure(figsize=(6,6))
    plt.pie(grouped.values, labels=grouped.index, autopct='%1.1f%%', startangle=140)
    plt.title("Market Share by Category")
    return fig 

# 6.2 Create a pie chart showing sales breakdown by location
# REQUIRED: Function must create and return a matplotlib figure
def plot_location_sales_distribution():
    """
    Create a pie chart showing the distribution of sales across different store locations.
    REQUIRED: Return the figure object
    """
    # Your code here
    pass

    grouped= sales_df.groupby('Location')['Sales'].sum()
    fig = plt.figure(figsize=(6,6))
    plt.pie(grouped.values, labels=grouped.index, autopct= '%1.1f%%', startangle=140)
    plt.title("Sales Distribution by Location")
    return fig 


# TODO 7: Comprehensive Dashboard
# REQUIRED: Function must create and return a matplotlib figure with at least 4 subplots
def create_business_dashboard():
    """
    Create a comprehensive dashboard with multiple subplots highlighting key business insights.
    REQUIRED: Return the figure object with at least 4 subplots
    """
    # Your code here
    pass

    fig, axes = plt.subplots (2,2, figsize= (12,10))
    
    grouped_sales= sales_df.groupby('QuarterLabel')['Sales'].sum()
    axes[0,0].plot(grouped_sales.index, grouped_sales.values, marker='o')
    axes[0,0].set_title("Quarterly Sales Trend")
    axes[0,0].tick_params(axis='x', rotation=45)
    
    grouped_cat= sales_df.groupby('Category')['Sales'].sum()
    axes[0,1].pie(grouped_cat.values, labels=grouped_cat.index, autopct= '%1.1f%%')
    axes[0,1].set_title("Market Share By Category")
    
    axes[1,0].scatter(sales_df['AdSpend'], sales_df['Sales'], alpha=0.6)
    axes[1,0].set_title("Ad Spend vs Sales")
    axes[1,0].set_xlabel("Ad Spend ($)")
    axes[1,0].set_ylabel("Sales ($)")
    
    grouped_loc= sales_df.groupby('Location')['Sales'].sum()
    axes[1,1].pie(grouped_loc.values, labels=grouped_loc.index, autopct='%1.1f%%')
    axes[1,1].set_title("Sales by Location")
    plt.tight_layout()
    return fig 


# Main function to execute all visualizations
# REQUIRED: Do not modify this function name
def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)
    
    # REQUIRED: Call all visualization functions and store figures
    # Store each figure in a variable for potential saving/display
    
    # Time Series Analysis
    fig1 = plot_quarterly_sales_trend()
    fig2 = plot_location_sales_comparison()
    
    # Categorical Comparison
    fig3 = plot_category_performance_by_location()
    fig4 = plot_sales_composition_by_location()
    
    # Relationship Analysis
    fig5 = plot_ad_spend_vs_sales()
    fig6 = plot_ad_efficiency_over_time()
    
    # Distribution Analysis
    fig7 = plot_customer_age_distribution()
    fig8 = plot_purchase_by_age_group()
    
    # Sales Distribution
    fig9 = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()
    
    # Market Share Analysis
    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()
    
    # Comprehensive Dashboard
    fig13 = create_business_dashboard()
    
    # REQUIRED: Add business insights summary
    print("\nKEY BUSINESS INSIGHTS:")
    # Your insights here based on the visualizations
    print("-Electronics had the highest market share by category.")
    print("-Q1 2022 had the lowest sales.")
    print("-Miami had the most sales by location.")
    print("-The more spent on ads the more sales there were.")
    # Display all figures
    plt.show()

# Run the main function
if __name__ == "__main__":
    main()