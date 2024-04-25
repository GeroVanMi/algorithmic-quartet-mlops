# Log in to the registry
cat algorithmic-quartet-cc60787a9158.json | docker login -u _json_key --password-stdin https://europe-west9-docker.pkg.dev

# Build the new image
docker build -t europe-west9-docker.pkg.dev/algorithmic-quartet/training-pipelines/pokemon-trainer .

# Push the image to the registry
docker push europe-west9-docker.pkg.dev/algorithmic-quartet/training-pipelines/pokemon-trainer:latest
