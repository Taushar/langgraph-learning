import streamlit as st
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import operator     
import math
from langgraph.checkpoint.memory import MemorySaver

from langgraph_backend import chatbot

CONFIG =  {'configurable': {'thread_id': 'thread-id'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

for message in st.session_state['message_history']:
     with st.chat_message(message['role']):
          st.text(message['content'])


message_history = []

#session state -> dict -> 

#{'role': 'user', 'content': 'Hi' }
#{'role': 'assitant', 'content' : 'hi=ello'}


user_input =  st.chat_input('type here')

if user_input:
    

    st.session_state['message_history'].append({'role': 'user' , 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    response = chatbot.invoke({'messages': [HumanMessage(content = user_input)]}, config = CONFIG)
    ai_message = response['messages'][-1].content    
    st.session_state['message_history'].append({'role': 'assitant' , 'content': user_input})
    with st.chat_message('assistant'):
            st.text(ai_message)





# with st.chat_message('user'):
#     st.text('Hi')

# with st.chat_message('Assitant'):
#     st.text('How can i help you')

#     user_input = st.chat_input('Type here')


#     if user_input:
#         with st.chat_message('user'):
#             st.text(user_input)





