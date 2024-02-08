# Import necessary libraries
from dotenv import load_dotenv
import os
from openai import OpenAI
import pandas as pd
import json

# load OPEN_API_KEY from .env - Need Open API account and token for this
load_dotenv()
TOKEN = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client with API key
client = OpenAI(api_key=TOKEN)


# Define the prompt for data generation
prompt = '''I need a dataset with 15 rows that mimics car insurance data. 
I need the following columns: Policy_Id, Policy_Year, Make, Body_Style, Model_Year, Model_Color, Miles_Driven, Driver_Hair_Color, Years_Customer, Accident_Reported.
The column names are very important, and must be spelled that exact way.
Policy_Id is a unique id starting at one and incrementing upwards, 
Make is Honda, Nissan, Ford, or Subaru,
Body style is convertible, suv, sedan, or truck, 
Model_Year is a year between 2000 and 2023, 
Model_Color is Red, White, or Blue, 
Miles_Driven is between 1,000 and 25,000, 
Driver_Hair_Color is Brown or Black, 
Years_Customer is between 1 and 20, 
and Accident_Reported is either 0 or 1.
We want approximately 30 percent of records to have Accident_Reported as 1 and the rest 0.  
This is also a dataset for predictive modeling. We want the variables that are most likely to predict Accident_Reported as 1 
to be the following variables.  Driver_Hair_Color is extremely tied to Accident_Reported, 
Miles_Driven over 20,000 for trucks is highly predictive regardless of Driver_Hair_Color,
and lastly customers with more than 6 years never an accident'''

# Generate the data using OpenAI's chat model
completion = client.chat.completions.create(
  model="gpt-4-turbo-preview",
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "You are a helpful assistant that specializes in generating data. For your responses, please do not include any verbal response and just return a json of the data requested that can be easily parsed and consumed in python."},
    {"role": "user", "content": "Hello!  " + prompt}
  ]
)

# Extract the generated data from the completion object
response_data = completion.choices[0].message.content

# Convert the JSON string into a Python object
data_dict = json.loads(response_data)

# Extract the list of dictionaries from the "data" key
data_list = data_dict['data']

# Convert the list of dictionaries into a DataFrame
df = pd.DataFrame(data_list)

# Write file to csv for consumption
df.to_csv('./data/generated_data_openai.csv')

