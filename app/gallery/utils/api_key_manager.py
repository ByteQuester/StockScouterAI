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
                st.rerun()

    def get_api_key(self):
        """Return the API key."""
        return self.api_key

    def validate_api_key(self):
        """Validate the API key without making a redundant call if it's not set."""
        if not self.api_key:
            return False
        return self._is_api_key_valid()

    def _is_api_key_valid(self):
        import openai
        try:
            openai.api_key = self.api_key  # Set the API key for the session
            # Attempt a minimal API call to check validity
            openai.completions.create(prompt="Hello world",
                                      model="gpt-3.5-turbo-instruct")
            return True  # If no exception, API key is valid
        except openai.AuthenticationError:
            st.error("Invalid API key. Please check your API key.")
        except (openai.APIConnectionError, openai.RateLimitError) as e:
            st.error(
                f"Connection error or rate limit exceeded: {e}. Please try again later."
            )
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
        return False
