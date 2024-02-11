import streamlit as st


class ApiKeyManager:

    def __init__(self):
        self.api_key = st.session_state.get('openai_api_key', '')

    def prompt_for_api_key(self):
        """Prompt the user for the API key if not already set and store it in the session state."""
        if not self.api_key:
            api_key = st.text_input("Enter your OpenAI API key",
                                    type="password")
            confirm_button = st.button("Confirm API Key")
            if confirm_button:
                self.api_key = api_key
                st.session_state['openai_api_key'] = api_key
                st.experimental_rerun()

    def get_api_key(self):
        """Return the API key."""
        return self.api_key

    def is_api_key_valid(self):
        """Check if the API key is valid."""
        return bool(self.api_key)
