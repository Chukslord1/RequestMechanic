# Use an appropriate Python base image
FROM python:3.11

# Install GDAL dependencies for Debian-based systems
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev

# Set environment variable to avoid buffering
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /code

# Copy the requirements file and install Python dependencies
COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Remove the requirements file after installing dependencies
RUN rm -f requirements.txt
