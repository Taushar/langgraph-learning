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
import uuid

from langgraph_backend import chatbot


def generate_thread_id ():
    thread_id = str(uuid.uuid4())
    return thread_id

def reset_chat():
    thread_id = str(uuid.uuid4())
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []
    add_thread(thread_id)

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state =  chatbot.get_state(
        config={'configurable': {'thread_id': thread_id}}
    )
    return state.values.get('messages',[])      

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []




if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []   

     
add_thread(st.session_state['thread_id'])


for message in st.session_state['message_history']:
     with st.chat_message(message['role']):
          st.text(message['content'])


message_history = []

#session state -> dict -> 

#{'role': 'user', 'content': 'Hi' }
#{'role': 'assitant', 'content' : 'hi=ello'}
with st.sidebar:

    st.title("💬 My Chats")

    if st.button("＋ New Chat", use_container_width=True):
        reset_chat()

    st.divider()

    st.caption("RECENT")

    for thread_id in st.session_state['chat_threads'][::-1]:

        if st.sidebar.button(thread_id):

            st.session_state['thread_id'] = thread_id

            messages = load_conversation(thread_id)

            temp_messages = []

            for message in messages:

                if isinstance(message, HumanMessage):
                    role = 'user'
                else:
                    role = 'assistant'

                temp_messages.append({
                    'role': role,
                    'content': message.content
                })

            st.session_state['message_history'] = temp_messages

    

user_input =  st.chat_input('type here')

if user_input:
    

    st.session_state['message_history'].append({'role': 'user' , 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)


    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}
    
    with st.chat_message('assistant'):
        ai_message  = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config =  CONFIG,
                stream_mode='messages'
            )
        )
    st.session_state['message_history'].append({'role':'assistant', 'content': ai_message})
            

