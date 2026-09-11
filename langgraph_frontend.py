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

    
    with st.chat_message('assistant'):
        ai_message  = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content = 'how to brainstorm for an essay')]},
                config =  {'configurable': {'thread_id': 'thread-1'}},
                stream_mode='messages'
            )
        )
    st.session_state['message_history'].append({'role':'assistant', 'content': ai_message})
            





# with st.chat_message('user'):
#     st.text('Hi')

# with st.chat_message('Assitant'):
#     st.text('How can i help you')

#     user_input = st.chat_input('Type here')


#     if user_input:
#         with st.chat_message('user'):
#             st.text(user_input)





