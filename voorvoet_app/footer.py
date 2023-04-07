"""Streamlit footer layout. Found on StackOverflow, but forgot the link."""
import streamlit as st
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


def image(src_as_string, **style):  # pragma: no cover
    """Create an image element with a given source and style."""
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):  # pragma: no cover
    """Create a link element with a given link and text."""
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):  # pragma: no cover
    """Create a footer layout with a given list of arguments."""
    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 20px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        right=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        padding=px(0, 15, 0, 0),
        width=percent(100),
        color="white",
        text_align="right",
        # height="auto",
        opacity=1,
    )

    style_hr = styles(
        display="block",
        margin=px(0, 0, 0, 0),
        padding=px(0, 0, 0, 0),
        # border_style="inset",
        border_width=px(0),
    )

    body = p()
    foot = div(style=style_div)(hr(style=style_hr), body)

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():  # pragma: no cover
    """Create a footer layout with a given list of arguments."""
    myargs = [
        "Made with ❤️ by ",
        link("https://linkedin.com/in/dennisbakhuis", "Dennis Bakhuis."),
    ]
    layout(*myargs)
