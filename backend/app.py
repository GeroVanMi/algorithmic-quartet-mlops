# 1. Library imports
import uvicorn
from fastapi import FastAPI
#from model import IrisModel, IrisSpecies
from generate_images import *

# 2. Create app and model objects
app = FastAPI()
#model = IrisModel()
model = create_model(Configuration)

# 3. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the predicted flower species with the confidence
""" Example:
@app.post('/predict')
def predict_species(iris: IrisSpecies):
    data = iris.dict()
    prediction, probability = model.predict_species(
        data['sepal_length'], data['sepal_width'], data['petal_length'], data['petal_width']
    )
    return {
        'prediction': prediction,
        'probability': probability
    }
"""

@app.post('/generate_images')
def generate_images():
    config = Configuration()
    accelerator = Accelerator(
        mixed_precision=config.mixed_precision,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        log_with="tensorboard",
        project_dir=os.path.join(config.output_dir, "logs"),
    )

    image_generation_pipeline = initialize_pipeline(accelerator, config)

    images = image_generation_pipeline(
        batch_size=config.eval_batch_size,
        generator=torch.manual_seed(config.seed),
        num_inference_steps=config.number_of_noise_steps,
    ).images  # type: ignore (There are multiple definitions which break the type hints)

    if isinstance(images, list):
        save_images(images)
        upload_directory_with_transfer_manager()

        
# 4. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8001)
