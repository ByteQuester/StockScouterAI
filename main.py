import streamlit as st

from app.gallery import apps, components
from app.gallery.utils.page import page_group


def main():

    page = page_group("p")

    with st.sidebar:
        st.title("Stock Scouter AI")

        with st.expander("✨ APPS", True):
            page.item("Streamlit gallery", apps.gallery, default=True)
            page.item("Chatbot", apps.chat)

        with st.expander("🧩 COMPONENTS", True):
            page.item("Demo", components.react_player)
            page.item("Disqus", components.disqus)
            page.item("Elements⭐", components.elements)

    page.show()


if __name__ == "__main__":
    st.set_page_config(page_title="Streamlit Gallery", page_icon="🎈", layout="wide", initial_sidebar_state="auto")
    main()
