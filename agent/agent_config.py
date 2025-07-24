import os
from agno.agent import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
from types import SimpleNamespace
from datetime import datetime

from tools.nse_tools import stock_analyst_tools
from tools.personal_finance_tools import personal_finance_tools # Assuming this is also simplified

load_dotenv()

class AgnoLLMWrapper:
    def __init__(self, llm_instance, llm_id: str, provider_name: str):
        self._llm = llm_instance
        self.id = llm_id
        self.provider = provider_name
        self.assistant_message_role = "assistant"

    def __deepcopy__(self, memo):
        return AgnoLLMWrapper(self._llm, self.id, self.provider)

    def response(self, messages=None, **kwargs):
        if not messages:
            return SimpleNamespace(
                content="", tool_executions=[], tools=[], thinking=None, redacted_thinking=None, 
                citations=None, audio=None, image=None, created_at=datetime.utcnow()
            )

        langchain_messages = []
        for agno_msg in messages:
            role = str(getattr(agno_msg, 'role', 'user')).lower()
            content = str(getattr(agno_msg, 'content', ''))
            if role == 'user':
                langchain_messages.append(HumanMessage(content=content))
            elif role in ['assistant', 'agent']:
                langchain_messages.append(AIMessage(content=content))
            elif role == 'system':
                langchain_messages.append(SystemMessage(content=content))

        ai_message_response = self._llm.invoke(input=langchain_messages)
        llm_content = ai_message_response.content
        
        tool_list = []
        if hasattr(ai_message_response, 'tool_calls') and ai_message_response.tool_calls:
            for lc_tool_call in ai_message_response.tool_calls:
                agno_tool_call = SimpleNamespace(
                    tool_name=lc_tool_call.get('name'),
                    tool_args=lc_tool_call.get('args'),
                    is_paused=False
                )
                tool_list.append(agno_tool_call)
            
        return SimpleNamespace(
            content=llm_content, tool_executions=tool_list, tools=tool_list, thinking=None, 
            redacted_thinking=None, citations=None, audio=None, image=None, created_at=datetime.utcnow()
        )

    def __getattr__(self, name: str):
        return getattr(self._llm, name)

original_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

gemini_llm_wrapped = AgnoLLMWrapper(
    llm_instance=original_llm,
    llm_id="gemini-1.5-flash-latest",
    provider_name="google"
)

stock_analyst_system_message = "You are a data-driven Stock Market Analyst agent. Your ONLY way to access financial data is by using the tools you have been given. You have no prior knowledge. When a user asks for information about a stock, you MUST call the correct tool. NEVER apologize or say you cannot access real-time data. After the tool returns the real data, you MUST use that data to synthesize a concise, well-structured report in Markdown format."
personal_finance_system_message = "You are a friendly and encouraging Personal Finance & Budgeting Assistant..."

def create_agent(role: str = "Stock Analyst") -> Agent:
    if role == "Stock Analyst":
        # Note: We are not pre-binding tools here for Agno
        return Agent(
            model=gemini_llm_wrapped,
            tools=stock_analyst_tools,
            system_message=stock_analyst_system_message
        )
    else:
        # This part has not been debugged and will likely require similar effort
        return Agent(
            model=gemini_llm_wrapped,
            tools=personal_finance_tools, # Placeholder
            system_message=personal_finance_system_message
        )