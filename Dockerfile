# Set Base Image
FROM python:3.9 as base

# Update Base Image
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

# Set virtual environment for dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
ADD requirements.txt .
RUN pip install -r requirements.txt

# Set Run Image 
FROM python:3.9-slim AS run

# Set working directory
WORKDIR /titanic

# Set pythonpath to ensure python runs from app directory
ENV PYTHONPATH ./src/app/

# Copy virtual environment from base image
COPY --from=base /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy app source code
COPY . ./

# Expose container port for uvicorn server
EXPOSE 8000

# Run app using uvicorn server
CMD uvicorn main:api --host 0.0.0.0 --port 8000 --reload
