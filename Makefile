# Define the Docker image name and tag
IMAGE_NAME := security_toolbox
CONTAINER_NAME := security_toolbox_container
PORT := 8080

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run:
	docker run --name $(CONTAINER_NAME) -p $(PORT):8080 -d $(IMAGE_NAME)

# Stop the Docker container
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Restart the Docker container
restart: stop run

# Remove the Docker image
clean:
	docker rmi $(IMAGE_NAME) || true

# Rebuild the Docker image and run the container
rebuild: stop clean build run

# Setup local environment for development
env:
	python3 -m venv env
	source env/bin/activate
	pip3 install -r requirements.txt