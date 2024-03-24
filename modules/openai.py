import openai


def generate_image(apikey, model, size, prompt):
    """Generates image based on prompt and DALL.E."""
    error_message, image_b64_json = None, None

    client = openai.OpenAI(api_key=apikey)

    try:
        response = client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality="standard",
            n=1,
            response_format="b64_json",
        )
    except Exception as err:
        error_message = err
    else:
        for image in response.data:
            image_b64_json = image.b64_json

    return image_b64_json, error_message
