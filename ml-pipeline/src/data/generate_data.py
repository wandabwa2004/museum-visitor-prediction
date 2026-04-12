"""
Museum Visitor Data Generation Script
Melbourne Museum of Migration - Synthetic Data Generator

This script generates realistic visitor data for modeling purposes.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def generate_temperature(month):
    """Generate realistic temperature for Melbourne based on month."""
    temp_map = {
        1: (15, 26, 5),   # Jan: Summer
        2: (15, 26, 5),   # Feb: Summer
        3: (13, 24, 4),   # Mar: Autumn
        4: (11, 20, 4),   # Apr: Autumn
        5: (8, 16, 3),    # May: Autumn
        6: (6, 14, 3),    # Jun: Winter
        7: (6, 13, 3),    # Jul: Winter
        8: (7, 15, 3),    # Aug: Winter
        9: (8, 17, 3),    # Sep: Spring
        10: (10, 20, 4),  # Oct: Spring
        11: (12, 22, 4),  # Nov: Spring
        12: (14, 25, 5)   # Dec: Summer
    }
    min_temp, max_temp, std = temp_map[month]
    avg_temp = (min_temp + max_temp) / 2
    return np.random.normal(avg_temp, std)


def get_weather_type(precip):
    """Determine weather type based on precipitation."""
    if precip < 0.5:
        return np.random.choice(['Sunny', 'Partly Cloudy'], p=[0.7, 0.3])
    elif precip < 5:
        return 'Cloudy'
    else:
        return 'Rainy'


def generate_museum_data(start_date='2023-01-01', end_date='2025-12-31', seed=42):
    """
    Generate synthetic museum visitor data.

    Parameters:
    -----------
    start_date : str
        Start date in 'YYYY-MM-DD' format
    end_date : str
        End date in 'YYYY-MM-DD' format
    seed : int
        Random seed for reproducibility

    Returns:
    --------
    pd.DataFrame
        DataFrame with visitor data and features
    """
    np.random.seed(seed)

    print(f"Generating data from {start_date} to {end_date}...")

    # 1. Generate date range
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    df = pd.DataFrame({'date': dates})
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day_name'] = df['date'].dt.day_name()
    df['week_of_year'] = df['date'].dt.isocalendar().week
    df['quarter'] = df['date'].dt.quarter

    # 2. Public holidays
    public_holidays = [
        # 2023
        '2023-01-01', '2023-01-02', '2023-01-26', '2023-03-13', '2023-04-07', '2023-04-08',
        '2023-04-09', '2023-04-10', '2023-04-25', '2023-06-12', '2023-11-07', '2023-12-25', '2023-12-26',
        # 2024
        '2024-01-01', '2024-01-26', '2024-03-11', '2024-03-29', '2024-03-30', '2024-03-31',
        '2024-04-01', '2024-04-25', '2024-06-10', '2024-11-05', '2024-12-25', '2024-12-26',
        # 2025
        '2025-01-01', '2025-01-27', '2025-03-10', '2025-04-18', '2025-04-19', '2025-04-20',
        '2025-04-21', '2025-04-25', '2025-06-09', '2025-11-04', '2025-12-25', '2025-12-26'
    ]
    df['is_public_holiday'] = df['date'].astype(str).isin(public_holidays).astype(int)

    # 3. School holidays
    school_holidays = []
    for year in [2023, 2024, 2025]:
        school_holidays.extend(pd.date_range(f'{year}-04-01', f'{year}-04-18'))
        school_holidays.extend(pd.date_range(f'{year}-06-24', f'{year}-07-10'))
        school_holidays.extend(pd.date_range(f'{year}-09-16', f'{year}-10-02'))
        school_holidays.extend(pd.date_range(f'{year}-12-18', f'{year}-12-31'))

    df['is_school_holiday'] = df['date'].isin(school_holidays).astype(int)

    # 4. Weather
    df['temperature'] = df['month'].apply(generate_temperature).round(1)
    df['precipitation'] = np.random.exponential(2, len(df)).round(1)
    df['weather_type'] = df['precipitation'].apply(get_weather_type)

    # 5. Special exhibitions
    df['special_exhibition'] = 0
    exhibitions = [
        ('2023-02-01', '2023-04-30'), ('2023-06-01', '2023-08-15'), ('2023-10-01', '2023-12-20'),
        ('2024-01-15', '2024-03-31'), ('2024-05-01', '2024-07-31'), ('2024-09-01', '2024-11-15'),
        ('2025-02-01', '2025-04-15'), ('2025-06-01', '2025-08-31'), ('2025-10-01', '2025-12-20')
    ]
    for start, end in exhibitions:
        mask = (df['date'] >= start) & (df['date'] <= end)
        df.loc[mask, 'special_exhibition'] = 1

    # 6. Local events
    df['local_event'] = 0
    major_events = [
        ('2023-03-20', '2023-03-26'), ('2023-10-05', '2023-10-22'),
        ('2024-03-18', '2024-03-24'), ('2024-10-03', '2024-10-20'),
        ('2025-03-17', '2025-03-23'), ('2025-10-02', '2025-10-19')
    ]
    for start, end in major_events:
        mask = (df['date'] >= start) & (df['date'] <= end)
        df.loc[mask, 'local_event'] = 1

    # 7. Marketing campaigns
    df['marketing_campaign'] = (np.random.rand(len(df)) < 0.15).astype(int)
    df['ticket_promotion'] = (np.random.rand(len(df)) < 0.10).astype(int)
    df['ticket_price'] = 25  # AUD
    df.loc[df['ticket_promotion'] == 1, 'ticket_price'] = 20

    # 8. Generate visitor counts
    base_visitors = 250
    df['visitors'] = base_visitors

    # Day of week effect
    day_multiplier = {0: 0.90, 1: 0.85, 2: 0.88, 3: 0.92, 4: 1.00, 5: 1.30, 6: 1.25}
    df['visitors'] *= df['day_of_week'].map(day_multiplier)

    # Seasonal effect
    season_multiplier = {
        1: 1.40, 2: 1.35, 3: 1.15, 4: 1.05, 5: 0.90, 6: 0.80,
        7: 0.75, 8: 0.85, 9: 1.00, 10: 1.10, 11: 1.20, 12: 1.45
    }
    df['visitors'] *= df['month'].map(season_multiplier)

    # Holiday effects
    df.loc[df['is_public_holiday'] == 1, 'visitors'] *= 1.50
    df.loc[df['is_school_holiday'] == 1, 'visitors'] *= 1.30

    # Weather impact
    df['weather_factor'] = 1.0
    df.loc[df['weather_type'] == 'Sunny', 'weather_factor'] = 1.20
    df.loc[df['weather_type'] == 'Partly Cloudy', 'weather_factor'] = 1.05
    df.loc[df['weather_type'] == 'Cloudy', 'weather_factor'] = 0.95
    df.loc[df['weather_type'] == 'Rainy', 'weather_factor'] = 0.70

    df['temp_factor'] = 1.0
    df.loc[(df['temperature'] >= 20) & (df['temperature'] <= 24), 'temp_factor'] = 1.15
    df.loc[df['temperature'] < 10, 'temp_factor'] = 0.85
    df.loc[df['temperature'] > 32, 'temp_factor'] = 0.90

    df['visitors'] *= df['weather_factor'] * df['temp_factor']

    # Event and promotion effects
    df.loc[df['special_exhibition'] == 1, 'visitors'] *= 1.25
    df.loc[df['local_event'] == 1, 'visitors'] *= 1.40
    df.loc[df['marketing_campaign'] == 1, 'visitors'] *= 1.15
    df.loc[df['ticket_promotion'] == 1, 'visitors'] *= 1.20

    # Add noise
    noise = np.random.normal(1.0, 0.12, len(df))
    df['visitors'] *= noise

    # Add outliers
    outlier_indices = np.random.choice(df.index, size=int(len(df) * 0.02), replace=False)
    df.loc[outlier_indices, 'visitors'] *= np.random.uniform(1.5, 2.5, len(outlier_indices))

    # Growth trend
    days_since_start = (df['date'] - df['date'].min()).dt.days
    growth_factor = 1 + (days_since_start * 0.0001)
    df['visitors'] *= growth_factor

    # Round and clip
    df['visitors'] = df['visitors'].round(0).astype(int).clip(lower=100, upper=1200)

    # 9. Lagged features
    df['visitors_last_week'] = df['visitors'].shift(7)
    df['visitors_last_2weeks'] = df['visitors'].shift(14)
    df['visitors_last_month'] = df['visitors'].shift(30)
    df['visitors_7day_avg'] = df['visitors'].rolling(window=7, min_periods=1).mean()
    df['visitors_14day_avg'] = df['visitors'].rolling(window=14, min_periods=1).mean()
    df['visitors_30day_avg'] = df['visitors'].rolling(window=30, min_periods=1).mean()
    df['visitors_same_day_last_year'] = df['visitors'].shift(365)

    # Fill NaN values
    for col in df.columns:
        if df[col].isna().any():
            if df[col].dtype in ['float64', 'int64']:
                df[col].fillna(df[col].mean(), inplace=True)

    # Select final columns
    final_columns = [
        'date', 'year', 'month', 'day', 'day_of_week', 'day_name', 'week_of_year', 'quarter',
        'is_public_holiday', 'is_school_holiday',
        'temperature', 'precipitation', 'weather_type',
        'special_exhibition', 'local_event',
        'marketing_campaign', 'ticket_promotion', 'ticket_price',
        'visitors_last_week', 'visitors_last_2weeks', 'visitors_last_month',
        'visitors_7day_avg', 'visitors_14day_avg', 'visitors_30day_avg',
        'visitors_same_day_last_year',
        'visitors'
    ]

    df_final = df[final_columns].copy()

    print(f"\nDataset generated successfully!")
    print(f"Shape: {df_final.shape}")
    print(f"Visitor stats - Mean: {df_final['visitors'].mean():.0f}, "
          f"Median: {df_final['visitors'].median():.0f}, "
          f"Min: {df_final['visitors'].min()}, "
          f"Max: {df_final['visitors'].max()}")

    return df_final


def main():
    """Main function to generate and save data."""
    # Create output directory if it doesn't exist
    output_dir = '../../data/raw'
    os.makedirs(output_dir, exist_ok=True)

    # Generate data
    df = generate_museum_data()

    # Save to CSV
    output_path = os.path.join(output_dir, 'museum_visitors_melbourne.csv')
    df.to_csv(output_path, index=False)

    print(f"\nData saved to: {output_path}")
    print(f"Total records: {len(df)}")
    print(f"\nFirst few rows:")
    print(df.head())


if __name__ == "__main__":
    main()
