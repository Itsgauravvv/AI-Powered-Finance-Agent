from tools.nse_tools import get_stock_market_overview
from tools.personal_finance_tools import (
    analyze_expenses_fn, create_expense_pie_chart_fn,
    analyze_expenses, create_expense_pie_chart  # still used by agent
)
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from agent.agent_config import create_agent

load_dotenv()

st.set_page_config(page_title="AI Powered Finance Agent", page_icon="📈", layout="wide")

if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'agent_role' not in st.session_state:
    st.session_state.agent_role = "Stock Analyst"

st.title("AI Finance Agent 💰")

with st.sidebar:
    st.header("Select Agent Role 👇")
    st.markdown("""Choose the role of the AI agent you want to interact with:
    """)
    

    if st.button("Stock Market Analyst", use_container_width=True):
        if st.session_state.agent_role != "Stock Analyst":
            st.session_state.agent_role = "Stock Analyst"
            st.session_state.agent = create_agent("Stock Analyst")
            st.session_state.messages = []

    if st.button("Personal Finance Assistant", use_container_width=True):
        if st.session_state.agent_role != "Personal Finance Assistant":
            st.session_state.agent_role = "Personal Finance Assistant"
            st.session_state.agent = create_agent("Personal Finance Assistant")
            st.session_state.messages = []


if st.session_state.agent_role == "Stock Analyst":
    st.header("Stock Market Analyst (NSE)")
    st.markdown("""
    Welcome to the **Stock Market Analyst Dashboard**. Here, you can:
    - 📈 Get an overview of popular stocks on the NSE
    - 🏦 Analyze individual stock performance (e.g., `Give me a market overview of INFY on NSE`)
    - 📊 View 52-week highs/lows, P/E ratios, and market caps
    ### 💡 Example Prompts You Can Try:
    - _"Give me a market overview of TCS on NSE"_
    - _"Show me the stock data for RELIANCE"_
    
    
    """)
    st.info("Tip: You can type your query in natural language — no command syntax required!")


    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("e.g., Give me a market overview of INFY on NSE"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_content = ""
                if "market overview" in prompt.lower() and "nse" in prompt.lower():
                    words = prompt.upper().split()
                    known_symbols = ["INFY", "TCS", "RELIANCE", "HDFCBANK", "ICICIBANK", "SBIN", "ITC", "WIPRO", "AXISBANK", "LT", "KOTAKBANK"]
                    possible_symbol = next((word for word in words if word in known_symbols), None)
                    if possible_symbol:
                        data = get_stock_market_overview(possible_symbol)
                        if "error" in data:
                            response_content = data["error"]
                        else:
                            response_content = (
                                f"**Company Name:** {data['Company Name']}\n\n"
                                f"**Symbol:** {data['Symbol']}\n\n"
                                f"**Current Price:** ₹{data['Current Price']}\n\n"
                                f"**Change:** ₹{data['Change']} ({data['% Change']}%)\n\n"
                                f"**52 Week High:** ₹{data['52 Week High']}\n\n"
                                f"**52 Week Low:** ₹{data['52 Week Low']}\n\n"
                                f"**Market Cap (Cr):** {data['Market Cap (Cr)']}\n\n"
                                f"**P/E Ratio:** {data['P/E Ratio']}"
                            )
                    else:
                        response_content = "Please specify a valid NSE stock symbol like INFY or RELIANCE."
                else:
                    run_response = st.session_state.agent.run(prompt)
                    response_content = run_response.content

                st.markdown(response_content)

        st.session_state.messages.append({"role": "assistant", "content": response_content})

else:
    st.header("Personal Finance Assistant (Budget & Expense Tracker)")
    st.markdown("""
Welcome to the **Personal Finance Assistant**. Upload your expense data and get instant insights on your spending habits!

### Here's What You Can Do:
- 🔍 _Analyze your expenses_ to see where most of your money goes.
- 📊 _Generate pie charts_ to visualize your spending by category.
- 💡 _Ask financial questions_ like:
    - "What's my biggest expense category?"
    - "Can you create a pie chart of my expenses?"
    - "How much did I spend on entertainment?"

###  CSV Format Expected:
Make sure your CSV has these columns:
- `Date`
- `Category`
- `Amount`
- `Description`

Example:

| Date       | Category     | Amount | Description              |
|------------|--------------|--------|--------------------------|
| 2025-07-01 | Groceries    | 3200   | Monthly grocery shopping |
| 2025-07-02 | Utilities    | 1800   | Electricity & water bills |


Once uploaded, feel free to chat below using simple natural language prompts!
""")


    uploaded_file = st.file_uploader("Upload your expense CSV", type=["csv"])
    df = None
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("CSV uploaded successfully!")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Failed to read CSV: {e}")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("e.g., Analyze my expenses from this CSV"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):

                response_content = ""

                if df is not None:
                    prompt_lower = prompt.lower()
                    if any(kw in prompt_lower for kw in ["analyze", "summary", "spending", "expenses"]):
                        response_content = analyze_expenses_fn(df)
                    
                    elif any(kw in prompt_lower for kw in ["chart", "visual", "pie"]):
                        fig = create_expense_pie_chart_fn(df)
                        if isinstance(fig, str):  # Error string
                            response_content = fig
                            st.markdown(response_content)
                        else:
                            st.pyplot(fig)  # Show chart
                            response_content = "Here is your pie chart!"
                    else:
                        response = st.session_state.agent.run(prompt)
                        response_content = response.content
                else:
                    response_content = "Please upload your CSV file first before requesting analysis."

                st.markdown(response_content)

        st.session_state.messages.append({"role": "assistant", "content": response_content})
