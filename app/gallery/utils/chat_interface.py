import streamlit as st


def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role":
            "assistant",
            "content":
            "Hello! How can I assist you today?"
        }]


def display_chat_messages():
    """
    Display gallery messages.
    """
    if not st.session_state.messages:
        st.write("No messages to display")
    else:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])


def handle_user_input():
    prompt = st.chat_input("Your question")
    if prompt and prompt.strip() != "":
        st.session_state.messages.append({"role": "user", "content": prompt})
        chat_response = generate_response(
            st.session_state.chat_engine_instance, prompt)
        if chat_response:
            st.session_state.messages.append({
                "role": "assistant",
                "content": chat_response
            })
        else:
            st.session_state.messages.append({
                "role":
                "assistant",
                "content":
                "I'm sorry, I couldn't generate a response."
            })
    display_chat_messages()


def generate_response(query_engine, prompt):
    """
    Generate response from the query engine.
    """
    try:
        with st.spinner("Thinking..."):
            response = query_engine.query(prompt)
            if response is not None and response.response is not None:
                return response.response
            else:
                return "I'm sorry, I couldn't generate a response."
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return "I'm sorry, I couldn't generate a response."
