# Traffic Accident Data Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap

# Set visual style
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# Load the dataset (change the filename if needed)
df = pd.read_csv("US_Accidents_March23.csv")

# Select important columns
df = df[['Severity', 'Start_Time', 'Start_Lat', 'Start_Lng', 'City',
         'Weather_Condition', 'Visibility(mi)', 'Wind_Speed(mph)',
         'Precipitation(in)', 'Street', 'Side']]

# Convert time to datetime and extract time-based features
df['Start_Time'] = pd.to_datetime(df['Start_Time'])
df['Hour'] = df['Start_Time'].dt.hour
df['DayOfWeek'] = df['Start_Time'].dt.day_name()

# ------------------------
# 1. Accidents by Hour
# ------------------------
plt.figure()
sns.countplot(data=df, x='Hour', palette='coolwarm')
plt.title('Accidents by Hour of Day')
plt.xlabel('Hour')
plt.ylabel('Number of Accidents')
plt.tight_layout()
plt.show()

# ------------------------
# 2. Accidents by Day
# ------------------------
plt.figure()
sns.countplot(data=df, x='DayOfWeek', order=['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                                             'Friday', 'Saturday', 'Sunday'], palette='magma')
plt.title('Accidents by Day of the Week')
plt.ylabel('Number of Accidents')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ------------------------
# 3. Weather Conditions
# ------------------------
plt.figure()
top_weather = df['Weather_Condition'].value_counts().head(10)
top_weather.plot(kind='bar', color='orange')
plt.title('Top 10 Weather Conditions During Accidents')
plt.xlabel('Weather Condition')
plt.ylabel('Number of Accidents')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ------------------------
# 4. Visibility Analysis
# ------------------------
plt.figure()
sns.histplot(data=df, x='Visibility(mi)', kde=True, bins=30, color='green')
plt.title('Visibility Distribution During Accidents')
plt.xlabel('Visibility (miles)')
plt.tight_layout()
plt.show()

# ------------------------
# 5. Wind Speed vs Severity
# ------------------------
plt.figure()
sns.boxplot(data=df, x='Severity', y='Wind_Speed(mph)', palette='Blues')
plt.title('Wind Speed by Severity Level')
plt.tight_layout()
plt.show()

# ------------------------
# 6. Correlation Heatmap
# ------------------------
plt.figure()
corr = df[['Severity', 'Visibility(mi)', 'Wind_Speed(mph)', 'Precipitation(in)']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap: Weather vs Severity")
plt.tight_layout()
plt.show()

# ------------------------
# 7. Accident Hotspots HeatMap
# ------------------------

# Create a subsample to speed up visualization
sample_df = df[['Start_Lat', 'Start_Lng']].dropna().sample(n=10000, random_state=42)

# Create a folium map
map_center = [sample_df['Start_Lat'].mean(), sample_df['Start_Lng'].mean()]
map_ = folium.Map(location=map_center, zoom_start=5, tiles='Stamen Toner')

# Add heatmap layer
HeatMap(data=sample_df.values, radius=10).add_to(map_)

# Save the map
map_.save("accident_hotspots.html")
print("✔️ Accident hotspot map saved as 'accident_hotspots.html'.")

# ------------------------
# 8. Export Cleaned Data (Optional)
# ------------------------
df.to_csv("processed_accident_data.csv", index=False)
print("✔️ Cleaned dataset saved as 'processed_accident_data.csv'.")
