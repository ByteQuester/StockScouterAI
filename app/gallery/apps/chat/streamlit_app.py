# main chat application file
from pathlib import Path

import streamlit as st

from app.gallery.configs import config
from app.gallery.ui.sidebar import update_sidebar_chat
from app.gallery.utils import (ApiKeyManager, DataLoader, handle_user_input,
                               initialize_session_state)


def main():
    st.write((Path(__file__).parent / "README.md").read_text())
    api_key_manager = ApiKeyManager()
    api_key_manager.prompt_for_api_key()

    if api_key_manager.is_api_key_valid():
        api_key = api_key_manager.get_api_key()
        config.set_openai_key(api_key)  # Set API key for use in app
        initialize_session_state()

        selected_cik, selected_query = update_sidebar_chat()

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

        # Handle user input and display messages
        handle_user_input()


if __name__ == "__main__":
    st.set_page_config(page_title="Chat with the Bot, powered by LlamaIndex",
                       layout="centered",
                       page_icon="🦙")
    main()
