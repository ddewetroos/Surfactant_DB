import os
import pandas as pd
import requests
import streamlit as st

# GitHub Repository Configuration
GITHUB_CSV_URL = "https://raw.githubusercontent.com/ddewetroos/Surfactant_DB/main/surfactants.csv"
LOCAL_CSV = "surfactors.csv"

# Function to download the CSV file from GitHub if not available locally
def download_csv():
    if not os.path.exists(LOCAL_CSV):
        st.info("Downloading CSV file from GitHub...")
        try:
            response = requests.get(GITHUB_CSV_URL)
            response.raise_for_status()
            with open(LOCAL_CSV, "wb") as f:
                f.write(response.content)
            st.success("CSV file downloaded successfully.")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to download CSV file: {e}")
            raise

# Load the CSV file into a Pandas DataFrame
def load_csv():
    try:
        return pd.read_csv(LOCAL_CSV)
    except Exception as e:
        st.error(f"Failed to load CSV file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# Save the DataFrame back to the CSV file
def save_csv(df):
    try:
        df.to_csv(LOCAL_CSV, index=False)
        st.success("Changes saved successfully.")
    except Exception as e:
        st.error(f"Failed to save CSV file: {e}")

# Streamlit app
st.title("Surfactant CSV Manager")
st.markdown("""
This application fetches and manages surfactant data from a CSV file hosted on GitHub.
""")

# Ensure the CSV file is available
try:
    download_csv()
except Exception:
    st.stop()

# Load the data
df = load_csv()

# Sidebar navigation
menu = st.sidebar.selectbox("Menu", ["View Data", "Add Data", "Delete Data", "Save Changes"])

if menu == "View Data":
    st.subheader("View Surfactants Data")
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No data found in the CSV file.")

elif menu == "Add Data":
    st.subheader("Add a New Surfactant")
    product_name = st.text_input("Product Name")
    cmc = st.text_input("CMC")
    cloud_point = st.text_input("Cloud Point")
    hlb = st.text_input("HLB")
    eo_content = st.text_input("EO Content")
    surface_tension = st.text_input("Surface Tension")
    foam_height = st.text_input("Foam Height")
    pour_point = st.text_input("Pour Point")
    form = st.text_input("Form")
    features = st.text_area("Features")
    applications = st.text_area("Applications")
    if st.button("Add Surfactant"):
        if product_name:
            new_row = {
                "Product Name": product_name,
                "CMC": cmc,
                "Cloud Point": cloud_point,
                "HLB": hlb,
                "EO Content": eo_content,
                "Surface Tension": surface_tension,
                "Foam Height": foam_height,
                "Pour Point": pour_point,
                "Form": form,
                "Features": features,
                "Applications": applications,
            }
            df = df.append(new_row, ignore_index=True)
            save_csv(df)
        else:
            st.error("Product Name is required!")

elif menu == "Delete Data":
    st.subheader("Delete a Surfactant")
    if not df.empty:
        row_index = st.number_input("Enter the row index to delete", min_value=0, max_value=len(df)-1, step=1)
        if st.button("Delete Surfactant"):
            if 0 <= row_index < len(df):
                df = df.drop(index=row_index).reset_index(drop=True)
                save_csv(df)
            else:
                st.error("Invalid row index.")
    else:
        st.info("No data found to delete.")

elif menu == "Save Changes":
    st.subheader("Save Changes to CSV")
    save_csv(df)
