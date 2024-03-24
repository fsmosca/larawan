import base64
from io import BytesIO

import streamlit as st


def download_image(placeholder, b64_string):
    if not b64_string:
        return
    img_data = base64.b64decode(b64_string)
    img_bytes = BytesIO(img_data)
    placeholder.download_button(
        label="Save image to disk",
        data=img_bytes,
        file_name='image.png',
        mime='image/png',
        key='download'
    )
    