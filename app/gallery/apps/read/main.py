from pathlib import Path

import streamlit as st


def main():
    st.markdown((Path(__file__).parents[2] / "README.md").read_text())
    st.sidebar.markdown("**Made by** [Mehrdad Touraji](https://www.linkedin.com/in/mehrdad-touraji/)") to be put in first page



if __name__ == "__main__":
    main()
