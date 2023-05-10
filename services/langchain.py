from langchain.chat_models import ChatOpenAI
from langchain import LLMChain, PromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage

import os
from dotenv import load_dotenv

load_dotenv()

from services.agent_tools.place_info import place_info_tool
from services.agent_tools.web_search import web_search_tool
from services.agent_tools.what_can_do import what_it_can_do_tool
from langchain.agents import AgentType, initialize_agent
from streamlit.logger import get_logger

logger = get_logger(__name__)

chat = ChatOpenAI(
    temperature=0,
    model_name="gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)
tools = [what_it_can_do_tool, place_info_tool, web_search_tool]

agent = initialize_agent(
    tools, chat, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)


def generate_response(message, user_history, generated_history):
    logger.info("Message: " + message)
    logger.info("User message: " + str(user_history))
    logger.info("Generated message: " + str(generated_history))

    # use agent
    result = agent(message)
    logger.info("Result: " + str(result))
    return result["output"]
