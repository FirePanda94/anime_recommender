# Use a lightweight Python base image
FROM python:3.10-slim

# Install uv directly using the official installer binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Prevent uv from creating a virtual environment inside the container
    UV_SYSTEM_PYTHON=1

# Work directory inside the docker container
WORKDIR /app

# Installing system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first to leverage Docker layer caching
# (Adjust these filenames if you are using requirements.txt instead)
COPY pyproject.toml uv.lock ./

# Install project dependencies without caching index lookups
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy the rest of your application code
COPY . .

# Used PORTS
EXPOSE 8501

# Run the app 
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
