import streamlit as st
import gcsfs
import time
import random
from streamlit_star_rating import st_star_rating


st.set_page_config(
    page_title="Pokemon Generator",
    page_icon="./pika.png",
    layout="wide",
)

st.title('Pokemon Generator')
st.subheader('Click on the button to generate new pokemons')

# Create a GCSFileSystem object, to connect it, you need to store a gbucket key in file .streamlit/secrets.toml
fs = gcsfs.GCSFileSystem(project='algorithmic-quartet')

# Set the path to the directory containing the images
directory_path = 'zhaw_algorithmic_quartet_training_images'

text = "Wow look at these pokemon!"
def text_stream(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)

def display_images():
    # TODO Think about a workaround so the picutres can be called directly from the model.
    files_info = fs.ls(directory_path, detail=True)
    # Sort files by 'updated' timestamp (most recent first)
    sorted_files = sorted(files_info, key=lambda x: x['updated'], reverse=True)
    # Select the top 4 most recently updated files
    recent_files = sorted_files[:4]
    # Randomly select 4 unique files from the list just for testing purposes
    random_files = random.sample(files_info, 4)

    images = []
    for file_info in random_files:#recent_files:
        with fs.open(file_info['name'], mode='rb') as f:
            img = f.read()
            images.append(img)


    st.image(images, width=300)  # Display images with ratings

# Possible way to create Feedback
def function_to_run_on_click(value):
    st.write(f"You gave the Pokemons **{value}** stars!")
    # Feedback for current model?


# Button to generate / model call! TODO How to call our model?
if st.button('Generate'):
    with st.spinner(text='In progress'):
        time.sleep(2) # TODO make it depend of the model inference? call server .predict()
    st.write_stream(text_stream(text))
    display_images()
    stars = st_star_rating("Please rate your generated Pokemons", maxValue=5, defaultValue=0, key="rating",
                           on_click=function_to_run_on_click)



