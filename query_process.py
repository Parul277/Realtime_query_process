import streamlit as st
import pandas as pd
import os
import pandas as pd
from scipy import stats
from PIL import Image
import numpy as np
from langchain_experimental.agents import create_csv_agent
from langchain_openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DEPLOYMENT = os.getenv('DEPLOYMENT')
OPENAI_API_VERSION = os.getenv('OPENAI_API_VERSION')
SERVICE_LINE = os.getenv('SERVICE_LINE')
BRAND = os.getenv('BRAND')
PROJECT = os.getenv('PROJECT')
AZURE_OPENAI_ENDPOINT = os.getenv('END_POINT')

openai_headers = {
        'x-service-line': SERVICE_LINE,
        'x-brand': BRAND,
        'x-project': PROJECT,
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'api-version': 'v10',
        'Ocp-Apim-Subscription-Key': OPENAI_API_KEY,
    }
client = AzureOpenAI(
    api_key = OPENAI_API_KEY,
    api_version = OPENAI_API_VERSION,
    azure_endpoint = AZURE_OPENAI_ENDPOINT,
    azure_deployment = "GPT35TurboInstruct4k",
    default_headers = openai_headers
)
def clean_dynamic_csv(df):
    # Iterate over each column and apply cleaning based on data type
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            print(f"Cleaning numeric column: {col}")
            # Handling missing values by filling with the mean
            df[col] = df[col].fillna(df[col].mean())

            # Detect and remove outliers using Z-score (outliers are Z > 3)
            z_scores = np.abs(stats.zscore(df[col].dropna()))
            df = df[z_scores < 3]  # Remove rows with outliers

        elif isinstance(df[col].dtype, pd.CategoricalDtype) or pd.api.types.is_object_dtype(df[col]):
            print(f"Cleaning categorical/text column: {col}")
            # Fill missing categorical/text values with the mode (most frequent value)
            df[col] = df[col].fillna(df[col].mode()[0])

            # Optional: Further process categorical columns if needed
            df[col] = df[col].astype('category')

        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            print(f"Cleaning datetime column: {col}")
            # Handle missing datetime values (e.g., fill with earliest date or drop)
            df[col] = df[col].fillna(df[col].min())

        else:
            print(f"Column {col} has an unrecognized data type. Skipping...")
    
    return df

# Step 3: Save cleaned CSV
def save_cleaned_csv(df, cleaned_file_path):
    df.to_csv(cleaned_file_path, index=False)
    print(f"Cleaned data saved to: {cleaned_file_path}")

def run_langchain_agent(client, cleaned_file_path):
    # Pass the cleaned CSV to the LangChain agent
    agent = create_csv_agent(client, cleaned_file_path, verbose=True, allow_dangerous_code=True)
    
    # Example query after loading the data
    query = "what was count of different Embarked?"
    response = agent.run(query)
    print(response)

# Main function to handle the CSV processing and querying
def process_and_query_csv(df, cleaned_file_path, client):
    # Load the CSV
    #df = load_csv(file_path)
    
    # Clean the CSV
    cleaned_df = clean_dynamic_csv(df)
    
    # Save the cleaned CSV
    save_cleaned_csv(cleaned_df, cleaned_file_path)
    
    # Run LangChain agent on cleaned data
  #  run_langchain_agent(client, cleaned_file_path)


# Load the image
logo = Image.open("logo.png")

# Display the logo using st.image and use markdown for positioning it to the top right
st.markdown(
    """
    <style>
    .top-right-logo {
        position: absolute;
        top: 10px;
        right: 100px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the logo using st.image in the top-right corner
st.image(logo, width=100, output_format="PNG")
# Set title for the app
# Add custom CSS to style the border
st.markdown("""
    <style>
        .title {
            border: 2px solid #000;
            padding: 10px;
            font-size: 24px;
            text-align: left;
        }
        .file-uploader {
            border: 2px solid #000;
            padding: 20px;
            margin-top: 10px;
            font-size: 18px;
            display: block;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Title with border
st.markdown('<div class="title">Upload your CSV to start chat</div>', unsafe_allow_html=True)

# Create a file uploader with a border
uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="csv_uploader")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    cleaned_csv_file_path = 'cleaned_data.csv'  # Path where cleaned data will be saved

   
    # Process and query the CSV dynamically
    process_and_query_csv(df, cleaned_csv_file_path, client)

    
    # Display the DataFrame
    #st.write("Here is your CSV file content:")
    question=st.text_area("Question")
    if question:
           # Pass the cleaned CSV to the LangChain agent
        agent = create_csv_agent(client, cleaned_csv_file_path, verbose=True, allow_dangerous_code=True)
        
        # Example query after loading the data
        #query = "what was count of different Embarked?"
       # query=question
        response = agent.run(question)
        #print(response)
        st.write(response)
        
    #st.dataframe(df)
else:
    st.write("Please upload a CSV file to display its content.")

if uploaded_file is not None:
  # Path to the file on your system
    file_path_cleaned = 'cleaned_data.csv'

    # Open the file in binary mode and read its content
    with open(file_path_cleaned, 'rb') as file:
        file_data = file.read()

    # Display a download button
    st.write("Download the cleaned data file below:")
    st.download_button(
        label="Download cleaned_data.csv",
        data=file_data,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

