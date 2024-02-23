# main chat application file
import logging
from pathlib import Path

import streamlit as st

from app.gallery.configs import config
from app.gallery.ui.sidebar import update_sidebar_chat
from app.gallery.utils import (ApiKeyManager, DataLoader, handle_user_input,
                               initialize_session_state)


def main():
    # Page setup and layout configurations
    st.title("Chat with the Bot 🦙")
    st.markdown("## Powered by LlamaIndex")
    with st.expander("read more"):
        st.write((Path(__file__).parent / "README.md").read_text())
    api_key_manager = ApiKeyManager()
    api_key_manager.prompt_for_api_key()

    if api_key_manager.validate_api_key():
        logging.info("API key is valid.")
        api_key = api_key_manager.get_api_key()
        config.set_openai_key(api_key)  # Set API key for use in app
        initialize_session_state()

        # Sidebar for user selections
        with st.sidebar:
            st.markdown("## Configuration")
            selected_cik, selected_query = update_sidebar_chat()
        # Main content area
        st.markdown("### Chat Interface")
        st.write(
            "Engage in conversation with our financial bot for insights and data."
        )

        # Check and update chat engine instance for new selections
        if (selected_cik,
                selected_query) != (st.session_state.get("selected_cik"),
                                    st.session_state.get("selected_query")):
            st.session_state["selected_cik"] = selected_cik
            st.session_state["selected_query"] = selected_query

            with st.spinner("Loading new data..."):
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
        else:
            st.info("API key validated.")
            logging.error("Invalid API is validating..")

        # Handle user input and display messages
        handle_user_input()


if __name__ == "__main__":
    st.set_page_config(page_title="Chat with the Bot, powered by LlamaIndex",
                       layout="centered",
                       page_icon="🦙")
    main()
