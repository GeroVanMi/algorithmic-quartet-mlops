import random
import time

import gcsfs
import requests
import streamlit as st
from streamlit_star_rating import st_star_rating

SERVER_URL = "https://pokemon-server-ukwlkels3q-ew.a.run.app/"

st.set_page_config(
    page_title="Pokemon Generator",
    page_icon="./pika.png",
    layout="wide",
)

st.title("Pokemon Generator")
st.subheader("Click on the button to generate new pokemons")

fs = gcsfs.GCSFileSystem(project="algorithmic-quartet")

# Set the path to the directory containing the images
directory_path = "zhaw_algorithmic_quartet_generated_images"

text = [
    "Wow look at these pokemon!",
    "These pokemon are absolutely incredible!",
    "I can't believe how amazing these pokemon are!",
    "Stunning pokemon, I'm in awe!",
    "Absolutely breathtaking pokemon, I'm mesmerized!",
    "These pokemon are truly magnificent, I'm captivated!",
    "Wow, the pokemon here are simply out of this world!",
    "I'm blown away by the beauty and power of these pokemon!",
    "These pokemon are a sight to behold, I'm enthralled!",
    "Incredible pokemon, I'm completely enchanted!",
]


def text_stream(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)


def display_images():
    files_info = fs.ls(directory_path, detail=True)
    # Sort files by 'updated' timestamp (most recent first)
    sorted_files = sorted(files_info, key=lambda x: x["updated"], reverse=True)
    recent_files = sorted_files[:2]

    images = []
    for file_info in recent_files:
        with fs.open(file_info["name"], mode="rb") as f:
            img = f.read()
            images.append(img)

    with st.container():
        st.image(images, width=300)


def handle_user_rating(value):
    st.markdown(f"You gave the Pokemons **{value}** stars!")
    requests.post(f"{SERVER_URL}/rate_model", json={"rating": value})


def display_stars():
    stars = st_star_rating(
        "Please rate your generated Pokemons",
        maxValue=5,
        defaultValue=0,
        key="rating",
        on_click=handle_user_rating,
    )
    st.write(stars)


# Button to generate / model call!
if st.button("Generate new Images"):
    with st.spinner(text="Generating contemporary art!"):
        random_text = random.choice(text)
        try:
            response = requests.get(f"{SERVER_URL}/generate_images")
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")

    st.write_stream(text_stream(random_text))

display_images()
display_stars()
