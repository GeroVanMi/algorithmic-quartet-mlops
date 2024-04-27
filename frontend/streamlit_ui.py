import streamlit as st
import gcsfs
import time
import random
from transformers import GPT2LMHeadModel, GPT2Tokenizer

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

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')
def generate_text(prompt):
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=20, num_return_sequences=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

text = generate_text("Pokemons are great")

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


# Button to generate / model call! TODO How to call our model?
if st.button('Generate'):
    with st.spinner(text='In progress'):
        time.sleep(2) # TODO make it depend of the model inference?
    st.write_stream(text_stream(text))
    display_images()
