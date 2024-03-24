import base64
from io import BytesIO

import streamlit as st
from streamlit import session_state as ss
from modules.openai import generate_image
from modules.download import download_image
from modules.nav import Navigator


st.set_page_config(page_title='Image generator', layout='wide')


if 'msg' not in ss:
    ss.msg = None
if 'output' not in ss:
    ss.output = None


def generate():
    """A callback function of button widget.
    
    Calls DALL.E image generator.
    """
    if ss.model == 'None':
        ss.model=None
    if ss.size == 'None':
        ss.size = None

    if not ss.prompt or not ss.apikey:
        ss.msg = 'prompt or apikey is missing'
        return
    
    image_b64_json, ss.msg = generate_image(
        ss.apikey,
        ss.model,
        ss.size,
        ss.prompt
    )
    ss.output = image_b64_json


def main():
    Navigator()

    st.title('Generates images with DALL.E')

    coltop = st.columns([2, 1], gap='large')

    with coltop[0]:
        with st.container(border=False):
            cols = st.columns([1, 1, 1])
            with cols[0]:
                api = st.popover('API')
                with api.container():
                    st.text_input('Openai API key', key='apikey', placeholder='enter openai api key')

            with cols[1]:
                opt = st.popover('Options')
                opt.selectbox(
                    'Model',
                    options=['None', 'dall-e-3', 'dall-e-2'],
                    key='model',
                    index=1
                )
                opt.selectbox(
                    'Image Size',
                    options=['None', '256x256', '512x512', '1024x1024', '1792x1024', '1024x1792'],
                    key='size',
                    index=3
                )

            with cols[2]:
                download = st.popover('Download')
                download_image(download, ss.output)


            st.text_area('Prompt', key='prompt', height=270)
            st.button('Generate image', on_click=generate, type='primary')

            if ss.msg:
                st.error(ss.msg)
                ss.msg = None
            elif not ss.output:
                pass

    with coltop[1]:
        st.write('Image preview')
        st.markdown('<div style="height: 42px"></div>', unsafe_allow_html=True)  # v spacer

        if ss.output:
            img_data = base64.b64decode(ss.output)
            img_bytes = BytesIO(img_data)
            st.image(img_bytes, use_column_width=True)


if __name__ == '__main__':
    main()
