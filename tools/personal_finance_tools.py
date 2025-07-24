from langchain.tools import tool
import pandas as pd
import matplotlib.pyplot as plt
import io

# 🔹 Raw logic (for direct use in Streamlit)
def analyze_expenses_fn(df: pd.DataFrame) -> str:
    """Analyzes expenses and returns top 5 categories by amount."""
    if 'Category' not in df.columns or 'Amount' not in df.columns:
        return "Error: DataFrame must have 'Category' and 'Amount' columns for analysis."

    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df.dropna(subset=['Amount'], inplace=True)

    category_expenses = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)

    analysis = "Here are your largest expense categories:\n"
    for category, total in category_expenses.head(5).items():
        analysis += f"- {category}: ₹{total:,.2f}\n"

    return analysis

@tool
def analyze_expenses(df: pd.DataFrame) -> str:
    """Tool: Analyzes a DataFrame with 'Category' and 'Amount' columns."""
    return analyze_expenses_fn(df)

# 🔹 Raw logic
def create_expense_pie_chart_fn(df: pd.DataFrame) -> str:
    """Generates a pie chart of expense categories and returns a confirmation message."""
    if 'Category' not in df.columns or 'Amount' not in df.columns:
        return "Error: DataFrame must have 'Category' and 'Amount' columns for chart."

    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df.dropna(subset=['Amount'], inplace=True)

    category_expenses = df.groupby('Category')['Amount'].sum()

    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(category_expenses, labels=category_expenses.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title('Expense Distribution by Category')

    return fig

@tool
def create_expense_pie_chart(df: pd.DataFrame) -> str:
    """Tool: Creates a pie chart of expenses by category from a DataFrame."""
    return create_expense_pie_chart_fn(df)

personal_finance_tools = [
    analyze_expenses,
    create_expense_pie_chart,
]
