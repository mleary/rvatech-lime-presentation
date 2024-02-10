import pandas as pd
import numpy as np

# Define the size of the dataset
size = 10000

# Define the columns of the dataset
columns = ['Policy_Id', 'Policy_Year', 'Make', 'Body_Style', 'Model_Year', 'Model_Color', 'Miles_Driven', 'Driver_Hair_Color', 'Years_Customer', 'Accident_Reported']

# Generate the dataset
df = pd.DataFrame(columns=columns)

df['Policy_Id'] = range(1, size + 1)
df['Policy_Year'] = np.random.choice(range(2000, 2024), size)
df['Make'] = np.random.choice(['Honda', 'Toyota', 'Subaru'], size)
df['Body_Style'] = np.random.choice(['sedan', 'suv', 'truck'], size)
df['Model_Year'] = np.random.choice(range(2000, 2024), size)
df['Model_Color'] = np.random.choice(['Red', 'White', 'Blue'], size)
df['Miles_Driven'] = np.random.choice(range(1000, 25001), size)
df['Driver_Hair_Color'] = np.random.choice(['Brown', 'Black'], size)
df['Years_Customer'] = np.random.choice(range(1, 21), size)

# Generate the Accident_Reported column based on the predictive columns
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def calculate_accident_reported(row):
    if row['Body_Style'] == 'truck' and row['Miles_Driven'] > 17500:
        return np.random.choice([1, 0], p=[0.65, 0.35])
    elif row['Years_Customer'] > 10:
        return np.random.choice([1, 0], p=[0.05, 0.95])
    elif row['Body_Style'] != 'truck' and row['Model_Color'] == "Blue":
        p_accident = sigmoid((row['Miles_Driven'] - 10000) / 5000)
        return np.random.choice([1, 0], p=[p_accident, 1 - p_accident])
    else:
        return np.random.choice([1, 0], p=[0.30, 0.70])

df['Accident_Reported'] = df.apply(calculate_accident_reported, axis=1)

# Write the dataset to a CSV file
df.to_csv('./data/generated_data_numpy.csv', index=False)
