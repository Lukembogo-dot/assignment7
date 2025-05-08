import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

# Fetch global COVID-19 data using the API
url = 'https://api.covid19api.com/summary'
response = requests.get(url)

# Check if the request was successful
if response.status_code != 200:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    exit()

data = response.json()

# Check if the expected keys exist in the response
if 'Global' not in data or 'Countries' not in data:
    print("Unexpected API response structure.")
    exit()

# Get global data (cases, deaths, recoveries)
global_data = data['Global']

# Display the global data
print("Global Data:")
print(global_data)

# Get country-specific data
countries_data = data['Countries']
df = pd.DataFrame(countries_data)

# Display the first few rows of the DataFrame
print("\nCountry Data (First 5 Rows):")
print(df.head())

# Sort the DataFrame by TotalConfirmed cases
df_sorted = df.sort_values('TotalConfirmed', ascending=False)

# Get the top 10 countries with the most confirmed cases
top_10_countries = df_sorted.head(10)

# Create a bar plot
plt.figure(figsize=(10, 6))
sns.barplot(x='TotalConfirmed', y='Country', data=top_10_countries)
plt.title('Top 10 Countries with the Highest Confirmed COVID-19 Cases')
plt.xlabel('Total Confirmed Cases')
plt.ylabel('Country')
plt.show()

# Calculate the recovery rate (TotalRecovered / TotalConfirmed)
# Avoid division by zero by replacing 0 in TotalConfirmed with 1
df['RecoveryRate'] = df['TotalRecovered'] / df['TotalConfirmed'].replace(0, 1) * 100

# Sort by recovery rate
df_sorted_by_recovery = df.sort_values('RecoveryRate', ascending=False)

# Get the top 10 countries with the highest recovery rates
top_10_recovery = df_sorted_by_recovery.head(10)

# Create a bar plot for recovery rate
plt.figure(figsize=(10, 6))
sns.barplot(x='RecoveryRate', y='Country', data=top_10_recovery)
plt.title('Top 10 Countries with the Highest COVID-19 Recovery Rates')
plt.xlabel('Recovery Rate (%)')
plt.ylabel('Country')
plt.show()


