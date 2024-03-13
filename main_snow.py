import streamlit as st

from app.gallery import components
from app.gallery.utils.page import page_group


def main():
    page = page_group("p")
    with st.sidebar:
        st.title("Stock Scouter AI")

        with st.expander("🧩 Analytics & Dashboards"):
            page.item("Third Tier View", components.elements.snow_third_tier_view, default=True)

    page.show()


if __name__ == "__main__":
    st.set_page_config(page_title="Streamlit Gallery", page_icon="🎈", layout="wide", initial_sidebar_state="auto")
    main()
