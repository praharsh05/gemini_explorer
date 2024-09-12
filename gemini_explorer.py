import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

project = 'gemini-explorer-435321'
vertexai.init(project=project)

config = generative_models.GenerationConfig(
    temperature=0.4
)
# Load Model with config
model = GenerativeModel(
    'gemini-1.5-flash-001',
    generation_config=config
)

chat = model.start_chat()

# Helper function to display and send streamlit messages


def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    with st.chat_message("model"):
        st.markdown(output)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )
    st.session_state.messages.append(
        {
            "role": "model",
            "content": output
        }
    )


st.title("Gemini Explorer")

# Initialise chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display and load to chat history
for index, message in enumerate(st.session_state.messages):
    content = Content(
        role=message["role"],
        parts=[Part.from_text(message["content"])]
    )

    chat.history.append(content)

# Capture user's name
# user_name = st.text_input("Please enter your name")
# Display the captured name
# st.write("Hello, " + user_name + "!")
# For capture user input
query = st.chat_input("Gemini Flights")

if len(st.session_state.messages) == 0:
    user_name = st.text_input("Please enter your name")
    if user_name:
        initial_prompt = f"Hey {user_name}! Introduce yourself as ReX, an assistant powered by Google Gemini. You use emojis to be interactive"
        llm_function(chat, initial_prompt)

if query:
    with st.chat_message("user"):
        st.markdown(query)

    response = llm_function(chat, query)
    chat.history.append(query)
    chat.history.append(response)
