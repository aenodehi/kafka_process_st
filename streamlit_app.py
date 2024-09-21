import streamlit as st
import pandas as pd

# Initialize an empty DataFrame
df = pd.DataFrame()

# Function to display DataFrame row by row
def display_dataframe(df):
    for index, row in df.iterrows():
        st.write(row)

# Main function to run the Streamlit app
def main():
    st.title('Kafka Streamlit App')
    st.write('Displaying DataFrame row by row')
    
    # Display the DataFrame
    display_dataframe(df)

if __name__ == '__main__':
    main()