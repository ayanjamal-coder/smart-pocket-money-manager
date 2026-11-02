import streamlit as st
import json
import os

# 1. Page Configuration
st.set_page_config(page_title="Smart Pocket Money Manager", page_icon="💰", layout="wide")

# JSON File ka naam
DATA_FILE = "expenses.json"

# 2. JSON File Se Data Load Karne Ka Function
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

# 3. JSON File Mein Data Save Karne Ka Function
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# 4. App Title & Description
st.title("💰 Smart Pocket Money Manager (JSON Powered)")
st.write("Apne daily kharche track karein. Aapka data permanent JSON file mein save rahega!")

# Data Load Karein
expenses = load_data()

# 5. Sidebar - Data Input Form
st.sidebar.header("➕ Add New Expense")
item_name = st.sidebar.text_input("Expense Name (e.g., Coffee, Books)")
amount = st.sidebar.number_input("Amount (PKR)", min_value=0.0, step=10.0)
category = st.sidebar.selectbox("Category", ["Food", "Travel", "Study", "Entertainment", "Other"])

if st.sidebar.button("Add Expense"):
    if item_name.strip() == "":
        st.sidebar.error("Barah-e-karam expense ka naam likhein!")
    else:
        new_entry = {
            "item": item_name,
            "amount": amount,
            "category": category
        }
        expenses.append(new_entry)
        save_data(expenses)
        st.sidebar.success("Expense successfully save ho gaya!")
        st.rerun()

# 6. Main Screen Dashboard
st.subheader("📊 Expense Overview")

if len(expenses) == 0:
    st.info("No expenses have been added yet. Use the sidebar to add your first expense!")
else:
    # Total Calculation using Python sum()
    total_spent = sum(item["amount"] for item in expenses)

    # Metrics Display
    col1, col2 = st.columns(2)
    col1.metric("Total Kharcha", f"Rs. {total_spent:,.2f}")
    col2.metric("Total Entries", len(expenses))

    # Data Table
    st.subheader("📋 Expense History (JSON Data)")
    st.dataframe(expenses, use_container_width=True)

    # Reset / Delete All Data Button
    if st.button("🗑️ Clear All Data"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        st.success("Saara data clear ho gaya!")
        st.rerun()