import streamlit as st
import gcsfs
import time

st.title('Pokemon Generator')
st.subheader('Click on the button to generate new pokemons')

# Create a GCSFileSystem object, to connect it, you need to store a gbucket key in file .streamlit/secrets.toml
fs = gcsfs.GCSFileSystem(project='algorithmic-quartet')

# Set the path to the directory containing the images
directory_path = 'zhaw_algorithmic_quartet_training_images'

text = "Great to see that you pressed the button, know let's check what out model is capable of:"
def display_images():
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)
    # TODO Think about a workaround so the picutres can be called directly from the model.
    files_info = fs.ls(directory_path, detail=True)
    # Sort files by 'updated' timestamp (most recent first)
    sorted_files = sorted(files_info, key=lambda x: x['updated'], reverse=True)
    # Select the top 4 most recently updated files
    recent_files = sorted_files[:4]

    images = []
    for file_info in recent_files:
        with fs.open(file_info['name'], mode='rb') as f:
            img = f.read()
            images.append(img)


    st.image(images, width=300)  # Display images with ratings


# Button to generate and rate images
if st.button('Generate'):
    st.write_stream(display_images())
