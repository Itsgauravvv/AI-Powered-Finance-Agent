# AI Powered Finance Agent 🤖

This is a full-stack AI-powered Finance Agent built with Python, the Agno framework, Gemini, and Streamlit. The agent serves two primary roles:

1.  **Stock Market Analyst**: Provides detailed analysis and insights for companies listed on the Indian National Stock Exchange (NSE).
2.  **Personal Finance Assistant**: Analyzes personal expense data from a CSV, answers budgeting questions, and offers savings advice.

## Tech Stack ⚙️

-   **Backend**: Python + Agno
-   **Frontend**: Streamlit
-   **LLM**: Google Gemini
-   **Data Tools**: `nsepython` for NSE data, LangChain + FAISS for financial memory.

## Setup Instructions 🚀

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd finance-agent
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install all the required Python packages.

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

You need a Google Gemini API key to run this application.

1.  Create a file named `.env` in the root of the project directory.
2.  Add your API key to this file:

    ```
    GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
    ```

## How to Run the App ▶️

Once the setup is complete, run the Streamlit application from your terminal:

```bash
streamlit run finance_agent_app.py
```

The application will open in your default web browser.

## Using the Agent 💡

### A. Stock Market Analyst

1.  Select the **"Stock Analyst"** role from the sidebar.
2.  Type your query into the chat input at the bottom of the screen.

**Sample Prompts:**

-   `Give me a market overview of INFY on NSE.`
-   `Show me the latest data for Reliance.`
-   `What's the news on HDFC Bank?`
-   `Analyze Tata Motors (TATAMOTORS).`

### B. Personal Finance Assistant

1.  Select the **"Personal Finance Assistant"** role from the sidebar.
2.  Upload a CSV file containing your transaction data. The CSV **must** have the columns: `Date`, `Description`, `Category`, `Amount`.
3.  Once the file is processed, you can ask questions about your finances.

**Sample CSV Data (`transactions.csv`):**

```csv
Date,Description,Category,Amount
2025-07-01,Zomato Order,Dining,450
2025-07-02,Big Bazaar Groceries,Groceries,2500
2025-07-03,Uber Ride to Office,Transport,220
2025-07-05,Electricity Bill,Utilities,1800
2025-07-05,Netflix Subscription,Entertainment,649
```

**Sample Prompts:**

-   `What are my biggest expenses this month?`
-   `Create a pie chart.`

