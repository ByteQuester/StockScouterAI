# main.py
import streamlit as st
from .ui.main_ui import render_ui
from app.gallery.utils import DataLoader

data_loader = DataLoader()


def main():
    st.set_page_config(layout="wide")
    render_ui(data_loader)


if __name__ == "__main__":
    main()
