from langchain.tools import Tool
from services.agent_tools import AgentTool
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from streamlit.logger import get_logger
from duckduckgo_search import ddg
import json
import requests
from bs4 import BeautifulSoup
import tiktoken
from func_timeout import func_timeout

logger = get_logger(__name__)

enc = tiktoken.get_encoding("gpt2")


class WebSearch(AgentTool):
    def __init__(self) -> None:
        super().__init__()

    def run(self, query: str, history=[]) -> str:
        chat = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        system_prompt = open("resources/web_search_prompt.txt", "r").read()
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query),
        ]
        search_keywords = chat(messages=messages).content

        region_keywords = ""
        with open("data/basic_info.json", "r") as f:
            basic_info = json.load(f)
        address_info = basic_info["address_obj"]
        if "city" in address_info:
            region_keywords += " " + address_info["city"]
        if "state" in address_info:
            region_keywords += " " + address_info["state"]
        if "country" in address_info:
            region_keywords += " " + address_info["country"]
        search_keywords += region_keywords
        logger.info("Search keywords: " + str(search_keywords))
        search_results = ddg(search_keywords, max_results=10)

        # search result prompt
        search_result_prompt = open("resources/search_result_prompt.txt", "r").read()
        search_result_prompt = search_result_prompt.replace("{{query}}", query)
        for result in search_results:
            logger.info("Search result: " + str(result))
            relevance_check = chat(
                messages=[
                    SystemMessage(content=search_result_prompt),
                    HumanMessage(content="Search result:" + result["body"]),
                ]
            )

            if "yes" in relevance_check.content.lower():
                # web search prompt
                url = result["href"]
                logger.info("URL:" + url)
                # Make a GET request to the URL
                try:
                    response = func_timeout(10, requests.get, args=(url,))

                    # Parse the HTML content using BeautifulSoup
                    soup = BeautifulSoup(response.content, "html.parser")

                    # Extract all the text from the HTML content
                    texts = soup.get_text()
                except:
                    continue

                # cut
                if len(enc.encode(texts)) > 3500:
                    texts = enc.decode(enc.encode(texts)[:3500])
                if len(texts) < 300:
                    continue

                summary_prompt = open(
                    "resources/summarise_answer_query.txt", "r"
                ).read()
                summary_prompt = summary_prompt.replace("{{query}}", query)
                return chat(
                    messages=[
                        SystemMessage(content=summary_prompt),
                        HumanMessage(content=texts),
                    ]
                )

        return "Sorry, I can't find the answer for you."


web_search = WebSearch()

web_search_tool = Tool.from_function(
    func=web_search.run,
    name="Region or Country Information",
    description="Can give some travel infomation in the region and country from web search."
    # coroutine= ... <- you can specify an async method if desired as well
)
