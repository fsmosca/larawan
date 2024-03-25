import base64
from io import BytesIO

import streamlit as st
from streamlit import session_state as ss
from modules.openai import generate_image
from modules.nav import Navigator
from modules.openai import MODELS


st.set_page_config(
    page_title='Bituin',
    layout='wide',
    page_icon='✨'
)


if 'msg' not in ss:
    ss.msg = None
if 'save' not in ss:
    ss.save = []

# Handles model value crossing to different pages.
# And updating the ui if selected model is not the default.
if 'model_value' not in ss:
    ss.model_value = list(MODELS.keys())[0]
if 'model_index' not in ss:
    ss.model_index = 0


def model_cb():
    # Copy the value from widget key because the value
    # via widget key is lost if we go to other pages and come back on this page.
    ss.model_value = ss.model
    ss.model_index = list(MODELS.keys()).index(ss.model_value)


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

    coltop = st.columns([3, 2], gap='large')

    with coltop[0]:
        with st.container(border=False):
            cols = st.columns([1, 1, 1])
            with cols[0]:
                api = st.popover('API')
                with api.container():
                    st.text_input(
                        'Openai API key',
                        key='apikey',
                        placeholder='enter openai api key'
                    )

            with cols[1]:
                opt = st.popover('Options')
                opt.radio('Model', options=list(MODELS.keys()), horizontal=True, key='model', on_change=model_cb, index=ss.model_index)
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

            with st.expander('Prompt Guides', expanded=False):
                st.markdown('''
To generate images using DALL-E, you don't necessarily need specific prompts in the same way you might prompt a conversation. Instead, you provide textual descriptions or prompts that DALL-E uses to create images. These prompts can vary widely depending on the type of image you want to generate. Here are some examples:

1. **Simple Descriptions:**
   - "A red apple with green leaves."
   - "A beach sunset with palm trees."
   - "A flying blue bird with yellow feathers."
   - "A cozy living room with a fireplace and a cat sleeping on the couch."
   - "A serene mountain landscape with a tranquil lake and pine trees."
   - "A bustling city street with people walking under neon lights and skyscrapers."
   - "A sunny beach scene with golden sands, palm trees, and clear blue water."
   - "A peaceful countryside setting with rolling hills, green meadows, and a farmhouse."
   - "A vibrant garden filled with colorful flowers, butterflies, and hummingbirds."
   - "A snowy winter wonderland with snow-capped trees and a cozy cabin."
   - "A starry night sky with a full moon and twinkling constellations."
   - "An enchanted forest with moss-covered trees, fairies, and magical creatures."
   - "A futuristic cityscape with sleek buildings, flying cars, and holographic displays."

2. **Abstract Concepts:**
   - "Sadness portrayed as a rainy day with a lonely figure."
   - "Freedom represented by a soaring eagle against a clear sky."
   - "Chaos depicted as swirling colors and shapes."  
   - **Wealth Accumulation**
      - "Prosperity depicted as a mountain of gold coins under a shining sun."
      - "Financial success symbolized by a rising stock market graph against a blue sky."
      - "Abundance represented by overflowing treasure chests surrounded by jewels."  
   - **Entrepreneurship**
      - "Startup innovation shown as a light bulb emerging from a maze of challenges and obstacles."
      - "Entrepreneurial spirit visualized as a phoenix rising from the ashes of failure."  
   - **Investment and Growth:**
      - "Investment opportunities visualized as a fertile garden with money trees and growing plants."
      - "Compound interest depicted as a snowball rolling downhill, gaining size and momentum."
      - "Portfolio diversification represented by a puzzle coming together to form a solid foundation."

3. **Hybrid Objects:**
   - "A combination of a bicycle and a fish."
   - "A shoe made of chocolate."
   - "A chair with wings like a butterfly."  
   - **Energy**
     - "A solar-powered car with wings like a bird, ready to take flight."
     - "A wind turbine shaped like a tree, harnessing the power of nature."
     - "A hydroelectric dam in the shape of a waterfall, blending seamlessly with the environment."  
   - **Environment**
      - "A tree made of recycled materials, with leaves shaped like solar panels."
      - "A sustainable cityscape with buildings adorned with vertical gardens and rooftop solar panels."
      - "An eco-friendly vehicle resembling a hybrid between a bicycle and a hovercraft."  
   - **Food**
      - "A sushi roll shaped like a burger, with seaweed 'buns' and fish 'patties'."
      - "A dessert fusion of cake and fruit, with layers of sponge cake sandwiched between slices of watermelon."
      - "A taco salad served in an edible bowl made from a giant tortilla chip, with lettuce, tomatoes, and cheese toppings."

4. **Surreal Scenarios:**
   - "A floating city in the clouds with upside-down buildings."
   - "A forest where the trees are made of candy."
   - "An underwater library filled with glowing jellyfish."

5. **Artistic Styles:**
   - "A portrait in the style of Picasso."
   - "A landscape in the style of Van Gogh's Starry Night."
   - "A still life in the style of Salvador Dalí."

6. **Creative Challenges:**
   - "Create an image that represents the concept of time travel."
   - "Generate an image of a futuristic cityscape."
   - "Design a creature that could inhabit a distant planet."  
   - **Economic Solutions:**
      - "Design an image that visualizes a universal basic income system lifting people out of poverty."
      - "Depict a sustainable economic model that balances growth with environmental conservation."
      - "Create an illustration of a circular economy where resources are recycled and reused to minimize waste."
   - **AI Applications:**
      - "Imagine an AI-powered platform that connects skilled workers with job opportunities tailored to their abilities and preferences."
      - "Illustrate a scenario where AI algorithms are used to optimize resource allocation in industries such as agriculture or transportation, leading to greater efficiency and reduced waste."
      - "Visualize the potential of AI in predicting and preventing financial crises by analyzing market trends and identifying early warning signs." 
   - **Peace and Harmony:**
      - "Design an image that embodies the concept of global cooperation and unity, transcending cultural and political boundaries."
      - "Depict a world where conflicts are resolved through dialogue and diplomacy, fostering lasting peace and reconciliation."
      - "Create an illustration of diverse communities living harmoniously together, celebrating their differences and embracing mutual respect." 
      - "Illustrate a peaceful resolution to a longstanding conflict, where dialogue and negotiation lead to reconciliation and mutual understanding."
      - "Visualize a scene where conflicting parties lay down their arms and embrace each other, symbolizing a commitment to peace and forgiveness."
      - "Depict a world where former adversaries work together to rebuild trust and cooperation, paving the way for lasting peace and stability."
      - "Illustrate a multicultural cityscape where diverse communities coexist peacefully, celebrating their cultural heritage."
      - "Visualize a world where music, art, and literature serve as universal languages, fostering understanding and empathy among different cultures."
      - "Depict a scene of cultural exchange and collaboration, where people from various backgrounds come together to create something beautiful."
      - "Design an image that showcases the strength of community solidarity in times of adversity, as people come together to support one another."
      - "Visualize a network of interconnected communities united by common values and shared goals, fostering a sense of belonging and mutual support."
      - "Depict a scene of grassroots activism and social movements advocating for positive change, inspiring hope and empowerment among marginalized groups."
   - **Equal Opportunities:**
      - "Visualize a society where access to education, healthcare, and employment is equitable for all individuals, regardless of background or socioeconomic status."
      - "Illustrate the empowerment of marginalized groups through initiatives promoting entrepreneurship and skill development."
      - "Imagine a future where AI technologies are used to identify and eliminate bias in hiring practices, ensuring equal opportunities for job seekers."
                            ''')

    with coltop[1]:
        st.write('**Image preview**')
        st.markdown('<div style="height: 42px"></div>', unsafe_allow_html=True)

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
