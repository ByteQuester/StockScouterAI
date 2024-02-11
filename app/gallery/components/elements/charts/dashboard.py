from abc import ABC, abstractmethod
from contextlib import contextmanager
from uuid import uuid4

import streamlit as st
from streamlit_elements import dashboard, mui


class Dashboard:

    DRAGGABLE_CLASS = "draggable"

    def __init__(self):
        self._layout = []

    def _register(self, item):
        self._layout.append(item)

    @contextmanager
    def __call__(self, **props):
        props["draggableHandle"] = f".{Dashboard.DRAGGABLE_CLASS}"

        with dashboard.Grid(self._layout, **props):
            yield

    class Item(ABC):

        def __init__(self, board, x, y, w, h, **item_props):
            self._key = str(uuid4())
            self._draggable_class = Dashboard.DRAGGABLE_CLASS
            self._dark_mode = False
            board._register(dashboard.Item(self._key, x, y, w, h,
                                           **item_props))
            print(
                f"Widget initialized: Key={self._key}, Position=({x}, {y}), Size=({w}x{h})"
            )

        def _switch_theme(self):
            self._dark_mode = not self._dark_mode
            st.session_state['dark_mode'] = self._dark_mode

        @contextmanager
        def title_bar(self, padding="5px 15px 5px 15px", dark_switcher=True):
            with mui.Stack(
                    className=self._draggable_class,
                    alignItems="center",
                    direction="row",
                    spacing=1,
                    sx={
                        "padding": padding,
                        "borderBottom": 1,
                        "borderColor": "divider",
                    },
            ):
                yield

                if dark_switcher:
                    if self._dark_mode:
                        mui.IconButton(mui.icon.DarkMode,
                                       onClick=self._switch_theme)
                    else:
                        mui.IconButton(mui.icon.LightMode,
                                       sx={"color": "#ffc107"},
                                       onClick=self._switch_theme)

        @abstractmethod
        def __call__(self):
            """Show elements."""
            raise NotImplementedError