import requests
import base64
from dotenv import load_dotenv
import os
import time
import streamlit as st

load_dotenv()

invoke_url = "https://ai.api.nvidia.com/v1/genai/briaai/bria-2.3"

api_key = os.getenv('NVIDIA_API_KEY')

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
}

st.title("Bria Image Generation App")

prompt = st.text_input("Enter Your Image Prompt Here:")
aspect_ratio = st.selectbox("Aspect Ratio", ["1:1", "16:9", "4:3"])

if st.button("Generate Image"):
    payload = {
        "prompt": prompt,
        "cfg_scale": 5,
        "aspect_ratio": aspect_ratio,
        "seed": 0,
        "steps": 30,
        "negative_prompt": ""
    }

    start_time = time.time()

    response = requests.post(invoke_url, headers=headers, json=payload)

    end_time = time.time()

    response.raise_for_status()
    response_body = response.json()
    image_data = response_body.get('image')

    if image_data:
        image_bytes = base64.b64decode(image_data)
        with open('generated_image.png', 'wb') as image_file:
            image_file.write(image_bytes)
        st.image('generated_image.png', caption='Generated Image')
        st.success("Image saved as 'generated_image.png'")
    else:
        st.error("No image data found in the response")

    response_time = end_time - start_time
    st.write(f"Response time: {response_time} seconds")