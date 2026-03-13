import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from expense_logic import ExpenseTracker

# Initialize the tracker (This loads our OOP Pandas logic!)
tracker = ExpenseTracker()

# Set up the aesthetic of the page
st.set_page_config(page_title="Expense Tracker", page_icon="💸", layout="wide")

st.title("💸 Personal Expense Analytics Dashboard")
st.markdown("Track and visualize your daily expenses. This dashboard demonstrates Exploratory Data Analysis (EDA) using Pandas, Seaborn, and Matplotlib.")

# Sidebar for user inputs
st.sidebar.header("Add New Expense")
with st.sidebar.form("expense_form", clear_on_submit=True):
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food", "Transport", "Utilities", "Entertainment", "Shopping", "Other"])
    amount = st.number_input("Amount (in Rs/USD)", min_value=0.0, format="%.2f")
    description = st.text_input("Description")
    
    submitted = st.form_submit_button("Add Expense")
    if submitted:
        if amount > 0:
            tracker.add_expense(date, category, amount, description)
            st.success("Expense added successfully!")
            # Rerun to update the data automatically
            st.rerun()
        else:
            st.error("Please enter an amount greater than 0.")

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Reset All Data", type="primary"):
    tracker.reset_data()
    st.sidebar.success("All data cleared!")
    st.rerun()

# Main dashboard area
col1, col2 = st.columns([1, 1]) # Split the screen into two equal columns

with col1:
    st.subheader("📊 Your Expense Data")
    # Show the Pandas DataFrame natively in Streamlit
    st.dataframe(tracker.df, use_container_width=True)
    
    # Calculate and show a metric
    total = tracker.get_total_expenses()
    st.metric(label="Total Expenses", value=f"₹{total:.2f}")

with col2:
    st.subheader("📈 Spending Analysis (EDA)")
    category_data = tracker.get_expenses_by_category()
    
    if not category_data.empty:
        # Create a Seaborn Bar chart
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=category_data, x="Category", y="Amount", palette="viridis", ax=ax)
        ax.set_title("Total Expenses by Category")
        plt.xticks(rotation=45)
        st.pyplot(fig) # Render Matplotlib/Seaborn inside Streamlit
        
        st.markdown("---") # Divider
        
        # Create a Matplotlib Pie chart
        fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
        
        # Use a nice seaborn color palette for the pie chart
        colors = sns.color_palette("pastel")[0:len(category_data)]
        ax_pie.pie(category_data["Amount"], labels=category_data["Category"], autopct='%1.1f%%', startangle=90, colors=colors)
        ax_pie.axis('equal') # Equal aspect ratio ensures circular pie chart
        ax_pie.set_title("Spending Distribution")
        st.pyplot(fig_pie)
    else:
        st.info("No expenses added yet. Add some data from the sidebar to see the visualizations!")
