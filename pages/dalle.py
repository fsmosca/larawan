import base64
from io import BytesIO

import streamlit as st
from streamlit import session_state as ss
from modules.openai import generate_image
from modules.nav import Navigator
from modules.openai import MODELS


st.set_page_config(page_title='Image generator', layout='wide')


if 'msg' not in ss:
    ss.msg = None
if 'save' not in ss:
    ss.save = []


def generate():
    """A callback function of button widget.
    
    Calls DALL.E image generator.
    """
    if not ss.prompt or not ss.apikey:
        ss.msg = 'prompt or apikey is missing'
        return
    
    ss.msg = generate_image(
        ss.apikey,
        ss.model,
        ss.size,
        ss.prompt,
        ss.num_images,
        ss.style,
        ss.quality
    )


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
                    options=list(MODELS.keys()),
                    key='model',
                    index=0
                )
                opt.selectbox(
                    'Image Size',
                    options=MODELS[ss.model]['size'],
                    key='size',
                    index=0
                )
                opt.selectbox(
                    'Number of images',
                    options=MODELS[ss.model]['num_image'],
                    key='num_images',
                    index=0
                )
                opt.selectbox(
                    'Style',
                    options=['vivid', 'natural'],
                    key='style',
                    index=1
                )
                opt.selectbox(
                    'Quality',
                    options=['standard', 'hd'],
                    key='quality',
                    index=0
                )

            st.text_area('Prompt', key='prompt', height=270)
            st.button('Generate image', on_click=generate, type='primary')

            if ss.msg:
                st.error(ss.msg)
                ss.msg = None

    with coltop[1]:
        st.write('Image preview')
        st.markdown('<div style="height: 42px"></div>', unsafe_allow_html=True)  # v spacer

        for n, img_json in enumerate(ss.save):
            img_data = base64.b64decode(img_json)
            img_bytes = BytesIO(img_data)
            st.image(img_bytes, use_column_width=True)

            fname = f'image_{n+1}.png'

            st.download_button(
                label=f"Save {fname} to disk",
                data=img_bytes,
                file_name=fname,
                mime='image/png',
                key=f'download_{n}'
            )


if __name__ == '__main__':
    main()
