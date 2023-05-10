from langchain.tools import Tool
from services.agent_tools import AgentTool
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from streamlit.logger import get_logger

logger = get_logger(__name__)


class WhatCanDo(AgentTool):
    def __init__(self) -> None:
        super().__init__()

    def run(self, query: str, history=[]) -> str:
        message = "You are an AI assistant to help a tourism business. You are to show some relavant information, recommend places to visit and to eat, suggest activities to do nearby. Help plan user's itinerary. Also, should be able to pull some reviews."
        return message


what_it_can_do = WhatCanDo()

what_it_can_do_tool = Tool.from_function(
    func=what_it_can_do.run,
    name="What the chatbot can do",
    description="Give information what the chatbot can do"
    # coroutine= ... <- you can specify an async method if desired as well
)
