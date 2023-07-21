# Use an appropriate Python base image
FROM python:3.9

# Install GDAL dependencies
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev

# Set environment variables required for GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Set environment variable to avoid buffering
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /code

# Copy the requirements file and install Python dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Remove the requirements file after installing dependencies
RUN rm -f requirements.txt







# FROM python:3.11
# ENV PYTHONUNBUFFERED=1
# RUN apt-get update && apt-get install -y \
#     gcc \
#     libgdal-dev \
#     gdal-bin
# # ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
# # ENV C_INCLUDE_PATH=/usr/include/gdal
# WORKDIR /code
# COPY requirements.txt /code/
# RUN pip install -r requirements.txt
# COPY . .
# RUN rm -f requirements.txt


