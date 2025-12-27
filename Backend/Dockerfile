# Use the official Python 3.10 image
FROM python:3.10

# Set the working directory to /code
WORKDIR /code

# Copy the requirements file into the container at /code
COPY ./requirements.txt /code/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application code
COPY . /code

# Create a writable directory for non-root user (Hugging Face specific)
# Hugging Face Spaces run as a random user with ID 1000, so we need to ensure permissions
RUN mkdir -p /code/app && chmod -R 777 /code/app

# Command to run the application
# Hugging Face expects the app to run on port 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
