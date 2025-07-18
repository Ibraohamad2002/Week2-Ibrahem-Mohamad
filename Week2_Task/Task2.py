import os
import streamlit as st
import pandas as pd

FOLDER = 'All Data - Ibrahem Mohamad'
os.makedirs(FOLDER, exist_ok=True)

st.set_page_config(page_title="Excel Manager", layout="wide")
st.title("📊 Excel Data Manager - Warehouse System")

# Display all Excel files in the folder
files = [f for f in os.listdir(FOLDER) if f.endswith('.xlsx')]
selected_file = st.selectbox("📂 Select Excel File", ["Select a file..."] + files)

# Create a new Excel file
st.subheader("Create New Excel File")
new_filename = st.text_input("Enter new file name (without .xlsx):")
if st.button("Create File"):
    if new_filename:
        path = os.path.join(FOLDER, f"{new_filename}.xlsx")
        if not os.path.exists(path):
            df_empty = pd.DataFrame(columns=["Product", "Quantity", "Amount", "Weight", "Product Serial Number", "Product Supplier"])
            df_empty.to_excel(path, index=False)
            st.success(f"File created successfully: {new_filename}.xlsx")
        else:
            st.warning("File already exists.")
    else:
        st.error("Please enter a file name.")

# Open and display file contents
if selected_file != "Select a file...":
    file_path = os.path.join(FOLDER, selected_file)
    df = pd.read_excel(file_path)
    st.subheader(f"Contents of {selected_file}")
    st.dataframe(df, use_container_width=True)

    # Add a row
    st.subheader("Add Row")
    with st.form("add_row_form"):
        new_data = {
            "Product": st.text_input("Product"),
            "Quantity": st.number_input("Quantity", min_value=0),
            "Amount": st.number_input("Amount", min_value=0.0),
            "Weight": st.number_input("Weight", min_value=0.0),
            "Product Serial Number": st.text_input("Product Serial Number"),
            "Product Supplier": st.text_input("Product Supplier"),
        }
        submitted = st.form_submit_button("Add Row")
        if submitted:
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_excel(file_path, index=False)
            st.success("Row added successfully.")

    # Edit a row
    st.subheader("Edit Row")
    row_to_edit = st.number_input("Enter row number to edit (starts at 0)", min_value=0, max_value=len(df)-1)
    with st.form("edit_row_form"):
        edited_data = {
            "Product": st.text_input("Product (Edit)", value=str(df.loc[row_to_edit, "Product"])),
            "Quantity": st.number_input("Quantity (Edit)", value=int(df.loc[row_to_edit, "Quantity"])),
            "Amount": st.number_input("Amount (Edit)", value=float(df.loc[row_to_edit, "Amount"])),
            "Weight": st.number_input("Weight (Edit)", value=float(df.loc[row_to_edit, "Weight"])),
            "Product Serial Number": st.text_input("Product Serial Number (Edit)", value=str(df.loc[row_to_edit, "Product Serial Number"])),
            "Product Supplier": st.text_input("Product Supplier (Edit)", value=str(df.loc[row_to_edit, "Product Supplier"])),
        }
        update = st.form_submit_button("Update Row")
        if update:
            for key in edited_data:
                df.at[row_to_edit, key] = edited_data[key]
            df.to_excel(file_path, index=False)
            st.success("Row updated successfully.")

    # Delete a row
    st.subheader("Delete Row")
    row_to_delete = st.number_input("Enter row number to delete", min_value=0, max_value=len(df)-1, key="delete_input")
    if st.button("Delete Row"):
        df = df.drop(index=row_to_delete).reset_index(drop=True)
        df.to_excel(file_path, index=False)
        st.success("Row deleted successfully.")

    # Delete the entire file
    st.subheader("Delete Entire File")
    if st.button("Delete File"):
        os.remove(file_path)
        st.success("File deleted successfully.")
        st.experimental_rerun()

# Create specific file: Warehouse Number One
st.subheader("Create 'Warehouse Number One'")
if st.button("Create Warehouse File"):
    path = os.path.join(FOLDER, "Warehouse Number One.xlsx")
    columns = ["Product", "Quantity", "Amount", "Weight", "Product Serial Number", "Product Supplier"]
    df_warehouse = pd.DataFrame(columns=columns)
    df_warehouse.to_excel(path, index=False)
    st.success("'Warehouse Number One.xlsx' created successfully.")

