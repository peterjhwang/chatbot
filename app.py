import openai
from uuid import uuid4 as uuid
import streamlit as st
from streamlit_chat import message
from services.langchain import generate_response
from streamlit.logger import get_logger

logger = get_logger(__name__)

st.set_page_config(page_title="Connectour", page_icon=":robot:")
st.title("Connectour")

# Create an empty container for the input box
input_box_placeholder = st.empty()

# Storing the chat
if "generated" not in st.session_state:
    st.session_state["generated"] = [
        "Welcome to Connectour! I'm your virtual tour guide. Ask me anything I'll try my best to answer you."
    ]

if "past" not in st.session_state:
    st.session_state["past"] = ["Hi"]


# We will get the user's input by calling the get_text function
def get_text():
    input_text = input_box_placeholder.text_input("You", "", key="input")
    return input_text


user_input = get_text()

if user_input and user_input != "":
    output = generate_response(
        user_input, st.session_state["past"], st.session_state["generated"]
    )
    # store the output
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)
    # logger.info("Output:\n" + str(st.session_state))


if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
