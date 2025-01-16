import sqlite3
import streamlit as st

# Database file
DATABASE = "surfactants.db"

# Utility function to connect to the database
def get_db_connection():
    return sqlite3.connect(DATABASE)

# Function to create the database and table
def initialize_database():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS surfactants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        cmc REAL,
        cloud_point REAL,
        hlb REAL,
        eo_content REAL,
        surface_tension REAL,
        foam_height TEXT,
        pour_point REAL,
        form TEXT,
        features TEXT,
        applications TEXT
    );
    """)
    connection.commit()
    connection.close()

# Function to fetch all surfactants
def fetch_surfactants():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM surfactants;")
    rows = cursor.fetchall()
    connection.close()
    return rows

# Function to add a new surfactant
def add_surfactant(data):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO surfactants (product_name, cmc, cloud_point, hlb, eo_content, surface_tension, foam_height, pour_point, form, features, applications)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, data)
    connection.commit()
    connection.close()

# Function to delete a surfactant by ID
def delete_surfactant(surfactant_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM surfactants WHERE id = ?;", (surfactant_id,))
    connection.commit()
    connection.close()

# Streamlit app
st.title("Surfactant Database")
st.markdown("""
Welcome to the **Surfactant Database** app. This tool allows you to manage and explore surfactant data. 
You can:
- **View existing surfactants** in the database.
- **Add new surfactants** by providing relevant details.
- **Delete surfactants** that are no longer needed.

Use the menu on the left to navigate through the app.
""")

# Initialize database
initialize_database()

# Sidebar navigation
menu = st.sidebar.selectbox("Menu", ["View Surfactants", "Add Surfactant", "Delete Surfactant"])

if menu == "View Surfactants":
    st.subheader("View All Surfactants")
    st.markdown("This section lists all the surfactants currently stored in the database.")
    surfactants = fetch_surfactants()
    if surfactants:
        for row in surfactants:
            st.write(f"**ID**: {row[0]}")
            st.write(f"**Product Name**: {row[1]}")
            st.write(f"**CMC (Critical Micelle Concentration)**: {row[2]}")
            st.write(f"**Cloud Point**: {row[3]}")
            st.write(f"**HLB (Hydrophilic-Lipophilic Balance)**: {row[4]}")
            st.write(f"**EO Content**: {row[5]}")
            st.write(f"**Surface Tension**: {row[6]}")
            st.write(f"**Foam Height**: {row[7]}")
            st.write(f"**Pour Point**: {row[8]}")
            st.write(f"**Form**: {row[9]}")
            st.write(f"**Features**: {row[10]}")
            st.write(f"**Applications**: {row[11]}")
            st.write("---")
    else:
        st.info("No surfactants found in the database.")

elif menu == "Add Surfactant":
    st.subheader("Add a New Surfactant")
    st.markdown("Fill in the fields below to add a new surfactant to the database.")
    product_name = st.text_input("**Product Name** (Required)", help="The name of the surfactant (e.g., TRITON™ X-100).")
    cmc = st.text_input("CMC", help="Critical Micelle Concentration (ppm).")
    cloud_point = st.text_input("Cloud Point", help="The temperature at which the surfactant becomes insoluble.")
    hlb = st.text_input("HLB", help="Hydrophilic-Lipophilic Balance.")
    eo_content = st.text_input("EO Content", help="Ethylene Oxide Content.")
    surface_tension = st.text_input("Surface Tension", help="Surface tension reduction capability (mN/m).")
    foam_height = st.text_input("Foam Height", help="Foam height, e.g., '50/40' (initial/5 min).")
    pour_point = st.text_input("Pour Point", help="Temperature at which the surfactant flows.")
    form = st.text_input("Form", help="Physical state (e.g., Liquid, Solid).")
    features = st.text_area("Features", help="Key features of the surfactant (e.g., detergency, stability).")
    applications = st.text_area("Applications", help="Applications for the surfactant (e.g., coatings, detergents).")

    if st.button("Add Surfactant"):
        if product_name:
            data = (
                product_name,
                float(cmc) if cmc else None,
                float(cloud_point) if cloud_point else None,
                float(hlb) if hlb else None,
                float(eo_content) if eo_content else None,
                float(surface_tension) if surface_tension else None,
                foam_height if foam_height else None,
                float(pour_point) if pour_point else None,
                form if form else None,
                features if features else None,
                applications if applications else None,
            )
            add_surfactant(data)
            st.success(f"Surfactant '{product_name}' added successfully!")
        else:
            st.error("Product Name is required!")

elif menu == "Delete Surfactant":
    st.subheader("Delete a Surfactant")
    st.markdown("Enter the ID of the surfactant you want to delete.")
    surfactants = fetch_surfactants()
    if surfactants:
        surfactant_id = st.number_input("Enter Surfactant ID", min_value=1, step=1, help="ID of the surfactant to delete.")
        if st.button("Delete Surfactant"):
            delete_surfactant(surfactant_id)
            st.success(f"Surfactant with ID {surfactant_id} deleted successfully!")
    else:
        st.info("No surfactants found in the database.")
