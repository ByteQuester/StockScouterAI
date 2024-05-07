import streamlit as st

from app.gallery import apps, components
from app.gallery.utils.page import page_group


def main():
    page = page_group("p")
    with st.sidebar:
        st.title("Stock Scouter AI")

        with st.expander("✨ APPS", True):
            page.item("Home", apps.gallery, default=True)
            page.item("Chatbot", apps.chat)

        with st.expander("🧩 Analytics & Dashboards"):
            page.item("General View⭐", components.elements.general_view)
            page.item("Second Tier View", components.elements.second_tier_view)
            page.item("Third Tier View", components.elements.third_tier_view)

        #with st.expander("🧩 How-Tos", True):
            #page.item("Demo", components.react_player)
            #page.item("Disqus", components.disqus)

    page.show()


if __name__ == "__main__":
    st.set_page_config(page_title="Streamlit Gallery", page_icon="🎈", layout="wide", initial_sidebar_state="auto")
    main()
