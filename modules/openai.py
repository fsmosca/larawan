from streamlit import session_state as ss
import openai


MODELS = {
    'dall-e-3': {'size': ['1024x1024', '1792x1024', '1024x1792'], 'num_image': [1]},
    'dall-e-2': {'size': ['256x256', '512x512', '1024x1024', '1792x1024', '1024x1792'], 'num_image': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
}


def generate_image(apikey, model, size:str, prompt, num_images:int, style:str, quality:str):
    """Generates image based on prompt and DALL.E."""
    if 'save' not in ss:
        ss.save = []
    else:
        ss.save = []

    num_images = 1 if model == MODELS[0] else num_images

    error_message = None

    client = openai.OpenAI(api_key=apikey)

    try:
        response = client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            n=num_images,
            style=style,
            quality=quality,
            response_format="b64_json",
        )
    except Exception as err:
        error_message = err
    else:
        for image in response.data:
            image_b64_json = image.b64_json
            ss.save.append(image_b64_json)

    return error_message
