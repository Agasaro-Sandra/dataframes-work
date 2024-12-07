import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    rooms_api=requests.get('http://127.0.0.1:8000/rooms')
    rooms_api.raise_for_status()
    rooms_api_data = rooms_api.json()

    clients_api=requests.get('http://127.0.0.1:8000/clients')
    clients_api.raise_for_status()
    clients_api_data = clients_api.json()

    print(rooms_api_data)  # Check if it's a list or dict
    print(clients_api_data)  

    pdf = pd.DataFrame(rooms_api_data)
    tdf = pd.DataFrame(clients_api_data)

    # Feature engineering
    inner_merged_df = pd.merge(tdf,pdf, left_on='room_choice', right_on='room_type', how='left')
except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")

# Original shape before modification
print(f"Dataset shape before data cleaning: {inner_merged_df.shape}")

# Describe the dataset
print("Summary Statistics:")
print(inner_merged_df.describe(include='all'))  

print("\nColumn Info:")
print(inner_merged_df.info()) 

print("\nFirst Few Rows:")
print(inner_merged_df.head()) 


print("Null Values in Each Column:")
print(inner_merged_df.isnull().sum())

inner_merged_df['id_y'].fillna(0, inplace=True)
inner_merged_df['room_choice'].fillna('Unknown', inplace=True)
inner_merged_df['room_type'].fillna('Unknown', inplace=True)
inner_merged_df['room_description'].fillna('No description available', inplace=True)


print("\nNull Values After Replacement:")
print(inner_merged_df.isnull().sum())

# Data preprocessing
# Check for duplicate rows
duplicates = inner_merged_df[inner_merged_df.duplicated(subset=['first_name', 'last_name', 'email', 'phone_number', 'room_type', 'room_description'])]
print(f"Number of duplicate rows: {len(duplicates)}")
print(duplicates)

# Drop duplicate rows
inner_merged_df = inner_merged_df.drop_duplicates()

print("Duplicate rows removed.")
print(f"Dataset shape after removing duplicates: {inner_merged_df.shape}")

# Display the column names
print(f"Column names: \n {inner_merged_df.columns.tolist()}")

# plt.figure(figsize = (20, 5))
# sns.countplot(x='room_type', data=inner_merged_df.sort_values(by='room_type'), hue='room_type', palette='husl', legend=False)
# plt.grid(color="green", linestyle="--", linewidth=0.5)
# plt.title("Rooms with the highest number of books.", fontdict={"family": "serif", "color": "blue", "size": 20})
# plt.xticks(rotation=90) 
# plt.show()

# plt.figure(figsize = (15, 4))
# inner_merged_df['room_type'].value_counts().plot(kind = 'pie', autopct='%1.1f%%', startangle=90, legend=False)
# plt.title("The distribution of customer's choice", fontsize = 20)
# plt.show()

plt.figure(figsize=(20, 4))
chosen_by_clients = inner_merged_df['room_type'].value_counts().sort_values(ascending = True).plot(kind='barh', color='g')
plt.title("Customer Favorites", fontsize=20)
plt.xlabel("Room Choice", fontsize=15)
plt.ylabel("Room Types", fontsize=15)
plt.xticks(rotation=45) # Rotate x-tick labels for better visibility
plt.grid(color="green", linestyle="--", linewidth=0.5)
plt.show()

# plt.figure(figsize=(20, 3))
# # Create scatter plot for room_type
# sns.scatterplot(x='room_type', y='count', data=inner_merged_df, color='r', label='Selling Price', alpha=0.6)
# # Create scatter plot for count
# sns.scatterplot(x='count', y='room_type', data=inner_merged_df, color='b', label='Purchase Price', alpha=0.6)
# plt.title("Scatter Plot between Selling Price and Purchase Price", fontsize=20)
# plt.grid(color="green", linestyle="--", linewidth=0.5)
# plt.xlabel("Price", fontsize=15)
# plt.ylabel("Price", fontsize=15)
# plt.legend()
# plt.show()

# plt.figure(figsize=(20, 3))
# # Create the scatter plot for room_type vs. count
# sns.scatterplot(x='room_type', y='count', data=inner_merged_df, color='b', alpha=0.6)
# plt.title("Scatter Plot between Selling Price and Purchase Price", fontsize=20)
# plt.grid(color="green", linestyle="--", linewidth=0.5)
# plt.xlabel("Selling Price", fontsize=15)
# plt.ylabel("Purchase Price", fontsize=15)
# plt.show()

# plt.figure(figsize = (20, 3))
# numeric_columns = ['owner_age', 'room_type', 'count', 'year', 'kilometers_driven']
# heatmap_data = inner_merged_df[numeric_columns].corr()
# sns.heatmap(heatmap_data, cmap = 'BuPu', annot = True)
# plt.show()

