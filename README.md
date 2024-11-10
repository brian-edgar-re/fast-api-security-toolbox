# Security Toolbox

This application is a FastAPI-based security tool that provides endpoints for encoding/decoding text in Base64 and generating/validating JWT tokens. It is packaged in a Docker container for easy deployment.

## Features

- **Ping Endpoint**: A simple health check to verify the service is running.
- **Base64 Encoding and Decoding**: Encode or decode text using Base64.
- **JWT Generation and Validation**: Generate and validate JSON Web Tokens (JWTs) with custom payloads and expiration times.

## Local Development Setup

To set up the project for local development, follow these steps:

### Prerequisites

- Python 3.13
- A virtual environment (recommended for dependency management)
- A `SECRET_KEY` environment variable for JWT functionality
- Docker

### Steps

1. **Clone the Repository**:

   Clone the repository to your local machine.

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set Up a Virtual Environment**:

   Create and activate a virtual environment to isolate dependencies.

   ```bash
   python3 -m venv env
   source env/bin/activate  # For macOS/Linux
   .\env\Scripts\activate   # For Windows
   ```

3. **Install Dependencies**:

   Install the required Python packages from `requirements.txt`.

   ```bash
   pip install -r requirements.txt
   ```

4. **Set the `SECRET_KEY` Environment Variable**:

   This application requires a `SECRET_KEY` environment variable for JWT operations. You can set it in your terminal session:

   ```bash
   export SECRET_KEY=your_secret_key  # For macOS/Linux
   set SECRET_KEY=your_secret_key     # For Windows
   ```

   Replace `your_secret_key` with a secure key of your choice.

5. **Run the FastAPI Application**:

   Use `uvicorn` to start the FastAPI application locally:

   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8080
   ```

   The application should now be accessible at `http://127.0.0.1:8080`.

6. **Access the API Documentation**:

   FastAPI provides interactive API documentation at the following URLs:
   - Swagger UI: [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)
   - ReDoc: [http://127.0.0.1:8080/redoc](http://127.0.0.1:8080/redoc)

### Example Commands for Testing

You can test the API endpoints with `curl` commands or a tool like Postman. Refer to the **Example Requests** section above for example requests you can try locally.


## Makefile Commands

The `Makefile` provides an easy way to manage the Docker container for this application. Available commands include:

- **Set Up Local Virtual Environment**:
  ```bash
  make env
  ```
  Creates a Python virtual environment named `env`, installs dependencies from `requirements.txt`, and prepares the project for local development. After running this command, activate the virtual environment:

  ```bash
  source env/bin/activate  # For macOS/Linux
  .\env\Scripts\activate   # For Windows
  ```

- **Build the Docker Image**:
  ```bash
  make build
  ```
  Builds the Docker image with the specified name (`security_toolbox`).

- **Run the Docker Container**:
  ```bash
  make run
  ```
  Runs the container with the specified name (`security_toolbox_container`) and exposes it on port 8080. Ensure you define the `SECRET_KEY` environment variable when running this command:
  
  ```bash
  SECRET_KEY=your_secret_key make run
  ```

- **Stop the Docker Container**:
  ```bash
  make stop
  ```
  Stops and removes the running container.

- **Restart the Docker Container**:
  ```bash
  make restart
  ```
  Stops, then starts the container again.

- **Remove the Docker Image**:
  ```bash
  make clean
  ```
  Removes the Docker image.

- **Rebuild and Run**:
  ```bash
  make rebuild
  ```
  Stops, removes, rebuilds, and runs the container.

## Usage

The application exposes the following endpoints:

1. **GET /ping** - Returns "pong" for a health check.
2. **GET /encode_base64?text={your_text}** - Encodes the provided text into Base64.
3. **GET /decode_base64?encoded_text={your_encoded_text}** - Decodes the provided Base64 text.
4. **POST /jwt/generate** - Generates a JWT with a specified payload and expiration time.
   - Requires `SECRET_KEY` environment variable.
5. **GET /jwt/validate?token={your_jwt_token}** - Validates a provided JWT token.
   - Requires `SECRET_KEY` environment variable.

## Setting the `SECRET_KEY`

The `SECRET_KEY` environment variable is required for JWT generation and validation. When using the `make run` command, you can set it as follows:

```bash
SECRET_KEY=your_secret_key make run
```

Replace `your_secret_key` with your actual secret key.

## Example Requests

- **Ping**:
  ```bash
  curl http://localhost:8080/ping
  ```

- **Base64 Encode**:
  ```bash
  curl "http://localhost:8080/encode_base64?text=hello"
  ```

- **Base64 Decode**:
  ```bash
  curl "http://localhost:8080/decode_base64?encoded_text=aGVsbG8="
  ```

- **Generate JWT**:
  ```bash
  curl -X POST "http://localhost:8080/jwt/generate" -H "Content-Type: application/json" -d '{"payload": {"user_id": 1}, "expiration_minutes": 10}'
  ```

- **Validate JWT**:
  ```bash
  curl "http://localhost:8080/jwt/validate?token=your_jwt_token"
  ```
