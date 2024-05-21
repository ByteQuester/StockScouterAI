# main chat application file
import gc
import logging
from pathlib import Path

import gc
import re
import uuid
import textwrap
import subprocess
import nest_asyncio
from dotenv import load_dotenv

import streamlit as st

from app.gallery.configs import config
from app.gallery.ui.sidebar import update_sidebar_chat
from app.gallery.utils import (DataLoader, handle_user_input,
                               initialize_session_state)


def main():
    # Page setup and layout configurations
    st.title("Chat with the Bot 🦙")
    with st.expander("read more"):
        st.write((Path(__file__).parent / "README.md").read_text())
    
    initialize_session_state() 

    # Sidebar for user selections # thjis can stay as we need that to 
    with st.sidebar: 
        st.markdown("## Configuration")
        selected_cik, selected_query = update_sidebar_chat()

        
        # Main content area # thjis can stay as we need that to 
    st.markdown("### Chat Interface")
    st.write(
        "Engage in conversation with our financial bot for insights and data."
        )

        # Check and update chat engine instance for new selections # thjis can stay as we need that to 
    if (selected_cik, selected_query) != (st.session_state.get("selected_cik"), st.session_state.get("selected_query")):
        st.session_state["selected_cik"] = selected_cik
        st.session_state["selected_query"] = selected_query

        with st.spinner(""):
            data_loader = DataLoader()
            st.session_state[
                "chat_engine_instance"] = data_loader.push_query_engine(
                    selected_cik, selected_query)
            st.session_state["messages"].append({
                "role":
                "assistant",
                "content":
                f"Data updated for CIK: {selected_cik}, Query: {selected_query}. Please continue chatting."
            })
    #TODO: Error often arrises for some reasons when user starts to interact with the bot
    #else:
        #st.info("Error.")
        #logging.error("Error.")

    # Handle user input and display messages
    handle_user_input()

if __name__ == "__main__":
    st.set_page_config(page_title="Chat with the Bot, powered by LlamaIndex",
                       layout="centered",
                       page_icon="🦙")
    main()


