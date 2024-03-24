import streamlit as st
from modules.nav import Navigator


st.set_page_config(
    page_title='Bituin',
    layout='centered',
    page_icon='✨'
)


def main():
    Navigator()

    st.title('Welcome!!')

    st.markdown('''
        A web app built using [streamlit](https://streamlit.io/) that can generate images using
        Openai's [DALL.E](https://platform.openai.com/docs/guides/images?context=node).
        This is not free, you have to supply an api key from Openai.

        Images from DALL.E.3 model starts at size 1024x1024. Whereas that of DALL.E.2
        can generate for as small as 256x256. You can preview
        and download the generated images.

        The model DALL.E.2 can generate more than 1 image at once. DALL.E.3 can only generate
        a single image at a time.
        ''')


if __name__ == '__main__':
    main()
