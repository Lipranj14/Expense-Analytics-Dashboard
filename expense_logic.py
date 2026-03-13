import pandas as pd
import os

class ExpenseTracker:
    def __init__(self, filename="expenses.csv"):
        self.filename = filename
        self.columns = ["Date", "Category", "Amount", "Description"]
        self.load_data()

    def load_data(self):
        """Loads data from CSV or creates a new DataFrame if it doesn't exist."""
        if os.path.exists(self.filename):
            self.df = pd.read_csv(self.filename)
        else:
            self.df = pd.DataFrame(columns=self.columns)
            self.df.to_csv(self.filename, index=False)

    def add_expense(self, date, category, amount, description):
        """Adds a new expense to the DataFrame and saves to CSV."""
        new_expense = pd.DataFrame([[date, category, amount, description]], columns=self.columns)
        self.df = pd.concat([self.df, new_expense], ignore_index=True)
        self.df.to_csv(self.filename, index=False)

    def get_expenses_by_category(self):
        """Returns total expenses grouped by category."""
        if self.df.empty:
            return pd.DataFrame()
        return self.df.groupby("Category")["Amount"].sum().reset_index()

    def get_total_expenses(self):
        """Returns the total sum of all expenses."""
        if self.df.empty:
            return 0
        return self.df["Amount"].sum()

    def reset_data(self):
        """Clears all data and overwrites the CSV."""
        self.df = pd.DataFrame(columns=self.columns)
        self.df.to_csv(self.filename, index=False)
