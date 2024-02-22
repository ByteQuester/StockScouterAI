import streamlit as st

from app.gallery.utils.data_loader import DataLoader
from app.services import generate_data_for_cik


def update_sidebar():
    with st.sidebar:
        st.title("Stock Scouter AI")

        new_cik = st.text_input("Enter new CIK Number")
        if st.button("Generate Data for CIK"):
            generate_data_for_cik(new_cik)
            st.success(f"Data generated for CIK: {new_cik}")


def update_sidebar_chat():
    data_loader = DataLoader()

    st.sidebar.title("Stock Scouter AI")

    # Handling new CIK input and data generation
    new_cik = st.sidebar.text_input("Enter new CIK Number", key="user_handle")
    if st.sidebar.button("Generate Data for CIK", key="generate_cik_button"):
        generate_data_for_cik(new_cik)
        st.sidebar.success(f"Data generated for CIK: {new_cik}")

    # Display available CIKs and allow selection
    available_ciks = data_loader.get_available_cik_numbers()
    selected_cik = st.sidebar.selectbox("Select CIK",
                                        available_ciks,
                                        key="selected_cik_chat")

    # Display available queries for the selected CIK
    available_queries = data_loader.get_available_query_types(
        selected_cik) if selected_cik else []
    selected_query = st.sidebar.selectbox("Select Query Type",
                                          available_queries,
                                          key="query_type_chat")
    formatted_query_type = format_query_type(
        selected_query) if selected_query else ""

    if st.sidebar.button("Refresh Chat", key="refresh_chat_button"):
        # Store the selections in session state to use after rerun
        st.session_state.selected_cik = selected_cik
        st.session_state.selected_query = formatted_query_type
        st.rerun()

    return selected_cik, formatted_query_type


def format_query_type(query_type):
    """Replaces spaces with underscores in a query type string."""
    return query_type.replace(" ", "_")
