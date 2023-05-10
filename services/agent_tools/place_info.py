from langchain.tools import Tool
from services.agent_tools import AgentTool
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from streamlit.logger import get_logger
import json

logger = get_logger(__name__)


class PlaceInfo(AgentTool):
    def __init__(self) -> None:
        super().__init__()

    def run(self, query: str, history=[]) -> str:
        chat = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        system_prompt = open("resources/general_question_prompt.txt", "r").read()
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query),
        ]
        # result = chat(messages=messages)
        with open("data/basic_info.json", "r") as f:
            basic_info = json.load(f)

        basic_info_str = ""
        if "description" in basic_info:
            basic_info_str += (
                "Description:" + json.dumps(basic_info["description"]) + "\n"
            )
        if "address_obj" in basic_info:
            basic_info_str += "Address:" + json.dumps(basic_info["address_obj"]) + "\n"
        if "hours" in basic_info and "weekday_text" in basic_info["hours"]:
            basic_info_str += (
                "Opening hours:"
                + json.dumps(basic_info["hours"]["weekday_text"])
                + "\n"
            )

        return basic_info_str


place_info = PlaceInfo()

place_info_tool = Tool.from_function(
    func=place_info.run,
    name="Place Information",
    description="Can provide basic information about the tourism business such as opening hours, offering services, cancellation policy, address, traffic information etc."
    # coroutine= ... <- you can specify an async method if desired as well
)
